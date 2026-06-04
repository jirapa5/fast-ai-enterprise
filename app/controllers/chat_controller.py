from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai_service import ai_service

router = APIRouter(prefix="/chat", tags=["AI Chatbot (Generative AI)"])

class QueryRequest(BaseModel):
    question: str

@router.post("/ask/")
async def ask_ai_chatbot(request: QueryRequest):
    try:
        response = await ai_service.answer_question(request.question)
        
        return {
            "ai_answer": response["answer"],
            "referenced_sources": [
                {
                    "content": doc.page_content[:150] + "...", 
                    "source_file": doc.metadata.get("source", "Unknown"),
                    "type": doc.metadata.get("type", "Unknown")
                } 
                for doc in response["context"]
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))