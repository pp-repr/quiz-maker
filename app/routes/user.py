from fastapi import APIRouter, BackgroundTasks, Depends, status, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.responses.user import UserResponse, LoginResponse
from app.schemas.user import RegisterUserRequest, VerifyUserRequest, EmailRequest, ResetRequest
from app.config.database import get_session
from app.config.security import oauth2_scheme, get_current_user
from app.services.user import *


user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"desription": "Not found"}}
)


auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404: {"desription": "Not found"}}
)


user_auth_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"desription": "Not found"}},
    dependencies=[Depends(oauth2_scheme), Depends(get_current_user)]
)

 
@user_router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(data: RegisterUserRequest, background_tasks: BackgroundTasks,
                        session: Session = Depends(get_session)):
    return await create_user_account(data, session, background_tasks)


@user_router.post("/verify", status_code=status.HTTP_200_OK)
async def verify_user_account(data: VerifyUserRequest, background_tasks: BackgroundTasks,
                        session: Session = Depends(get_session)):
    await activate_user_account(data, session, background_tasks)
    return JSONResponse({"Message": "Account is activated."})


@auth_router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def user_login(data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    return await get_login_token(data, session)


@auth_router.post("/refresh", status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def refresh_token(refresh_token = Header(), session: Session = Depends(get_session)):
    return await get_refresh_token(refresh_token, session)


@auth_router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(data: EmailRequest, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    await email_forgot_password_link(data, background_tasks, session)
    return JSONResponse({"message": "A email with password reset link has been sent to you."})


@auth_router.put("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(data: ResetRequest, session: Session = Depends(get_session)):
    await reset_user_password(data, session)
    return JSONResponse({"message": "Your password has been updated."})


@user_auth_router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user(user = Depends(get_current_user)):
    return user


@user_auth_router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user_by_id(id, session: Session = Depends(get_session)):
    return await get_user_details(id, session)
    