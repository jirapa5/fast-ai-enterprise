import os
from langchain_google_genai import ChatGoogleGenerativeAI

class AIService:

    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.2
        )

    async def answer_question(self, question: str):
        response = self.llm.invoke(question)

        return {
            "answer": response.content,
            "context": []
        }

ai_service = AIService()