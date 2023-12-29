from scripts.config import Databases
from scripts.utils.mongo_utils import MongoConnect

mongo_client = MongoConnect(Databases.MONGO_URI)()
