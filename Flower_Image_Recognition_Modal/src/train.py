# training loop

# ============================================================
# train.py — Training loop for flower classification model
#
# WHY THIS FILE EXISTS:
# This file trains the model in two stages:
#
# STAGE 1 (epochs 1-5):
#   Backbone is frozen — only the classification head trains.
#   Learning rate: 1e-3 (higher, safe because backbone is frozen)
#   Purpose: warm up the head without corrupting pretrained weights
#
# STAGE 2 (epochs 6 onwards):
#   Entire network unfreezes and fine-tunes together.
#   Learning rate: 1e-4 (lower, careful adjustments)
#   Purpose: fine-tune EfficientNet features for flowers
#
# EARLY STOPPING:
#   If validation loss doesn't improve for 10 epochs in a row,
#   training stops automatically to prevent overfitting.
#
# BEST MODEL SAVING:
#   Every time validation accuracy improves, the model weights
#   are saved to results/checkpoints/best_model.pth
#   This ensures we always keep the best version, not the last.
# ============================================================

import os
import time
import torch
import torch.nn as nn
from tqdm import tqdm

from src.config import (
    DEVICE, NUM_EPOCHS, LR_STAGE1, LR_STAGE2,
    WEIGHT_DECAY, EARLY_STOPPING_PATIENCE,
    CHECKPOINT_DIR, CLASSES
)
from src.model import build_model, freeze_backbone, unfreeze_backbone
from src.dataset import get_dataloaders


# ------------------------------------------------------------
# EARLY STOPPING CLASS
#
# Monitors validation loss after every epoch.
# If it doesn't improve for PATIENCE epochs in a row,
# it signals the training loop to stop.
#
# WHY EARLY STOPPING?
# Without it, the model keeps training even after it has
# started memorizing training data (overfitting).
# Early stopping catches this automatically.
# ------------------------------------------------------------

class EarlyStopping:
    def __init__(self, patience=10, min_delta=0.001):
        """
        patience  : how many epochs to wait without improvement
        min_delta : minimum change to count as improvement
        """
        self.patience = patience
        self.min_delta = min_delta
        self.counter = 0
        self.best_loss = float('inf')
        self.should_stop = False

    def __call__(self, val_loss):
        if val_loss < self.best_loss - self.min_delta:
            # Improvement found — reset counter
            self.best_loss = val_loss
            self.counter = 0
        else:
            # No improvement — increment counter
            self.counter += 1
            print(f"  EarlyStopping: {self.counter}/{self.patience}")
            if self.counter >= self.patience:
                self.should_stop = True
                print("  Early stopping triggered.")


# ------------------------------------------------------------
# TRAIN ONE EPOCH
#
# Runs through the entire training set once.
# For each batch of 16 images:
# 1. Forward pass — model makes predictions
# 2. Loss calculation — how wrong are the predictions?
# 3. Backward pass — calculate gradients
# 4. Optimizer step — adjust weights to reduce loss
#
# Returns average loss and accuracy for this epoch.
# ------------------------------------------------------------

def train_one_epoch(model, loader, criterion, optimizer):
    model.train()   # enables dropout and batch norm in train mode

    total_loss = 0.0
    correct = 0
    total = 0

    # tqdm wraps the loader to show a live progress bar
    loop = tqdm(loader, desc="  Training", leave=False)

    for images, labels in loop:
        # Move data to same device as model (CPU or GPU)
        images = images.to(DEVICE)
        labels = labels.to(DEVICE)

        # Zero gradients from previous batch
        # (PyTorch accumulates gradients by default)
        optimizer.zero_grad()

        # Forward pass — get predictions
        outputs = model(images)

        # Calculate loss — how wrong are predictions?
        loss = criterion(outputs, labels)

        # Backward pass — calculate how to adjust weights
        loss.backward()

        # Update weights based on gradients
        optimizer.step()

        # Track metrics
        total_loss += loss.item()
        _, predicted = torch.max(outputs, dim=1)
        correct += (predicted == labels).sum().item()
        total += labels.size(0)

        # Update progress bar
        loop.set_postfix(loss=f"{loss.item():.4f}")

    avg_loss = total_loss / len(loader)
    accuracy = 100.0 * correct / total
    return avg_loss, accuracy


# ------------------------------------------------------------
# VALIDATE ONE EPOCH
#
# Runs through the validation set once.
# No weight updates happen here — we only measure performance.
#
# torch.no_grad() speeds this up by skipping gradient
# calculations that are only needed for training.
# ------------------------------------------------------------

