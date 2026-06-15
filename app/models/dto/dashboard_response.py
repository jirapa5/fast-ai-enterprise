from pydantic import BaseModel

class DashboardSummaryResponse(BaseModel):
    total_documents: int
    total_pdf_documents: int
    total_ocr_documents: int
    total_chunks: int
    total_conversations: int
    system_status: str
    last_updated: str