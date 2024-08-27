from fastapi import APIRouter, status, Depends

from app.services.admin import require_role
from app.models.enums import Role


admin_router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    responses={404: {"desription": "Not found"}}
)


@admin_router.get("/", status_code=status.HTTP_200_OK, response_model=dict)
async def get_admin(user = Depends(require_role(Role.ADMIN))):
    return {"hello": user.role}


@admin_router.get("/moderator", status_code=status.HTTP_200_OK, response_model=dict)
async def get_moderator(user = Depends(require_role(Role.MODERATOR))):
    return {"hello": user.role}