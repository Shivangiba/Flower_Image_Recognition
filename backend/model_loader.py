# ============================================================
# model_loader.py — Loads trained EfficientNet-B0 model
#
# WHY SEPARATE FILE?
# Model loading is slow (~2-3 seconds).
# We load it ONCE when server starts, then reuse
# the same loaded model for every request.
# This makes predictions fast (no reload per request).
# ============================================================

import torch
import torch.nn as nn
import timm
from torchvision import transforms
from PIL import Image
import io

from config import (
    MODEL_PATH, MODEL_NAME, NUM_CLASSES,
    DROPOUT_RATE, DEVICE, IMAGE_SIZE,
    IMAGENET_MEAN, IMAGENET_STD, CLASSES
)


# ------------------------------------------------------------
# LOAD MODEL
# Called once when FastAPI server starts
# ------------------------------------------------------------

def load_model():
    """Load trained EfficientNet-B0 from checkpoint."""

    print(f"Loading model from: {MODEL_PATH}")
    print(f"Device: {DEVICE}")

    # Build same architecture as training
    model = timm.create_model(
        MODEL_NAME,
        pretrained=False,   # don't download weights
        num_classes=0       # remove original head
    )

    # Add same custom head as training
    num_features = model.num_features
    model.classifier = nn.Sequential(
        nn.Dropout(p=DROPOUT_RATE),
        nn.Linear(num_features, NUM_CLASSES)
    )

    # Load your trained weights
    model.load_state_dict(
        torch.load(MODEL_PATH, map_location=DEVICE)
    )

    model = model.to(DEVICE)
    model.eval()  # inference mode

    print(f"Model loaded successfully")
    print(f"Classes: {NUM_CLASSES}")

    return model


# ------------------------------------------------------------
# INFERENCE TRANSFORM
# Identical to val_test_transforms from training
# MUST be the same — different transforms = wrong predictions
# ------------------------------------------------------------

inference_transform = transforms.Compose([
    transforms.Resize(int(IMAGE_SIZE * 1.1)),
    transforms.CenterCrop(IMAGE_SIZE),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=IMAGENET_MEAN,
        std=IMAGENET_STD
    )
])


# ------------------------------------------------------------
# PREDICT FUNCTION
# Called for every incoming image request
# ------------------------------------------------------------

def predict(image_bytes: bytes):
    """
    Run inference on raw image bytes.

    Args:
        image_bytes: raw bytes of uploaded image file

    Returns:
        dict with prediction results
    """

    # Load image from bytes
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # Apply transforms
    tensor = inference_transform(image).unsqueeze(0).to(DEVICE)

    # Run inference
    with torch.no_grad():
        outputs = model(tensor)
        probabilities = torch.softmax(outputs, dim=1)[0]

    # Get top 5 predictions
    top5_probs, top5_indices = torch.topk(probabilities, 5)

    top5 = [
        {
            "class": CLASSES[idx.item()],
            "probability": round(prob.item() * 100, 2)
        }
        for prob, idx in zip(top5_probs, top5_indices)
    ]

    return {
        "predicted": top5[0]["class"],
        "confidence": top5[0]["probability"],
        "top5": top5
    }


# Load model at module import time
# This means it loads once when server starts
model = load_model()