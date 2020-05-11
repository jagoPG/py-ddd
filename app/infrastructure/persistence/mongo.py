from pymongo import MongoClient


class Mongo:
    def __init__(self):
        self.client = MongoClient('mongodb://root:root@127.0.0.1:27017')

    def collection(self, name):
        return self.client.stubhub[name]