from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class ContactSchema(BaseModel):
    first_name: str = Field(max_length=150)
    last_name: str = Field(max_length=150)
    email: EmailStr
    phone_number: str = Field(max_length=30)
    birthday : date
    add_info: Optional[str]=''


class ContactResponseSchema(ContactSchema):
    id: int = 1
    created_at: datetime

    class Config:
        from_attributes = True

class UserSchema(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=8)


class UserResponse(BaseModel):
    id: int = 1
    username: str
    email: EmailStr
    avatar: str

    class Config:
        from_attributes = True


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RequestEmail(BaseModel):
    email: EmailStr