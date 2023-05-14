from backend.event_handlers.base import EventHandlerBase
from fastapi import HTTPException, status
from sqlmodel import create_engine, Session
from typing import Any, Mapping

from backend.models.questionnaire import User
from backend.core.database import get_session


@EventHandlerBase.register_handler("create_user")
class CreateUserHandler(EventHandlerBase):
    def handle_event(self, message: Mapping[str, Any], session: Session) -> User:
        try:
            engine = create_engine("sqlite:///database.db")
            with Session(engine) as session:
                u = User(**message)
                session.add(u)
                session.commit()
                session.refresh(u)
                return u

        except Exception as e:
            # TODO: Raise an actual error/return 404?
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error creating user: {e}",
            )