from fastapi import APIRouter, BackgroundTasks, Depends, status, Header, File, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.responses.user import UserResponse, LoginResponse
from app.schemas.user import *
from app.config.database import get_session
from app.auth.user import *
from app.services.user import *
from app.services.admin import get_user_details


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
    """
    Register a new user using details such as name, email, and password, and store this information in the database. Upon successful
    registration, send an activation link to the user's email

    - **name**: the name of the user, you can change it later
    - **email**: the email of the user, it's an unique identifier
    - **password**: the password of the user, must contain **8** characters, including both **uppercase** and **lowercase** letters, 
    a **number**, and a **special** character
    """
    return await create_user_account(data, session, background_tasks)


@user_router.post("/verify", status_code=status.HTTP_200_OK)
async def verify_user_account(data: VerifyUserRequest, background_tasks: BackgroundTasks,
                        session: Session = Depends(get_session)):
    """
    Verify the new user account

    - **token**: a unique string included in the email to verify the user account
    - **email**: the email of the user, it's an unique identifier
    """
    await activate_user_account(data, session, background_tasks)
    return JSONResponse({"Message": "Account is activated."})


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
async def forgot_password(data: EmailRequest, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    """
    Endpoint allows users to initiate a password reset process if they have forgotten their current password
    
    - **email**: the email of the user used to register the user, a **reset link** will be sent to this email address
    """
    await email_forgot_password_link(data, background_tasks, session)
    return JSONResponse({"message": "A email with password reset link has been sent to you."})


@auth_router.put("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(data: ResetRequest, session: Session = Depends(get_session)):
    """
    Change your password using the token received in the email
    
    - **token**: a unique string included in the email
    - **email**: the email of the user
    - **password**: new password of the user, must contain **8** characters, including both **uppercase** and **lowercase** letters, 
    a **number**, and a **special** character
    """
    await reset_user_password(data, session)
    return JSONResponse({"message": "Your password has been updated."})


@user_auth_router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user(user = Depends(get_current_user)):
    """
    Display all the information for the authorized user
    """
    return user


@user_auth_router.get("/{id}", status_code=status.HTTP_200_OK, response_model=dict)
async def get_another_user(id, session: Session = Depends(get_session)):
    """
    Show information about the user, including their name, description, image, active status, and creation date

    - **id**: unique identifier of the user, must be an integer
    """
    fields = ['name', 'description', 'image_url', 'is_active', 'created_at']
    return await get_user_details(id, session, fields)


@user_auth_router.patch("/me/edit", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def update_profile(data: UpdateProfileRequest, user = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Edit basic information about the user, all fields are optional; you can change just one or two if you wish

    - **name**: the user's name
    - **mobile**: the user's mobile number
    - **description**:  the user's description
    """
    updated_user = await update_user_profile(user.email, data, session)
    return updated_user


@user_router.put("/me/profile-image", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def update_image(file: UploadFile = File(...), user = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Edit the user's profile image

    - **file**: choose a photo from your disk for your profile image
    """
    updated_user = await save_user_image(user.email, file, session)
    return updated_user
   