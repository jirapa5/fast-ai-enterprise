import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document

from app.config import settings


class VectorService:

    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")

        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=api_key
        )

        self.db = Chroma(
            persist_directory="./chroma_db",
            embedding_function=self.embeddings
        )

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

    def add_pdf_document(self, file_path: str, source_name: str):
        loader = PyPDFLoader(file_path)

        docs = loader.load()

        for doc in docs:
            doc.metadata["source"] = source_name
            doc.metadata["type"] = "PDF"

        chunks = self.text_splitter.split_documents(docs)

        self.db.add_documents(chunks)

        return len(chunks)

    def add_text_document(
        self,
        text: str,
        source_name: str,
        document_type: str = "TEXT"
    ):
        document = Document(
            page_content=text,
            metadata={
                "source": source_name,
                "type": document_type
            }
        )

        chunks = self.text_splitter.split_documents([document])

        self.db.add_documents(chunks)

        return len(chunks)

    def search_similar_documents(
        self,
        query: str,
        k: int = 3
    ):
        return self.db.similarity_search(query, k=k)

    def search_similar_context(
        self,
        query: str,
        k: int = 3
    ):
        results = self.db.similarity_search(query, k=k)

        return "\n---\n".join(
            [doc.page_content for doc in results]
        )


vector_service = VectorService()