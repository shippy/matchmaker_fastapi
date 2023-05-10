from typing import Any, Mapping


class EventHandlerBase:
    handlers = {}

    @classmethod
    def register_handler(cls, event_type):
        def decorator(handler_cls):
            cls.handlers[event_type] = handler_cls()
            return handler_cls

        return decorator

    def handle_event(self, message: Mapping[str, Any]):
        raise NotImplementedError("Subclasses must implement this method")
