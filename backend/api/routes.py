from fastapi import APIRouter, Depends, HTTPException
from models.questionnaire import Questionnaire
from schemas.questionnaire import QuestionnaireCreate
from core.database import get_session
from sqlmodel import Session

router = APIRouter()

@router.get("/questionnaire/{questionnaire_id}", response_model=Questionnaire)
async def get_questionnaire(questionnaire_id: int, session: Session = Depends(get_session)):
    questionnaire = session.get(Questionnaire, questionnaire_id)
    if questionnaire is None:
        raise HTTPException(status_code=404, detail="Questionnaire not found")
    return questionnaire
