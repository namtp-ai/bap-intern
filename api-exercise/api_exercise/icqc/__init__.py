from .IDCardQuailityClassification import IDCardQuailityClassification
import torch

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
weight_path = './icqc/icqc_model/model.pt'
threshold = 0.3
icqc = IDCardQuailityClassification(device, weight_path, threshold)