import numpy as np
from models import PredictHistory
from pymongo import MongoClient
from config import Settings

settings = Settings()
conn = MongoClient(settings.DB_CONNECTION_STRING)


async def add_predict_history(img_name: str, pred_msg: str, outputs: np.array) -> PredictHistory:
    predict_history_dict = {
        'name': img_name,
        'predictions': pred_msg["Predict"],
        'blur': outputs[0],
        'missing': outputs[1],
        'overexposed': outputs[2],
        'sharp': outputs[3],
    }
    predict_history = PredictHistory.parse_obj(predict_history_dict)
    conn.ICQC.history.insert_one(dict(predict_history))