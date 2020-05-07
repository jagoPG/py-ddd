from uuid import uuid4
from infrastructure.domain_events import DomainRoot, DomainEvent


class Event(DomainRoot):
    def __init__(self, identifier, name):
        super().__init__()
        self.identifier = identifier
        self.name = name

    def event_created(self):
        self.publish(EventCreated(self.identifier, self.name))


class EventId:
    def __init__(self, identifier):
        self.identifier = identifier

    @staticmethod
    def generate_id():
        return EventId(uuid4())


class EventName:
    def __init__(self, name):
        self.__validate_name(name)
        self.name = name

    @staticmethod
    def __validate_name(name):
        if len(name) < 10 or len(name) > 40:
            raise EventNameInvalid


class EventNameInvalid(Exception):
    """
    The name of the event requires 10-40 characters
    """


class EventCreated(DomainEvent):
    def __init__(self, identifier, name):
        super(EventCreated, self).__init__()
        self.identifier = identifier
        self.name = name
