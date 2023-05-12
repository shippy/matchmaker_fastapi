from fastapi import APIRouter, Depends
from sqlmodel import Session
from backend.event_handlers.base import EventHandlerBase
from backend.core.database import get_session

# Import your event handler subclasses to ensure they get registered
import backend.event_handlers.questionnaire
import backend.event_handlers.user

router = APIRouter()

@router.post("/events/{topic}")
def dispatch_event(*, topic: str, message: dict, session: Session = Depends(get_session)):
    handler = EventHandlerBase.handlers.get(topic)
    if handler:
        return handler.handle_event(message=message, session=session)
    else:
        print(f"No handler found for topic {topic}")
