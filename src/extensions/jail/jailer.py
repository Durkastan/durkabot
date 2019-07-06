from storage import StorageHandler


class Jailer:
    subcollection_name = 'jail'

    def __init__(self, guild_id):
        self.guild_id = guild_id

    @property
    def collection(self):
        return StorageHandler.guild_collection(self.guild_id)

    def jail(self, member, role_list):
        jail_collection = self.collection[self.subcollection_name]
        doc = jail_collection.find_one({'member_id': member.id})
        doc = self._jail(doc, member, role_list)
        jail_collection.replace_one({'member_id': member.id}, doc, upsert=True)

    def _jail(self, doc, member, role_list):
        doc = doc or self.default_doc(member.id)

        if doc['is_jailed'] is True:
            return doc

        doc['roles'] = [role.id for role in role_list]
        doc['is_jailed'] = True

        return doc

    def unjail(self, member):
        jail_collection = self.collection[self.subcollection_name]
        doc = jail_collection.find_one({'member_id': member.id})
        doc, roles = self._unjail(doc, member)
        jail_collection.replace_one({'member_id': member.id}, doc, upsert=True)

        return roles

    def _unjail(self, doc, member):
        doc = doc or self.default_doc(member.id)

        if doc['is_jailed'] is False:
            return doc

        old_roles = doc['roles']
        doc['roles'] = []
        doc['is_jailed'] = False

        return doc, old_roles

    @staticmethod
    def default_doc(member_id):
        return {'member_id': member_id, 'roles': [], 'is_jailed': False}

