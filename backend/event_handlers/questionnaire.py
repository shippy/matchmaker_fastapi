from backend.event_handlers.base import EventHandlerBase
from typing import Any, Mapping

from backend.models.questionnaire import User, Questionnaire, Question, Answer, Respondent, Response

@EventHandlerBase.register_handler("create_questionnaire")
class CreateQuestionnaireHandler(EventHandlerBase):
    def handle_event(self, message: Mapping[str, Any]):
        try:
            q = Questionnaire(**message)
            print(f"Handling create_questionnaire event: {q}")
        except Exception as e:
            print(f"Error creating questionnaire: {e}")

@EventHandlerBase.register_handler("update_questionnaire")
class UpdateQuestionnaireHandler(EventHandlerBase):
    def handle_event(self, message: Mapping[str, Any]):
        print("Handling update_questionnaire event")

@EventHandlerBase.register_handler("delete_questionnaire")
class DeleteQuestionnaireHandler(EventHandlerBase):
    def handle_event(self, message: Mapping[str, Any]):
        print("Handling delete_questionnaire event")