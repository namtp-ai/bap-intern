API-exercise:
********
::

- Choose 1 dataset + algorithm => build a model.
- Build API to communicate with that model with request (using FastAPI, swagger, mongodb).
- The application can withstand 200 requests 1 time.
- Create documents for the API with excel presented in your own style.
- Additional part: Create docker image, run the project on docker environment.


Installation
************
::

 git clone https://github.com/namtp-ai/bap-intern.git
 git checkout minhhnh/api-exercise
 cd ./api-exercise/api_exercise  
 poetry install  
 poetry config virtualenvs.in-project true 
 poetry update  

Folder Tree
***********
::

| 📁 ./
| ├─📄 .gitignore
| ├─📁 api-exercise/
| │ ├─📁 api_exercise/
| │ │ ├─📁 config/
| │ │ │ ├─📄 db_config.py
| │ │ │ ├─📄 icqc_config.py
| │ │ │ └─📄 __init__.py
| │ │ ├─📁 database/
| │ │ │ ├─📄 database.py
| │ │ │ └─📄 __init__.py
| │ │ ├─📁 icqc/
| │ │ │ ├─📁 icqc_model/
| │ │ │ │ └─📄 model.pt
| │ │ │ ├─📄 IDCardQuailityClassification.py
| │ │ │ └─📄 __init__.py
| │ │ ├─📄 index.py
| │ │ ├─📁 models/
| │ │ │ ├─📄 predict_history.py
| │ │ │ └─📄 __init__.py
| │ │ ├─📁 routes/
| │ │ │ ├─📄 predict_routes.py
| │ │ │ └─📄 __init__.py
| │ │ ├─📁 schemas/
| │ │ │ ├─📄 predict_history.py
| │ │ │ └─📄 __init__.py
| │ │ ├─📁 tests/
| │ │ │ ├─📄 test_api_exercise.py
| │ │ │ └─📄 __init__.py
| │ │ └─📄 __init__.py
| │ ├─📄 poetry.lock
| │ ├─📄 pyproject.toml
| │ └─📄 README.rst
| └─📄 README.md
 
Run
***
::

 api-exercise/.venv/Scripts/activate  
 uvicorn index:app --reload 
 

Testing
*******
::

 python -m unittest tests/test_api_exercise.py  

Data flowchart
*******

.. image:: https://res.cloudinary.com/thefour123/image/authenticated/s--z-DJ1HvF--/v1656405147/DFC_mle57q.png
    :width: 500
    :alt: my-picture1
