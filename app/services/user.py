from fastapi import HTTPException
from datetime import datetime, timedelta, timezone
import logging
from sqlalchemy.orm import joinedload

from app.models.user import User, UserToken
from app.config.security import *
from app.services.email import *
from app.utils.context import USER_VERIFY_ACCOUNT, FORGOT_PASSWORD
from app.utils.string import unique_string
from app.config.settings import get_settings

settings = get_settings()


async def create_user_account(data, session, background_tasks):
    if get_user_by_email(data.email, session):
        raise HTTPException(status_code=400, detail="Email is already exists")
    
    if not check_password_strength(data.password):
        raise HTTPException(status_code=400, detail="Please provide password with lower, upper, digit and special char")
    
    user = User()
    user.name = data.name
    user.email = data.email
    user.password = get_hash_password(data.password)
    user.is_active = False
    user.updated_at = datetime.now(timezone.utc)
    session.add(user)
    session.commit()
    session.refresh(user)

    await send_account_verification_email(user, background_tasks)
    return user


async def activate_user_account(data, session, background_tasks):
    user = get_user_by_email(data.email, session)
    if not user:
        raise HTTPException(status_code=400, detail=f"This link is valid...")
    user_token = user.get_context(USER_VERIFY_ACCOUNT)
    try:
        token = verify_password(user_token, data.token)
    except Exception as verify_exception:
        logging.exception(verify_exception)
        token = False
    if not token:
        raise HTTPException(status_code=400, detail="This link expired")
    user.is_active = True
    user.updated_at = datetime.now(timezone.utc)
    user.verified_at = datetime.now(timezone.utc)
    session.add(user)
    session.commit()
    session.refresh(user)
    await send_account_activation_confirmation_email(user, background_tasks)
    return user


async def get_login_token(data, session):
    user = await load_user(data.username, session)
    if not user:
        raise HTTPException(status_code=400, detail="Email not found")
    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Your account is deactivated, contact with support")
    if not user.verified_at:
        raise HTTPException(status_code=400, detail="Your account is not verified, check your email inbox")

    return create_token_payload(user, session)


async def get_refresh_token(refresh_token, session):
    payload = get_token_payload(refresh_token, settings.SECRET_KEY, settings.JWT_ALGORITHM)
    if not payload:
        raise HTTPException(status_code=400, detail="Invalid request")
    refresh_key = payload.get('t')
    access_key = payload.get('a')
    user_id = str_decode(payload.get('sub'))
    user_token = session.query(UserToken).options(joinedload(UserToken.user)).filter(UserToken.refresh_key == refresh_key,
                                                 UserToken.access_key == access_key,
                                                 UserToken.user_id == user_id,
                                                 UserToken.expires_at > datetime.now(timezone.utc)
                                                 ).first()
    if not user_token:
        raise HTTPException(status_code=400, detail="Invalid request")
    user_token.expires_at = datetime.now(timezone.utc)
    session.add(user_token)
    session.commit()
    return create_token_payload(user_token.user, session)


def create_token_payload(user, session):
    refresh_key = unique_string(100)
    access_key = unique_string(50)
    rt_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    user_token = UserToken()
    user_token.user_id = user.id
    user_token.refresh_key = refresh_key
    user_token.access_key = access_key
    user_token.expires_at = datetime.now(timezone.utc) + rt_expires
    session.add(user_token)
    session.commit()
    session.refresh(user_token)

    at_payload = {
        "sub": str_encode(str(user.id)),
        'a': access_key,
        'r': str_encode(str(user_token.id)),
        'n': str_encode(f"{user.name}")
    }
    at_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(at_payload, at_expires)
    
    rt_payload = {
        "sub": str_encode(str(user.id)), 
        "t": refresh_key, 
        'a': access_key
        }
    refresh_token = create_refresh_token(rt_payload, rt_expires)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": at_expires.seconds
    }


def create_access_token(payload, expires):
    return generate_token(payload, settings.JWT_SECRET, settings.JWT_ALGORITHM, expires)


def create_refresh_token(payload, expires):
    return generate_token(payload, settings.SECRET_KEY, settings.JWT_ALGORITHM, expires)


async def email_forgot_password_link(data, background_tasks, session):
    user = await load_user(data.email, session)
    if not user.verified_at:
        raise HTTPException(status_code=400, detail="Your account is not verified. Please check your email inbox to verify your account.")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Your account has been dactivated. Please contact support.")
    await send_password_reset_email(user, background_tasks)


async def reset_user_password(data, session):
    user = await load_user(data.email, session)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid request")
    if not user.verified_at:
        raise HTTPException(status_code=400, detail="Invalid request")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Invalid request")
    
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


async def get_user_details(id, session):
    user = session.query(User).filter(User.id == id).first()
    if user:
        return user
    raise HTTPException(status_code=400, detail="User does not exists.")