def validate_one_epoch(model, loader, criterion):
    model.eval()    # disables dropout for consistent evaluation

    total_loss = 0.0
    correct = 0
    total = 0

    loop = tqdm(loader, desc="  Validating", leave=False)

    with torch.no_grad():   # no gradients needed for validation
        for images, labels in loop:
            images = images.to(DEVICE)
            labels = labels.to(DEVICE)

            outputs = model(images)
            loss = criterion(outputs, labels)

            total_loss += loss.item()
            _, predicted = torch.max(outputs, dim=1)
            correct += (predicted == labels).sum().item()
            total += labels.size(0)

    avg_loss = total_loss / len(loader)
    accuracy = 100.0 * correct / total
    return avg_loss, accuracy


# ------------------------------------------------------------
# MAIN TRAINING FUNCTION
#
# Orchestrates the full two-stage training process.
# Call this function from main.py to start training.
# ------------------------------------------------------------

def train_model():

    # Create checkpoint directory if it doesn't exist
    os.makedirs(CHECKPOINT_DIR, exist_ok=True)

    # ── Load data ──────────────────────────────────────────
    print("=" * 55)
    print("LOADING DATA")
    print("=" * 55)
    train_loader, val_loader, _ = get_dataloaders()

    # ── Build model ────────────────────────────────────────
    print("\n" + "=" * 55)
    print("BUILDING MODEL")
    print("=" * 55)
    model = build_model()

    # ── Loss function ──────────────────────────────────────
    # CrossEntropyLoss is standard for multi-class classification
    # It combines Softmax + negative log likelihood internally
    criterion = nn.CrossEntropyLoss()

    # ── Training history ───────────────────────────────────
    # Stores metrics for every epoch (used for plotting later)
    history = {
        'train_loss': [], 'train_acc': [],
        'val_loss':   [], 'val_acc':  []
    }

    # ── Early stopping ─────────────────────────────────────
    early_stopping = EarlyStopping(patience=EARLY_STOPPING_PATIENCE)

    # ── Best model tracking ────────────────────────────────
    best_val_acc = 0.0
    checkpoint_path = os.path.join(CHECKPOINT_DIR, "best_model.pth")

    # ── STAGE 1: Frozen backbone ───────────────────────────
    STAGE1_EPOCHS = 5   # train only head for first 5 epochs

    print("\n" + "=" * 55)
    print("STAGE 1 — Training classification head (frozen backbone)")
    print("=" * 55)

    model = freeze_backbone(model)

    # Optimizer for Stage 1 — higher learning rate
    optimizer = torch.optim.AdamW(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=LR_STAGE1,
        weight_decay=WEIGHT_DECAY
    )

    # Learning rate scheduler — reduces LR when val loss plateaus
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='min', factor=0.5, patience=3
    )

    for epoch in range(1, STAGE1_EPOCHS + 1):
        start = time.time()

        train_loss, train_acc = train_one_epoch(model, train_loader, criterion, optimizer)
        val_loss, val_acc     = validate_one_epoch(model, val_loader, criterion)

        scheduler.step(val_loss)
        elapsed = time.time() - start

        # Save history
        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_acc)

        print(f"Epoch [{epoch:02d}/{STAGE1_EPOCHS}] "
              f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.2f}% | "
              f"Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.2f}% | "
              f"Time: {elapsed:.1f}s")

        # Save best model
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), checkpoint_path)
            print(f"  Best model saved — Val Acc: {best_val_acc:.2f}%")

    # ── STAGE 2: Unfrozen backbone ─────────────────────────
    print("\n" + "=" * 55)
    print("STAGE 2 — Fine-tuning full network (unfrozen backbone)")
    print("=" * 55)

    model = unfreeze_backbone(model)

    # New optimizer for Stage 2 — lower learning rate
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=LR_STAGE2,
        weight_decay=WEIGHT_DECAY
    )

    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='min', factor=0.5, patience=3
    )

    remaining_epochs = NUM_EPOCHS - STAGE1_EPOCHS  # 25 more epochs

    for epoch in range(STAGE1_EPOCHS + 1, NUM_EPOCHS + 1):
        start = time.time()

        train_loss, train_acc = train_one_epoch(model, train_loader, criterion, optimizer)
        val_loss, val_acc     = validate_one_epoch(model, val_loader, criterion)

        scheduler.step(val_loss)
        elapsed = time.time() - start

        # Save history
        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_acc)

        print(f"Epoch [{epoch:02d}/{NUM_EPOCHS}] "
              f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.2f}% | "
              f"Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.2f}% | "
              f"Time: {elapsed:.1f}s")

        # Save best model
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), checkpoint_path)
            print(f"  Best model saved — Val Acc: {best_val_acc:.2f}%")

        # Early stopping check
        early_stopping(val_loss)
        if early_stopping.should_stop:
            print("  Stopping early...")
            break

    print("\nTraining Finished.")
    print(f"Best Overall Val Acc: {best_val_acc:.2f}%")
    return history

if __name__ == "__main__":
    train_model()