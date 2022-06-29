# bap-intern
# Serve a transfer learning model using FastAPI, MongoDB and poetry to classify 102 flower categories.

Preprocessing data, building, training, saving and serving model using FastAPI.

## Tasks 
* Preprocessing data
* Building model
  * Using Resnet50
* Training
* Evaluating
  * Accuracy: approx 93%


## Installation

Clone the repo from Github and pull the project.
```bash
git clone https://github.com/namtp-ai/bap-intern.git
git checkout hanlhn/api-excercise
git pull
cd hanlhn/hanlhn
poetry install
poetry config virtualenvs.in-project true
poetry update
```

# Project tree 
.  
├── hanlhn                       
│     ├── __pycache__  
│     ├── .venv             
│     ├── poetry.lock    
│     ├── pyproject.toml   
│     ├── README.rst  
│     └── hanlhn   
│           ├── __pycache__  
│           ├── config      
│           │      ├── __pycache__  
│           │      └── mongodb.py           
│           ├── models   
│           │      ├── flower_classification.pt  
│           │      └── flower.py    
│           ├── predict  
│           │      ├── __pycache__  
│           │      ├── __init__.py  
│           │      └── predict.py      
│           ├── routes  
│           │      ├── __pycache__  
│           │      └── flower.py   
│           ├── schemas  
│           │      ├── __pycache__  
│           │      └── flower.py   
│           ├── tests  
│           │      ├── __pycache__  
│           │      ├── __init__.py  
│           │      └── test_hanlhn.py   
│           ├── __init__.py   
│           ├── index2name.pkl  
│           ├── main.py  
│           └── Rose_test.jpg  
├── .gitignore                 
└── README.md  


## Usage: For running server
```bash
cd hanlhn 
.venv/Scripts/activate
uvicorn main:app --reload
```

## Testing API
Using Postman for testing
* Method: GET / POST
* URL: 127.0.0.1:8080/
* Body: file (choose an image to test)

## Usage: For unittest 
```bash
cd hanlhn/hanlhn
python -m uniitest tests/test_hanlhn.py 
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Author
[Lê Hoàng Ngọc Hân - Đại học Bách Khoa - Đại học Đà Nẵng (DUT)](https://github.com/hanahh080601) 