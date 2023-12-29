from scripts.constants import DBConstants
from scripts.core.db.mongo import mongo_client
from scripts.utils.mongo_utils import MongoCollectionBaseClass


class UsersCollection(MongoCollectionBaseClass):
    def __init__(self):
        super().__init__(
            mongo_client=mongo_client, database=DBConstants.DB_SKAESSENTIALS, collection=DBConstants.COLLECTION_USERS
        )

    def get_user(self, username: str):
        """
        Get user by username
        :param username:
        :return:
        """
        query = {"username": username}
        record = self.find_one(query)
        return dict(record) if record else {}
