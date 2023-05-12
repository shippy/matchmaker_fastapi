from backend.event_handlers.base import EventHandlerBase
from datetime import datetime
from sqlmodel import Session, SQLModel
from typing import Any, Mapping

from backend.models.questionnaire import User, Questionnaire, Question, Answer, Respondent, Response

def _save_and_return_refreshed(session: Session, obj: SQLModel) -> SQLModel:
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

@EventHandlerBase.register_handler("create_questionnaire")
class CreateQuestionnaireHandler(EventHandlerBase):
    def handle_event(self, message: Mapping[str, Any], session: Session) -> Questionnaire:
        # TODO: Verify that the user passed in is the current user
        user = session.get(User, message.pop("user_id"))
        q = Questionnaire(**message, user=user)
        return _save_and_return_refreshed(session, q)

@EventHandlerBase.register_handler("update_questionnaire")
class UpdateQuestionnaireHandler(EventHandlerBase):
    def handle_event(self, message: Mapping[str, Any], session: Session) -> Questionnaire:
        q = session.get(Questionnaire, message.pop("id"))
        for key, value in message.items():
            setattr(q, key, value)
        return _save_and_return_refreshed(session, q)

@EventHandlerBase.register_handler("delete_questionnaire")
class DeleteQuestionnaireHandler(EventHandlerBase):
    def handle_event(self, message: Mapping[str, Any], session: Session) -> Questionnaire:
        q = session.get(Questionnaire, message.pop("id"))
        q.deleted_at = datetime.now()
        return _save_and_return_refreshed(session, q)

@EventHandlerBase.register_handler("create_question")
class CreateQuestionHandler(EventHandlerBase):
    def handle_event(self, message: Mapping[str, Any], session: Session) -> Question:
        questionnaire = session.get(Questionnaire, message.pop("questionnaire_id"))
        user = session.get(User, message.pop("user_id"))
        # TODO: Verify that this is current user
        q = Question(**message, questionnaire=questionnaire, user=user)
        return _save_and_return_refreshed(session, q)
    
@EventHandlerBase.register_handler("update_question")
class UpdateQuestionHandler(EventHandlerBase):
    def handle_event(self, message: Mapping[str, Any], session: Session) -> Question:
        q = session.get(Question, message.pop("id"))
        for key, value in message.items():
            setattr(q, key, value)
        return _save_and_return_refreshed(session, q)

@EventHandlerBase.register_handler("delete_question")
class DeleteQuestionHandler(EventHandlerBase):
    def handle_event(self, message: Mapping[str, Any], session: Session):
        q = session.get(Question, message.pop("id"))
        q.deleted_at = datetime.now()
        return _save_and_return_refreshed(session, q)

@EventHandlerBase.register_handler("create_answer")
class CreateAnswerHandler(EventHandlerBase):
    def handle_event(self, message: Mapping[str, Any], session: Session) -> Answer:
        question = session.get(Question, message.pop("question_id"))
        user = session.get(User, message.pop("user_id"))
        # TODO: Verify that this is current user

        a = Answer(**message, question=question, user=user)
        return _save_and_return_refreshed(session, a)
            
@EventHandlerBase.register_handler("update_answer")
class UpdateAnswerHandler(EventHandlerBase):
    def handle_event(self, message: Mapping[str, Any], session: Session) -> Answer:
        a = session.get(Answer, message.pop("id"))
        for key, value in message.items():
            setattr(a, key, value)
        return _save_and_return_refreshed(session, a)

@EventHandlerBase.register_handler("delete_answer")
class DeleteAnswerHandler(EventHandlerBase):
    def handle_event(self, message: Mapping[str, Any], session: Session) -> Answer:
        a = session.get(Answer, message.pop("id"))
        a.deleted_at = datetime.now()
        return _save_and_return_refreshed(session, a)

@EventHandlerBase.register_handler("create_respondent")
class CreateRespondentHandler(EventHandlerBase):
    def handle_event(self, message: Mapping[str, Any], session: Session) -> Respondent:
        questionnaire = session.get(Questionnaire, message.pop("questionnaire_id"))
        respondent = Respondent()
        return _save_and_return_refreshed(session, respondent)
        
@EventHandlerBase.register_handler("create_response")
class CreateResponseHandler(EventHandlerBase):
    def handle_event(self, message: Mapping[str, Any], session: Session) -> Response:
        try:
            respondent = session.get(Respondent, message.pop("respondent_id"))
        except KeyError:
            respondent = Respondent()
        # answer = session.get(Answer, message.pop("answer_id"))
        response = Response(**message, respondent=respondent)
        return _save_and_return_refreshed(session, response)

@EventHandlerBase.register_handler("update_response")
class UpdateResponseHandler(EventHandlerBase):
    def handle_event(self, message: Mapping[str, Any], session: Session) -> Response:
        r = session.get(Response, message.pop("id"))
        for key, value in message.items():
            setattr(r, key, value)
        return _save_and_return_refreshed(session, r)
    
@EventHandlerBase.register_handler("delete_response")
class DeleteResponseHandler(EventHandlerBase):
    def handle_event(self, message: Mapping[str, Any], session: Session) -> Response:
        r = session.get(Response, message.pop("id"))
        r.deleted_at = datetime.now()
        return _save_and_return_refreshed(session, r)