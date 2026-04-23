# metrics, confusion matrix

# ============================================================
# evaluate.py — Model evaluation and result visualization
#
# WHY THIS FILE EXISTS:
# Training tells us how the model performs on training data.
# Evaluation tells us how it performs on UNSEEN test data —
# which is the only metric that actually matters.
#
# THIS FILE PRODUCES:
# 1. Classification report — precision, recall, F1 per class
# 2. Confusion matrix — which flowers get confused with which
# 3. Training history plots — loss and accuracy curves
# 4. Sample predictions — visual proof the model works
#
# These outputs are what you include in your college report
# and show during your viva presentation.
# ============================================================

import os
import torch
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)
#A library that shows a progress bar while your loop is running.
from tqdm import tqdm

#Python Imaging Library (used via Pillow)
#A library used to open, process, and manipulate images
from PIL import Image

from src.config import (
    DEVICE, CLASSES, PLOTS_DIR, METRICS_DIR,
    CHECKPOINT_DIR, NUM_CLASSES
)
from src.transforms import val_test_transforms, inference_transform
from src.model import build_model


# ------------------------------------------------------------
# EVALUATE ON TEST SET
#
# Loads the best saved model and runs it on the test set.
# Collects all predictions and true labels for analysis.
#
# WHY USE TEST SET AND NOT VAL SET?
# Validation set was used during training to tune hyperparameters
# and decide when to stop — so the model has indirectly "seen" it.
# Test set is completely untouched — gives honest performance.
# ------------------------------------------------------------

def evaluate_model(model, test_loader):
    """
    Run model on test set and collect predictions.

    Returns:
        all_preds  : list of predicted class indices
        all_labels : list of true class indices
    """

    model.eval()

    all_preds = []
    all_labels = []

    print("Running evaluation on test set...")
    loop = tqdm(test_loader, desc="  Evaluating")

    with torch.no_grad():
        for images, labels in loop:
            images = images.to(DEVICE)
            labels = labels.to(DEVICE)

            outputs = model(images)
            _, predicted = torch.max(outputs, dim=1)

            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    return all_preds, all_labels


# ------------------------------------------------------------
# PRINT CLASSIFICATION REPORT
#
# Shows precision, recall, and F1-score for every class.
#
# WHAT THESE METRICS MEAN:
# Precision — of all images predicted as "Rose",
#             how many were actually Rose?
#             High precision = few false positives
#
# Recall    — of all actual Rose images,
#             how many did the model correctly identify?
#             High recall = few false negatives
#
# F1-Score  — harmonic mean of precision and recall
#             Best single metric for classification quality
#             F1 = 1.0 is perfect, 0.0 is worst
#
# Macro-F1  — average F1 across all classes equally
#             Best for balanced datasets like yours
# ------------------------------------------------------------

def print_classification_report(all_preds, all_labels):
    """Print and save the classification report."""

    os.makedirs(METRICS_DIR, exist_ok=True)

    print("\n" + "=" * 55)
    print("CLASSIFICATION REPORT")
    print("=" * 55)

    report = classification_report(
        all_labels,
        all_preds,
        target_names=CLASSES,
        digits=4
    )
    print(report)

    # Overall accuracy
    acc = accuracy_score(all_labels, all_preds)
    print(f"Overall Accuracy : {acc * 100:.2f}%")

    # Save report to file
    report_path = os.path.join(METRICS_DIR, "classification_report.txt")
    with open(report_path, "w") as f:
        f.write("FLOWER CLASSIFICATION — TEST SET RESULTS\n")
        f.write("=" * 55 + "\n\n")
        f.write(report)
        f.write(f"\nOverall Accuracy: {acc * 100:.2f}%\n")

    print(f"\nReport saved to: {report_path}")
    return acc


# ------------------------------------------------------------
# PLOT CONFUSION MATRIX
#
# A grid where:
# - Rows = actual flower class
# - Columns = predicted flower class
# - Diagonal = correct predictions (want these HIGH)
# - Off-diagonal = mistakes (want these LOW)
#
# Example: if row=Rose, col=Hibiscus has value 5,
# it means the model confused 5 Rose images as Hibiscus.
# This tells you exactly where the model struggles.
# ------------------------------------------------------------

