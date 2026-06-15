from fastapi import APIRouter

from app.services.dashboard_service import dashboard_service

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/summary")
def get_dashboard_summary():
    try:
        return dashboard_service.get_summary()
    except Exception as e:
        return {
            "error": str(e)
        }
    