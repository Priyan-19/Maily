from typing import Type

from langchain_groq import ChatGroq
from pydantic import BaseModel

from app.core.config import settings


def get_llm(model: str = "llama-3.3-70b-versatile") -> ChatGroq:
    return ChatGroq(
        model=model,
        api_key=settings.groq_api_key,
        temperature=0,
    )


def get_structured_llm(schema: Type[BaseModel] | None = None):
    llm = get_llm("llama-3.3-70b-versatile")

    if schema is not None:
        return llm.with_structured_output(schema)

    return llm