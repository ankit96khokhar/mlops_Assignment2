from src.dataset import get_transforms
from PIL import Image
import torch

def test_transform_output_shape():
    transform = get_transforms()
    img = Image.new("RGB", (300, 300))
    tensor = transform(img)
    assert tensor.shape == (3, 224, 224)
