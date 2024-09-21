from fastapi import APIRouter, BackgroundTasks, Depends, status, Header, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates

from app.responses.user import LoginResponse
from app.schemas.user import *
from app.config.database import get_session
from app.auth.user import *
from app.services.user import *


templates=Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.dirname(__file__)), "static/html"))


auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404: {"desription": "Not found"}}
)


@auth_router.get("/login")
async def login_page(request: Request):
    """
    Login page
    """
    return templates.TemplateResponse("login.html", {"request": request})


@auth_router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def user_login(data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    """
    Login user

    - **username**: email address used to register the user
    - **password**: password used to register the user
    """
    return await get_login_token(data, session)


@auth_router.post("/refresh", status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def refresh_token(refresh_token = Header(), session: Session = Depends(get_session)):
    """
    Refresh token
    """
    return await get_refresh_token(refresh_token, session)


@auth_router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(background_tasks: BackgroundTasks, data: EmailRequest = Depends(EmailRequest.form), session: Session = Depends(get_session)):
    """
    Endpoint allows users to initiate a password reset process if they have forgotten their current password
    
    - **email**: the email of the user used to register the user, a **reset link** will be sent to this email address
    """
    await email_forgot_password_link(data, background_tasks, session)
    return JSONResponse({"message": "A email with password reset link has been sent to you."})


@auth_router.put("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(data: ResetRequest = Depends(ResetRequest.form), session: Session = Depends(get_session)):
    """
    Change your password using the token received in the email
    
    - **token**: a unique string included in the email
    - **email**: the email of the user
    - **password**: new password of the user, must contain **8** characters, including both **uppercase** and **lowercase** letters, 
    a **number**, and a **special** character
    """
    await reset_user_password(data, session)
    return JSONResponse({"message": "Your password has been updated."})