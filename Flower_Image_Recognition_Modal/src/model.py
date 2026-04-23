# EfficientNet model definition

# ============================================================
# model.py — EfficientNet-B0 model definition
#
# WHY THIS FILE EXISTS:
# This file builds the neural network that will classify flowers.
#
# WHAT IS TRANSFER LEARNING?
# EfficientNet-B0 was pre-trained on ImageNet — 1.2 million
# images across 1000 categories. It already knows how to detect
# low-level features (edges, curves, textures) and high-level
# features (shapes, patterns). We take that knowledge and
# fine-tune it for our 13 flower classes.
#
# TWO-STAGE TRAINING STRATEGY:
# Stage 1 — Frozen backbone:
#   Only the new classification head trains.
#   The pretrained weights are locked (frozen).
#   This teaches the head to work with EfficientNet features
#   without destroying the pretrained weights.
#
# Stage 2 — Unfrozen backbone:
#   We unlock the entire network and train everything
#   with a very low learning rate.
#   This fine-tunes the pretrained features specifically
#   for flower recognition.
# ============================================================

import torch
import torch.nn as nn
import timm

from src.config import (
    MODEL_NAME, NUM_CLASSES, DROPOUT_RATE, DEVICE
)


# ------------------------------------------------------------
# BUILD MODEL FUNCTION
#
# Creates EfficientNet-B0 with a custom classification head.
#
# ARCHITECTURE:
# Input (224x224 RGB image)
#     ↓
# EfficientNet-B0 backbone (pretrained, 1280 features out)
#     ↓
# Dropout (0.4) — randomly drops 40% of neurons to prevent
#                 overfitting during training
#     ↓
# Linear layer (1280 → 13) — maps features to 13 flower classes
#     ↓
# Output: 13 scores (one per class)
# The class with the highest score is the prediction.
#
# NOTE: We do NOT add Softmax here because PyTorch's
# CrossEntropyLoss applies it internally during training.
# During inference we apply Softmax manually to get
# probabilities (0-100%) for the user to see.
# ------------------------------------------------------------

def build_model():
    """
    Builds and returns EfficientNet-B0 model ready for training.
    The model is automatically moved to GPU if available,
    otherwise stays on CPU.
    """

    # Load EfficientNet-B0 with pretrained ImageNet weights
    # pretrained=True downloads weights automatically on first run
    model = timm.create_model(
        MODEL_NAME,
        pretrained=True,
        num_classes=0       # num_classes=0 removes the original
                            # 1000-class head so we can add our own
    )

    # Get the number of features the backbone outputs
    # For EfficientNet-B0 this is 1280
    num_features = model.num_features

    # Add our custom classification head
    # This replaces the original 1000-class ImageNet classifier
    # with our 13-class flower classifier
    model.classifier = nn.Sequential(
        nn.Dropout(p=DROPOUT_RATE),             # prevent overfitting
        nn.Linear(num_features, NUM_CLASSES)    # 1280 → 13
    )

    # Move model to GPU if available, otherwise CPU
    model = model.to(DEVICE)

    print(f"Model     : {MODEL_NAME}")
    print(f"Device    : {DEVICE}")
    print(f"Features  : {num_features}")
    print(f"Classes   : {NUM_CLASSES}")

    return model


# ------------------------------------------------------------
# FREEZE BACKBONE — used in Stage 1
#
# Freezes all layers EXCEPT the classifier head.
# This means only the final Linear layer will update
# its weights during Stage 1 training.
#
# WHY FREEZE FIRST?
# If we train all layers immediately with random head weights,
# the large gradients from the random head will corrupt the
# carefully pretrained backbone weights.
# Freezing protects those weights while the head stabilizes.
# ------------------------------------------------------------

def freeze_backbone(model):
    """Freeze all layers except the classifier head."""

    # Freeze everything
    for param in model.parameters():
        param.requires_grad = False

    # Unfreeze only the classifier head
    for param in model.classifier.parameters():
        param.requires_grad = True

    # Count trainable parameters
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total = sum(p.numel() for p in model.parameters())
    print(f"Stage 1 — Frozen backbone")
    print(f"Trainable params : {trainable:,} / {total:,}")

    return model


# ------------------------------------------------------------
# UNFREEZE BACKBONE — used in Stage 2
#
# Unfreezes ALL layers so the entire network can fine-tune.
# Used with a much lower learning rate (LR_STAGE2 = 1e-4)
# to make small, careful adjustments to pretrained weights.
# ------------------------------------------------------------

def unfreeze_backbone(model):
    """Unfreeze all layers for full fine-tuning."""

    for param in model.parameters():
        param.requires_grad = True

    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Stage 2 — Unfrozen backbone")
    print(f"Trainable params : {trainable:,} / {trainable:,}")

    return model


# ------------------------------------------------------------
# PREDICT SINGLE IMAGE — used when user uploads a photo
#
# Takes a preprocessed image tensor and returns:
# - predicted class name
# - confidence percentage
# - all class probabilities
#
# This is the function that runs when a user submits
# an image for flower recognition.
# ------------------------------------------------------------

def predict_single_image(model, image_tensor, classes):
    """
    Run inference on a single preprocessed image tensor.

    Args:
        model        : trained FlowerNet model
        image_tensor : tensor of shape [1, 3, 224, 224]
        classes      : list of class name strings

    Returns:
        predicted_class : string name of predicted flower
        confidence      : float percentage (0-100)
        all_probs       : dict of {class_name: probability}
    """

    model.eval()    # set to evaluation mode (disables dropout)

    with torch.no_grad():   # no gradient calculation needed
        # Move tensor to same device as model
        image_tensor = image_tensor.to(DEVICE)

        # Forward pass through the model
        outputs = model(image_tensor)

        # Apply Softmax to convert raw scores to probabilities
        # Now each value is between 0 and 1, and all sum to 1
        probabilities = torch.softmax(outputs, dim=1)

        # Get the highest probability and its class index
        confidence, predicted_idx = torch.max(probabilities, dim=1)

        # Convert to readable values
        predicted_class = classes[predicted_idx.item()]
        confidence_pct = confidence.item() * 100

        # Build a dictionary of all class probabilities
        all_probs = {
            classes[i]: round(probabilities[0][i].item() * 100, 2)
            for i in range(len(classes))
        }

    return predicted_class, confidence_pct, all_probs


# ------------------------------------------------------------
# QUICK TEST
# Run this file directly to verify model builds correctly:
# python -m src.model
# ------------------------------------------------------------

if __name__ == "__main__":
    print("Testing model build...\n")

    model = build_model()
    print()

    # Test Stage 1 freezing
    model = freeze_backbone(model)
    print()

    # Test Stage 2 unfreezing
    model = unfreeze_backbone(model)
    print()

    # Test forward pass with a dummy image
    import torch
    dummy_input = torch.randn(1, 3, 224, 224).to(DEVICE)
    output = model(dummy_input)
    print(f"\nDummy forward pass output shape: {output.shape}")
    print(f"Expected: torch.Size([1, 13])")
    print("\nModel builds correctly.")
