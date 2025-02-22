from fastapi import APIRouter, Request, Form, Depends, Query
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import os

from app.services.quiz import *
from app.services.save_quiz import *
from app.config.database import get_session
from app.auth.user import get_current_user
from app.schemas.quiz import QuizEditRequest

templates=Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.dirname(__file__)), "static/html"))


router = APIRouter(
    prefix="",
    tags=["Quiz"],
    responses={404: {"desription": "Not found"}}
)


router_quiz = APIRouter(
    prefix="/users",
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
        return {"id_quiz": id_quiz}
    else:
        request.session["correct_answers"] = correct_answers
        request.session["questions"] = questions
        return {"message": "Text has been saved in session"}


@router.get("/quiz")
async def get_text(request: Request,
                   id: int = Query(..., description="Id quiz"),
                   session: Session = Depends(get_session)):
    """
    Display the quiz page
    """
    token = request.cookies.get("Authorization")
    if token is not None:
        user = await get_current_user(token[7:], session)
        questions, _ = await get_questions_and_answers(session, id, user)
        request.session["id_quiz"] = id
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
        user = await get_current_user(token[7:], session)
        questions, correct_answers = await get_questions_and_answers(session, id_quiz, user)
    else:
        correct_answers = request.session.get("correct_answers", {})
        questions = request.session.get("questions", {})
    results = await check_answers(user_answers, correct_answers)
    request.session.clear()
    return templates.TemplateResponse("submit.html", {"request": request, "results": results, "questions": questions})


@router_quiz.get("/me/quizzes")
async def get_quizzes(request: Request,
                      session: Session = Depends(get_session),
                      user = Depends(get_current_user)):
    """
    Show all user's quizzes.
    """
    quizzes = await get_all_quizzes(user, session)
    return templates.TemplateResponse("quizzes.html", {"request": request, "quizzes": quizzes})


@router_quiz.post("/me/quizzes")
async def edit_quiz(session: Session = Depends(get_session),
                    data: QuizEditRequest = Depends(QuizEditRequest.form)):
    await update_name_quiz(session, data)
    return {"message": "Quiz updated successfully"}
