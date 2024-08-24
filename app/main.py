from fastapi import FastAPI
from app.routes import user


app = FastAPI()

app.include_router(user.user_router)
app.include_router(user.auth_router)
app.include_router(user.user_auth_router)
