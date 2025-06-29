from datetime import datetime
from typing import List, Optional
from  datetime import date
from pydantic import BaseModel, EmailStr, Field


class ContactBase(BaseModel):
    name: str
    surname: str
    email: EmailStr
    phone: str
    birthday: date
    info: Optional[str] = None


class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=15)
    surname: Optional[str] = Field(None, max_length=15)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=15)
    birthday: Optional[date] = None
    info: Optional[str] = None


class ContactResponse(ContactBase):
    id: int

    class Config:
        from_attributes = True


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr
