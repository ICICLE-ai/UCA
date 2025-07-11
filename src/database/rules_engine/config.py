import os


class Config:
    TAPIS_URL = os.getenv("TAPIS_BASE_URL")
    TAPIS_USER = os.getenv("TAPIS_USER")
    TAPIS_PASS = os.getenv("TAPIS_PASS")
    MONGO_URI = os.getenv("MONGO_URI")