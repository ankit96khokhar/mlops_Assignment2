# src/train.py

import torch
import torch.nn as nn
import torch.optim as optim
import mlflow
import mlflow.pytorch
import os
import time

from src.dataset import get_dataloaders
from src.model import SimpleCNN

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

def train():

    data_dir = "data/raw"
    batch_size = 32
    epochs = 5
    lr = 0.001

    train_loader, val_loader, test_loader = get_dataloaders(data_dir, batch_size)

    model = SimpleCNN().to(device)
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    mlflow.set_experiment("cats_vs_dogs")
    
    with mlflow.start_run():

        mlflow.log_param("batch_size", batch_size)
        mlflow.log_param("epochs", epochs)
        mlflow.log_param("learning_rate", lr)

        for epoch in range(epochs):
            model.train()
            running_loss = 0

            start = time.time()

            for images, labels in train_loader:
                images = images.to(device)
                labels = labels.float().unsqueeze(1).to(device)

                optimizer.zero_grad()
                outputs = model(images)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                running_loss += loss.item()

            epoch_time = time.time() - start

            mlflow.log_metric("train_loss", running_loss, step=epoch)
            mlflow.log_metric("epoch_time", epoch_time, step=epoch)

            print(f"Epoch {epoch+1}/{epochs}, Loss: {running_loss:.4f}")

        os.makedirs("models", exist_ok=True)
        model_path = "models/model.pt"
        torch.save(model.state_dict(), model_path)

        mlflow.log_artifact(model_path)

if __name__ == "__main__":
    train()
