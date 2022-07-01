from mongodb.mongoDB import MongoDBConnection
import numpy as np
from sklearn.linear_model import LogisticRegression

def remove_nan(list_weather,list_lable):
    """ Remove the rows containing nan in the data """
    list_nan = np.argwhere(np.isnan(list_weather))
    for nan in range(len(list_nan)):
        list_weather = np.delete(list_weather, (list_nan[2 * nan, 0]), axis=0)
        list_lable = np.delete(list_lable, list_nan[2 * nan, 1], axis=0)
        list_nan = list_nan - 1
    return list_weather,list_lable

def convert_data(list_temperature,list_humidity,lable_rain):
    """ Tranform data from mongo to data training """
    m = len(list_temperature)
    weather = np.zeros((m,2))
    rain = np.zeros((m,1))
    for count in range(m):
        weather[count,0] = float(list_temperature[count])
        weather[count,1] = float(list_humidity[count])
        rain[count] = float(lable_rain[count])
    return weather,rain


if __name__ == "__main__":
    #Connect Mongo
    mongodb = MongoDBConnection()
    mycol = mongodb.mycol

    #Get value mongo
    list_humidity = []
    list_temperature = []
    lable_rain = []
    while True:
        try:
            for x in mycol.find():
                list_temperature.append(x["temperature"])
                list_humidity.append(x["humidity"])
                lable_rain.append(x["rain"])
            break
        except:
            pass

    weather,rain = convert_data(list_temperature,list_humidity,lable_rain)
    weather,rain = remove_nan(weather,rain)

    one = np.ones((weather.shape[0], 1))
    weatherb = np.concatenate((one, weather), axis = 1)

    weather_test = weather[200:,:]
    print(weather_test)
    rain1 = np.reshape(rain,(len(rain)))
    model = LogisticRegression()
    model.fit(weather,rain1)

    # pickle.dump(model, open('model_LgRegress.pkl', 'wb'))
