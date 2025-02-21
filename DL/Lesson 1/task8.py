import torch
from torch import nn

def function04(x: torch.Tensor, y: torch.Tensor):
    n_steps = 2000
    step_size = 1e-2

    n_features = x.shape[1]

    layer = nn.Linear(in_features=n_features, out_features=1)

    for i in range(n_steps):
        y_pred = layer(x).view(-1)

        mse = torch.mean((y_pred - y) ** 2)

        if i < 20 or i % 50 == 0:
            print(f'MSE РЅР° С€Р°РіРµ {i + 1} {mse.item():.5f}')

        if mse < 0.3:
            print('break', mse)
            break

        mse.backward()

        with torch.no_grad():
            layer.weight -= step_size * layer.weight.grad
            layer.bias -= step_size * layer.bias.grad

        layer.zero_grad()

    return layer

if __name__ == '__main__':
    n_features = 2
    n_objects = 300

    w_true = torch.randn(n_features)
    X = (torch.rand(n_objects, n_features) - 0.5) * 5
    Y = X @ w_true + torch.randn(n_objects) / 2

    trained_layer = function04(X, Y)
    print(trained_layer.weight)
    print(trained_layer.bias)
