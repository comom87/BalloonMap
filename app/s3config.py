import os
from datetime import datetime

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from fastapi import UploadFile

load_dotenv()

ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME")
REGION = os.getenv("REGION")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)


def upload_file(file: UploadFile):
    now = datetime.now()
    file_name = "BalloonMap_" + now.strftime("%Y%m%d%H%M%S")
    s3_client.upload_fileobj(file.file, BUCKET_NAME, file_name, ExtraArgs={"ContentType": f"{file.content_type}"})

    file_url = f'https://{BUCKET_NAME}.s3.{REGION}.amazonaws.com/{file_name}'
    return file_url
