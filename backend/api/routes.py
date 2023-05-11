from fastapi import APIRouter, Depends, HTTPException
from backend.models.questionnaire import Questionnaire, Question, QuestionnaireWithQuestions
from backend.schemas.questionnaire import QuestionnaireCreate
from backend.core.database import get_session
from sqlmodel import Session
from sqlalchemy.orm import joinedload

router = APIRouter()


# Response model is QuestionnaireWithQuestions because we want to eagerly load the questions
# and answers for the questionnaire, and this is how SQLModel recommends doing that:
# https://sqlmodel.tiangolo.com/tutorial/fastapi/relationships/
@router.get("/questionnaire/{questionnaire_id}", response_model=QuestionnaireWithQuestions)
def get_questionnaire(questionnaire_id: int, session: Session = Depends(get_session)):
    questionnaire = session.get(Questionnaire, questionnaire_id)
    if questionnaire is None:
        raise HTTPException(status_code=404, detail="Questionnaire not found")
    return questionnaire
