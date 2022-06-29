import unittest
from fastapi.testclient import TestClient

from fastapi import FastAPI
from routes.flower import flower

app = FastAPI()
app.include_router(flower)

class UnitTest(unittest.TestCase):
    client = TestClient(app)

    def test_get_list(self):
        res = self.client.get('/')
        assert res.status_code == 200

    def test_predict_flower(self):
        filepath = 'Rose_test.jpg'
        try:
            with open(filepath, "rb") as file:
                res = self.client.post(
                    "/", 
                    files={
                        "file": ( 
                            filepath,
                            file, 
                            "image/jpg"
                        )
                    }
                )
                assert res.status_code == 200
                print(res.text)
        except Exception as e:
            print("Here error: ", e)
