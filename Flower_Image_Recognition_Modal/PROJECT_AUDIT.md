# Project Audit: Flower Image Recognition (13 Classes, EfficientNet-B0)

## Section 1: Executive Summary
1.  **Modular Architecture**: The project follows a clean, professional modular structure with clear separation of concerns (data, transforms, model, training, evaluation).
2.  **Critical Truncation**: `src/train.py` is incomplete and ends abruptly at line 297, missing the closure of the Stage 2 loop, logging, best-model saving, and early stopping checks.
3.  **Empty Orchestrator**: `main.py` is an empty placeholder (~39 bytes), making the project impossible to run as a single pipeline as described in the comments.
4.  **Environment Rigidity**: `src/config.py` hardcodes absolute Windows paths for `BASE_DIR`, which will cause immediate failures if the project is moved or executed on a different machine.
5.  **Dataset Integrity**: The stratified 70/15/15 split logic is correctly implemented using `sklearn`, ensuring balanced class distribution across train/val/test sets.
6.  **EfficientNet Implementation**: The project correctly uses `timm` to load `efficientnet_b0`. Note: Configuration comments mention B3, but the code correctly targets B0 (224x224).
7.  **Transfer Learning Strategy**: The two-stage training approach (Frozen Backbone → Full Fine-tuning) is a high-quality implementation that protects pretrained weights.
8.  **Pipeline Consistency**: Preprocessing transforms (normalization and resizing) are correctly synchronized between training, validation, and inference.
9.  **Metrics & Evaluation**: The use of Macro F1 and normalized confusion matrices provides a robust understanding of model performance beyond simple accuracy.
10. **Resource Management**: DataLoaders are configured with `num_workers=0`, which is the correct "fail-safe" setting for PyTorch on Windows to avoid multiprocessing crashes.

---

## Section 2: Detailed Audit Findings

### A. Imports & Dependency Issues
- **Missing Entry Points**: `main.py` is a 1-line comment. `train.py` is missing its `if __name__ == "__main__":` block.
- **Unpinned Dependencies**: `requirements.txt` lacks version numbers, which can lead to environment drift (e.g., `timm` updates changing the head naming).

### B. Dataset Pipeline
- **Status**: Verified Correct.
- **Note**: The stratified split logic is solid. `Image.open().convert("RGB")` is essential for handling inconsistent input formats.

### C. Model Architecture
- **Inconsistency**: `config.py` mentions B3 while code uses B0. Image size 224 is correct for B0.
- **Head modification**: Using `num_classes=0` in `timm` and then overwriting `model.classifier` is valid but slightly less idiomatic than passing `num_classes=13` to `create_model`.

### D. Training Pipeline
- **MAJOR BUG**: The fine-tuning loop in `src/train.py` (Stage 2) is truncated. It starts the loop but never ends it, meaning checkpoints aren't saved and history isn't recorded for the final 25 epochs.
- **Early Stopping**: The `should_stop` signal from the `EarlyStopping` class is never checked in the Stage 2 loop.

### E. Evaluation Metrics
- **Status**: Verified Correct.
- **Note**: Normalized confusion matrix implementation is excellent for detecting per-class performance gaps.

### F. Inference Pipeline
- **Inconsistency**: Inference logic is duplicated in `evaluate.py` rather than importing from a centralized `predict.py` or `model.py`.

---

## Section 3: Surgical Fixes

### Fix 1: Portable Paths (`src/config.py`)
```python
# Change line 16 from absolute to relative
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
```

### Fix 2: Complete Stage 2 Logic (`src/train.py`)
```python
# Add the missing closure to the Stage 2 loop
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
```

### Fix 3: Implement Orchestration (`main.py`)
```python
import argparse
from src.train import train_model
from src.evaluate import (
    load_best_model, evaluate_model, print_classification_report, 
    plot_confusion_matrix, plot_training_history, predict_from_path
)

def main():
    parser = argparse.ArgumentParser(description="Flower classification pipeline")
    parser.add_argument("--mode", type=str, choices=["train", "eval", "predict"], required=True)
    parser.add_argument("--image", type=str, help="Path to image for prediction")
    args = parser.parse_args()

    if args.mode == "train":
        history = train_model()
        plot_training_history(history)
    elif args.mode == "eval":
        model = load_best_model()
        from src.dataset import get_dataloaders
        _, _, test_loader = get_dataloaders()
        preds, labels = evaluate_model(model, test_loader)
        print_classification_report(preds, labels)
        plot_confusion_matrix(preds, labels)
    elif args.mode == "predict":
        if not args.image:
            print("Error: --image path required.")
            return
        model = load_best_model()
        predict_from_path(args.image, model)

if __name__ == "__main__":
    main()
```

---

## Section 4: Recommended Improvements

1.  **Mixed Precision**: Use `torch.cuda.amp` to speed up training on modern GPUs.
2.  **Versioning**: Add `timm==0.9.12` and `torch==2.x` to `requirements.txt`.
3.  **Label Map**: Export a `classes.json` file during training for robust inference.
4.  **TTA**: Implement Test-Time Augmentation for a ~1% boost in final accuracy.
5.  **Weighted Loss**: If Rose F1 score remains low, use `weight` parameter in `CrossEntropyLoss`.
6.  **Checkpointing**: Save `latest_checkpoint.pth` every epoch to allow recovery from crashes.
7.  **Web Export**: Add an ONNX/TorchScript export script for easier deployment.
8.  **Logging**: Switch from basic `print` to Python's `logging` module for cleaner file/console output.
