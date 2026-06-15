from datetime import datetime

from sqlalchemy import String
from sqlalchemy import DateTime

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database.database import Base


class ChatSession(Base):

    __tablename__ = "chat_session"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True
    )

    title: Mapped[str] = mapped_column(
        String(500)
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )