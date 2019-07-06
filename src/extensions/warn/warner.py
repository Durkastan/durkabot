import asyncio
import textwrap
from datetime import datetime, timedelta
from enum import Enum

from storage import StorageHandler


class AfterWarnAction(Enum):
    REPLY = 0
    REPLY_KICK = 1


class Warner:
    subcollection_name = 'warns'

    def __init__(self, guild_id):
        self.collection = StorageHandler.guild_collection(guild_id)
        self.warns_collection = self.collection[self.subcollection_name]

    def warn(self, member, reason, channel_id, message_id, author_id):
        doc = self.warns_collection.find_one({'member_id': member.id})
        ret, num_warns, doc = self.process_warning(author_id, doc, member, channel_id, message_id, reason)
        self.warns_collection.replace_one({'member_id': member.id}, doc, upsert=True)

        return ret, num_warns

    @staticmethod
    def process_warning(author_id, doc, member, channel_id, message_id, reason):
        ret = AfterWarnAction.REPLY
        if doc is None:
            doc = {'member_id': member.id, 'warns': [], 'previous_warns': []}

        doc['warns'].append({
            'timestamp': datetime.now(),
            'reason': reason,
            'message_id': message_id,
            'channel_id': channel_id,
            'by': author_id
        })

        num_warns = len(doc["warns"])
        if num_warns > 3:
            ret = AfterWarnAction.REPLY_KICK
            doc['previous_warns'] += doc['warns']
            doc['warns'] = []

        return ret, num_warns, doc

    def get_raw_warns(self, member):
        return self.warns_collection.find_one({'member_id': member.id}, projection={'warns': True, 'previous_warns': True})

    @staticmethod
    def format_warns(data):
        ret = ''
        index = 0
        for warning, link in data:
            index += 1

            x = (f"{warning['timestamp'].strftime('%a %d/%m/%Y %I:%M:%S %p')} {warning.get('tag') or ''}\n"
                 f"by: {warning['by']}\n"
                 f"reason: {warning.get('reason') or '(not given)'}\n"
                 f"link: {link}")
            x = textwrap.indent(x, '  ')

            ret += f"{index}." + x + '\n'
        return ret

    @classmethod
    async def periodically_forget_warns(cls, guild_id):
        guild_collection = StorageHandler.guild_collection(guild_id)
        while True:
            cursor = guild_collection[cls.subcollection_name].find(filter={'warns': {'$ne': []}},
                                                                   projection={'warns': True, 'previous_warns': True,
                                                                    'member_id': True})

            for doc in cursor:
                for warn in doc['warns'].copy():
                    if datetime.today() - warn['timestamp'] > timedelta(days=7):
                        doc['previous_warns'].append(warn)
                        doc['warns'].remove(warn)

                cursor.collection.update_one({'member_id': doc['member_id']}, {'$set': doc})

            cursor.close()

            await asyncio.sleep(3600)
