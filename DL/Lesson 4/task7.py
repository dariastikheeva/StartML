import torch
from torch import nn
from torch.utils.data import DataLoader

def predict(model: nn.Module, loader: DataLoader, device: torch.device):
    model.eval()
    preds = []

    with torch.no_grad():
        for x,y in loader:
            y_pred = torch.argmax(model(x), dim=1)
            preds.append(y_pred)

    return torch.concat(preds)
