from storage import StorageHandler


class Jailer:
    collection_name = 'jail'

    def __init__(self):
        self.db = StorageHandler.db
        self.collection = self.db[self.collection_name]

    def jail(self, member, role_list):
        doc = self.collection.find_one({'member_id': member.id})
        doc = self._jail(doc, member, role_list)
        self.collection.replace_one({'member_id': member.id}, doc, upsert=True)

    def _jail(self, doc, member, role_list):
        doc = doc or self.default_doc(member.id)

        if doc['is_jailed'] is True:
            return doc

        doc['roles'] = [role.id for role in role_list]
        doc['is_jailed'] = True

        return doc

    def unjail(self, member):
        doc = self.collection.find_one({'member_id': member.id})
        doc, roles = self._unjail(doc, member)
        self.collection.replace_one({'member_id': member.id}, doc, upsert=True)

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

