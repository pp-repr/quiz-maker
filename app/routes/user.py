from fastapi import APIRouter,Depends, status
from app.responses.user import UserResponse
from app.schemas.user import RegisterUserRequest
from app.config.database import get_session
from sqlalchemy.orm import Session
from app.services import user


user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"desription": "Not found"}}
)
 
@user_router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(data: RegisterUserRequest, session: Session = Depends(get_session)):
    return await user.create_user_account(data, session)