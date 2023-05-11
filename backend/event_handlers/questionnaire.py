from backend.event_handlers.base import EventHandlerBase
from backend.core.database import engine
from sqlmodel import Session
from typing import Any, Mapping

from backend.models.questionnaire import User, Questionnaire, Question, Answer, Respondent, Response

@EventHandlerBase.register_handler("create_questionnaire")
class CreateQuestionnaireHandler(EventHandlerBase):
    def handle_event(self, message: Mapping[str, Any]) -> Questionnaire:
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
    def handle_event(self, message: Mapping[str, Any]) -> Questionnaire:
        print("Handling update_questionnaire event")

@EventHandlerBase.register_handler("delete_questionnaire")
class DeleteQuestionnaireHandler(EventHandlerBase):
    def handle_event(self, message: Mapping[str, Any]):
        print("Handling delete_questionnaire event")


@EventHandlerBase.register_handler("create_question")
class CreateQuestionHandler(EventHandlerBase):
    def handle_event(self, message: Mapping[str, Any]) -> Question:
        with Session(engine) as session:
            questionnaire = session.get(Questionnaire, message.pop("questionnaire_id"))
            user = session.get(User, message.pop("user_id"))
            # TODO: Verify that this is current user
            q = Question(**message, questionnaire=questionnaire, user=user)

            session.add(q)
            session.commit()
            session.refresh(q)

            return q

@EventHandlerBase.register_handler("update_question")
class UpdateQuestionHandler(EventHandlerBase):
    def handle_event(self, message: Mapping[str, Any]) -> Question:
        print("Handling update_question event")

@EventHandlerBase.register_handler("delete_question")
class DeleteQuestionHandler(EventHandlerBase):
    def handle_event(self, message: Mapping[str, Any]):
        print("Handling delete_question event")

@EventHandlerBase.register_handler("create_answer")
class CreateAnswerHandler(EventHandlerBase):
    def handle_event(self, message: Mapping[str, Any]) -> Answer:
        with Session(engine) as session:
            question = session.get(Question, message.pop("question_id"))
            user = session.get(User, message.pop("user_id"))
            # TODO: Verify that this is current user

            a = Answer(**message, question=question, user=user)
            session.add(a)
            session.commit()
            session.refresh(a)

            return a
        
@EventHandlerBase.register_handler("update_answer")
class UpdateAnswerHandler(EventHandlerBase):
    def handle_event(self, message: Mapping[str, Any]) -> Answer:
        print("Handling update_answer event")

@EventHandlerBase.register_handler("delete_answer")
class DeleteAnswerHandler(EventHandlerBase):
    def handle_event(self, message: Mapping[str, Any]):
        print("Handling delete_answer event")

@EventHandlerBase.register_handler("create_respondent")
class CreateRespondentHandler(EventHandlerBase):
    def handle_event(self, message: Mapping[str, Any]) -> Respondent:
        with Session(engine) as session:
            questionnaire = session.get(Questionnaire, message.pop("questionnaire_id"))
            respondent = Respondent()
            session.add(respondent)
            session.commit()
            session.refresh(respondent)

            return respondent
        
@EventHandlerBase.register_handler("create_response")
class CreateResponseHandler(EventHandlerBase):
    def handle_event(self, message: Mapping[str, Any]) -> Response:
        with Session(engine) as session:
            respondent = session.get(Respondent, message.pop("respondent_id"))
            answer = session.get(Answer, message.pop("answer_id"))
            response = Response(**message, respondent=respondent, answer=answer)
            session.add(response)
            session.commit()
            session.refresh(response)

            return response
            