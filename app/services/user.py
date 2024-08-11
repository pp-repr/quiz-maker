from app.models.user import User
from app.config.security import get_hash_password, check_password_strength, get_user_by_email
from fastapi import HTTPException
import datetime
from app.services.email import send_account_verification_email


async def create_user_account(data, session, background_tasks):
    if get_user_by_email(data, session):
        raise HTTPException(status_code=400, detail="Email is already exists")
    
    if not check_password_strength(data.password):
        raise HTTPException(status_code=400, detail="Please provide password with lower, upper, digit and special char")
    
    user = User()
    user.name = data.name
    user.email = data.email
    user.password = get_hash_password(data.password)
    user.is_active = False
    user.updated_at = datetime.datetime.utcnow()
    session.add(user)
    session.commit()
    session.refresh(user)

    await send_account_verification_email(user, background_tasks)
    return user