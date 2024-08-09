from fastapi import FastAPI
from app.routes import user

# from app.config.utils import wait_for_mysql
# from app.models.user import Base
# from app.config.database import engine


app = FastAPI()

# @app.on_event("startup")
# def startup_event():
#     wait_for_mysql()
#     Base.metadata.create_all(bind=engine)

app.include_router(user.user_router)


