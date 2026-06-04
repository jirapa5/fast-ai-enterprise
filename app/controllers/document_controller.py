import os
import shutil
import tempfile
from io import BytesIO

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.storage_service import storage_service
from app.services.ocr_service import ocr_service
from app.services.vector_service import vector_service

router = APIRouter(
    prefix="/documents",
    tags=["Document Management (Ingestion)"]
)


@router.post("/upload-image-ocr/")
async def upload_image_ocr(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="ไม่พบชื่อไฟล์"
        )

    if not file.filename.lower().endswith(
        (".png", ".jpg", ".jpeg")
    ):
        raise HTTPException(
            status_code=400,
            detail="รองรับเฉพาะไฟล์ PNG, JPG, JPEG เท่านั้น"
        )

    try:
        # อ่านไฟล์ครั้งเดียว
        file_bytes = await file.read()

        if not file_bytes:
            raise HTTPException(
                status_code=400,
                detail="ไฟล์ว่างเปล่า"
            )

        # Upload เข้า MinIO
        minio_url = storage_service.upload_file_stream(
            BytesIO(file_bytes),
            file.filename
        )

        # OCR
        extracted_text = await ocr_service.extract_text_from_bytes(
            file_bytes
        )

        if not extracted_text.strip():
            return {
                "status": "warning",
                "message": "สแกนภาพสำเร็จแต่ไม่พบตัวอักษร",
                "filename": file.filename,
                "storage_destination": minio_url
            }

        # Save ลง Vector DB
        chunks_count = vector_service.add_text_document(
            extracted_text,
            file.filename,
            "OCR Image"
        )

        return {
            "status": "success",
            "filename": file.filename,
            "storage_destination": minio_url,
            "chunks_created": chunks_count,
            "text_length": len(extracted_text)
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"OCR Processing Error: {str(e)}"
        )


@router.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="ไม่พบชื่อไฟล์"
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="รองรับเฉพาะไฟล์ PDF เท่านั้น"
        )

    temp_path = None

    try:
        # อ่านไฟล์ครั้งเดียว
        file_bytes = await file.read()

        if not file_bytes:
            raise HTTPException(
                status_code=400,
                detail="ไฟล์ PDF ว่างเปล่า"
            )

        # Upload เข้า MinIO
        minio_url = storage_service.upload_file_stream(
            BytesIO(file_bytes),
            file.filename
        )

        # สร้าง temp file แบบ unique
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:
            temp_file.write(file_bytes)
            temp_path = temp_file.name

        # Parse PDF และเก็บลง ChromaDB
        chunks_count = vector_service.add_pdf_document(
            temp_path,
            file.filename
        )

        return {
            "status": "success",
            "filename": file.filename,
            "storage_destination": minio_url,
            "chunks_created": chunks_count
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"PDF Processing Error: {str(e)}"
        )

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)