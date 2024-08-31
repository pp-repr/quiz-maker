from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from typing import List, Literal

from app.services.admin import *
from app.models.enums import Role
from app.config.database import get_session
from app.responses.user import UserResponse
from app.services.admin import get_user_details


admin_router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    responses={404: {"desription": "Not found"}},
    dependencies=[Depends(require_role(Role.ADMIN))]
)


@admin_router.get("/", response_model=dict)
async def get_admin():
    return {"hello": "admin"}


@admin_router.get("/users", response_model=List[UserResponse])
async def get_users(session: Session = Depends(get_session)):
    return await get_all_users(session)


@admin_router.delete("/users/delete/{id}")
async def delete_user(id, session: Session = Depends(get_session)):
    await delete_user_account(id, session)
    return {"message": "User deleted successfully"}   


@admin_router.get("/users/{id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user_by_id(id, session: Session = Depends(get_session)):
    return await get_user_details(id, session, "all")


@admin_router.put("/users/{user_id}/role", response_model=UserResponse)
async def update_role(user_id: int, role: Role, session: Session = Depends(get_session)):
    user = await update_user_role(user_id, role, session)
    return user

# @admin_router.get("/moderator", response_model=dict)
# async def get_moderator(user = Depends(require_role(Role.MODERATOR))):
#     return {"hello": user.role}
