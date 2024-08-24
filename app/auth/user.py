from fastapi import Depends, HTTPException
from datetime import datetime, timedelta, timezone
import jwt
import logging
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import joinedload, Session

from app.models.user import UserToken
from app.config.settings import get_settings
from app.config.database import get_session
from app.auth.utils import str_decode, str_encode, generate_keys_and_expiry, verify_password
from app.services.user import load_user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
settings = get_settings()


def get_token_payload(token: str, secret: str, algo: str):
    try:
        payload = jwt.decode(token, secret, algorithms=algo)
    except Exception as jwt_exec:
        logging.debug(f"JWT Error: {str(jwt_exec)}")
        payload = None
    return payload


def create_jwt(payload: dict, secret: str, algo: str, expiry: timedelta):
    expire = datetime.now(timezone.utc) + expiry 
    payload.update({"exp": expire})
    return jwt.encode(payload, secret, algorithm=algo)


async def get_token_user(token: str, db):
    payload = get_token_payload(token, settings.JWT_SECRET, settings.JWT_ALGORITHM)
    if payload:
        user_token = await find_user_token(db, payload)
        if user_token:
            return user_token.user
    return None


async def find_user_token(db, payload):
    user_token_id = decode_token_field(payload, 'r')
    user_id = decode_token_field(payload, 'sub')
    access_key = payload.get('a')
    
    return db.query(UserToken).options(joinedload(UserToken.user)).filter(
        UserToken.access_key == access_key,
        UserToken.id == user_token_id,
        UserToken.user_id == user_id,
        UserToken.expires_at > datetime.now(timezone.utc)
    ).first()


def decode_token_field(payload, field):
    encoded_value = payload.get(field)
    return str_decode(encoded_value) if encoded_value else None


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)):
    user = await get_token_user(token, db)
    if user:
        return user
    raise HTTPException(status_code=401, detail="Not authorised.")


def create_user_token(user_id: int, refresh_key: str, access_key: str, expires_at: datetime, 
                      session: Session) -> UserToken:
    user_token = UserToken()
    user_token.user_id = user_id
    user_token.refresh_key = refresh_key
    user_token.access_key = access_key
    user_token.expires_at = expires_at
    session.add(user_token)
    session.commit()
    session.refresh(user_token)
    return user_token


def create_access_token_payload(user, access_key: str, user_token_id: int) -> dict:
    return {
        "sub": str_encode(str(user.id)),
        'a': access_key,
        'r': str_encode(str(user_token_id)),
        'n': str_encode(f"{user.name}")
    }


def create_refresh_token_payload(user_id: int, refresh_key: str, access_key: str) -> dict:
    return {
        "sub": str_encode(str(user_id)),
        "t": refresh_key,
        'a': access_key
    }


def generate_tokens(at_payload: dict, rt_payload: dict, at_expires: timedelta, rt_expires: timedelta) -> dict:
    access_token = create_jwt(at_payload, settings.JWT_SECRET, settings.JWT_ALGORITHM, at_expires)
    refresh_token = create_jwt(rt_payload, settings.SECRET_KEY, settings.JWT_ALGORITHM, rt_expires)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": at_expires.seconds
    }


def create_token_payload(user, session: Session):
    refresh_key, access_key, rt_expires = generate_keys_and_expiry(settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    expires_at = datetime.now(timezone.utc) + rt_expires
    
    user_token = create_user_token(user.id, refresh_key, access_key, expires_at, session)
    
    at_payload = create_access_token_payload(user, access_key, user_token.id)
    rt_payload = create_refresh_token_payload(user.id, refresh_key, access_key)
    
    at_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    return generate_tokens(at_payload, rt_payload, at_expires, rt_expires)


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
    payload = validate_refresh_token(refresh_token)
    user_token = get_valid_refresh_token(payload, session)
    user_token.expires_at = datetime.now(timezone.utc)
    session.add(user_token)
    session.commit()
    return create_token_payload(user_token.user, session)


def validate_refresh_token(refresh_token):
    payload = get_token_payload(refresh_token, settings.SECRET_KEY, settings.JWT_ALGORITHM)
    if not payload:
        raise HTTPException(status_code=400, detail="Invalid request")
    return payload


def get_valid_refresh_token(payload, session):
    refresh_key = payload.get('t')
    access_key = payload.get('a')
    user_id = str_decode(payload.get('sub'))
    user_token = session.query(UserToken).options(joinedload(UserToken.user)).filter(
        UserToken.refresh_key == refresh_key,
        UserToken.access_key == access_key,
        UserToken.user_id == user_id,
        UserToken.expires_at > datetime.now(timezone.utc)
    ).first()
    if not user_token:
        raise HTTPException(status_code=400, detail="Invalid request")
    return user_token
