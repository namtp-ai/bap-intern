import torch
from predict.predict import Prediction

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
prediction = Prediction(device)