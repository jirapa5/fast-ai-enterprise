import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from contextlib import asynccontextmanager
from app.database.init_db import init_db
from app.controllers.document_controller import router as document_router
from app.controllers.chat_controller import router as chat_router
from app.controllers.dashboard_controller import (
    router as dashboard_router
)

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):

    init_db()

    yield


app = FastAPI(
    title="Enterprise AI Agent Platform (Modular Architecture)",
    description="ระบบโครงสร้างแบบแยกส่วน Controllers และ Services สำหรับประมวลผล OCR และ RAG Chatbot",
    version="4.0",
    lifespan=lifespan
)


raw_origins = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
allowed_origins = [origin.strip() for origin in raw_origins.split(",")]

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# register API Routers
app.include_router(dashboard_router)
app.include_router(document_router)
app.include_router(chat_router)

@app.get("/", tags=["System Health"])
def root_check():
    return {
        "status": "healthy",
        "architecture": "MVC/Service-Pattern Architecture"
    }