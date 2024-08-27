from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

from app.models.enums import Role
from app.models.user import User
from app.auth.utils import get_hash_password


def get_admin_data():
    load_dotenv()
    admin = User(
            name=os.getenv("ADMIN_NAME"),
            email=os.getenv("ADMIN_EMAIL"),
            role=Role.ADMIN,
            is_active=True,
            password=get_hash_password(os.getenv("ADMIN_PASSWORD")),
            created_at=datetime.now(timezone.utc),
            verified_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
    return admin


def create_admin_if_not_exists(session: Session):
    admin_exists = session.query(User).filter_by(role=Role.ADMIN).first()
    if not admin_exists:
        admin = get_admin_data()
        session.add(admin)
        session.commit()
