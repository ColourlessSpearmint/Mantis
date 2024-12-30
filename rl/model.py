import torch
import torch.nn as nn

class MantisNN(nn.Module):
    def __init__(self):
        super(MantisNN, self).__init__()
        self.fc1 = nn.Linear(35, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, 4)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x
