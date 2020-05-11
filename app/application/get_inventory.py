from app.domain.model.Event import EventId


class GetInventoryOfEventQuery:
    def __init__(self, event_id):
        self.event_id = event_id


class GetInventoryOfEvent:
    def __init__(self, repository):
        self.repository = repository

    def handle(self, query):
        return [self.__transform(item) for item in self.repository.of_event_id(
            EventId(query.event_id)
        )]

    def __transform(self, inventory):
        return {
            'seller_name': inventory.seller_name.name,
            'amount': inventory.amount.amount
        }
