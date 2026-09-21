from langchain_core.runnables import Runnable

from app.ai.llm import get_structured_llm


from app.ai.prompts.action_extraction import action_prompt
from app.ai.prompts.classification import classification_prompt
from app.ai.prompts.deadline_extraction import deadline_prompt
from app.ai.prompts.email_analysis import email_analysis_prompt
from app.ai.prompts.reply import reply_prompt

from app.schemas.analysis import (
    ActionExtraction,
    DeadlineExtraction,
    EmailAnalysis,
    EmailClassification,
    ReplyGeneration,
)


def get_classification_chain() -> Runnable:
    llm = get_structured_llm(EmailClassification)

    return classification_prompt | llm


def get_action_chain() -> Runnable:
    llm = get_structured_llm(ActionExtraction)

    return action_prompt | llm


def get_deadline_chain() -> Runnable:
    llm = get_structured_llm(DeadlineExtraction)

    return deadline_prompt | llm


def get_email_analysis_chain() -> Runnable:
    llm = get_structured_llm(EmailAnalysis)

    return email_analysis_prompt | llm

def get_reply_chain() -> Runnable:
    llm = get_structured_llm(ReplyGeneration)

    return reply_prompt | llm