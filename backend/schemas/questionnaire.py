from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr

class QuestionnaireCreate(BaseModel):
    title: str
    user_id: int

class QuestionCreate(BaseModel):
    text: str
    weight: Optional[float] = 1.0
    questionnaire_id: int

class AnswerCreate(BaseModel):
    text: str
    value: int = 0
    explanation: str
    question_id: int

class RespondentCreate(BaseModel):
    name: str
    email: Optional[EmailStr]

class ResponseCreate(BaseModel):
    respondent_id: int
    answer_id: int
