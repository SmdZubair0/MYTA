from typing import Optional
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from src.main.core.config import settings

class LLMClient:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            cls._client = ChatGroq(
                model = settings.LLM_Model,
                temperature = settings.temerature,
                timeout = settings.timeout
            )
        return cls._client

    @classmethod
    def generate(
        cls,
        prompt: str,
        system_prompt: Optional[str] = None
    ) -> str:
        messages = []

        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
    

        messages.append(
            HumanMessage(content=prompt)
        )

        response = cls.get_client().invoke(messages)

        return response.content