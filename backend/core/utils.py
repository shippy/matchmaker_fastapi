from fastapi import HTTPException, status
from typing import Type, TypeVar
from sqlmodel import Session, SQLModel
from backend.models.questionnaire import Questionnaire, Question, Answer, Response, User

# Accept SQLModel and its subclasses as a type
SQLModelChild = TypeVar("SQLModelChild", bound=SQLModel)


def save_and_return_refreshed(session: Session, obj: SQLModelChild) -> SQLModelChild:
    """Save an object to the database and return a refreshed version of it."""
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


def get_object_by_id(
    model: Type[SQLModelChild], object_id: int, session: Session
) -> SQLModelChild:
    """Get an object by its ID, or raise an exception if it doesn't exist."""
    if object_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{model.__name__} ID is required",
        )
    obj = session.get(model, object_id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{model.__name__} not found"
        )
    return obj


def get_object_owner(obj: SQLModelChild, session: Session) -> User:
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
