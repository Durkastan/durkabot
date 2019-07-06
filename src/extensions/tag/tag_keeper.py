import pymongo

from storage import StorageHandler


class TagKeeper:
    subcollection_name = 'tags'

    def __init__(self, guild_id):
        self.collection = StorageHandler.guild_collection(guild_id)
        self.tags_collection = self.collection[self.subcollection_name]

    def get(self, tag_key):
        tag = self.tags_collection.find_one({'key': tag_key})
        return tag['value']

    def create(self, tag_key, tag_value):
        self.tags_collection.replace_one({'key': tag_key}, {'key': tag_key, 'value': tag_value}, upsert=True)

    def delete(self, tag_key):
        return self.tags_collection.delete_one({'key': tag_key}).deleted_count > 0

    def list(self):
        cursor = self.tags_collection.find(projection={'key': True})
        cursor.sort('key', pymongo.ASCENDING)
        return "\n".join([tag['key'] for tag in cursor])
