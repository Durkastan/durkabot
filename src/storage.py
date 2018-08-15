import os

from pymongo import MongoClient


class StorageHandler:
    def __init__(self, ctx):
        self.database_name = f'db_{ctx.guild.id}'
        self._db = None
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = self._get_client()
        return self._client

    @staticmethod
    def _get_client():
        return MongoClient(os.getenv("MONGOURL"))

    @property
    def db(self):
        if self._db is None:
            self._db = self._get_db()
        return self._db

    def _get_db(self):
        db = self.client[self.database_name]
        db.authenticate(name=os.getenv("MONGO_USERNAME"), password=os.getenv("MONGO_PASSWORD"))
        return db
