# loads and splits your images

# ============================================================
# dataset.py — Data loading and splitting
#
# WHY THIS FILE EXISTS:
# PyTorch needs data in a specific format to train.
# This file handles three things:
# 1. SPLIT — divides data_combined into train/val/test
#    using stratified splitting (equal class distribution
#    in every split)
# 2. LOAD — wraps the splits into PyTorch Dataset objects
#    so the model can read images one by one
# 3. BATCH — groups images into batches using DataLoader
#    so the model processes 16 images at a time
# ============================================================
#PiL is used to convert image into numpy array,resize image into 224X224 which is accepted by efficientnetB0
#And reads image from backend and gives it to model 

#transformers converts image into tensor(container) from pil formet to methamatical matrix to do operations in it


import os
import random
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split

from src.config import (
    DATA_DIR, CLASSES, TRAIN_SPLIT, VAL_SPLIT,
    TEST_SPLIT, SEED, BATCH_SIZE
)
from src.transforms import train_transforms, val_test_transforms


# ------------------------------------------------------------
# STEP 1: COLLECT ALL IMAGE PATHS AND LABELS
#
# Walks through data_combined folder and builds two lists:
# - all_paths: full file path to every image
# - all_labels: numeric class index (0-12) for every image
#
# Example:
# all_paths[0]  = "data_combined/Rose/Single_rose_001.jpg"
# all_labels[0] = 9  (index of "Rose" in CLASSES list)
# ------------------------------------------------------------

def collect_image_paths():
    all_paths = []
    all_labels = []

    for class_idx, class_name in enumerate(CLASSES):
        class_folder = os.path.join(DATA_DIR, class_name)

        if not os.path.exists(class_folder):
            print(f"WARNING: folder not found — {class_folder}")
            continue

        for img_file in os.listdir(class_folder):
            # Only include actual image files
            if img_file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.webp')):
                full_path = os.path.join(class_folder, img_file)
                all_paths.append(full_path)
                all_labels.append(class_idx)

    print(f"Total images found: {len(all_paths)}")
    return all_paths, all_labels


# ------------------------------------------------------------
# STEP 2: STRATIFIED SPLIT
#
# Splits all images into train / val / test sets.
#
# WHY STRATIFIED?
# Random splitting might put 90% of Zinnia images in train
# and only 10% in test — model never properly validates on it.
# Stratified split guarantees every class is proportionally
# represented in all three sets.
#
# Split sizes (approx per class of ~620 images):
# Train : 70% → ~434 images
# Val   : 15% → ~93 images
# Test  : 15% → ~93 images
# ------------------------------------------------------------

def split_dataset(all_paths, all_labels):

    # First split: separate test set from the rest
    train_val_paths, test_paths, train_val_labels, test_labels = train_test_split(
        all_paths,
        all_labels,
        test_size=TEST_SPLIT,
        stratify=all_labels,     # ensures balanced classes in test
        random_state=SEED        # same split every run
    )

    # Second split: separate val from train
    # val_size is relative to train_val, not total
    # e.g. 0.15 / (1 - 0.15) = 0.176 of train_val = 15% of total
    relative_val_size = VAL_SPLIT / (1 - TEST_SPLIT)

    train_paths, val_paths, train_labels, val_labels = train_test_split(
        train_val_paths,
        train_val_labels,
        test_size=relative_val_size,
        stratify=train_val_labels,
        random_state=SEED
    )

    print(f"Train set : {len(train_paths)} images")
    print(f"Val set   : {len(val_paths)} images")
    print(f"Test set  : {len(test_paths)} images")

    return train_paths, val_paths, test_paths, \
           train_labels, val_labels, test_labels


# ------------------------------------------------------------
# STEP 3: PYTORCH DATASET CLASS
#
# PyTorch needs a Dataset object that:
# - knows how many images exist (via __len__)
# - can return one image+label pair by index (via __getitem__)
#
# When the model requests image #42, this class:
# 1. Opens the image file from disk
# 2. Applies the appropriate transform (augment or not)
# 3. Returns the tensor + label to the model
#
# This is where augmentation happens — every time an image
# is loaded during training, it gets a RANDOMLY different
# transform applied, so the model never sees the exact
# same version of an image twice.
# ------------------------------------------------------------

class FlowerDataset(Dataset):

    def __init__(self, image_paths, labels, transform=None):
        """
        image_paths : list of full file paths to images
        labels      : list of integer class indices
        transform   : torchvision transform pipeline to apply
        """
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform

    def __len__(self):
        # Returns total number of images in this dataset
        return len(self.image_paths)

    def __getitem__(self, idx):
        # Load image from disk
        img_path = self.image_paths[idx]
        image = Image.open(img_path).convert("RGB")
        # convert("RGB") handles grayscale or RGBA images
        # by converting them to standard 3-channel RGB

        # Apply transform (resize, augment, normalize, tensorize)
        if self.transform:
            image = self.transform(image)

        label = self.labels[idx]
        return image, label


# ------------------------------------------------------------
# STEP 4: CREATE DATALOADERS
#
# DataLoader wraps a Dataset and:
# - Groups images into batches (e.g. 16 at a time)
# - Shuffles training data every epoch
# - Loads images in parallel (num_workers)
#
# WHY SHUFFLE TRAIN ONLY?
# Shuffling training data prevents the model from learning
# the ORDER of images instead of their features.
# Val/test are not shuffled so results are reproducible.
# ------------------------------------------------------------

def get_dataloaders():

    # Collect all paths and labels
    all_paths, all_labels = collect_image_paths()

    # Split into train / val / test
    train_paths, val_paths, test_paths, \
    train_labels, val_labels, test_labels = split_dataset(all_paths, all_labels)

    # Create Dataset objects with appropriate transforms
    # Training gets augmentation, val/test get clean transforms
    train_dataset = FlowerDataset(train_paths, train_labels, transform=train_transforms)
    val_dataset   = FlowerDataset(val_paths,   val_labels,   transform=val_test_transforms)
    test_dataset  = FlowerDataset(test_paths,  test_labels,  transform=val_test_transforms)

    # Wrap datasets in DataLoaders
    # num_workers=0 is safest on Windows (avoids multiprocessing issues)
    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,           # shuffle every epoch
        num_workers=0
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,          # no shuffle for validation
        num_workers=0
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,          # no shuffle for test
        num_workers=0
    )

    return train_loader, val_loader, test_loader


# ------------------------------------------------------------
# QUICK TEST
# Run this file directly to verify dataset loads correctly:
# python -m src.dataset
# ------------------------------------------------------------

if __name__ == "__main__":
    print("Testing dataset loading...\n")
    train_loader, val_loader, test_loader = get_dataloaders()

    # Grab one batch and print its shape
    images, labels = next(iter(train_loader))
    print(f"\nSample batch:")
    print(f"  Image tensor shape : {images.shape}")
    print(f"  Labels shape       : {labels.shape}")
    print(f"  Label values       : {labels.tolist()}")
    print(f"  Class names        : {[CLASSES[l] for l in labels.tolist()]}")
    print("\nDataset loading works correctly.")