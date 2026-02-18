# src/inference.py

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import torch
from PIL import Image
from torchvision import transforms
import io
import time
from prometheus_client import Counter, Histogram, generate_latest
from src.model import SimpleCNN
import logging

# ----------------------------
# Logging Configuration
# ----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

# ----------------------------
# Device
# ----------------------------
device = torch.device("cpu")
logger.info(f"Using device: {device}")

# ----------------------------
# Load model at startup
# ----------------------------
try:
    model = SimpleCNN()
    model.load_state_dict(torch.load("models/model.pt", map_location=device))
    model.eval()
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.exception("Model failed to load.")
    raise e

# ----------------------------
# Transform (NO augmentation)
# ----------------------------
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.5]*3, [0.5]*3)
])

# ----------------------------
# Monitoring Metrics
# ----------------------------
REQUEST_COUNT = Counter("request_count_total", "Total prediction requests")
LATENCY = Histogram("prediction_latency_seconds", "Prediction latency")

# ----------------------------
# FastAPI app
# ----------------------------
app = FastAPI(title="Cats vs Dogs Classifier")

@app.get("/health")
def health():
    logger.info("Health check called.")
    return {"status": "ok"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        REQUEST_COUNT.inc()
        logger.info("Prediction request received.")

        start_time = time.time()

        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image = transform(image).unsqueeze(0)

        with torch.no_grad():
            output = model(image)
            prob = output.item()

        label = "dog" if prob > 0.5 else "cat"

        latency = time.time() - start_time
        LATENCY.observe(latency)

        logger.info(
            f"Prediction completed | label={label} | "
            f"probability={prob:.4f} | latency={latency:.4f}s"
        )

        return {
            "label": label,
            "probability": round(prob, 4),
            "latency_seconds": round(latency, 4)
        }

    except Exception as e:
        logger.exception("Prediction failed.")
        return JSONResponse(status_code=400, content={"error": str(e)})

@app.get("/metrics")
def metrics():
    logger.info("Metrics endpoint called.")
    return generate_latest()
