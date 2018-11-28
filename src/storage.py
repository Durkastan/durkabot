import os

from pymongo import MongoClient


class StorageHandler:
    _client = None

    def __init__(self):
        self.database_name = ''
        self._db = None

    def feed(self, ctx):
        self.database_name = f'db_{ctx.guild.id}'

    @property
    def client(self):
        return self._get_client()

    @classmethod
    def _get_client(cls):
        if cls._client is None:
            cls._client = MongoClient(os.getenv("MONGOURL"))
        return cls._client

    @property
    def db(self):
        if self._db is None:
            self._db = self._get_db()
        return self._db

    def _get_db(self):
        db = self.client[self.database_name]
        db.authenticate(name=os.getenv("MONGO_USERNAME"), password=os.getenv("MONGO_PASSWORD"))
        return db
