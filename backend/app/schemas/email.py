from datetime import datetime

from pydantic import BaseModel, Field


class EmailMessage(BaseModel):
    id: str
    thread_id: str | None = None

    sender: str = ""
    recipient: str = ""
    subject: str = ""

    snippet: str = ""
    body: str = ""

    received_at: datetime | None = None

    labels: list[str] = Field(default_factory=list)


class EmailListResponse(BaseModel):
    emails: list[EmailMessage]
    next_page_token: str | None = None