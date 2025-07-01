import os

MONGO_URI = os.getenv("MONGO_URI", "")
DB_NAME   = os.getenv("CI_DB", "")