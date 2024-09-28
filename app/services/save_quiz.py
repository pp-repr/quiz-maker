from fastapi import HTTPException
import logging
import json

from app.models.quiz import UserQuiz, QuizQuestion
from app.services.quiz import split_json


async def save_quiz(questions, correct_answers, session, user_id):
    if len(questions) != len(correct_answers):
        raise HTTPException(status_code=500,
                            detail="Something went wrong, try again")
    id_quiz = create_quiz_id(user_id, session)
    add_questions_to_database(questions, correct_answers, session, id_quiz)
    return id_quiz


def create_quiz_id(user_id, session):
    new_quiz = UserQuiz(user_id=user_id)
    session.add(new_quiz)
    session.commit()
    session.refresh(new_quiz)
    return new_quiz.id


def add_questions_to_database(questions, correct_answers, session, id_quiz):
    for question, correct in zip(questions, correct_answers.values()):
        ques = QuizQuestion(quiz_id = id_quiz,
                            question_text = question["pytanie"],
                            answer_a = question["a"],
                            answer_b = question["b"],
                            answer_c = question["c"],
                            answer_d = question["d"],
                            correct_answer = correct)
        session.add(ques)
        session.commit()
        session.refresh(ques)


def get_questions_and_answers(session, quiz_id):
    quiz = get_quiz(session, quiz_id)
    json_quiz = objects_to_json(quiz)
    data = json.loads(json_quiz)
    questions, correct_answers = split_json(data, "correct_answer")
    return questions, correct_answers


def get_quiz(session, quiz_id):
    try:
        quiz = session.query(QuizQuestion).filter(QuizQuestion.quiz_id == quiz_id).all()
    except Exception as e:
        logging.info(f"Quiz Not Found")
        quiz = None
    return quiz


def object_to_dict(obj):
    exclude_columns = {'id', 'quiz_id'}
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns if c.name not in exclude_columns}


def objects_to_json(objects):
    dict_list = [object_to_dict(obj) for obj in objects]
    return json.dumps(dict_list)
