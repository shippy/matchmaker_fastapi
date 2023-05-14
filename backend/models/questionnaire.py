from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, create_engine
from typing import List, Optional
from pydantic import EmailStr

class UserBase(SQLModel, table=False):
    name: str = Field(...)
    email: EmailStr = Field(unique=True)

class User(UserBase, table=True):
    id: Optional[int] = Field(primary_key=True, default=None, nullable=False)
    questionnaires: List["Questionnaire"] = Relationship(back_populates="user")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = Field(default=None)
    access_token: Optional[str] = Field(default=None)
    hashed_password: str = Field(...)

class QuestionnaireBase(SQLModel):
    title: str = Field(max_length=100)
    user_id: int = Field(foreign_key="user.id")

class Questionnaire(QuestionnaireBase, table=True):
    id: Optional[int] = Field(primary_key=True, default=None, nullable=False)
    user: User = Relationship(back_populates="questionnaires")
    questions: List["Question"] = Relationship(back_populates="questionnaire")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = Field(default=None)

class QuestionnaireWithQuestions(QuestionnaireBase, table=False):
    questions: List["QuestionWithAnswers"] = []

class QuestionBase(SQLModel):
    text: str = Field(max_length=100)
    weight: Optional[float] = Field(default=1.0)
    questionnaire_id: int = Field(foreign_key="questionnaire.id")

class Question(QuestionBase, table=True):
    id: Optional[int] = Field(primary_key=True, default=None, nullable=False)
    questionnaire: Questionnaire = Relationship(back_populates="questions")
    answers: List["Answer"] = Relationship(back_populates="question")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = Field(default=None)

class QuestionWithAnswers(QuestionBase):
    answers: List["Answer"] = []

class Answer(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None, nullable=False)
    text: str = Field()
    value: int = Field(default=0)
    explanation: str = Field()
    question_id: int = Field(foreign_key="question.id")
    question: Question = Relationship(back_populates="answers")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = Field(default=None)
    responses: List["Response"] = Relationship(back_populates="answers")

class Respondent(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None, nullable=False)
    email: Optional[EmailStr] = Field()
    responses: List["Response"] = Relationship(back_populates="respondent")
    user_id: Optional[int] = Field(foreign_key="user.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = Field(default=None)

class ResponseBase(SQLModel, table=False):
    pass

class Response(ResponseBase, table=True):
    id: Optional[int] = Field(primary_key=True, default=None, nullable=False)
    respondent_id: int = Field(foreign_key="respondent.id")
    respondent: Respondent = Relationship(back_populates="responses")
    answer_id: int = Field(foreign_key="answer.id")
    answers: List[Answer] = Relationship(back_populates="responses")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = Field(default=None)


# class ResponseWithQuestions(ResponseBase, table=False):
#     answer: "AnswerWithQuestion"


QuestionnaireWithQuestions.update_forward_refs()
QuestionWithAnswers.update_forward_refs()
# Question.update_forward_refs()
Answer.update_forward_refs()

if __name__ == "__main__":
    from backend.core.database import engine

    SQLModel.metadata.create_all(engine)
