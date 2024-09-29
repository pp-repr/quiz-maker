from fastapi import Form

from app.schemas.base import BaseRequest

class QuizEditRequest(BaseRequest):
    id: int
    quiz_name: str

    @staticmethod
    def form(
        id: int = Form(...),
        quiz_name: str = Form(...),
    ) -> 'QuizEditRequest':
        return QuizEditRequest(
            id=id,
            quiz_name=quiz_name
        )
