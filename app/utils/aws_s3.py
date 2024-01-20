# s3_manager.py
import boto3
from botocore.exceptions import NoCredentialsError

S3_BUCKET = "voguebebucket"
S3_REGION = "us-east-1"
S3_ACCESS_KEY = "AKIAWVQEMTMX6XW6XE6I"
S3_SECRET_KEY = "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"

def upload_to_s3(file, file_name):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY,
        region_name=S3_REGION
    )

    try:
        s3.upload_fileobj(file, S3_BUCKET, file_name,  ExtraArgs={"ContentType": "image/jpeg"})
        return True
    except NoCredentialsError:
        raise RuntimeError("AWS credentials not available.")
    except Exception as e:
        raise RuntimeError(f"Error uploading file to S3: {str(e)}")

def generate_s3_url(file_name):
    return f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{file_name}"
