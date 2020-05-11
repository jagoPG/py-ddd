from pymongo import MongoClient

from app.domain.model.Event import EventId
from app.domain.model.Inventory import InventoryRepository, Inventory, InventoryId, SellerName, \
    InventoryAmount


class MongoInventoryRepository(InventoryRepository):
    def __init__(self):
        self.client = MongoClient('mongodb://root:root@127.0.0.1:27017')
        self.collection = self.client.stubhub.inventory

    def persist(self, inventory) -> None:
        if self.exists_document(inventory.identifier):
            self.collection.update_one(
                {'identifier': inventory.identifier.identifier},
                {
                    "$set": {
                        'identifier': inventory.identifier.identifier,
                        'eventId': inventory.event_id.identifier,
                        'sellerName': inventory.seller_name.name,
                        'amount': inventory.amount.amount
                    }
                }
            )
        else:
            self.collection.insert_one({
                'identifier': inventory.identifier.identifier,
                'eventId': inventory.event_id.identifier,
                'sellerName': inventory.seller_name.name,
                'amount': inventory.amount.amount

            })
        inventory.release()

    def delete(self, inventory) -> None:
        self.collection.delete_one({'identifier': inventory.identifier})

    def of_id(self, identifier) -> object:
        result = self.collection.find_one({'identifier': identifier})
        if result is not None:
            return self.__to_instance(
                result
            )
        else:
            return None

    def of_event_id(self, event_id) -> object:
        result = self.collection.find_one({'eventId': event_id.identifier})
        if result is not None:
            return self.__to_instance(
                result
            )
        else:
            return None

    def __to_instance(self, record):
        return Inventory(
            InventoryId(record['identifier']),
            EventId(record['eventId']),
            InventoryAmount(record['amount']),
            SellerName(record['sellerName'])
        )

    def exists_document(self, identifier) -> object:
        result = self.collection.find_one({'identifier': identifier.identifier})
        return result is not None
