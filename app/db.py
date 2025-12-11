from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
master_db = client[settings.MASTER_DB]

# Collections in master_db
orgs_col = master_db["organizations"]
admins_col = master_db["admins"]
