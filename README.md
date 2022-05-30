# bap-intern
# Problem 2 - Image classification with transfer learning

Preprocessing data from scratch using OpenCV, building model (VGG16) and training model using PyTorch.

## Tasks
### Preprocessing data
  * Class CFG
    * Contains hyperparameters for training.
  * Split dataset into train, valid and test sets.
  * Class DataProcess
    * Get images & labels from paths
    * Convert images into 'RGB'
    * Transform images (resize, normalize)
  * Class DataLoader
    * Divide data in batch with size=batch_size
  * Create 3 subset: train_data, valid_data and test_data and pass them to DataLoader
### Building model
* Initialization
  * Pick VGG16 with mode pretrain=True
  * Replace last layer in model with 2 fully connected layers and pass model to device
* Forward
### Training
* Train
* Validation (using early stopping technique)
### Evaluating
## Installation

Clone the repo from Github and pull the project.
```bash
git clone https://github.com/namtp-ai/bap-intern.git
git checkout hanldn/problem2
git pull
```
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.txt.

```bash
pip install -r requirements.txt
```

## Usage
Click 'Run All'

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Author
[Lê Hoàng Ngọc Hân - Đại học Bách Khoa - Đại học Đà Nẵng (DUT)](https://github.com/hanahh080601) 