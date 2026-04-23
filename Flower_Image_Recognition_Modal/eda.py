# ============================================================
# eda.py — Exploratory Data Analysis
#
# WHY THIS FILE EXISTS:
# Before training any model, a data scientist must UNDERSTAND
# the dataset. This script answers:
# - How many images per class?
# - Are classes balanced?
# - What do sample images look like?
# - What sizes are the images?
# - Are there any corrupted files?
#
# Run this BEFORE training to understand your data.
# The plots it generates go into your college report.
#
# HOW TO RUN:
#   python eda.py
# ============================================================

import os
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from PIL import Image
from collections import defaultdict

from src.config import DATA_DIR, CLASSES, PLOTS_DIR

# Create plots directory if it doesn't exist
os.makedirs(PLOTS_DIR, exist_ok=True)


# ------------------------------------------------------------
# STEP 1: COUNT IMAGES PER CLASS
#
# Walks through data_combined and counts how many images
# are in each class folder.
# This tells us if the dataset is balanced or not.
# ------------------------------------------------------------

def count_images_per_class():
    print("=" * 55)
    print("STEP 1 — Class Distribution")
    print("=" * 55)

    class_counts = {}
    corrupt_files = []

    for class_name in CLASSES:
        class_path = os.path.join(DATA_DIR, class_name)
        if not os.path.exists(class_path):
            print(f"WARNING: {class_name} folder not found")
            class_counts[class_name] = 0
            continue

        images = [
            f for f in os.listdir(class_path)
            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.webp'))
        ]
        class_counts[class_name] = len(images)

        # Check for corrupted images
        for img_file in images:
            img_path = os.path.join(class_path, img_file)
            try:
                with Image.open(img_path) as img:
                    img.verify()
            except Exception:
                corrupt_files.append(img_path)

    # Print counts
    print(f"\n{'Class':<25} {'Count':>6}")
    print("-" * 35)
    for cls, count in class_counts.items():
        bar = '█' * (count // 20)
        print(f"{cls:<25} {count:>6}  {bar}")

    print("-" * 35)
    print(f"{'TOTAL':<25} {sum(class_counts.values()):>6}")
    print(f"\nMin class : {min(class_counts, key=class_counts.get)}"
          f" ({min(class_counts.values())})")
    print(f"Max class : {max(class_counts, key=class_counts.get)}"
          f" ({max(class_counts.values())})")
    print(f"Imbalance : {max(class_counts.values()) / min(class_counts.values()):.2f}:1")
    print(f"Corrupted : {len(corrupt_files)} files")

    if corrupt_files:
        print("\nCorrupted files:")
        for f in corrupt_files:
            print(f"  {f}")

    return class_counts, corrupt_files


# ------------------------------------------------------------
# STEP 2: PLOT CLASS DISTRIBUTION
#
# Bar chart showing image count per class.
# A good dataset has bars of similar height (balanced).
# This chart goes directly into your college report.
# ------------------------------------------------------------

def plot_class_distribution(class_counts):
    print("\n" + "=" * 55)
    print("STEP 2 — Plotting Class Distribution")
    print("=" * 55)

    counts = [class_counts[cls] for cls in CLASSES]
    avg = sum(counts) / len(counts)

    # Color bars based on count vs average
    colors = ['#2ecc71' if c >= avg else '#e74c3c' for c in counts]

    plt.figure(figsize=(14, 6))
    bars = plt.bar(CLASSES, counts, color=colors, edgecolor='white', linewidth=0.5)

    # Add count labels on top of each bar
    for bar, count in zip(bars, counts):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 5,
            str(count),
            ha='center', va='bottom', fontsize=9
        )

    # Add average line
    plt.axhline(y=avg, color='steelblue', linestyle='--',
                linewidth=1.5, label=f'Average ({avg:.0f})')

    # Legend
    above = mpatches.Patch(color='#2ecc71', label='Above average')
    below = mpatches.Patch(color='#e74c3c', label='Below average')
    plt.legend(handles=[above, below,
               plt.Line2D([0], [0], color='steelblue',
               linestyle='--', label=f'Average ({avg:.0f})')])

    plt.title('Class Distribution — data_combined', fontsize=14)
    plt.xlabel('Flower Class', fontsize=11)
    plt.ylabel('Number of Images', fontsize=11)
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.ylim(0, max(counts) + 60)
    plt.tight_layout()

    save_path = os.path.join(PLOTS_DIR, "eda_class_distribution.png")
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Saved: {save_path}")


# ------------------------------------------------------------
# STEP 3: ANALYZE IMAGE DIMENSIONS
#
# Checks the width and height of every image.
# Tells us if images are consistent or vary wildly in size.
# EfficientNet-B0 resizes everything to 224x224 anyway,
# but this shows us the raw data quality.
# ------------------------------------------------------------

