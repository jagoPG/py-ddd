from domain.model.Event import Event


class PersistEventCommand:
    def __init__(self, identifier, name):
        self.identifier = identifier
        self.name = name


class PersistEvent:
    def __init__(self, repository):
        self.repository = repository

    def handle(self, command):
        event = Event(
            command.identifier,
            command.name
        )
        event.event_created()
        self.repository.persist(event)
