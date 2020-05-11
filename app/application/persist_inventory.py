from app.domain.model.Event import EventId
from app.domain.model.Inventory import Inventory, InventoryId, InventoryAmount, SellerName


class PersistInventoryCommand:
    def __init__(self, identifier, event_id, amount, seller_name):
        self.identifier = identifier
        self.event_id = event_id
        self.amount = amount
        self.seller_name = seller_name


class PersistInventory:
    def __init__(self, repository):
        self.repository = repository

    def handle(self, command):
        self.repository.persist(
            Inventory(
                InventoryId(command.identifier),
                EventId(command.event_id),
                InventoryAmount(command.amount),
                SellerName(command.seller_name)
            )
        )
