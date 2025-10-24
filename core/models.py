from pydantic import BaseModel, HttpUrl, field_validator
from datetime import date


class CDLIntake(BaseModel):
    date: date
    stream: str
    founder_name: str
    venture_name: str
    venture_manager_name: str
    link: HttpUrl
    password: str
    comments: str | None = None


    @field_validator("stream")
    @classmethod
    def non_empty_stream(cls, v: str) -> str:
        if not v or v.strip() == "":
            raise ValueError("Stream is required")
        return v


    @field_validator("founder_name", "venture_name", "venture_manager_name", "password")
    @classmethod
    def non_empty_text(cls, v: str) -> str:
        if not v or v.strip() == "":
            raise ValueError("Field cannot be empty")
        return v.strip()