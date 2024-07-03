import boto3
import os
from fastapi import UploadFile
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

async def upload_image_to_s3(file: UploadFile):
    try:
        s3_client.upload_fileobj(file.file, BUCKET_NAME, file.filename)
        return f"https://{BUCKET_NAME}.s3.amazonaws.com/{file.filename}"
    except (NoCredentialsError, PartialCredentialsError) as e:
        raise Exception("AWS credentials not available or incomplete.") from e

def delete_image_from_s3(url: str):
    key = url.split(f"https://{BUCKET_NAME}.s3.amazonaws.com/")[1]
    s3_client.delete_object(Bucket=BUCKET_NAME, Key=key)
