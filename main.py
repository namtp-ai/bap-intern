import uvicorn

from switch.fastapi import app

if __name__ == '__main__':
    print("Start")
    uvicorn.run(app, host="127.0.0.1", port=8000, debug=True)
