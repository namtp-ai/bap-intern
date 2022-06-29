import pickle

import uvicorn
from fastapi import FastAPI
from pymongo import MongoClient
from starlette.responses import JSONResponse

connection = MongoClient(
    "mongodb+srv://thanhha101180167:ha01648664492@cluster0.4kt5x.mongodb.net/?retryWrites=true&w=majority")
mydb = connection["weather_db"]
mycol = mydb["weather_data"]

app = FastAPI()


@app.get('/')
def home():
    return {'text': 'Predict weather'}


@app.get('/predict')
def predict(temperature: float, humidity: float):
    try:
        model = pickle.load(open("E:/TaiLieu_PhanMem2/Guithub/Git_API/bap-intern/model_LgRegress.pkl", 'rb'))
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


if __name__ == '__main__':
    print("Start")
    uvicorn.run(app, host="127.0.0.1", port=8000, debug=True)
