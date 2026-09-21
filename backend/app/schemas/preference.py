from pydantic import BaseModel


class UserPreferenceBase(BaseModel):
    language: str = "Tanglish"
    digest_enabled: bool = True
    digest_time: str = "08:00"


class UserPreferenceUpdate(BaseModel):
    language: str | None = None
    digest_enabled: bool | None = None
    digest_time: str | None = None


class UserPreferenceResponse(UserPreferenceBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
