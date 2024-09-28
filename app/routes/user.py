from fastapi import APIRouter, BackgroundTasks, Depends, status, File, UploadFile, Request, Query
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from app.responses.user import UserResponse
from app.schemas.user import *
from app.config.database import get_session
from app.auth.user import *
from app.services.user import *
from app.services.admin import get_user_details


templates=Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.dirname(__file__)), "static/html"))


user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"desription": "Not found"}}
)


user_auth_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"desription": "Not found"}},
    dependencies=[Depends(oauth2_scheme), Depends(get_current_user)]
)

 
@user_router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(background_tasks: BackgroundTasks, data: RegisterUserRequest = Depends(RegisterUserRequest.form),
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


@user_router.get("/")
async def register_page(request: Request):
    """
    Register page
    """
    return templates.TemplateResponse("register.html", {"request": request})


@user_router.get("/account-verify", status_code=status.HTTP_200_OK)
async def verify_user_account(background_tasks: BackgroundTasks, 
                              token: str = Query(..., description="Verification token"),
                              email: str = Query(..., description="Email address"),
                              session: Session = Depends(get_session)):
    """
    Verify the new user account

    - **token**: a unique string included in the email to verify the user account
    - **email**: the email of the user, it's an unique identifier
    """
    data = VerifyUserRequest(token=token, email=email)
    await activate_user_account(data, session, background_tasks)
    return JSONResponse({"Message": "Account is activated."})


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
async def update_profile(data: UpdateProfileRequest = Depends(UpdateProfileRequest.form), user = Depends(get_current_user), session: Session = Depends(get_session)):
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


@user_router.get("/logout")
async def logout(response: Response,
                 request: Request,
                 user = Depends(get_current_user)):
    """
    Logout user
    """
    response = RedirectResponse(url="/?logout=true", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="rt", httponly=True, secure=True, samesite='Lax')
    response.delete_cookie(key="Authorization", httponly=True, secure=False, samesite='Lax')
    request.session.clear()
    return response
   