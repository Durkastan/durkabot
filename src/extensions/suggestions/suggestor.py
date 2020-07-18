import pymongo

from storage import StorageHandler


class Suggestor:
    subcollection_name = 'suggestions'
    suggestion_bans_subcollection_name = 'suggestion_bans'

    def __init__(self, guild_id):
        self.collection = StorageHandler.guild_collection(guild_id)
        self.suggestions_collection = self.collection[self.subcollection_name]
        self.bans_collection = self.collection[self.suggestion_bans_subcollection_name]

    def get_suggestion(self, msg_id):
        return self.suggestions_collection.find_one({'msg_id': msg_id})

    def add_new_suggestion(self, message, date, msg_id):
        self.suggestions_collection.insert_one({
            'user_id': message.author.id,
            'date': date,
            'msg_id': msg_id,
            'suggestions': message.content[message.content.find(' '):]
        })

    def get_latest_suggestion_from_user(self, user_id):
        return self.suggestions_collection.find_one({'user_id': user_id}, sort=[('date', pymongo.ASCENDING)])

    def get_suggestions_from_user(self, user_id):
        return self.suggestions_collection.find({'user_id': user_id})

    def ban_suggestions_from(self, user_id):
        if not self.is_suggestion_banned(user_id):
            self.bans_collection.insert_one({'user_id': user_id})

    def unban_suggestions_from(self, user_id):
        if self.is_suggestion_banned(user_id):
            self.bans_collection.delete_one({'user_id': user_id})

    def is_suggestion_banned(self, user_id):
        return self.bans_collection.find_one({'user_id': user_id}) is not None
