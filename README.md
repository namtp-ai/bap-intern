# bap-intern
# Deploy Pytorch model using TorchServe on Docker

Preprocessing data, building model, and deploying model on Docker using Pytorch.

## Tasks 
* Preprocessing data
  * Class CFG
    * Contains hyperparameters for training.
  * Class ProcessData
    * Split dataset into train, valid and test sets.
    * Create transforming pipeline for dataset with 2 modes - 'train' & 'valid', 'test'.
  * Class CustomDataset
    * Get images & labels from paths
    * Convert images into 'RGB'
    * Transform images using transforming pipeline from class ProcessData 
  * Class DatasetLoader
    * Preprocessing data using CustomDataset
    * Get data in batch using class DataLoader of PyTorch
    * Return 3 data loaders: train_loader, valid_loader and test_loader
* Building model
  * Initialization
    * Max Pooling (2D)
    * Dropout
    * Convolution layer (2D)
    * Linear layer
  * Forward
    * Conv => ReLU => Pool
    * Linear => ReLU => Dropout
    * Linear (output)
* Training
  * Class Trainer
    * train
    * validation (use early stopping technique)
* Evaluating
  * Accuracy: approx 87%
## Installation

Clone the repo from Github and pull the project.
```bash
git clone https://github.com/namtp-ai/bap-intern.git
git checkout hanldn/problem3-deploy-docker
git pull
```
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.txt.

```bash
pip install -r requirements.txt
```

# Project tree 
.  
├── .idea   
├── archive   
├── logs     
├── model-store                 
│     ├── model.pt            
│     ├── model.pth   
│     └── hana_model.mar  
├── venv    
├── .gitignore   
├── handler.py   
├── index_to_name.json   
├── model.py   
├── problem3.ipynb              
└── requirements.txt 


## Usage
```bash
docker run --rm -it -p 8080:8080 -p 8081:8081 --name mar -v "<path_to_folder_model_store>:/home/model-server/model-store" -v "<path_to_folder_bap-intern>:/home/model-server/examples" pytorch/torchserve:latest
docker ps
docker exec -it <container_name> /bin/bash
# Run once if hana_model is not in folder model-store.
torch-model-archiver --model-name hana_model --version 1.0 --model-file /home/model-server/examples/model.py --serialized-file /home/model-server/model-store/model.pth --export-path /home/model-server/model-store --extra-files /home/model-server/examples/index_to_name.json --handler /home/model-server/examples/handler.py
torchserve --stop
torchserve --start --ncs --model-store model-store --models hana_model.mar
```
## Testing
Using Postman for testing
* Method: GET
* URL: 127.0.0.1:8080/predictions/hana_model
* Body: binary file (choose an image to test)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Author
[Lê Hoàng Ngọc Hân - Đại học Bách Khoa - Đại học Đà Nẵng (DUT)](https://github.com/hanahh080601) 