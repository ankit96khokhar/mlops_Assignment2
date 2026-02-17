# src/dataset.py

from torchvision import datasets, transforms
from torch.utils.data import DataLoader, random_split

def get_transforms(img_size=224):
    return transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.5]*3, [0.5]*3)
    ])

def get_dataloaders(data_dir, batch_size=32, img_size=224):

    transform = get_transforms(img_size)
    dataset = datasets.ImageFolder(data_dir, transform=transform)

    train_size = int(0.8 * len(dataset))
    val_size = int(0.1 * len(dataset))
    test_size = len(dataset) - train_size - val_size

    train, val, test = random_split(dataset, [train_size, val_size, test_size])

    return (
        DataLoader(train, batch_size=batch_size, shuffle=True),
        DataLoader(val, batch_size=batch_size),
        DataLoader(test, batch_size=batch_size)
    )
