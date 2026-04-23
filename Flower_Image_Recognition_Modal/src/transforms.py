# image preprocessing and augmentation

# ============================================================
# transforms.py — Image preprocessing and augmentation
#
# WHY THIS FILE EXISTS:
# Neural networks don't understand images — they understand numbers.
# This file converts every image into a normalized tensor (array of numbers).
#
# TWO PIPELINES:
# 1. train_transforms — augments images randomly so the model
#    sees variety and cannot memorize training images
# 2. val_test_transforms — only resizes and normalizes, NO augmentation
#    because we want clean, consistent evaluation
# ============================================================

from torchvision import transforms
from src.config import IMAGE_SIZE, IMAGENET_MEAN, IMAGENET_STD


# ------------------------------------------------------------
# TRAINING TRANSFORMS
# Applied only during training to prevent memorization.
#
# Each augmentation and why we use it:
# - RandomResizedCrop: crops a random portion and resizes to IMAGE_SIZE
#   → model sees flowers at different zoom levels
# - RandomHorizontalFlip: flips image left-right 50% of the time
#   → a Rose facing left is still a Rose
# - RandomVerticalFlip: flips image upside down 20% of the time
#   → adds more variety for bulk/cluster images
# - RandomRotation: rotates up to 30 degrees
#   → flowers grow at different angles in real photos
# - ColorJitter: randomly changes brightness, contrast, saturation, hue
#   → model handles different lighting conditions (sunny, cloudy, indoor)
# - RandomGrayscale: converts to grayscale 10% of the time
#   → forces model to rely on shape, not just color
# - ToTensor: converts PIL image (0-255) to PyTorch tensor (0.0-1.0)
# - Normalize: shifts pixel values using ImageNet mean and std
#   → required because EfficientNet was pre-trained on ImageNet
# ------------------------------------------------------------

train_transforms = transforms.Compose([
    transforms.RandomResizedCrop(IMAGE_SIZE, scale=(0.7, 1.0)),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomVerticalFlip(p=0.2),
    transforms.RandomRotation(degrees=30),
    transforms.ColorJitter(
        brightness=0.3,
        contrast=0.3,
        saturation=0.3,
        hue=0.1
    ),
    transforms.RandomGrayscale(p=0.1),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=IMAGENET_MEAN,
        std=IMAGENET_STD
    )
])


# ------------------------------------------------------------
# VALIDATION AND TEST TRANSFORMS
# Applied during validation and testing — NO augmentation here.
#
# Why no augmentation?
# We want to measure how the model performs on real, unmodified
# images — the same way a user will submit a photo in real life.
#
# Steps:
# - Resize: makes image slightly larger than IMAGE_SIZE first
# - CenterCrop: crops the center to exact IMAGE_SIZE
#   → cleaner than RandomResizedCrop for evaluation
# - ToTensor + Normalize: same as training (always required)
# ------------------------------------------------------------

val_test_transforms = transforms.Compose([
    transforms.Resize(int(IMAGE_SIZE * 1.1)),   # e.g. 330 for B3
    transforms.CenterCrop(IMAGE_SIZE),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=IMAGENET_MEAN,
        std=IMAGENET_STD
    )
])


# ------------------------------------------------------------
# INFERENCE TRANSFORM
# Used when a USER submits a single image for prediction.
# Identical to val_test_transforms — clean, no augmentation.
# This is the pipeline that runs when someone uploads a photo.
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