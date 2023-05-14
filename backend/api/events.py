from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from backend.event_handlers.base import EventHandlerBase
from backend.core.database import get_session
from backend.core.security import get_current_user
from backend.models.questionnaire import User

# Import your event handler subclasses to ensure they get registered
import backend.event_handlers.questionnaire
import backend.event_handlers.user

router = APIRouter()


@router.post("/events/{topic}")
def dispatch_event(
    *, topic: str, message: dict, session: Session = Depends(get_session)
):
    handler = EventHandlerBase.handlers.get(topic)
    if handler:
        return handler.handle_event(message=message, session=session)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No public handler found for topic {topic}",
        )


@router.post("/events/{topic}/authenticated")
def dispatch_authenticated_event(
    *,
    topic: str,
    message: dict,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    handler = EventHandlerBase.authenticated_handlers.get(topic)
    if handler:
        return handler.handle_event(message=message, session=session, user=user)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No authenticated handler found for topic {topic}",
        )
