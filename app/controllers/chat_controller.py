from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai_service import ai_service
from typing import Optional
from uuid import uuid4

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.models.chat_session import ChatSession
from app.models.chat_message import ChatMessage

router = APIRouter(prefix="/chat", tags=["AI Chatbot (Generative AI)"])

class QueryRequest(BaseModel):
    question: str
    session_id: Optional[str] = None


@router.post("/ask/")
async def ask_ai_chatbot(
    request: QueryRequest,
    db: Session = Depends(get_db)
):
    try:

        session_id = request.session_id

        # สร้าง Session ใหม่
        if not session_id:

            session = ChatSession(
                id=str(uuid4()),
                title=request.question[:100]
            )

            db.add(session)
            db.commit()

            session_id = session.id

        # Save User Question
        user_message = ChatMessage(
            session_id=session_id,
            role="USER",
            content=request.question
        )

        db.add(user_message)
        db.commit()

        # Call AI
        response = await ai_service.answer_question(
            request.question
        )

        # Save AI Answer
        assistant_message = ChatMessage(
            session_id=session_id,
            role="ASSISTANT",
            content=response["answer"]
        )

        db.add(assistant_message)
        db.commit()

        return {
            "session_id": session_id,
            "ai_answer": response["answer"],
            "referenced_sources": [
                {
                    "content": doc.page_content[:150] + "...",
                    "source_file": doc.metadata.get(
                        "source",
                        "Unknown"
                    ),
                    "type": doc.metadata.get(
                        "type",
                        "Unknown"
                    )
                }
                for doc in response["context"]
            ]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    

@router.get("/sessions")
async def get_sessions(
    db: Session = Depends(get_db)
):

    sessions = (
        db.query(ChatSession)
        .order_by(ChatSession.created_at.desc())
        .all()
    )

    return [
        {
            "id": s.id,
            "title": s.title,
            "created_at": s.created_at
        }
        for s in sessions
    ]


@router.get("/sessions/{session_id}")
async def get_session_messages(
    session_id: str,
    db: Session = Depends(get_db)
):

    messages = (
        db.query(ChatMessage)
        .filter(
            ChatMessage.session_id == session_id
        )
        .order_by(ChatMessage.created_at.asc())
        .all()
    )

    return {
        "session_id": session_id,
        "messages": [
            {
                "role": m.role,
                "content": m.content,
                "created_at": m.created_at
            }
            for m in messages
        ]
    }