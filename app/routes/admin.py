from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from app.services.admin import require_role, delete_user_account
from app.models.enums import Role
from app.schemas.user import DeleteRequest
from app.config.database import get_session
from app.responses.user import UserResponse
from app.services.user import get_user_details


admin_router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    responses={404: {"desription": "Not found"}},
    dependencies=[Depends(require_role(Role.ADMIN))]
)


@admin_router.get("/", response_model=dict)
async def get_admin():
    return {"hello": "admin"}


@admin_router.delete("/delete-user")
async def delete_user(data: DeleteRequest,
                      session: Session = Depends(get_session)):
    await delete_user_account(data.email, session)
    return {"message": "User deleted successfully"}   


@admin_router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user_by_id(id, session: Session = Depends(get_session)):
    return await get_user_details(id, session, "all")


# @admin_router.get("/moderator", response_model=dict)
# async def get_moderator(user = Depends(require_role(Role.MODERATOR))):
#     return {"hello": user.role}
