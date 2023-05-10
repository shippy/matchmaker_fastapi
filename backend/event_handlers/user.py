from backend.event_handlers.base import EventHandlerBase
from typing import Any, Mapping

from backend.models.questionnaire import User
from backend.core.database import get_session

@EventHandlerBase.register_handler("create_user")
class CreateUserHandler(EventHandlerBase):
    def handle_event(self, message: Mapping[str, Any]):
        try:
            u = User(**message)
            print(f"Handling create_user event: {u}")
        except Exception as e:
            print(f"Error creating user: {e}")