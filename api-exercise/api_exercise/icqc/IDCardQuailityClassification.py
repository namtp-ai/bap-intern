import numpy as np
import torch
from torch import nn, threshold
from torchvision import transforms
import timm
from PIL import Image
import torch.nn.functional as F
from config.icqc_config import icqc_config

class IDCardQuailityClassification:
    """
    Class IDCardQuailityClassification
    ------------------------
    Methods:
        get_transforms(self): torch.tensor
        Transform image and convert to torch.tensor

        predict(self, img): tuple
        Return list of predictions and list of probality for each class.
    """
    def __init__(self, device, weight_path, threshold) -> None:
        self.model = timm.create_model("efficientnet_b4", pretrained=True)
        for param in self.model.parameters():
            param.requires_grad = True
        self.model.classifier = nn.Linear(
            self.model.classifier.in_features, icqc_config.num_classes)
        self.model.to(device)
        self.model.load_state_dict(
            torch.load(
                weight_path,
                map_location=device
            )
        )
        self.threshold = threshold
        self.device = device

    def get_transforms(self):
        return transforms.Compose([
            transforms.Resize((icqc_config.height, icqc_config.width)),
            transforms.ToTensor(),
            transforms.Normalize(mean=icqc_config.mean, std=icqc_config.std)
        ])

    def predict(self, img):
        self.model.eval()
        tensor_img = self.get_transforms()(img).unsqueeze(0).to(self.device)
        outputs = self.model(tensor_img).detach().squeeze(0)
        outputs = F.softmax(outputs, 0)
        probality, pred = torch.topk(outputs, 2, 0)
        pred = pred.squeeze(0).cpu().numpy()
        outputs = np.round(outputs.numpy(), 3)
        return (pred if probality[1] > self.threshold else [pred[0]]),outputs