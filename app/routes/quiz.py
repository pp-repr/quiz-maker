from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

from app.services.quiz import create_quiz

templates=Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.dirname(__file__)), "static/html"))


router = APIRouter(
    prefix="",
    tags=["Quiz"],
    responses={404: {"desription": "Not found"}}
)


@router.get("/")
async def get_main(request:Request):
    return templates.TemplateResponse("index.html",{"request":request})


@router.post("/quiz")
async def quiz(request: Request, text: str = Form(...)):
    request.session["submitted_text"] = text
    return {"message": "Text has been saved in session"}
    

@router.get("/quiz", response_class=HTMLResponse)
async def get_text(request: Request):
    text = request.session.get("submitted_text", None)
    quiz = await create_quiz(text)
    if text:
        return f"<h1>Oto Twój tekst: {quiz}</h1>"
    else:
        return "<h1>Brak tekstu do wyświetlenia</h1>"