from pymongo import MongoClient
from pymongo.collection import Collection


class MongoDBConnection:
    mycol: Collection

    def __init__(self):
        self.connection = MongoClient(
            "mongodb+srv://thanhha101180167:ha01648664492@cluster0.4kt5x.mongodb.net/?retryWrites=true&w=majority")

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
