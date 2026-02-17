import torch
from src.model import SimpleCNN

def test_model_output_shape():
    model = SimpleCNN()
    dummy = torch.randn(1, 3, 224, 224)
    output = model(dummy)
    assert output.shape == (1, 1)
