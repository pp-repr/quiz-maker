from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.config.database import Base

from app.models.enums import Answer

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(4096), nullable=False)
    quiz_number = Column(Integer, nullable=False)
    question = Column(String(1000), nullable=False)
    answer_a = Column(String(1000), nullable=False)
    answer_b = Column(String(1000), nullable=False)
    answer_c = Column(String(1000), nullable=False)
    answer_d = Column(String(1000), nullable=False)
    correct_answer = Column(Enum(Answer), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    user = relationship("User", back_populates="quiz")