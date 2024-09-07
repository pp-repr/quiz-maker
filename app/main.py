from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from app.routes import quiz, user, admin
from app.config.settings import get_settings
import os

main_path = os.path.dirname(__file__)
settings = get_settings()

app = FastAPI()
app.mount('/static', StaticFiles(directory=os.path.join(main_path, 'static')), name='static')
app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_KEY)

app.include_router(user.user_router)
app.include_router(user.auth_router)
app.include_router(user.user_auth_router)
app.include_router(admin.admin_router)
app.include_router(quiz.router)
