from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class RegisterUserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class VerifyUserRequest(BaseModel):
    token: str
    email: EmailStr


class EmailRequest(BaseModel):
    email: EmailStr


class ResetRequest(BaseModel):
    token: str
    email: EmailStr
    password: str


class UpdateProfileRequest(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    mobile: Optional[str] = Field(None, max_length=9)
    description: Optional[str] = Field(None, max_length=1000)


class DeleteRequest(BaseModel):
    email: EmailStr
