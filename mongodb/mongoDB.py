from pymongo import MongoClient
from pymongo.collection import Collection

from global_variable.global_variable import url_mongodb


class MongoDBConnection:
    """Connect local with mongodb"""
    mycol: Collection

    def __init__(self):
        self.connection = MongoClient(url_mongodb)

    def __connect__(self):
        mydb = self.connection["weather_db"]
        self.mycol = mydb["weather_data"]

    def insert_data(self, dict_weather):
        x = self.mycol.insert_one(dict_weather)


mongo_db = MongoDBConnection()
# account
'''thanhha101180167
   ha01648664492
   118.69.187.7/32'''
