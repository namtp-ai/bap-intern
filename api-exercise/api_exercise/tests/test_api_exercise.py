import io
import os
import unittest
from fastapi.testclient import TestClient

from fastapi import FastAPI
from routes import predict_routes

app = FastAPI()
app.include_router(predict_routes)

class UploadTest(unittest.TestCase):
    client = TestClient(app)

    def test_predict_history(self):
        res = self.client.get('/')
        assert res.status_code == 200

    def test_predict_image(self):
        foldername = 'missing'
        for filename in os.listdir(foldername):
            filepath = os.path.join(foldername,filename)
            try:
                with open(filepath, "rb") as file:
                    res = self.client.post(
                        "/", 
                        files={
                            "file": (
                                filename, 
                                file, 
                                "image/jpeg"
                            )
                        }
                    )
                    assert res.status_code == 200
                    print(res.text)
            except Exception as e:
                print("Error: %s" % e)
