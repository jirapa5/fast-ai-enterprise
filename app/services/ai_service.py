import os

from langchain_google_genai import ChatGoogleGenerativeAI


class AIService:
    def __init__(self):
        self.llm = None

    def _initialize(self):
        if self.llm is not None:
            return

        api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GOOGLE_API_KEY is not set"
            )

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.2
        )

    async def answer_question(
        self,
        question: str
    ):
        self._initialize()

        response = self.llm.invoke(question)

        return {
            "answer": response.content,
            "context": []
        }


ai_service = AIService()