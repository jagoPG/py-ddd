from uuid import uuid4
from app.infrastructure.domain_events import DomainRoot, DomainEvent


class Inventory(DomainRoot):
    def __init__(self, identifier, event_id, amount, seller_name):
        super().__init__()
        self.identifier = identifier
        self.event_id = event_id
        self.amount = amount
        self.seller_name = seller_name

    def inventory_updated(self):
        self.publish(
            InventoryUpdated(self.identifier, self.event_id, self.amount, self.seller_name)
        )


class InventoryId:
    def __init__(self, identifier):
        self.identifier = identifier

    @staticmethod
    def generate_id():
        return InventoryId(uuid4())


class InventoryAmount:
    def __init__(self, amount):
        self.amount = amount


class SellerName:
    def __init__(self, name):
        self.name = name


class InventoryUpdated(DomainEvent):
    def __init__(self, identifier, event_id, amount, seller_name):
        super(InventoryUpdated, self).__init__()
        self.identifier = identifier
        self.event_id = event_id
        self.amount = amount
        self.seller_name = seller_name


class InventoryRepository:
    def persist(self, event) -> None:
        raise NotImplementedError

    def delete(self, event) -> None:
        raise NotImplementedError

    def of_id(self, identifier) -> object:
        raise NotImplementedError

    def of_event_id(self, event_id) -> list:
        raise NotImplementedError
