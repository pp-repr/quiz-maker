from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.responses.user import UserResponse, LoginResponse
from app.schemas.user import RegisterUserRequest, VerifyUserRequest
from app.config.database import get_session
from app.services.user import create_user_account, activate_user_account, get_login_token
from app.config.security import oauth2_scheme
from app.services import user


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

 
@user_router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(data: RegisterUserRequest, background_tasks: BackgroundTasks,
                        session: Session = Depends(get_session)):
    return await create_user_account(data, session, background_tasks)


@user_router.post("/verify", status_code=status.HTTP_200_OK)
async def verify_user_account(data: VerifyUserRequest, background_tasks: BackgroundTasks,
                        session: Session = Depends(get_session)):
    await activate_user_account(data, session, background_tasks)
    return JSONResponse({"Message": "Account is activated."})


@user_router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def user_login(data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    return await get_login_token(data, session)


@auth_router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def user_login(data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    return await user.get_login_token(data, session)
    