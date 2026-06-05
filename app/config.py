import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    # if not OPENAI_API_KEY:
    #     raise RuntimeError("OPENAI_API_KEY is not set")

    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    # if not GOOGLE_API_KEY:
    #     raise RuntimeError("GOOGLE_API_KEY is not set")
    
    # MinIO (S3) Configuration
    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "minio:9000")
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY", "minioadminpassword")
    MINIO_BUCKET_NAME: str = os.getenv("MINIO_BUCKET_NAME", "enterprise-intelligence-data")

settings = Settings()