from datetime import date, datetime

from pydantic import BaseModel, Field


class DigestEmailItem(BaseModel):
    email_id: int
    subject: str
    sender: str
    summary: str
    category: str
    importance: str
    actions: list[str] = Field(default_factory=list)
    deadlines: list[str] = Field(default_factory=list)


class DailyDigestResponse(BaseModel):
    id: int
    user_id: int
    digest_date: date

    total_emails: int
    important_emails: int

    emails: list[DigestEmailItem] = Field(
        default_factory=list
    )

    created_at: datetime