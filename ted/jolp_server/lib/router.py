from fastapi import APIRouter, Form, UploadFile
from itertools import groupby
from operator import itemgetter
from typing import Annotated
from lib import function
from pydantic import BaseModel
from app.logger import logger
from app.database import Database
from app.s3 import S3
from io import BytesIO
import os
import uuid
import traceback

router = APIRouter(prefix="/jolp")

class RequestBody(BaseModel):
    userId : str = "ted"
    token : str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6MzAwMCwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvYXV0aGVudGljYXRpb24iOiIwMDAzIiwibmJmIjoxNjk1MzczMzAyLCJleHAiOjE4MDMzNzMzMDIsImlhdCI6MTY5NTM3MzMwMn0.PWm7C2nT1Ampjx1BuL1LoYvS8VL8HZZJPzsO9mS3_sY"
    
@router.post("/uploadFile", tags= ["upload_file"])
async def upload_file(userId: Annotated[str, Form()], fileName: Annotated[str, Form()], file: Annotated[UploadFile, Form()]):
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
        
        function.insert_file(db, user_id, file_id, file_name, file_url)
        
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
        all_file_list = [{"file_id" :_dict["file_id"], "file_name" : _dict["file_name"], "file_url" : _dict["file_url"]} for _dict in result]
        
        
        data = list()
        
        for key, group_data in grouped_result:
            group_data = list(group_data)
            category_id = key
            category_name = group_data[0]["category_name"]
            file_list = list()
            for _dict in group_data:
                file_list.append({"file_id" : _dict["file_id"] , "file_name" : _dict["file_name"], "file_url" : _dict["file_url"]})
            data.append({"category_id" : category_id, "category_name" : category_name, "file_list" : file_list})
        
        result_dict = {"all_file_list" : all_file_list, "category_list" : data}
        return {"code" : 200, "data" : result_dict}
        
    except:
        logger.error(traceback.format_exc())
        return {"code" : 500, "message" : "Internal Error"}


@router.post("/clusterFiles", tags=["clustering"])
def cluster_files(body:RequestBody):
    try:
        pass
    except:
        logger.error(traceback.format_exc())
        return {"code" : 500, "message" : "Internal Error"}
    
    
