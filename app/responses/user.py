from typing import Any, Dict, Union
from datetime import datetime
from typing import Optional
from pydantic import EmailStr

from app.responses.base import BaseResponse
from app.models.enums import Role


class UserResponse(BaseResponse):
    id: int
    name: str
    email: EmailStr
    mobile: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    is_active: bool
    role: Role
    created_at: Union[str, None, datetime] = None


class LoginResponse(BaseResponse):
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = "Bearer"
