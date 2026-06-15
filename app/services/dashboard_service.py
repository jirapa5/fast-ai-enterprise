from datetime import datetime, timezone

from app.services.vector_service import vector_service

class DashboardService:

    def get_summary(self):

        total_chunks = 0

        try:
            if vector_service and vector_service.db:
                total_chunks = len(
                    vector_service.db.get()["ids"]
                )
        except Exception as e:
            print(f"Dashboard Error: {e}")

        return {
            "total_documents": total_chunks,
            "total_pdf_documents": 0,
            "total_ocr_documents": 0,
            "total_chunks": total_chunks,
            "total_conversations": 0,
            "system_status": "healthy",
            "last_updated": datetime.now(
                timezone.utc
            ).isoformat()
        }

dashboard_service = DashboardService()