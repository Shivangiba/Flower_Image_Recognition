# ============================================================
# config.py — Backend configuration
# Keeps all settings in one place
# ============================================================

import os

# Base directory of backend folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to saved model weights
MODEL_PATH = os.path.join(BASE_DIR, "model", "best_model.pth")

# Model settings — must match what was used in training
MODEL_NAME   = "efficientnet_b0"
NUM_CLASSES  = 13
IMAGE_SIZE   = 224
DROPOUT_RATE = 0.4

# ImageNet normalization values
# Must be identical to training transforms
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD  = [0.229, 0.224, 0.225]

# Your 13 flower classes
# Order MUST match training order exactly
CLASSES = [
    "Bougainvillea",
    "Chrysanthemum",
    "Cosmos flower",
    "Hibiscus",
    "Jungle Geranium",
    "Marigold",
    "Marvel of peru",
    "Peacock Flower",
    "Periwinkle",
    "Rose",
    "Salvia",
    "Sunflower",
    "Zinnia"
]

# Device
import torch
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")