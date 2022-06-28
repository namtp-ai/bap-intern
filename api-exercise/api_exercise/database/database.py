import numpy as np
from pymongo import MongoClient
from config import Settings

settings = Settings()
conn = MongoClient(settings.DB_CONNECTION_STRING)

