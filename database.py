import os
import certifi

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "chhabra")

client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=30000,
)

try:
    client.admin.command("ping")
    print("✅ MongoDB Connected Successfully")

except Exception as e:
    print("❌ MongoDB Connection Error:")
    print(e)


db = client[DATABASE_NAME]

blogs_collection = db["blogs"]
users_collection = db["users"]