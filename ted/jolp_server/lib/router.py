from fastapi import APIRouter, Form, UploadFile
from itertools import groupby
from operator import itemgetter
from typing import Annotated
from sklearn.feature_extraction.text import CountVectorizer
import requests
from lib import function
from pydantic import BaseModel
from app.logger import logger
from app.database import Database
from app.s3 import S3
from io import BytesIO
import os
import uuid
import traceback
import re
from PyPDF2 import PdfReader
from model.tokenizer import CustomTokenizer
from model.representation_model import RepresentationModel


from bertopic import BERTopic

router = APIRouter(prefix="/jolp")

class RequestBody(BaseModel):
    userId : str = "ted"
    token : str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6MzAwMCwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvYXV0aGVudGljYXRpb24iOiIwMDAzIiwibmJmIjoxNjk1MzczMzAyLCJleHAiOjE4MDMzNzMzMDIsImlhdCI6MTY5NTM3MzMwMn0.PWm7C2nT1Ampjx1BuL1LoYvS8VL8HZZJPzsO9mS3_sY"
    
@router.post("/uploadFile", tags= ["upload_file"])
async def upload_file(userId: Annotated[str, Form()], fileName: Annotated[str, Form()], file: Annotated[UploadFile, Form()], fileSize: Annotated[str, Form()]):
    """
    파일 업로드용 api\n
    form data 형식으로 부탁해요 \n
    userId : user_id \n
    file : 파일 \n
    fileName : 파일 이름
    """
    try:
        user_id = userId
        file_name = fileName
        file_size = fileSize
        origin_file_data = await file.read()
        file_object = BytesIO(origin_file_data)
        db = Database()
        s3 = S3()
        db.connect()
        s3.connect()        
    except:
        logger.error(traceback.format_exc())
        return {"code" : 500, "message" : "Internal Error"}
        
    try:
        file_id = uuid.uuid4()
        file_name_list = os.path.splitext(file_name)
        extension = file_name_list[-1]
        s3_file_name = f"{file_id}{extension}"
        
        if not s3.upload_file(file_object, s3_file_name):
            return {"code" : 500, "message" : "S3_upload Failed"}
        
        file_url = s3.get_file_url(s3_file_name)
        
        function.insert_file(db, user_id, file_id, file_name, file_url, file_size)
        
        return {"code" : 200, "message" : "success"}
    except:
        logger.error(traceback.format_exc())
        return {"code" : 500, "message" : "Internal Error"}
    
    
@router.post("/getFiles", tags=["getFile"])
def get_files(body : RequestBody):
    """
    사용자의 파일들을 볼 수 있는 API임미다
    """
    try:
        dict_body = body.dict()
        user_id = dict_body["userId"]
        db = Database()
        db.connect()
        
    except:
        return {"code" : 500, "message" : "Internal Error"}
    
    try:
        result = function.get_files(db, user_id)
        result = sorted(result, key=itemgetter('category_id'))
        grouped_result = groupby(result, itemgetter('category_id'))
        logger.error(result)
        all_file_list = [{"file_id" :_dict["file_id"], "file_name" : _dict["file_name"], "file_url" : _dict["file_url"], "file_size": _dict["file_size"], "register_date" : _dict["register_date"]} for _dict in result]
        
        
        data = list()
        
        for key, group_data in grouped_result:
            group_data = list(group_data)
            category_id = key
            category_name = group_data[0]["category_name"]
            file_list = list()
            for _dict in group_data:
                file_list.append({"file_id" : _dict["file_id"] , "file_name" : _dict["file_name"], "file_url" : _dict["file_url"], "file_size": _dict["file_size"], "register_date" : _dict["register_date"]})
            data.append({"category_id" : category_id, "category_name" : category_name, "file_list" : file_list})
        
        result_dict = {"all_file_list" : all_file_list, "category_list" : data}
        return {"code" : 200, "data" : result_dict}
        
    except:
        logger.error(traceback.format_exc())
        return {"code" : 500, "message" : "Internal Error"}


@router.post("/clusterFiles", tags=["clustering"])
def cluster_files(body:RequestBody):
    try:
        dict_body = body.dict()
        user_id = dict_body["userId"]
        db = Database()
        db.connect()
        tokenizer = CustomTokenizer()
        model = BERTopic(embedding_model="sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens",
                            vectorizer_model=CountVectorizer(tokenizer=tokenizer, max_features=3000),                    
                            nr_topics= "auto",
                            representation_model=RepresentationModel("gpt-3.5-turbo"),
                            top_n_words=5,
                            verbose=True,                    
                            calculate_probabilities=True)

    except:
        logger.error(traceback.format_exc())
        return {"code" : 500, "message" : "Internal Error"}
    
    try:
        result = function.get_files(db, user_id)
        file_dict_list = list()
        string_list = list()
        for file in result:
            file_dict = dict()
            start_index = len(string_list)
            string = ""
            file_id = file["file_id"]
            file_url = file["file_url"]
            file_name = file["file_name"]
            file_name_list = os.path.splitext(file_name)
            extension = file_name_list[-1]
            
            if extension == ".pdf":
                response_content = function.request_file_url(file_url)
                file_like = BytesIO(response_content)
                pdf = PdfReader(file_like)
                for page in pdf.pages:
                    line = page.extract_text().split('\n')
                    string+=(" ".join(line))
            elif extension == ".docx":
                continue
                
            elif extension == ".txt":
                response = requests.get(file_url)
                line = response.text.split('\n')
                string+=(" ".join(line))
                
            token_list = tokenizer(string)
            tokenized_string = " ".join(token_list)

            string_list += ([tokenized_string[i:i+300] for i in range(0, len(tokenized_string), 300)])
            end_index = len(string_list)
            file_dict["file_id"] = file_id
            file_dict["file_name"] = file_name
            file_dict["start_index"] = start_index
            file_dict["end_index"] = end_index
            file_dict_list.append(file_dict)
        
            
        topics, pred = model.fit_transform(string_list) 
        #fit_transform 학습시켰어
        
        topic_dict = model.topic_representations_
        category_dict = dict()
        default_category_id = function.get_default_category_id(db, user_id)
        for key in topic_dict.keys():
            if key == -1:
                category_dict[key] = {"category_id" : default_category_id, "category_name" : "기타"}
                continue
            category_id = uuid.uuid4()
            category_name = topic_dict[key][0][0]
            category_dict[key] = {"category_id" : category_id, "category_name" : category_name}
            function.insert_category(db, category_id, user_id, category_name)
        
        for file_dict in file_dict_list :
            file_id = file_dict["file_id"]
            start_index = file_dict["start_index"]
            end_index = file_dict["end_index"]
            topics_per_file = topics[start_index:end_index]
            file_topic = max(topics_per_file, key=topics_per_file.count)
            category_id = category_dict[file_topic]["category_id"]
            function.update_file(db, file_id, category_id)
        
        return {"code" : 200, "message" : "SUCCESS"}
    except:
        logger.error(traceback.format_exc())
        return {"code" : 500, "message" : "Internal Error"}
    


@router.post("/deleteAllFiles", tags=["DELETE"])
def cluster_files(body:RequestBody):
    try:
        dict_body = body.dict()
        user_id = dict_body["userId"]
        db = Database()
        db.connect()
        
        if user_id == "ted":
            function.delete_all_file(db)
            return {"code" : 200, "message" : "SUCCESS"}
        else:
            return{"code" : 500 , "message" : "Internal Error"}

    except:
        logger.error(traceback.format_exc())
        return {"code" : 500, "message" : "Internal Error"}
    
   
    
    
