import os

from pymongo import MongoClient


class StorageHandler:
    def __init__(self, ctx):
        self.client = MongoClient(os.getenv("MONGOURL"))
        self.database_name = f'db_{ctx.guild.id}'
        self._db = None

    @property
    def db(self):
        if self._db is None:
            self._db = self._get_database()
        return self._db

    def _get_database(self):
        db = self.client[self.database_name]
        db.authenticate(name=os.getenv("MONGO_USERNAME"), password=os.getenv("MONGO_PASSWORD"))
        return db
