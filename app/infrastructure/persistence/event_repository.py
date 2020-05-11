from pymongo import MongoClient

from app.domain.model.Event import Event, EventId, EventName


class EventRepository:
    def persist(self, event) -> None:
        raise NotImplementedError

    def delete(self, event) -> None:
        raise NotImplementedError

    def of_id(self, identifier) -> object:
        raise NotImplementedError

    def all(self) -> list:
        raise NotImplementedError


class MongoEventRepository(EventRepository):
    def __init__(self):
        self.client = MongoClient('mongodb://root:root@127.0.0.1:27017')
        self.collection = self.client.stubhub.events
    
    def persist(self, event) -> None:
        if self.__exist_document(event.identifier.identifier):
            self.collection.update_one(
                {'identifier': event.identifier.identifier},
                {
                    "$set": {
                        'identifier': event.identifier.identifier,
                        'name': event.name.name
                    }
                }
            )
        else:
            self.collection.insert_one({
                'identifier': event.identifier.identifier,
                'name': event.name.name
            })
        event.release()

    def delete(self, event) -> None:
        self.collection.delete_one({'identifier': event.identifier})

    def of_id(self, identifier) -> object:
        result = self.collection.find_one({'identifier': identifier})
        if result is not None:
            return self.__to_instance(
                result
            )
        else:
            return None

    def all(self) -> list:
        events = self.collection.find({})
        return [self.__to_instance(event) for event in events]

    def __exist_document(self, identifier):
        return self.of_id(identifier) is not None

    def __to_instance(self, record):
        return Event(
            EventId(record['identifier']),
            EventName(record['name'])
        )
