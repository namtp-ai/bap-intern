import pickle

from fastapi import FastAPI
from pymongo import MongoClient
from starlette.responses import JSONResponse

from global_variable.global_variable import url_mongodb, address_model

"""
Test manually on uvicorn and get data new then push it mongo
"""

connection = MongoClient(url_mongodb)
mydb = connection["weather_db"]
mycol = mydb["weather_data"]

app = FastAPI()


@app.get('/')
def home():
    return {'text': 'Predict weather'}


@app.get('/predict')
def predict(temperature: float, humidity: float):
    try:
        model = pickle.load(open(address_model, 'rb'))
        model_predict = model.predict([[temperature, humidity]])
        output = round(model_predict[0], 2)
        if temperature > 60:
            return JSONResponse(
                status_code=400,
                content={
                    "message": "Temperature higher limit",
                })
        elif (humidity < 0) or (humidity > 100):
            return JSONResponse(
                status_code=400,
                content={
                    "message": "Humidity is not within the limit",
                })

        object_data = {"temperature": temperature, "humidity": humidity, "rain": float(model_predict)}
        while True:
            try:
                push = mycol.insert_one(object_data)
                break
            except:
                pass
        return JSONResponse(
            status_code=444,
            content={
                "message": "Weather of date {} - {} : {}".format(temperature, humidity, output),
            })
    except Exception as e:
        return JSONResponse(
            status_code=455,
            content={
                "Error": str(e),
            })
