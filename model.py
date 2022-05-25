import torch.nn as nn
import torch.nn.functional as F


weight_decay = 0.2
num_classes = 4

class BaseModel(nn.Module):
    def __init__(self):
        super(BaseModel, self).__init__()
        self.pool = nn.MaxPool2d(2, 2)
        self.dropout = nn.Dropout(p=weight_decay)

        self.conv1 = nn.Conv2d(3, 6, 4)
        self.conv2 = nn.Conv2d(6, 12, 4)
        self.conv3 = nn.Conv2d(12, 14, 4)
        self.conv4 = nn.Conv2d(14, 16, 4)
        self.conv5 = nn.Conv2d(16, 20, 4)

        self.fc1 = nn.Linear(20 * 4 * 4, 250)
        self.fc2 = nn.Linear(250, 200)
        self.fc3 = nn.Linear(200, 50)
        self.fc4 = nn.Linear(50, 20)
        self.fc5 = nn.Linear(20, num_classes)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.pool(x)

        x = self.conv2(x)
        x = F.relu(x)
        x = self.pool(x)

        x = self.conv3(x)
        x = F.relu(x)
        x = self.pool(x)

        x = self.conv4(x)
        x = F.relu(x)
        x = self.pool(x)

        x = self.conv5(x)
        x = F.relu(x)
        x = self.pool(x)

        x = x.reshape(-1, 20 * 4 * 4)

        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout(x)

        x = self.fc2(x)
        x = F.relu(x)
        x = self.dropout(x)

        x = self.fc3(x)
        x = F.relu(x)
        x = self.dropout(x)

        x = self.fc4(x)
        x = F.relu(x)
        x = self.dropout(x)

        x = self.fc5(x)

        return x
