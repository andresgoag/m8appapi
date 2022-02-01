import os

class Config:
    SECRET_KEY = 'UwG;&H3bwvmMAKeZ'
    MONGO_URI = os.environ.get("MONGO_URI")