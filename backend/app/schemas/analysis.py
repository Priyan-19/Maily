from typing import Literal

from pydantic import BaseModel, Field


class EmailClassification(BaseModel):
    category: Literal[
        "work",
        "education",
        "finance",
        "social",
        "marketing",
        "notification",
        "personal",
        "other",
    ]

    importance: Literal[
        "low",
        "medium",
        "high",
    ]


class EmailAnalysis(BaseModel):
    summary: str = Field(
        description="Concise summary of the email."
    )

    language: str = Field(
        description="Language used in the email."
    )

    category: Literal[
        "work",
        "education",
        "finance",
        "social",
        "marketing",
        "notification",
        "personal",
        "other",
    ]

    importance: Literal[
        "low",
        "medium",
        "high",
    ]

    actions: list[str] = Field(
        default_factory=list,
        description="Actions the recipient needs to perform.",
    )

    deadlines: list[str] = Field(
        default_factory=list,
        description="Important dates or deadlines.",
    )

class ActionExtraction(BaseModel):
    actions: list[str] = Field(
        default_factory=list,
        description="Specific actions the email recipient needs to perform."
    )


class DeadlineExtraction(BaseModel):
    deadlines: list[str] = Field(
        default_factory=list,
        description="Important dates and deadlines mentioned in the email."
    )

class ReplyGeneration(BaseModel):
    reply: str = Field(
        description="A natural and context-appropriate email reply."
    )