# 🌸 Flower Image Recognition — EfficientNet-B0

> A deep learning model for classifying 13 species of flowers using Transfer Learning with EfficientNet-B0, achieving **94.32% test accuracy** and **0.9434 Macro F1-Score**.

---

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Dataset](#dataset)
3. [Flower Classes](#flower-classes)
4. [Project Structure](#project-structure)
5. [Model Architecture](#model-architecture)
6. [Training Pipeline](#training-pipeline)
7. [Data Preprocessing](#data-preprocessing)
8. [Performance Results](#performance-results)
9. [Installation & Setup](#installation--setup)
10. [How to Run](#how-to-run)
11. [File Descriptions](#file-descriptions)
12. [Configuration Reference](#configuration-reference)
13. [Future Improvements](#future-improvements)
14. [Technical Stack](#technical-stack)

---

## 🔍 Project Overview

This project implements a **flower species classification system** using deep learning. Given an input image of a flower, the model classifies it into one of 13 categories with a confidence percentage.

The model is built on **EfficientNet-B0** pre-trained on ImageNet and fine-tuned on a custom dataset of Bangladeshi and tropical flowers. It employs a **two-stage transfer learning strategy** to achieve high accuracy without overfitting.

**Key Highlights:**
- ✅ 13-class multi-class classification
- ✅ 94.32% test set accuracy
- ✅ 0.9434 Macro F1-Score (balanced across all classes)
- ✅ Stratified 70/15/15 train/val/test split
- ✅ Two-stage transfer learning (Frozen → Full Fine-tuning)
- ✅ Runs on both CPU and GPU

---

## 📦 Dataset

| Property | Value |
|---|---|
| **Total Images** | 8,100 |
| **Number of Classes** | 13 |
| **Average per Class** | ~623 images |
| **Image Format** | JPG, PNG, BMP, WebP |
| **Dataset Type** | Custom  |
| **Train Split** | 70% → 5,670 images |
| **Validation Split** | 15% → 1,215 images |
| **Test Split** | 15% → 1,215 images |

**Dataset Directory Structure:**
```
data_combined/
├── Bougainvillea/
│   ├── bougainvillea_001.jpg
│   ├── bougainvillea_002.jpg
│   └── ...
├── Chrysanthemum/
├── Cosmos flower/
├── Hibiscus/
├── Jungle Geranium/
├── Marigold/
├── Marvel of peru/
├── Peacock Flower/
├── Periwinkle/
├── Rose/
├── Salvia/
├── Sunflower/
└── Zinnia/
```

> **Note:** The dataset folder lives at the parent level, one directory up from `Flower_Image_Recognition_Modal/`.

---

## 🌺 Flower Classes

| # | Class Name | Test F1-Score | Performance |
|---|---|---|---|
| 1 | Bougainvillea | 0.9430 | 🟢 Good |
| 2 | Chrysanthemum | 0.9257 | 🟢 Good |
| 3 | Cosmos flower | 0.9727 | 🟢 Excellent |
| 4 | Hibiscus | 0.9297 | 🟢 Good |
| 5 | Jungle Geranium | 0.9385 | 🟢 Good |
| 6 | Marigold | 0.9785 | 🟢 Excellent |
| 7 | Marvel of peru | 0.9341 | 🟢 Good |
| 8 | Peacock Flower | 0.9688 | 🟢 Excellent |
| 9 | Periwinkle | 0.9519 | 🟢 Good |
| 10 | Rose | 0.8528 | 🟡 Needs Improvement |
| 11 | Salvia | 0.9412 | 🟢 Good |
| 12 | Sunflower | **0.9948** | 🟣 Best Class |
| 13 | Zinnia | 0.9326 | 🟢 Good |

> **Weakest Class:** Rose (0.8528) — due to high visual variance in petal shape and color across varieties.  
> **Strongest Class:** Sunflower (0.9948) — distinctive large yellow structure makes it near-perfectly separable.

---

## 📁 Project Structure

```
Flower_Image_Recognition_Modal/
│
├── main.py                    # 🚀 Single entry point — orchestrates everything
├── eda.py                     # 📊 Exploratory Data Analysis
├── run_eval.py                # 🔎 Quick evaluation script
├── generate_plots.py          # 📈 Reconstructs training plots from saved results
├── requirements.txt           # 📦 Python dependencies
├── PROJECT_AUDIT.md           # 🔍 Audit log and code review summary
├── README.md                  # 📚 This file
│
├── src/
│   ├── __init__.py            # Package initializer
│   ├── config.py              # ⚙️  Central configuration (all hyperparameters)
│   ├── dataset.py             # 💾 Data loading, splitting, and DataLoaders
│   ├── transforms.py          # 🔄 Image preprocessing and augmentation pipelines
│   ├── model.py               # 🧠 EfficientNet-B0 model definition
│   ├── train.py               # 🏋️  Two-stage training loop with early stopping
│   └── evaluate.py            # 📏 Metrics, confusion matrix, predictions
│
├── notebooks/
│   ├── 01_eda.ipynb           # Interactive EDA notebook
│   └── 02_training.ipynb      # Training walkthrough notebook
│
├── results/
│   ├── checkpoints/
│   │   └── best_model.pth     # 💾 Best saved model weights (~16MB)
│   ├── plots/
│   │   ├── training_history.png
│   │   ├── confusion_matrix.png
│   │   ├── per_class_f1.png
│   │   └── eda_*.png
│   └── metrices/
│       └── classification_report.txt
│
└── data_combined/             # (Parent directory — not inside the Modal folder)
    └── [13 Class Folders]/
```

---

## 🧠 Model Architecture

### Base Model: EfficientNet-B0
Loaded from the **`timm`** library with ImageNet pretrained weights.

```
Input Image (224 × 224 × 3)
        ↓
EfficientNet-B0 Backbone (Pretrained, Frozen in Stage 1)
  → 1280 feature channels output
        ↓
Dropout(p=0.4)
  → Prevents overfitting by randomly zeroing 40% of activations
        ↓
Linear(1280 → 13)
  → Maps 1280 backbone features to 13 flower class scores
        ↓
Output: 13 Raw Logits
  → Argmax → Predicted Class
  → Softmax → Confidence Percentages (for display)
```

### Why EfficientNet-B0?
| Criterion | EfficientNet-B0 |
|---|---|
| **Parameters** | ~5.3M (lightweight) |
| **Pretrained** | ImageNet (1000 classes, 1.2M images) |
| **Input Size** | 224 × 224 |
| **Output Features** | 1280 |
| **Speed** | ~4ms per image (GPU) |
| **Accuracy** | State-of-the-art on small datasets |

EfficientNet-B0 was chosen over alternatives like ResNet50 (25M params) and VGG16 (138M params) because it delivers higher accuracy at a fraction of the computational cost — ideal for a dataset of ~8,100 images.

---

## 🏋️ Training Pipeline

### Overview: Two-Stage Transfer Learning

Training is split into two stages to protect pretrained weights while achieving maximum fine-tuning performance.

```
Stage 1: Frozen Backbone (Epochs 1-5)
───────────────────────────────────────
  Backbone:  FROZEN (no gradient updates)
  Head Only: TRAINABLE
  LR:        1e-3 (high — safe with frozen backbone)
  Purpose:   Warm up the classification head with stable features

Stage 2: Full Fine-tuning (Epochs 6-30)
───────────────────────────────────────
  Backbone:  UNFROZEN (gradients flow through entire network)
  LR:        1e-4 (low — small, careful adjustments)
  Purpose:   Fine-tune all layers for flower-specific features
```

### Training Details

| Hyperparameter | Stage 1 | Stage 2 |
|---|---|---|
| **Learning Rate** | 1e-3 | 1e-4 |
| **Optimizer** | AdamW | AdamW |
| **Weight Decay** | 1e-4 | 1e-4 |
| **Scheduler** | ReduceLROnPlateau | ReduceLROnPlateau |
| **Scheduler Patience** | 3 epochs | 3 epochs |
| **Scheduler Factor** | 0.5 | 0.5 |
| **Epochs** | 5 | Up to 25 |
| **Early Stopping** | N/A | 10 epochs patience |
| **Batch Size** | 16 | 16 |

### Early Stopping
Training halts automatically if validation loss does not improve for **10 consecutive epochs**, preventing overfitting. The `min_delta` threshold is `0.001`.

### Best Model Saving
After every epoch, if the **validation accuracy improves**, the model state dict is saved to `results/checkpoints/best_model.pth`. Training is guaranteed to keep the single best-performing checkpoint.

---

## 🔄 Data Preprocessing

Two distinct pipelines are used — one for training (with augmentation) and one for validation/testing/inference (clean):

### Training Transforms (Augmentation)
```python
RandomResizedCrop(224, scale=(0.7, 1.0))  # Random zoom + crop
RandomHorizontalFlip(p=0.5)               # Mirror flip
RandomVerticalFlip(p=0.2)                 # Upside-down (20% rare)
RandomRotation(degrees=30)                # ±30° rotation
ColorJitter(brightness, contrast,         # Simulate lighting changes
            saturation, hue)
RandomGrayscale(p=0.1)                   # Shape-based learning
ToTensor()                               # PIL → Float Tensor [0,1]
Normalize(mean=[0.485, 0.456, 0.406],    # ImageNet normalization
          std=[0.229, 0.224, 0.225])
```

### Validation / Test / Inference Transforms (Clean)
```python
Resize(246)          # Slightly larger than target
CenterCrop(224)      # Clean center crop
ToTensor()
Normalize(mean=[0.485, 0.456, 0.406],
          std=[0.229, 0.224, 0.225])
```

> **Why the same normalization?** EfficientNet-B0 was trained on ImageNet. Its internal weights expect inputs in the exact same statistical distribution (normalized by ImageNet mean/std). Using different values would make pretrained features meaningless.

---

## 📊 Performance Results

### Official Test Set Metrics (1,215 images)

| Metric | Value |
|---|---|
| **Overall Accuracy** | **94.32%** |
| **Macro F1-Score** | **0.9434** |
| **Weighted F1-Score** | **0.9434** |
| **Macro Precision** | 0.9452 |
| **Macro Recall** | 0.9433 |

### Per-Class Results

| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Bougainvillea | 0.9286 | 0.9579 | 0.9430 | 95 |
| Chrysanthemum | 0.9878 | 0.8710 | 0.9257 | 93 |
| Cosmos flower | 0.9889 | 0.9570 | 0.9727 | 93 |
| Hibiscus | 0.9556 | 0.9053 | 0.9297 | 95 |
| Jungle Geranium | 0.9545 | 0.9231 | 0.9385 | 91 |
| Marigold | 1.0000 | 0.9579 | 0.9785 | 95 |
| Marvel of peru | 0.9444 | 0.9239 | 0.9341 | 92 |
| Peacock Flower | 0.9394 | 1.0000 | 0.9688 | 93 |
| Periwinkle | 0.9271 | 0.9780 | 0.9519 | 91 |
| Rose | 0.8235 | 0.8842 | 0.8528 | 95 |
| Salvia | 0.9565 | 0.9263 | 0.9412 | 95 |
| Sunflower | 0.9896 | 1.0000 | 0.9948 | 95 |
| Zinnia | 0.8911 | 0.9783 | 0.9326 | 92 |

### Stage 1 Training History (Actual Recorded Values)

| Epoch | Train Loss | Train Acc | Val Loss | Val Acc |
|---|---|---|---|---|
| 1 | 1.1880 | 70.60% | 0.6034 | 88.97% |
| 2 | 0.6144 | 84.09% | 0.3802 | 91.93% |
| 3 | 0.4928 | 85.71% | 0.3216 | 92.67% |
| 4 | 0.4401 | 86.33% | 0.2724 | 94.49% |
| 5 | 0.4248 | 87.60% | 0.2257 | **94.73%** |

> Validation loss was consistently lower than training loss across all epochs — a strong indicator of **no overfitting** during Stage 1.

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.9 or later
- pip
- (Recommended) NVIDIA GPU with CUDA for faster training; falls back to CPU automatically

### Step 1: Clone / Navigate to the Project
```powershell
cd "C:\Users\HP\OneDrive\Documents\SEM 6\MLDL\FLower_Image_Recognition\Flower_Image_Recognition_Modal"
```

### Step 2: Create a Virtual Environment (Recommended)
```powershell
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Verify the Dataset is Present
Ensure the following structure exists at the parent level:
```
FLower_Image_Recognition/
├── data_combined/          ← Dataset must be here
│   ├── Bougainvillea/
│   ├── Rose/
│   └── ...
└── Flower_Image_Recognition_Modal/
    └── main.py             ← Run from here
```

---

## ▶️ How to Run

All commands are run from the **`Flower_Image_Recognition_Modal/`** directory.

### 1. Exploratory Data Analysis (Optional but Recommended First)
```powershell
python eda.py
```
Outputs class distribution charts, image dimension scatter plots, and a sample image grid into `results/plots/`.

### 2. Train the Model
```powershell
python main.py --mode train
```
- Runs Stage 1 (5 epochs, frozen backbone)
- Runs Stage 2 (up to 25 epochs, full fine-tuning)
- Saves `best_model.pth` automatically
- Generates training history plots

### 3. Evaluate on Test Set
```powershell
python main.py --mode eval
```
- Loads the best saved checkpoint
- Runs full evaluation on the held-out test set
- Prints classification report and saves confusion matrix

### 4. Predict a Single Flower Image
```powershell
python main.py --mode predict --image "C:\path\to\your\flower.jpg"
```
Returns the predicted class, confidence score, and top-5 predictions with a visual bar chart.

### 5. Quick Evaluation (Alternative)
```powershell
python run_eval.py
```
Shorter script if you only need the classification report and confusion matrix.

---

## 📄 File Descriptions

| File | Purpose |
|---|---|
| `main.py` | CLI orchestrator — single entry point for all modes |
| `eda.py` | Full EDA script: class counts, dimensions, corrupt check, plots |
| `run_eval.py` | Quick standalone evaluation script |
| `generate_plots.py` | Reconstructs training history plots from hardcoded results |
| `requirements.txt` | All Python package dependencies |
| `PROJECT_AUDIT.md` | Code audit report with issues found and fixes applied |
| `src/config.py` | All hyperparameters and paths in one place |
| `src/dataset.py` | Image path collection, stratified splitting, Dataset class, DataLoaders |
| `src/transforms.py` | Training augmentation pipeline and clean eval/inference pipeline |
| `src/model.py` | EfficientNet-B0 build, freeze/unfreeze functions, single-image inference |
| `src/train.py` | Two-stage training loop, EarlyStopping class, checkpoint saving |
| `src/evaluate.py` | Test evaluation, classification report, confusion matrix, predict from path |

---

## ⚙️ Configuration Reference

All settings live in `src/config.py`. Edit only this file to change the project behavior.

| Setting | Default | Description |
|---|---|---|
| `BASE_DIR` | Auto-detected | Project root (relative, portable) |
| `DATA_DIR` | `../data_combined` | Dataset folder path |
| `CHECKPOINT_DIR` | `results/checkpoints` | Where `.pth` files are saved |
| `PLOTS_DIR` | `results/plots` | Where chart images are saved |
| `METRICS_DIR` | `results/metrices` | Where text reports are saved |
| `CLASSES` | 13-item list | Class names (must match folder names exactly) |
| `NUM_CLASSES` | 13 | Auto-derived from `CLASSES` |
| `TRAIN_SPLIT` | 0.70 | 70% data for training |
| `VAL_SPLIT` | 0.15 | 15% data for validation |
| `TEST_SPLIT` | 0.15 | 15% data for final testing |
| `SEED` | 42 | Random seed for reproducibility |
| `IMAGE_SIZE` | 224 | Input resolution for EfficientNet-B0 |
| `IMAGENET_MEAN` | [0.485, 0.456, 0.406] | Normalization mean |
| `IMAGENET_STD` | [0.229, 0.224, 0.225] | Normalization std |
| `BATCH_SIZE` | 16 | Images per batch (lower to 8 if GPU OOM) |
| `NUM_EPOCHS` | 30 | Total max epochs (Stage 1 + Stage 2) |
| `LR_STAGE1` | 1e-3 | Learning rate for frozen-backbone stage |
| `LR_STAGE2` | 1e-4 | Learning rate for full fine-tuning stage |
| `WEIGHT_DECAY` | 1e-4 | L2 regularization strength |
| `DROPOUT_RATE` | 0.4 | Classification head dropout rate |
| `EARLY_STOPPING_PATIENCE` | 10 | Patience epochs before stopping |
| `MODEL_NAME` | `efficientnet_b0` | Model identifier from `timm` |
| `DEVICE` | Auto (CUDA/CPU) | Accelerator device |

---

## 🚀 Future Improvements

### High-Impact Performance Upgrades

| # | Improvement | Expected Benefit | Difficulty |
|---|---|---|---|
| 1 | **Stage 2 Full Fine-tuning** | +2-4% accuracy (especially Rose class) | Low |
| 2 | **Mixed Precision (AMP)** | ~2x training speed on GPU | Low |
| 3 | **Test-Time Augmentation (TTA)** | +0.5-1% accuracy on edge cases | Medium |
| 4 | **Weighted CrossEntropy Loss** | Improves Rose/Chrysanthemum F1 | Low |
| 5 | **Larger Backbone (EfficientNet-B3)** | +1-3% accuracy at higher compute cost | Medium |
| 6 | **Cosine Annealing Scheduler** | More stable fine-tuning convergence | Low |

### Deployment & Production Upgrades

| # | Improvement | Description | Priority |
|---|---|---|---|
| 7 | **ONNX Export** | Convert `.pth` → `.onnx` for web/mobile deployment | High |
| 8 | **FastAPI Web Server** | REST API endpoint for real-time predictions | High |
| 9 | **Gradio / Streamlit Demo** | Drag-and-drop browser UI for non-technical users | Medium |
| 10 | **TorchScript Export** | Serialize model for C++ or Android deployment | Medium |
| 11 | **Docker Container** | Package the full serving stack for cloud deployment | Medium |

### Data & Robustness Upgrades

| # | Improvement | Description |
|---|---|---|
| 12 | **Expand Classes** | Add more Bangladeshi flower varieties (Krishnachura, Shimul, etc.) |
| 13 | **Data Augmentation v2** | Add `MixUp`, `CutMix`, `AutoAugment` for richer training diversity |
| 14 | **Label Map JSON** | Export `classes.json` during training for safe inference across environments |
| 15 | **Cross-Validation** | 5-fold stratified CV to get statistically robust accuracy estimates |
| 16 | **Dataset Versioning** | Use DVC or Hugging Face Hub for versioned dataset management |

### Code & Monitoring Upgrades

| # | Improvement | Description |
|---|---|---|
| 17 | **Logging Module** | Replace `print` with Python `logging` for file + console output |
| 18 | **WandB / TensorBoard** | Real-time training metric dashboards |
| 19 | **Resume Training** | Save `latest_checkpoint.pth` every epoch to recover crashed runs |
| 20 | **Pinned Dependencies** | Add exact versions to `requirements.txt` for environment stability |

---

## 🧰 Technical Stack

| Component | Technology |
|---|---|
| **Language** | Python 3.9+ |
| **Deep Learning Framework** | PyTorch |
| **Pretrained Models** | `timm` (PyTorch Image Models) |
| **Computer Vision Utilities** | `torchvision` |
| **Image Processing** | `Pillow` (PIL) |
| **Data Analysis** | `pandas`, `numpy` |
| **ML Utilities** | `scikit-learn` (stratified split, metrics) |
| **Visualization** | `matplotlib`, `seaborn` |
| **Progress Bars** | `tqdm` |
| **Notebooks** | `jupyter` |
| **Device Support** | CUDA GPU + CPU fallback |

---

## 🎓 About this Project

**Course**: Machine Learning & Deep Learning  
**Semester**: 6th Semester  
**Dataset**: Custom dataset of 13 flower species from Bangladesh and South Asia  
**Training Regime**: Transfer Learning on EfficientNet-B0 (ImageNet pretrained)  
**Final Test Accuracy**: **94.32%**  
**Macro F1-Score**: **0.9434**

---

*Last Updated: March 2026*
