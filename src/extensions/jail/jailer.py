from storage import StorageHandler


class Jailer:
    collection_name = 'jail'

    def __init__(self):
        self.db = StorageHandler.db
        self.collection = self.db[self.collection_name]

    async def jail(self, member, jail_role):
        doc = self.collection.find_one({'member_id': member.id})
        doc = await self._jail(doc, member, jail_role)
        self.collection.replace_one({'member_id': member.id}, doc, upsert=True)

    async def _jail(self, doc, member, jail_role):
        doc = doc or self.default_doc(member.id)

        if doc['is_jailed'] is True:
            return doc

        doc['roles'] = member.roles
        doc['is_jailed'] = True
        await member.add_roles(jail_role)
        await member.remove_roles(doc['roles'])

        return doc

    async def unjail(self, member, jail_role):
        doc = self.collection.find_one({'member_id': member.id})
        doc = await self._unjail(doc, member, jail_role)
        self.collection.replace_one({'member_id': member.id}, doc, upsert=True)

    async def _unjail(self, doc, member, jail_role):
        doc = doc or self.default_doc(member.id)

        if doc['is_jailed'] is False:
            return doc

        await member.add_roles(doc['roles'])
        await member.remove_roles(jail_role)

        return doc

    @staticmethod
    def default_doc(member_id):
        return {'member_id': member_id, 'roles': [], 'is_jailed': False}

