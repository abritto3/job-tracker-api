from pydantic import BaseModel, EmailStr, Field
from pydantic import ConfigDict
from datetime import datetime


# -------- Auth --------
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    created_at: datetime



class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# -------- Applications --------
class ApplicationCreate(BaseModel):
    company: str = Field(min_length=1, max_length=200)
    role_title: str = Field(min_length=1, max_length=200)
    status: str = Field(default="applied", max_length=50)
    location: str | None = Field(default=None, max_length=200)
    link: str | None = Field(default=None, max_length=500)
    notes: str | None = None


class ApplicationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company: str
    role_title: str
    status: str
    applied_at: datetime
    location: str | None
    link: str | None
    notes: str | None
    is_active: bool


ALLOWED_STATUSES = {"applied", "interview", "offer", "rejected"}


class ApplicationUpdate(BaseModel):
    company: str | None = Field(default=None, min_length=1, max_length=200)
    role_title: str | None = Field(default=None, min_length=1, max_length=200)
    status: str | None = Field(default=None, max_length=50)
    location: str | None = Field(default=None, max_length=200)
    link: str | None = Field(default=None, max_length=500)
    notes: str | None = None
    is_active: bool | None = None