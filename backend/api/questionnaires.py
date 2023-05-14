from fastapi import APIRouter, Depends, HTTPException
from backend.models.questionnaire import (
    Answer,
    Questionnaire,
    Question,
    QuestionnaireWithQuestions,
    Respondent,
    Response,
    User,
)
from backend.schemas.questionnaire import QuestionnaireCreate
from backend.core.database import get_session
from backend.core.security import get_current_user
from sqlmodel import Session, SQLModel, select
from typing import Sequence

router = APIRouter()


# Response model is QuestionnaireWithQuestions because we want to eagerly load the questions
# and answers for the questionnaire, and this is how SQLModel recommends doing that:
# https://sqlmodel.tiangolo.com/tutorial/fastapi/relationships/
@router.get(
    "/questionnaire/{questionnaire_id}", response_model=QuestionnaireWithQuestions
)
def get_questionnaire(questionnaire_id: int, session: Session = Depends(get_session)):
    questionnaire = session.get(Questionnaire, questionnaire_id)
    if questionnaire is None:
        raise HTTPException(status_code=404, detail="Questionnaire not found")
    return questionnaire


@router.get("/questionnaire/{questionnaire_id}/respondents")
def get_questionnaire_respondents(
    questionnaire_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):  # -> Sequence[Respondent]:
    questionnaire = session.get(Questionnaire, questionnaire_id)
    if questionnaire is None:
        raise HTTPException(status_code=404, detail="Questionnaire not found")
    # Questionnaire doesn't actually have a direct link to respondents, so cannot do
    # return questionnaire.respondents
    sql_query_sqlmodel = (
        select(Respondent)
        .join(Response)
        .join(Answer)
        .join(Question)
        .join(Questionnaire)
        .where(Questionnaire.id == questionnaire_id)
    )
    result = session.exec(sql_query_sqlmodel)
    return result.fetchall()


@router.get("/questionnaire/{questionnaire_id}/respondent/{respondent_id}")
def get_respondent_responses(
    questionnaire_id: int,
    respondent_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):  # -> Sequence[Response]:
    questionnaire = session.get(Questionnaire, questionnaire_id)
    if questionnaire is None:
        raise HTTPException(status_code=404, detail="Questionnaire not found")
    respondent = session.get(Respondent, respondent_id)
    if respondent is None:
        raise HTTPException(status_code=404, detail="Respondent not found")
    # Respondent doesn't actually have a direct link to responses, so must get it through joins
    sql_query_sqlmodel = (
        select(
            Response.id,
            Question.text,
            Question.weight,
            Answer.text.label("answer_text"),  # type: ignore
            Answer.value,
        )
        .select_from(Respondent)
        .join(Response)
        .join(Answer)
        .join(Question)
        .where(
            Response.respondent_id == respondent_id,
            Question.questionnaire_id == questionnaire_id,
        )
    )
    result = session.exec(sql_query_sqlmodel)
    return result.fetchall()
