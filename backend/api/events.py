from schemas.questionnaire import (
    UserCreate, QuestionnaireCreate, QuestionCreate, AnswerCreate, RespondentCreate, ResponseCreate
)
from models.questionnaire import User, Questionnaire, Question, Answer, Respondent, Response

# Replace these with your Redis event handler functions
def handle_create_user(user: UserCreate) -> User:
    return User(name=user.name)

def handle_create_questionnaire(questionnaire: QuestionnaireCreate) -> Questionnaire:
    return Questionnaire(title=questionnaire.title, user_id=questionnaire.user_id)

def handle_create_question(question: QuestionCreate) -> Question:
    return Question(text=question.text, questionnaire_id=question.questionnaire_id)

def handle_create_answer(answer: AnswerCreate) -> Answer:
    return Answer(text=answer.text, question_id=answer.question_id)

def handle_create_respondent(respondent: RespondentCreate) -> Respondent:
    return Respondent(name=respondent.name)

def handle_create_response(response: ResponseCreate) -> Response:
    return Response(respondent_id=response.respondent_id, answer_id=response.answer_id)
