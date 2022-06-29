import pickle
import uvicorn
from fastapi import FastAPI
from pymongo import MongoClient

connection = MongoClient("mongodb+srv://thanhha101180167:ha01648664492@cluster0.4kt5x.mongodb.net/?retryWrites=true&w=majority")
mydb = connection["weather_db"]
mycol = mydb["weather_data"]

app = FastAPI()

@app.get('/')
def home():
    return {'text': 'Predict weather'}

@app.get('/predict')
def predic(temperature: float, humidity: float):
    try:
        model = pickle.load(open("E:/TaiLieu_PhanMem2/Guithub/Git_API/bap-intern/model_LgRegress.pkl", 'rb'))
        modelpredict = model.predict([[temperature, humidity]])
        output = round(modelpredict[0], 2)
        dict = {"temperature": temperature, "humidity": humidity, "rain": float(modelpredict)}
        while True:
            try:
                push = mycol.insert_one(dict)
                break
            except:
                pass
        return {"Weather of date {} - {} : {}".format(temperature, humidity, output)}
    except Exception as e:
        return {"Error": str(e)}

if __name__ == '__main__':
    print("Start")
    uvicorn.run(app, host="127.0.0.1", port=8020, debug=True)