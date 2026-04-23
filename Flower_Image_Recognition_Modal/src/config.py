#all settings in one place

# ============================================================
# config.py — Central configuration for the entire project
# All hyperparameters, paths, and settings live here.
# If you want to change anything, change it ONLY in this file.
# ============================================================

import os

# ------------------------------------------------------------
# PATHS — where your data and results are stored
# ------------------------------------------------------------

# Root folder of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Combined dataset folder (your working data)
DATA_DIR = os.path.join(BASE_DIR, "data_combined")

# Where model checkpoints (saved weights) will be stored
CHECKPOINT_DIR = os.path.join(BASE_DIR, "results", "checkpoints")

# Where plots and charts will be saved
PLOTS_DIR = os.path.join(BASE_DIR, "results", "plots")

# Where metric logs will be saved
METRICS_DIR = os.path.join(BASE_DIR, "results", "metrices")

# ------------------------------------------------------------
# DATASET SETTINGS
# ------------------------------------------------------------

# Your 13 flower classes (must match folder names exactly)
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

# Number of classes
NUM_CLASSES = len(CLASSES)

# Train / Validation / Test split ratios (must add up to 1.0)
TRAIN_SPLIT = 0.70   # 70% for training
VAL_SPLIT   = 0.15   # 15% for validation
TEST_SPLIT  = 0.15   # 15% for final testing

# Random seed — keeps your splits identical every run
SEED = 42

# ------------------------------------------------------------
# IMAGE SETTINGS
# ------------------------------------------------------------

# EfficientNet-B0 expects 224x224 images
IMAGE_SIZE = 224

# ImageNet mean and std — used to normalize images
# We use ImageNet values because our model was pre-trained on ImageNet
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD  = [0.229, 0.224, 0.225]

# ------------------------------------------------------------
# TRAINING HYPERPARAMETERS
# ------------------------------------------------------------

# How many images to process at once (reduce to 16 if you run out of GPU memory)
BATCH_SIZE = 16

# Maximum number of training rounds
NUM_EPOCHS = 30

# How fast the model learns
# Stage 1: only top layers train (higher LR is fine)
# Stage 2: backbone unfreezes (must use lower LR to avoid destroying pretrained weights)
LR_STAGE1 = 1e-3
LR_STAGE2 = 1e-4

# Weight decay — prevents overfitting by penalizing large weights
WEIGHT_DECAY = 1e-4

# Dropout — randomly turns off neurons during training to prevent overfitting
DROPOUT_RATE = 0.4

# Early stopping — stop training if val loss doesn't improve for this many epochs
EARLY_STOPPING_PATIENCE = 10

# ------------------------------------------------------------
# MODEL SETTINGS
# ------------------------------------------------------------

# Pre-trained model to use from the timm library
# EfficientNet-B0 is the best balance of accuracy and speed for your dataset size
MODEL_NAME = "efficientnet_b0"

# Use GPU if available, otherwise fall back to CPU
import torch
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")