def plot_confusion_matrix(all_preds, all_labels):
    """Plot and save confusion matrix heatmap."""

    os.makedirs(PLOTS_DIR, exist_ok=True)

    cm = confusion_matrix(all_labels, all_preds)

    # Normalize to percentages (easier to read than raw counts)
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    cm_percent = cm_normalized * 100

    plt.figure(figsize=(14, 12))
    sns.heatmap(
        cm_percent,
        annot=True,
        fmt='.1f',
        cmap='Blues',
        xticklabels=CLASSES,
        yticklabels=CLASSES,
        linewidths=0.5,
        cbar_kws={'label': 'Percentage (%)'}
    )

    plt.title('Confusion Matrix — Test Set (%)', fontsize=15, pad=15)
    plt.ylabel('Actual Class', fontsize=12)
    plt.xlabel('Predicted Class', fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.yticks(rotation=0, fontsize=9)
    plt.tight_layout()

    save_path = os.path.join(PLOTS_DIR, "confusion_matrix.png")
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Confusion matrix saved to: {save_path}")


# ------------------------------------------------------------
# PLOT TRAINING HISTORY
#
# Shows two graphs:
# 1. Loss curve — train loss and val loss over epochs
#    Good training: both decrease and stay close together
#    Overfitting: train loss keeps dropping, val loss rises
#
# 2. Accuracy curve — train acc and val acc over epochs
#    Good training: both increase and converge
#
# These graphs are essential for your report — they prove
# the model trained properly and didn't overfit.
# ------------------------------------------------------------

def plot_training_history(history):
    """Plot and save training loss and accuracy curves."""

    os.makedirs(PLOTS_DIR, exist_ok=True)

    epochs = range(1, len(history['train_loss']) + 1)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # ── Loss plot ──────────────────────────────────────────
    ax1.plot(epochs, history['train_loss'],
             'b-o', markersize=3, label='Train Loss', linewidth=1.5)
    ax1.plot(epochs, history['val_loss'],
             'r-o', markersize=3, label='Val Loss', linewidth=1.5)
    ax1.axvline(x=5, color='gray', linestyle='--',
                alpha=0.7, label='Stage 1→2')
    ax1.set_title('Training & Validation Loss', fontsize=13)
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.legend()
    ax1.grid(alpha=0.3)

    # ── Accuracy plot ──────────────────────────────────────
    ax2.plot(epochs, history['train_acc'],
             'b-o', markersize=3, label='Train Acc', linewidth=1.5)
    ax2.plot(epochs, history['val_acc'],
             'r-o', markersize=3, label='Val Acc', linewidth=1.5)
    ax2.axvline(x=5, color='gray', linestyle='--',
                alpha=0.7, label='Stage 1→2')
    ax2.set_title('Training & Validation Accuracy', fontsize=13)
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy (%)')
    ax2.legend()
    ax2.grid(alpha=0.3)

    plt.suptitle('EfficientNet-B0 — Flower Classification',
                 fontsize=14, y=1.02)
    plt.tight_layout()

    save_path = os.path.join(PLOTS_DIR, "training_history.png")
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Training history saved to: {save_path}")


# ------------------------------------------------------------
# PREDICT FROM USER IMAGE PATH
#
# This is the function that runs when a user provides
# an image path for flower recognition.
#
# Takes a file path, processes the image through the
# inference pipeline, and returns the prediction with
# confidence scores for all 13 classes.
# ------------------------------------------------------------

def predict_from_path(image_path, model):
    """
    Predict flower class from an image file path.

    Args:
        image_path : full path to the image file
        model      : trained model (loaded from checkpoint)

    Returns:
        predicted_class : name of predicted flower
        confidence      : confidence percentage
        top5            : top 5 predictions with percentages
    """

    # Check file exists
    if not os.path.exists(image_path):
        print(f"ERROR: Image not found at {image_path}")
        return None

    # Load and preprocess image
    image = Image.open(image_path).convert("RGB")
    tensor = inference_transform(image).unsqueeze(0)
    # unsqueeze(0) adds batch dimension: [3,224,224] → [1,3,224,224]

    model.eval()
    with torch.no_grad():
        tensor = tensor.to(DEVICE)
        outputs = model(tensor)
        probabilities = torch.softmax(outputs, dim=1)[0]

    # Get top 5 predictions
    top5_probs, top5_indices = torch.topk(probabilities, 5)
    top5 = [
        (CLASSES[idx.item()], round(prob.item() * 100, 2))
        for prob, idx in zip(top5_probs, top5_indices)
    ]

    predicted_class = top5[0][0]
    confidence = top5[0][1]

    # Display result
    print(f"\nPrediction Results:")
    print(f"{'─' * 35}")
    print(f"Predicted : {predicted_class}")
    print(f"Confidence: {confidence:.2f}%")
    print(f"\nTop 5 predictions:")
    for i, (cls, prob) in enumerate(top5, 1):
        bar = '█' * int(prob / 5)
        print(f"  {i}. {cls:<20} {prob:>6.2f}%  {bar}")

    # Show image with prediction
    plt.figure(figsize=(5, 5))
    plt.imshow(image)
    plt.title(f"Predicted: {predicted_class}\nConfidence: {confidence:.2f}%",
              fontsize=12)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

    return predicted_class, confidence, top5


# ------------------------------------------------------------
# LOAD BEST MODEL
#
# Loads the saved best model weights from training.
# Called before running evaluation or user predictions.
# ------------------------------------------------------------

def load_best_model():
    """Load the best saved model from checkpoints."""

    checkpoint_path = os.path.join(CHECKPOINT_DIR, "best_model.pth")

    if not os.path.exists(checkpoint_path):
        print(f"ERROR: No saved model found at {checkpoint_path}")
        print("Please run training first.")
        return None

    model = build_model()
    model.load_state_dict(torch.load(checkpoint_path, map_location=DEVICE))
    model.eval()

    print(f"Model loaded from: {checkpoint_path}")
    return model


# ------------------------------------------------------------
# QUICK TEST
# python -m src.evaluate
# ------------------------------------------------------------

if __name__ == "__main__":
    print("Testing evaluate module...\n")
    model = load_best_model()
    if model:
        print("Model loaded successfully.")
        print("Run main.py to train and evaluate the full pipeline.")