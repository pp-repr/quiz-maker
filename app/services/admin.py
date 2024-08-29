from fastapi import HTTPException, status, Depends

from app.models.enums import Role
from app.models.user import User
from app.auth.user import get_current_user
from app.services.user import load_user


def require_role(required_role: Role):
    def role_dependency(user: User = Depends(get_current_user)):
        if user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return user
    return role_dependency


async def delete_user_account(email, session):
    user = await load_user(email, session)
    try:
        session.delete(user)
        session.commit()
    except Exception as e:
        session.rollback()
