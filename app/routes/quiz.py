from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

from app.services.quiz import *

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
    

@router.get("/quiz")
async def get_text(request: Request):
    text = request.session.get("submitted_text", None)
    output = create_output(text)
    questions, correct_answers = parse_quiz(output)
    request.session["correct_answers"] = correct_answers
    return templates.TemplateResponse("quiz.html", {"request": request, "questions": questions})


@router.post("/submit")
async def submit_quiz(request: Request):
    form_data = await request.form()
    user_answers = {key: form_data[key] for key in form_data}
    # correct_answers = request.session.get("correct_answers", None)
    # to do
    request.session["user_answers"] = user_answers
    return {"message": "Dziękujemy za wypełnienie quizu!", "user_answers": user_answers}


@router.get("/submit")
async def get_submit_quiz(request: Request):
    correct_answers = request.session.get("correct_answers", None)
    user_answers = request.session.get("user_answers", None)
    # to do
    return "correct answers: ", correct_answers, "user answers: ", user_answers
