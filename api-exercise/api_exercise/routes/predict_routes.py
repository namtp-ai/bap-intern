from fastapi import APIRouter, Form, UploadFile
import numpy as np
from icqc import icqc
from PIL import Image
import io
from config import icqc_config
from database import add_predict_history

predict_routes = APIRouter()


@predict_routes.post("/")
async def predict_image(file: UploadFile = Form(...)):
    try:
        contents = await file.read()
        img = Image.open(io.BytesIO(contents))
        pred, outputs = icqc.predict(img)
        pred_msg = {
            "Predict": str(icqc_config.itos[pred[0]] + ' ' + icqc_config.itos[pred[1]])
            if len(pred)>1
            else icqc_config.itos[pred[0]]
        }
        await add_predict_history(file.filename, pred_msg, outputs)
    except Exception as e:
        print(e)
        return {"Message": "There was an error uploading the file"}
    finally:
        await file.close()
    return pred_msg
