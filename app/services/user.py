from app.models.user import User

async def create_user_account(data, session):
    user = User()
    user.name = data.name
    user.email = data.email
    user.password = data.password
    user.is_active = False
    session.add(user)
    session.commit()
    session.refresh(user)
    return user