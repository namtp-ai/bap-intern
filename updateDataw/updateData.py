from mongodb.mongoDB import MongoDBConnection
import pandas as pd

data = pd.read_csv("testset.csv")

humidity = data[" _hum"]
temperature = data[" _tempm"]
rain = data[" _rain"]

mongodb = MongoDBConnection()
mydb = mongodb.connection["weather_db"]
mycol = mydb["weather_data"]

# x = mycol.insert_one({"temperature": "27", "humidity": "67", "rain": "0"})
# list_data = []
# for count in range(8500,9400,1):
#     data_dict = {"temperature": str(temperature[count]), "humidity": str(humidity[count]), "rain": str(rain[count])}
#     list_data.append(data_dict)
#
# x = mycol.insert_many(list_data)
# x = mycol.delete_many({})