
class GetEventsQuery:
    def __init__(self, identifier=None):
        self.identifier = identifier


class GetEvents:
    def __init__(self, repository):
        self.repository = repository

    def handle(self, query):
        if query.identifier is None:
            result = [self.__transform_event(item) for item in self.repository.all()]
        else:
            result = self.repository.of_id(query.identifier)
            result = self.__transform_event(result) if result is not None else {}
        return result

    def __transform_event(self, record):
        return {
            'id': record.identifier.identifier,
            'name': record.name.name
        }
