import os

from pymongo import MongoClient


class StorageHandler:
    client = MongoClient(os.getenv("MONGOURL"))
    database_name = "durkadb"
    db = client[database_name]
