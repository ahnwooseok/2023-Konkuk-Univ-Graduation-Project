from fastapi import APIRouter, Form, UploadFile
from pydantic import BaseModel
from app.logger import logger
from app.database import Database
import traceback

router = APIRouter(prefix="/v2/admin/user")

class fileForm:
    file : UploadFile
    userId : str

    
@router.post("/uploadFile", tags= ["upload_file"])
async def upload_file(item : fileForm):
    try:
        file = item.file
        user_id = item.userId
        logger.error(user_id)
        
    except:
        logger.error(traceback.format_exc())
        return {"code" : 500, "message" : "Internal Error"}
    
    try:
        pass
        return {"code" : 200, "message" : "success"}
    except:
        logger.error(traceback.format_exc())
        return {"code" : 500, "message" : "Internal Error"}
        
