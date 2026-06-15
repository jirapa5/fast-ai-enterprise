from datetime import datetime

from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import BigInteger
from sqlalchemy import DateTime

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database.database import Base


class Document(Base):

    __tablename__ = "document"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True
    )

    file_name: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    document_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    chunk_count: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    minio_path: Mapped[str] = mapped_column(
        String(1000),
        nullable=False
    )

    file_size: Mapped[int] = mapped_column(
        BigInteger,
        default=0
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="ACTIVE"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )