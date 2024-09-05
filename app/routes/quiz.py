from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import os

templates=Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.dirname(__file__)), "static/html"))


router = APIRouter(
    prefix="",
    tags=["Quiz"],
    responses={404: {"desription": "Not found"}}
)

@router.get("/")
async def get_main(request:Request):
    return templates.TemplateResponse("index.html",{"request":request})