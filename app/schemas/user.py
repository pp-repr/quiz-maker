from pydantic import EmailStr, Field
from fastapi import Form
from typing import Optional

from app.schemas.base import BaseRequest


class RegisterUserRequest(BaseRequest):
    name: str
    email: EmailStr
    password: str

    @staticmethod
    def form(
        name: str = Form(...),
        email: EmailStr = Form(...),
        password: str = Form(...),
    ) -> 'RegisterUserRequest':
        return RegisterUserRequest(
            name=name,
            email=email,
            password=password
        )


class VerifyUserRequest(BaseRequest):
    token: str
    email: EmailStr

    @staticmethod
    def form(
        token: str = Form(...),
        email: EmailStr = Form(...),
    ) -> 'VerifyUserRequest':
        return VerifyUserRequest(
            token=token,
            email=email
        )


class EmailRequest(BaseRequest):
    email: EmailStr

    @staticmethod
    def form(
        email: EmailStr = Form(...),
    ) -> 'EmailRequest':
        return EmailRequest(
            email=email
        )


class ResetRequest(BaseRequest):
    token: str
    email: EmailStr
    password: str

    @staticmethod
    def form(
        token: str = Form(...),
        email: EmailStr = Form(...),
        password: str = Form(...),
    ) -> 'ResetRequest':
        return ResetRequest(
            token=token,
            email=email,
            password=password
        )


class UpdateProfileRequest(BaseRequest):
    name: Optional[str]
    mobile: Optional[str]
    description: Optional[str]

    @staticmethod
    def form(
        name: Optional[str] = Form(None, max_length=50),
        mobile: Optional[str] = Form(None, max_length=9),
        description: Optional[str] = Form(None, max_length=1000),
    ) -> 'UpdateProfileRequest':
        return UpdateProfileRequest(
            name=name,
            mobile=mobile,
            description=description
        )
