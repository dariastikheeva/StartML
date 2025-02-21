import torch
from torch import nn
from torch.utils.data import DataLoader

@torch.inference_mode()
def predict_tta(model: nn.Module, loader: DataLoader, device: torch.device, iterations: int = 2):
	model.eval()

	with torch.no_grad():
		iterations_list = []
		for it in range(iterations):
			iter_list = []
			for x, y in loader:
				x, y = x.to(device), y.to(device)

				output = model(x)

				iter_list.append(output)

			iterations_list.append(torch.concat(iter_list).unsqueeze(0))

	res = torch.concat(iterations_list)

	return torch.argmax(res.mean(dim=0), dim=1)
