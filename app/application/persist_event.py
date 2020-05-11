from app.domain.model.Event import Event, EventName, EventId


class PersistEventCommand:
    def __init__(self, identifier, name):
        self.identifier = identifier
        self.name = name


class PersistEvent:
    def __init__(self, repository):
        self.repository = repository

    def handle(self, command):
        event = Event(
            EventId(command.identifier),
            EventName(command.name)
        )
        event.event_created()
        self.repository.persist(event)
