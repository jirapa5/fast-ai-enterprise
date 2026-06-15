from datetime import datetime

from sqlalchemy import (
    BigInteger,
    String,
    Text,
    DateTime
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.database.database import Base


class ChatMessage(Base):

    __tablename__ = "chat_message"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    session_id: Mapped[str] = mapped_column(
        String(36)
    )

    role: Mapped[str] = mapped_column(
        String(20)
    )

    content: Mapped[str] = mapped_column(
        Text
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )