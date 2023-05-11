from fastapi import APIRouter, Depends, HTTPException
from backend.models.questionnaire import Questionnaire, Question
from backend.schemas.questionnaire import QuestionnaireCreate
from backend.core.database import get_session
from sqlmodel import Session
from sqlalchemy.orm import joinedload

router = APIRouter()

@router.get("/questionnaire/{questionnaire_id}", response_model=Questionnaire)
def get_questionnaire(questionnaire_id: int, session: Session = Depends(get_session)):
    questionnaire = session.get(Questionnaire, questionnaire_id)
    # questionnaire = session.query(Questionnaire).options(joinedload(Questionnaire.questions)).filter(Questionnaire.id == questionnaire_id).first()

    questions = session.query(Question).where(Question.questionnaire_id == questionnaire_id).all()
    if questionnaire is None:
        raise HTTPException(status_code=404, detail="Questionnaire not found")
    questionnaire.questions = questions
    return questionnaire
