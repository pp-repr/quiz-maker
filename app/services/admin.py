from fastapi import HTTPException, status, Depends
import logging

from app.models.enums import Role
from app.models.user import User
from app.auth.user import get_current_user


async def get_user_by_id(id, session):
    try:
        user = session.query(User).filter(User.id==id).first()
    except Exception as user_exec:
        logging.ERROR(f"User Not Found, Id: {id}")
        user = None
    return user


async def get_user_details(id, session, fields):   
    user = await get_user_by_id(id, session)
    if fields == "all": 
        return user
    else:
        user_data = {field: getattr(user, field) for field in fields}
        return user_data


def require_role(required_role: Role):
    def role_dependency(user: User = Depends(get_current_user)):
        if user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return user
    return role_dependency


async def delete_user_account(id, session):
    user = await get_user_by_id(id, session)
    try:
        session.delete(user)
        session.commit()
    except Exception as e:
        session.rollback()

    
async def get_all_users(session):
    return session.query(User).all()


async def update_user_role(id, role, session):
    user = await get_user_by_id(id, session)
    user.role = role
    session.commit()
    session.refresh(user)
    return user


