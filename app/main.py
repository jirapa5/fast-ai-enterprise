# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from app.controllers.document_controller import router as document_router
from app.controllers.chat_controller import router as chat_router


app = FastAPI(
    title="Enterprise AI Agent Platform (Modular Architecture)",
    description="ระบบโครงสร้างแบบแยกส่วน Controllers และ Services สำหรับประมวลผล OCR และ RAG Chatbot",
    version="4.0"
)

# ลงทะเบียนเชื่อมเส้นทาง API โดยเรียกใช้ชื่อตัวแปรที่ระบุมาด้านบน
app.include_router(document_router)
app.include_router(chat_router)

@app.get("/", tags=["System Health"])
def root_check():
    return {"status": "healthy", "architecture": "MVC/Service-Pattern Architecture"}