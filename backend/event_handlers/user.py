from backend.event_handlers.base import EventHandlerBase
from fastapi import HTTPException, status
from sqlmodel import SQLModel, create_engine, Session
from typing import Any, Mapping

from backend.models.questionnaire import User, UserBase
from backend.core.database import get_session
from backend.core.utils import get_object_by_id, save_and_return_refreshed
from backend.core.security import get_password_hash

@EventHandlerBase.register_handler("create_user")
class CreateUserHandler(EventHandlerBase):
    def handle_event(self, message: Mapping[str, Any], session: Session) -> UserBase:
        u = User(
            name=message["name"],
            email=message["email"],
            hashed_password=get_password_hash(message["password"]),
        )
        return save_and_return_refreshed(session, u)
    
@EventHandlerBase.register_authenticated_handler("update_user")
class UpdateUserHandler(EventHandlerBase):
    def handle_event(self, message: Mapping[str, Any], session: Session, user: User) -> UserBase:
        u = user
        for key, value in message.items():
            if key not in ["name", "email"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only update your name and email",
                )
            setattr(u, key, value)
        return save_and_return_refreshed(session, u)