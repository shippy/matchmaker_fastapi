from backend.event_handlers.base import EventHandlerBase
from datetime import datetime
from sqlmodel import Session, SQLModel
from typing import Any, Dict, Type, TypeVar, Union
from fastapi import HTTPException, status

from backend.models.questionnaire import (
    User,
    Questionnaire,
    Question,
    Answer,
    Respondent,
    Response,
)

# Accept SQLModel and its subclasses as a type
S = TypeVar("S", bound=SQLModel)


def _save_and_return_refreshed(session: Session, obj: S) -> S:
    """Save an object to the database and return a refreshed version of it."""
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


def _get_object_by_id(model: Type[S], object_id: int, session: Session) -> S:
    """Get an object by its ID, or raise an exception if it doesn't exist."""
    if object_id is None:
        raise HTTPException(status_code=400, detail=f"{model.__name__} ID is required")
    obj = session.get(model, object_id)
    if not obj:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    return obj


def get_object_owner(obj: S, session: Session) -> User:
    if isinstance(obj, Questionnaire):
        return obj.user
    elif isinstance(obj, Question):
        return obj.questionnaire.user
    elif isinstance(obj, Answer):
        return obj.question.questionnaire.user
    elif isinstance(obj, Response):
        raise NotImplementedError("Responses don't have owners yet")
    else:
        raise NotImplementedError(f"Unknown object type {type(obj)}")


@EventHandlerBase.register_authenticated_handler("create_questionnaire")
class CreateQuestionnaireHandler(EventHandlerBase):
    def handle_event(
        self, message: Dict[str, Any], session: Session, user: User
    ) -> Questionnaire:
        _ = message.pop("user_id", None)  # Remove user_id from message to avoid user_id injection
        q = Questionnaire(**message, user=user)
        return _save_and_return_refreshed(session, q)


@EventHandlerBase.register_authenticated_handler("update_questionnaire")
class UpdateQuestionnaireHandler(EventHandlerBase):
    def handle_event(
        self, message: Dict[str, Any], session: Session, user: User
    ) -> Questionnaire:
        q = _get_object_by_id(Questionnaire, message.pop("id"), session)
        owner = get_object_owner(q, session)
        if owner != user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update questionnaires you own",
            )
        for key, value in message.items():
            setattr(q, key, value)
        return _save_and_return_refreshed(session, q)


@EventHandlerBase.register_authenticated_handler("delete_questionnaire")
class DeleteQuestionnaireHandler(EventHandlerBase):
    def handle_event(
        self, message: Dict[str, Any], session: Session, user: User
    ) -> Questionnaire:
        q = _get_object_by_id(Questionnaire, message.pop("id"), session)
        owner = get_object_owner(q, session)
        if owner != user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete questionnaires you own",
            )
        q.deleted_at = datetime.now()
        return _save_and_return_refreshed(session, q)


@EventHandlerBase.register_authenticated_handler("create_question")
class CreateQuestionHandler(EventHandlerBase):
    def handle_event(
        self, message: Dict[str, Any], session: Session, user: User
    ) -> Question:
        questionnaire = _get_object_by_id(
            Questionnaire, message.pop("questionnaire_id"), session
        )
        owner = get_object_owner(questionnaire, session)
        if owner != user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only create questions in questionnaires you own",
            )
        q = Question(**message, questionnaire=questionnaire)
        return _save_and_return_refreshed(session, q)


@EventHandlerBase.register_authenticated_handler("update_question")
class UpdateQuestionHandler(EventHandlerBase):
    def handle_event(
        self, message: Dict[str, Any], session: Session, user: User
    ) -> Question:
        q = _get_object_by_id(Question, message.pop("id"), session)
        owner = get_object_owner(q, session)
        if owner != user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update questions in questionnaires you own",
            )
        for key, value in message.items():
            setattr(q, key, value)
        return _save_and_return_refreshed(session, q)


@EventHandlerBase.register_authenticated_handler("delete_question")
class DeleteQuestionHandler(EventHandlerBase):
    def handle_event(self, message: Dict[str, Any], session: Session, user: User):
        q = _get_object_by_id(Question, message.pop("id"), session)
        owner = get_object_owner(q, session)
        if owner != user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update questions in questionnaires you own",
            )
        q.deleted_at = datetime.now()
        return _save_and_return_refreshed(session, q)


@EventHandlerBase.register_authenticated_handler("create_answer")
class CreateAnswerHandler(EventHandlerBase):
    def handle_event(
        self, message: Dict[str, Any], session: Session, user: User
    ) -> Answer:
        question = _get_object_by_id(Question, message.pop("id"), session)
        owner = get_object_owner(question, session)
        if owner != user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only create answers to questions in questionnaires you own",
            )

        a = Answer(**message, question=question)
        return _save_and_return_refreshed(session, a)


@EventHandlerBase.register_authenticated_handler("update_answer")
class UpdateAnswerHandler(EventHandlerBase):
    def handle_event(
        self, message: Dict[str, Any], session: Session, user: User
    ) -> Answer:
        a = _get_object_by_id(Answer, message.pop("id"), session)
        owner = get_object_owner(a, session)
        if owner != user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update answers to questions in questionnaires you own",
            )
        for key, value in message.items():
            setattr(a, key, value)
        return _save_and_return_refreshed(session, a)


@EventHandlerBase.register_authenticated_handler("delete_answer")
class DeleteAnswerHandler(EventHandlerBase):
    def handle_event(
        self, message: Dict[str, Any], session: Session, user: User
    ) -> Answer:
        a = _get_object_by_id(Answer, message.pop("id"), session)
        owner = get_object_owner(a, session)
        if owner != user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update answers to questions in questionnaires you own",
            )
            
        a.deleted_at = datetime.now()
        return _save_and_return_refreshed(session, a)


@EventHandlerBase.register_handler("create_respondent")
class CreateRespondentHandler(EventHandlerBase):
    def handle_event(self, message: Dict[str, Any], session: Session) -> Respondent:
        questionnaire = session.get(Questionnaire, message.pop("questionnaire_id"))
        respondent = Respondent(**message)
        return _save_and_return_refreshed(session, respondent)


@EventHandlerBase.register_handler("create_response")
class CreateResponseHandler(EventHandlerBase):
    def handle_event(self, message: Dict[str, Any], session: Session) -> Response:
        try:
            respondent = _get_object_by_id(
                Respondent, message.pop("respondent_id"), session
            )
        except KeyError:
            respondent = Respondent(
                email=None, user_id=None
            )  # TODO: Check if User logged in
        # answer = session.get(Answer, message.pop("answer_id"))
        response = Response(**message, respondent=respondent)
        return _save_and_return_refreshed(session, response)


@EventHandlerBase.register_handler("update_response")
class UpdateResponseHandler(EventHandlerBase):
    def handle_event(self, message: Dict[str, Any], session: Session) -> Response:
        r = _get_object_by_id(Response, message.pop("id"), session)
        for key, value in message.items():
            setattr(r, key, value)
        return _save_and_return_refreshed(session, r)


@EventHandlerBase.register_handler("delete_response")
class DeleteResponseHandler(EventHandlerBase):
    def handle_event(self, message: Dict[str, Any], session: Session) -> Response:
        r = _get_object_by_id(Response, message.pop("id"), session)
        r.deleted_at = datetime.now()
        return _save_and_return_refreshed(session, r)
