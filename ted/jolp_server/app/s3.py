import boto3
import os
from dotenv import load_dotenv
from io import BytesIO

class S3:
    def __init__(self):
        load_dotenv()
        self.s3 = None
        self.bucket_name = os.environ["bucket_name"]

    def connect(self):
        load_dotenv()
        self.s3 = boto3.client(
            service_name="s3",
            region_name="us-east-2", # 자신이 설정한 bucket region
            aws_access_key_id=os.environ["s3_key"],
            aws_secret_access_key=os.environ["s3_secret_key"]
        )
    
    def upload_file(self, file_object, file_name):
        try:
            self.s3.upload_fileobj(file_object, self.bucket_name, file_name)
            return True
        except:
            return False
    
    def get_file_url(self, file_name):
        return f'https://{self.bucket_name}.s3.us-east-2.amazonaws.com/{file_name}'
    
    def download_file(self, file_name):
        file_object = BytesIO()
        self.s3.download_fileobj(self.bucket_name, file_name, file_object)
        return file_object

   
