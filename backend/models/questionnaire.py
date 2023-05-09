from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, create_engine
from typing import List, Optional
from pydantic import EmailStr

class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None, nullable=False)
    name: str = Field()
    email: EmailStr = Field()
    questionnaires: List["Questionnaire"] = Relationship(back_populates="user")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

class Questionnaire(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None, nullable=False)
    title: str = Field(max_length=100)
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="questionnaire")
    questions: List["Question"] = Relationship(back_populates="questionnaire")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

class Question(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None, nullable=False)
    text: str = Field(max_length=100)
    weight: Optional[float] = Field(default=1.0)
    questionnaire_id: int = Field(foreign_key="questionnaire.id")
    questionnaire: Questionnaire = Relationship(back_populates="question")
    answers: List["Answer"] = Relationship(back_populates="question")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

class Answer(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None, nullable=False)
    text: str = Field()
    value: int = Field(default=0)
    explanation: str = Field()
    question_id: int = Field(foreign_key="question.id")
    question: Question = Relationship(back_populates="answer")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

class Respondent(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None, nullable=False)
    email: Optional[EmailStr] = Field()
    responses: List["Response"] = Relationship(back_populates="respondent")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

class Response(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None, nullable=False)
    respondent_id: int = Field(foreign_key="respondent.id")
    respondent: Respondent = Relationship(back_populates="response")
    answer_id: int = Field(foreign_key="answer.id")
    answer: Answer = Relationship(back_populates="answer")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

if __name__ == "__main__":
    sqlite_file_name = "database.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"

    engine = create_engine(sqlite_url, echo=True)

    SQLModel.metadata.create_all(engine)
