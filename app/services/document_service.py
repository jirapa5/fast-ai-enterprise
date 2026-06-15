from sqlalchemy.orm import Session
from app.models.document import Document


class DocumentService:

    def get_summary(self, db: Session):

        total_documents = (
            db.query(Document)
            .count()
        )

        total_pdf = (
            db.query(Document)
            .filter(
                Document.document_type == "PDF"
            )
            .count()
        )

        total_ocr = (
            db.query(Document)
            .filter(
                Document.document_type == "OCR"
            )
            .count()
        )

        return {
            "total_documents": total_documents,
            "total_pdf_documents": total_pdf,
            "total_ocr_documents": total_ocr
        }


document_service = DocumentService()