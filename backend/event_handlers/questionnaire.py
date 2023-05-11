from backend.event_handlers.base import EventHandlerBase
from backend.core.database import engine
from sqlmodel import Session
from typing import Any, Mapping

from backend.models.questionnaire import User, Questionnaire, Question, Answer, Respondent, Response

@EventHandlerBase.register_handler("create_questionnaire")
class CreateQuestionnaireHandler(EventHandlerBase):
    def handle_event(self, message: Mapping[str, Any]):
        # TODO: Verify that the user passed in is the current user
        with Session(engine) as session:
            user = session.get(User, message.pop("user_id"))
            q = Questionnaire(**message, user=user)
            session.add(q)
            session.commit()
            session.refresh(q)
            print(f"Handled create_questionnaire event: {q}")
            return q

@EventHandlerBase.register_handler("update_questionnaire")
class UpdateQuestionnaireHandler(EventHandlerBase):
    def handle_event(self, message: Mapping[str, Any]):
        print("Handling update_questionnaire event")

@EventHandlerBase.register_handler("delete_questionnaire")
class DeleteQuestionnaireHandler(EventHandlerBase):
    def handle_event(self, message: Mapping[str, Any]):
        print("Handling delete_questionnaire event")


@EventHandlerBase.register_handler("create_question")
class CreateQuestionHandler(EventHandlerBase):
    def handle_event(self, message: Mapping[str, Any]):
        with Session(engine) as session:
            questionnaire = session.get(Questionnaire, message.pop("questionnaire_id"))
            user = session.get(User, message.pop("user_id"))
            # TODO: Verify that this is current user
            q = Question(**message, questionnaire=questionnaire, user=user)

            session.add(q)
            session.commit()
            session.refresh(q)

            return q