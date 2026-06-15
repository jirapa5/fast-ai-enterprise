from app.config import settings

from app.database.database import Base
from app.database.database import engine

from app.models.document import Document
from app.models.chat_session import ChatSession
from app.models.chat_message import ChatMessage



def init_db():

    if settings.is_dev:
        print(
            "Development Mode: Auto create tables"
        )

        Base.metadata.create_all(
            bind=engine
        )

    else:
        print(
            "Production Mode: Skip create_all()"
        )