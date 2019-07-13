import os

from pymongo import MongoClient

from static import DEFAULT_CONFIG


class StorageHandler:
    database_name = "durkadb"

    client = MongoClient(os.getenv("MONGOURL"))
    db = client[database_name]

    @classmethod
    def guild_collection(cls, guild_id):
        return cls.db['_' + str(guild_id)]

    @classmethod
    def config(cls, guild_id):
        return cls.guild_collection(guild_id)['config'].find_one({}) or DEFAULT_CONFIG

    @classmethod
    def write_config(cls, guild_id, document):
        cls.guild_collection(guild_id)['config'].update_one({}, document)
