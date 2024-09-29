from fastapi import HTTPException
from datetime import datetime, timezone
import logging
import os
import shutil

from app.services.email import *
from app.utils.context import USER_VERIFY_ACCOUNT, FORGOT_PASSWORD
from app.config.settings import get_settings
from app.auth.utils import verify_password, check_password_strength, str_encode
from app.schemas.user import *


settings = get_settings()


def get_user_by_email(email, session):
    return session.query(User).filter(User.email==email).first()


async def create_user_account(data, session, background_tasks):
    validate_user_data(data, session)
    user = User(
        name=data.name,
        email=data.email,
        password=get_hash_password(data.password),
        is_active=False,
        updated_at=datetime.now(timezone.utc)
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    await send_account_verification_email(user, background_tasks)
    return user


def validate_user_data(data, session):
    if get_user_by_email(data.email, session):
        raise HTTPException(status_code=400, detail="Email already exists")
    if not check_password_strength(data.password):
        raise HTTPException(status_code=400, detail="Password must include lower, upper, digit, and special char")


async def activate_user_account(data, session, background_tasks):
    user = get_user_by_email(data.email, session)
    if not user:
        raise HTTPException(status_code=400, detail=f"This link is valid...")
    verify_user_token(user, data.token)
    user.is_active = True
    user.updated_at = datetime.now(timezone.utc)
    user.verified_at = datetime.now(timezone.utc)
    session.add(user)
    session.commit()
    session.refresh(user)
    await send_account_activation_confirmation_email(user, background_tasks)
    return user


def verify_user_token(user, token):
    user_token = user.get_context(USER_VERIFY_ACCOUNT)
    if not (user_token and verify_password(user_token, token)):
        raise HTTPException(status_code=400, detail="Invalid or expired activation link.")


async def load_user(email: str, db):
    try:
        user = get_user_by_email(email, db)
    except Exception as user_exec:
        logging.info(f"User Not Found, Email: {email}")
        user = None
    return user


async def email_forgot_password_link(data, background_tasks, session):
    user = await load_user(data.email, session)
    if user is None:
        raise HTTPException(status_code=400, detail="Your account is not existing. Register your account.")
    if not user.verified_at:
        raise HTTPException(status_code=400, detail="Your account is not verified. Please check your email inbox to verify your account.")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Your account has been dactivated. Please contact support.")
    await send_password_reset_email(user, background_tasks)


async def reset_user_password(data, session):
    user = await validate_user_for_password_reset(data.email, session)
    user_token = user.get_context(FORGOT_PASSWORD)
    try:
        token = verify_password(user_token, data.token)
    except Exception as exec:
        logging.exception(exec)
        token = False
    if not token:
        raise HTTPException(status_code=400, detail="Invalid window.")
    
    user.password = get_hash_password(data.password)
    user.updated_at = datetime.now()
    session.add(user)
    session.commit()
    session.refresh(user)


async def validate_user_for_password_reset(email, session):
    user = await load_user(email, session)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid request")
    if not user.verified_at:
        raise HTTPException(status_code=400, detail="Invalid request, user not verified")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Invalid request, user disabled")
    return user


async def update_user_profile(email, data, session):
    user = await load_user(email, session)
    user = await update_user_fields(user, data)
    session.commit()
    session.refresh(user)
    return user


async def update_user_fields(user, data):
    update_data = data.model_dump() 
    for key, value in update_data.items():
         if value is not None:
            setattr(user, key, value)
    return user


async def save_user_image(email, file, session):
    try:
        file_location = f"app/static/profile-images/{str_encode(email)}/{file.filename}"
        os.makedirs(os.path.dirname(file_location), exist_ok=True)
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)
        user = await load_user(email, session)
        user.image_url = file_location
        session.commit()
        session.refresh(user)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")