def analyze_image_dimensions():
    print("\n" + "=" * 55)
    print("STEP 3 — Image Dimension Analysis")
    print("=" * 55)

    widths = []
    heights = []
    sample_count = 0

    for class_name in CLASSES:
        class_path = os.path.join(DATA_DIR, class_name)
        if not os.path.exists(class_path):
            continue

        images = [
            f for f in os.listdir(class_path)
            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.webp'))
        ]

        # Sample 50 images per class for speed
        sample = random.sample(images, min(50, len(images)))

        for img_file in sample:
            img_path = os.path.join(class_path, img_file)
            try:
                with Image.open(img_path) as img:
                    w, h = img.size
                    widths.append(w)
                    heights.append(h)
                    sample_count += 1
            except Exception:
                pass

    print(f"\nAnalyzed    : {sample_count} sample images")
    print(f"Avg Width   : {np.mean(widths):.0f}px")
    print(f"Avg Height  : {np.mean(heights):.0f}px")
    print(f"Min Size    : {min(widths)}x{min(heights)}")
    print(f"Max Size    : {max(widths)}x{max(heights)}")

    # Scatter plot of dimensions
    plt.figure(figsize=(8, 6))
    plt.scatter(widths, heights, alpha=0.15, s=8, color='steelblue')
    plt.axvline(x=224, color='red', linestyle='--',
                linewidth=1, label='Target: 224px')
    plt.axhline(y=224, color='red', linestyle='--', linewidth=1)
    plt.title('Image Dimensions (sample)', fontsize=13)
    plt.xlabel('Width (px)')
    plt.ylabel('Height (px)')
    plt.legend()
    plt.tight_layout()

    save_path = os.path.join(PLOTS_DIR, "eda_image_dimensions.png")
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Saved: {save_path}")

    return widths, heights


# ------------------------------------------------------------
# STEP 4: SAMPLE IMAGE GRID
#
# Shows one random image from each of the 13 classes.
# This is a visual sanity check — confirming labels match
# the actual flower images, and images look clean.
# This grid is great to include in your report.
# ------------------------------------------------------------

def plot_sample_images():
    print("\n" + "=" * 55)
    print("STEP 4 — Sample Images Per Class")
    print("=" * 55)

    # 3 rows x 5 cols = 15 slots for 13 classes
    fig, axes = plt.subplots(3, 5, figsize=(16, 10))
    axes = axes.flatten()

    for i, class_name in enumerate(CLASSES):
        class_path = os.path.join(DATA_DIR, class_name)
        images = [
            f for f in os.listdir(class_path)
            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.webp'))
        ]

        # Pick a random image
        img_file = random.choice(images)
        img_path = os.path.join(class_path, img_file)

        try:
            img = Image.open(img_path).convert("RGB")
            axes[i].imshow(img)
            axes[i].set_title(class_name, fontsize=9, fontweight='bold')
            axes[i].axis('off')
        except Exception:
            axes[i].set_title(f"{class_name}\n(error)", fontsize=8)
            axes[i].axis('off')

    # Hide unused subplot slots
    for j in range(len(CLASSES), len(axes)):
        axes[j].axis('off')

    plt.suptitle('Sample Images — One Per Class', fontsize=14, y=1.01)
    plt.tight_layout()

    save_path = os.path.join(PLOTS_DIR, "eda_sample_images.png")
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Saved: {save_path}")


# ------------------------------------------------------------
# STEP 5: DATASET SUMMARY
#
# Prints a clean final summary of everything we found.
# Copy this into your college report introduction.
# ------------------------------------------------------------

def print_summary(class_counts, corrupt_files, widths, heights):
    print("\n" + "=" * 55)
    print("DATASET SUMMARY")
    print("=" * 55)
    print(f"  Dataset path     : {DATA_DIR}")
    print(f"  Total classes    : {len(CLASSES)}")
    print(f"  Total images     : {sum(class_counts.values())}")
    print(f"  Avg per class    : {sum(class_counts.values()) // len(CLASSES)}")
    print(f"  Min class        : {min(class_counts, key=class_counts.get)}"
          f" ({min(class_counts.values())} images)")
    print(f"  Max class        : {max(class_counts, key=class_counts.get)}"
          f" ({max(class_counts.values())} images)")
    print(f"  Imbalance ratio  : "
          f"{max(class_counts.values()) / min(class_counts.values()):.2f}:1")
    print(f"  Avg image size   : {np.mean(widths):.0f} x {np.mean(heights):.0f} px")
    print(f"  Corrupted files  : {len(corrupt_files)}")
    print(f"  Target size      : 224 x 224 px (EfficientNet-B0)")
    print(f"  Train split      : 70% "
          f"(~{int(sum(class_counts.values()) * 0.70)} images)")
    print(f"  Val split        : 15% "
          f"(~{int(sum(class_counts.values()) * 0.15)} images)")
    print(f"  Test split       : 15% "
          f"(~{int(sum(class_counts.values()) * 0.15)} images)")
    print("=" * 55)
    print("\nEDA complete. All plots saved to results/plots/")
    print("You can now run training:")
    print("  python main.py --mode train")


# ------------------------------------------------------------
# MAIN — runs all EDA steps in order
# ------------------------------------------------------------

if __name__ == "__main__":
    print("\n" + "=" * 55)
    print("  FLOWER DATASET — EXPLORATORY DATA ANALYSIS")
    print("=" * 55)

    # Step 1: Count and check
    class_counts, corrupt_files = count_images_per_class()

    # Step 2: Distribution chart
    plot_class_distribution(class_counts)

    # Step 3: Image dimensions
    widths, heights = analyze_image_dimensions()

    # Step 4: Visual sample grid
    plot_sample_images()

    # Step 5: Final summary
    print_summary(class_counts, corrupt_files, widths, heights)


# **Now your correct run order is:**
# ```
# # Step 1 — Explore your data first
# python eda.py

# # Step 2 — Train the model
# python main.py --mode train

# # Step 3 — Predict a user image
# python main.py --mode predict --image "path/to/flower.jpg"