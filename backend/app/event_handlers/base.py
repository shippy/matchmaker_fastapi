from sqlmodel import SQLModel, Session
from typing import Any, Mapping


class EventHandlerBase:
    handlers = {}
    authenticated_handlers = {}

    @classmethod
    def register_handler(cls, event_type):
        def decorator(handler_cls):
            cls.handlers[event_type] = handler_cls()
            return handler_cls

        return decorator
    
    @classmethod
    def register_authenticated_handler(cls, event_type):
        def decorator(handler_cls):
            cls.authenticated_handlers[event_type] = handler_cls()
            return handler_cls
        
        return decorator

    def handle_event(self, message: Mapping[str, Any], session: Session) -> SQLModel:
        raise NotImplementedError("Subclasses must implement this method")
