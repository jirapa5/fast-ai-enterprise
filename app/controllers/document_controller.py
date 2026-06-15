import os
import shutil
import tempfile
from io import BytesIO
from uuid import uuid4

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from app.services.storage_service import storage_service
from app.services.ocr_service import ocr_service
from app.services.vector_service import vector_service

from app.database.dependencies import get_db
from app.models.document import Document

router = APIRouter(
    prefix="/documents",
    tags=["Document Management (Ingestion)"]
)


@router.post("/upload-image-ocr/")
async def upload_image_ocr(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
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
        file_bytes = await file.read()

        if not file_bytes:
            raise HTTPException(
                status_code=400,
                detail="ไฟล์ว่างเปล่า"
            )

        minio_url = storage_service.upload_file_stream(
            BytesIO(file_bytes),
            file.filename
        )

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

        chunks_count = vector_service.add_text_document(
            extracted_text,
            file.filename,
            "OCR Image"
        )

        document = Document(
            id=str(uuid4()),
            file_name=file.filename,
            document_type="OCR",
            chunk_count=chunks_count,
            minio_path=minio_url,
            file_size=len(file_bytes),
            status="ACTIVE"
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        return {
            "status": "success",
            "document_id": document.id,
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
async def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
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
        file_bytes = await file.read()

        if not file_bytes:
            raise HTTPException(
                status_code=400,
                detail="ไฟล์ PDF ว่างเปล่า"
            )

        minio_url = storage_service.upload_file_stream(
            BytesIO(file_bytes),
            file.filename
        )

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:
            temp_file.write(file_bytes)
            temp_path = temp_file.name

        chunks_count = vector_service.add_pdf_document(
            temp_path,
            file.filename
        )

        document = Document(
            id=str(uuid4()),
            file_name=file.filename,
            document_type="PDF",
            chunk_count=chunks_count,
            minio_path=minio_url,
            file_size=len(file_bytes),
            status="ACTIVE"
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        return {
            "status": "success",
            "document_id": document.id,
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


@router.get("/")
def get_documents(
    db: Session = Depends(get_db)
):
    documents = (
        db.query(Document)
        .filter(
            Document.status == "ACTIVE"
        )
        .order_by(
            Document.created_at.desc()
        )
        .all()
    )

    return [
        {
            "id": d.id,
            "file_name": d.file_name,
            "document_type": d.document_type,
            "chunk_count": d.chunk_count,
            "file_size": d.file_size,
            "minio_path": d.minio_path,
            "status": d.status,
            "created_at": d.created_at,
            "updated_at": d.updated_at
        }
        for d in documents
    ]


@router.get("/{document_id}")
def get_document_detail(
    document_id: str,
    db: Session = Depends(get_db)
):
    document = (
        db.query(Document)
        .filter(
            Document.id == document_id
        )
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return {
        "id": document.id,
        "file_name": document.file_name,
        "document_type": document.document_type,
        "chunk_count": document.chunk_count,
        "minio_path": document.minio_path,
        "created_at": document.created_at
    }


@router.delete("/{document_id}")
def delete_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    document = (
        db.query(Document)
        .filter(
            Document.id == document_id
        )
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    document.status = "DELETED" #Todo: Change hard code to enum later

    db.commit()

    return {
        "message": "Document deleted"
    }

