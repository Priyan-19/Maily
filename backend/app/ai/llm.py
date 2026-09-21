from typing import Type

from langchain_groq import ChatGroq
from pydantic import BaseModel

from app.core.config import settings


def get_llm(model: str = "openai/gpt-oss-20b") -> ChatGroq:
    return ChatGroq(
        model=model,
        api_key=settings.groq_api_key,
        temperature=0,
    )


def get_structured_llm(schema: Type[BaseModel] | None = None):
    llm = get_llm("openai/gpt-oss-20b")

    if schema is not None:
        return llm.with_structured_output(schema)

    return llm