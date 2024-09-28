from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import os

from app.services.quiz import *
from app.services.save_quiz import *
from app.config.database import get_session
from app.auth.user import get_current_user
# from app.auth.user import get_current_user_or_none

templates=Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.dirname(__file__)), "static/html"))


router = APIRouter(
    prefix="",
    tags=["Quiz"],
    responses={404: {"desription": "Not found"}}
)


@router.get("/")
async def get_main(request:Request):
    """
    Display the main page with a form to create a quiz
    """
    return templates.TemplateResponse("index.html",{"request":request})


@router.post("/quiz")
async def quiz(request: Request, 
               text: str = Form(...),
               session: Session = Depends(get_session)):
    """
    Create quiz from the text provided by the user using Google Gemini, and save it in session (when user is anonymous)
    or save it in the database (when user is authorized)
    - **text**: text from which the quiz will be generated 
    """
    output = await create_output(text)
    questions, correct_answers = await parse_quiz(output, text)
    token = request.cookies.get("Authorization")
    if token is not None:
        access_token = token[7:]
        user = await get_current_user(access_token, session)
        id_quiz = await save_quiz(questions, correct_answers, session, user.id)
        request.session["id_quiz"] = id_quiz
    else:
        request.session["correct_answers"] = correct_answers
        request.session["questions"] = questions
    return {"message": "Text has been saved in session"}


@router.get("/quiz")
async def get_text(request: Request,
                   session: Session = Depends(get_session)):
    """
    Display the quiz page
    """
    token = request.cookies.get("Authorization")
    if token is not None:
        id_quiz =  request.session.get("id_quiz", None)
        questions, _ = get_questions_and_answers(session, id_quiz)
    else:
        questions = request.session.get("questions", {})
    return templates.TemplateResponse("quiz.html", {"request": request, "questions": questions})


@router.post("/submit")
async def submit_quiz(request: Request,
                      session: Session = Depends(get_session)):
    """
    Display the quiz results
    """
    user_answers = await get_user_answer(request)
    token = request.cookies.get("Authorization")
    if token is not None:
        id_quiz =  request.session.get("id_quiz", None)
        questions, correct_answers = get_questions_and_answers(session, id_quiz)
    else:
        correct_answers = request.session.get("correct_answers", {})
        questions = request.session.get("questions", {})
    results = await check_answers(user_answers, correct_answers)
    request.session.clear()
    return templates.TemplateResponse("submit.html", {"request": request, "results": results, "questions": questions})
