from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, Enum
from sqlalchemy.orm import relationship, mapped_column
from datetime import datetime

from app.config.database import Base
from app.models.enums import Answer


class UserQuiz(Base):
    __tablename__ = 'user_quizzes'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    quiz_name = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="quiz")
    questions = relationship("QuizQuestion", back_populates="quiz")


class QuizQuestion(Base):
    __tablename__ = 'quiz_questions'

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey('user_quizzes.id'), nullable=False)
    question_text = Column(String(255), nullable=False)
    answer_a = Column(String(255), nullable=False)
    answer_b = Column(String(255), nullable=False)
    answer_c = Column(String(255), nullable=False)
    answer_d = Column(String(255), nullable=False)
    correct_answer = Column(String(1), nullable=False)

    quiz = relationship("UserQuiz", back_populates="questions")
