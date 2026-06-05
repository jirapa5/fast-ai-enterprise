import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

from app.config import settings


class StorageService:
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=f"http://{settings.MINIO_ENDPOINT}",
            aws_access_key_id=settings.MINIO_ACCESS_KEY,
            aws_secret_access_key=settings.MINIO_SECRET_KEY,
            config=Config(signature_version="s3v4"),
            region_name="us-east-1",
        )

    def ensure_bucket_exists(self):
        try:
            self.s3_client.head_bucket(
                Bucket=settings.MINIO_BUCKET_NAME
            )
        except ClientError:
            self.s3_client.create_bucket(
                Bucket=settings.MINIO_BUCKET_NAME
            )

    def upload_file_stream(
        self,
        file_obj,
        filename: str
    ) -> str:
        self.ensure_bucket_exists()

        file_obj.seek(0)

        self.s3_client.upload_fileobj(
            file_obj,
            settings.MINIO_BUCKET_NAME,
            filename,
        )

        return f"s3://{settings.MINIO_BUCKET_NAME}/{filename}"

    def upload_local_file(
        self,
        local_path: str,
        filename: str
    ) -> str:
        self.ensure_bucket_exists()

        self.s3_client.upload_file(
            local_path,
            settings.MINIO_BUCKET_NAME,
            filename,
        )

        return f"s3://{settings.MINIO_BUCKET_NAME}/{filename}"


storage_service = StorageService()