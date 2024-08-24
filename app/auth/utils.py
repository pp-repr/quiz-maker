from passlib.context import CryptContext
from app.utils.string import unique_string
from datetime import timedelta
import string
import base64

from app.models.user import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def check_password_strength(password: str) -> bool:
    if len(password)<8: return False

    if not any (char.isupper() for char in password): return False

    if not any (char.islower() for char in password): return False

    if not any (char.isdigit() for char in password): return False

    if not any (char in string.punctuation for char in password): return False
    return True


def str_encode(string: str) -> str:
    return base64.b85encode(string.encode('ascii')).decode('ascii')


def str_decode(string: str) -> str:
    return base64.b85decode(string.encode('ascii')).decode('ascii')


def get_hash_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def generate_keys_and_expiry(expire_time):
    refresh_key = unique_string(100)
    access_key = unique_string(50)
    rt_expires = timedelta(minutes=expire_time)
    return refresh_key, access_key, rt_expires
