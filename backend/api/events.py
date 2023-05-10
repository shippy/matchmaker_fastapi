from fastapi import APIRouter
from backend.event_handlers.base import EventHandlerBase

# Import your event handler subclasses to ensure they get registered
import backend.event_handlers.questionnaire
import backend.event_handlers.user

router = APIRouter()

@router.post("/events/{topic}")
def dispatch_event(topic: str, message: dict):
    handler = EventHandlerBase.handlers.get(topic)
    if handler:
        handler.handle_event(message)
    else:
        print(f"No handler found for topic {topic}")
