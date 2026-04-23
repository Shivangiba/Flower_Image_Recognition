# ============================================================
# generate_plots.py — Reconstructs training history plots
# This generates two plots:
# training_history.png — loss and accuracy curves
# per_class_f1.png — F1 score per class bar chart
# from saved Stage 1 training results
# Run: python generate_plots.py
# ============================================================

import os
import matplotlib
matplotlib.use('Agg')  # prevents GUI popup issues
import matplotlib.pyplot as plt

from src.config import PLOTS_DIR
os.makedirs(PLOTS_DIR, exist_ok=True)

# ── Stage 1 results from your actual training run ──────────
epochs      = [1, 2, 3, 4, 5]
train_loss  = [1.1880, 0.6144, 0.4928, 0.4401, 0.4248]
train_acc   = [70.60,  84.09,  85.71,  86.33,  87.60]
val_loss    = [0.6034, 0.3802, 0.3216, 0.2724, 0.2257]
val_acc     = [88.97,  91.93,  92.67,  94.49,  94.73]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# ── Loss plot ───────────────────────────────────────────────
ax1.plot(epochs, train_loss, 'b-o', markersize=6,
         label='Train Loss', linewidth=2)
ax1.plot(epochs, val_loss, 'r-o', markersize=6,
         label='Val Loss', linewidth=2)

# Annotate final values
ax1.annotate(f'{train_loss[-1]:.4f}',
             xy=(5, train_loss[-1]),
             xytext=(4.6, train_loss[-1] + 0.04),
             fontsize=9, color='blue')
ax1.annotate(f'{val_loss[-1]:.4f}',
             xy=(5, val_loss[-1]),
             xytext=(4.6, val_loss[-1] + 0.04),
             fontsize=9, color='red')

ax1.set_title('Training & Validation Loss\n(Stage 1 — Frozen Backbone)',
              fontsize=12)
ax1.set_xlabel('Epoch')
ax1.set_ylabel('Loss')
ax1.set_xticks(epochs)
ax1.legend()
ax1.grid(alpha=0.3)
ax1.set_ylim(0, 1.4)

# ── Accuracy plot ───────────────────────────────────────────
ax2.plot(epochs, train_acc, 'b-o', markersize=6,
         label='Train Acc', linewidth=2)
ax2.plot(epochs, val_acc, 'r-o', markersize=6,
         label='Val Acc', linewidth=2)

# Annotate final values
ax2.annotate(f'{train_acc[-1]:.2f}%',
             xy=(5, train_acc[-1]),
             xytext=(4.6, train_acc[-1] - 2.5),
             fontsize=9, color='blue')
ax2.annotate(f'{val_acc[-1]:.2f}%',
             xy=(5, val_acc[-1]),
             xytext=(4.6, val_acc[-1] + 0.5),
             fontsize=9, color='red')

ax2.set_title('Training & Validation Accuracy\n(Stage 1 — Frozen Backbone)',
              fontsize=12)
ax2.set_xlabel('Epoch')
ax2.set_ylabel('Accuracy (%)')
ax2.set_xticks(epochs)
ax2.legend()
ax2.grid(alpha=0.3)
ax2.set_ylim(60, 100)

# ── Key observations box ────────────────────────────────────
observations = (
    "Key Observations:\n"
    "• Val Loss consistently below Train Loss\n"
    "  → No overfitting detected\n"
    "• Val Acc exceeded Train Acc every epoch\n"
    "  → Strong generalization\n"
    "• Final Val Acc: 94.73% (epoch 5)"
)
fig.text(0.5, -0.08, observations,
         ha='center', fontsize=10,
         bbox=dict(boxstyle='round', facecolor='lightyellow',
                   alpha=0.8, edgecolor='gray'))

plt.suptitle(
    'EfficientNet-B0 — Flower Classification Training History\n'
    'Dataset: Colored Flowers in Bangladesh | Classes: 13',
    fontsize=13, y=1.02
)
plt.tight_layout()

save_path = os.path.join(PLOTS_DIR, "training_history.png")
plt.savefig(save_path, dpi=150, bbox_inches='tight')
print(f"Training history plot saved to: {save_path}")

# ── Per class F1 bar chart ──────────────────────────────────
classes = [
    'Sunflower', 'Marigold', 'Cosmos flower',
    'Peacock Flower', 'Periwinkle', 'Bougainvillea',
    'Salvia', 'Jungle Geranium', 'Marvel of peru',
    'Zinnia', 'Hibiscus', 'Chrysanthemum', 'Rose'
]
f1_scores = [
    0.9948, 0.9785, 0.9727, 0.9688, 0.9519,
    0.9430, 0.9412, 0.9385, 0.9341, 0.9326,
    0.9297, 0.9257, 0.8528
]

colors = [
    '#1D9E75' if f >= 0.95 else
    '#5DCAA5' if f >= 0.90 else
    '#EF9F27'
    for f in f1_scores
]

plt.figure(figsize=(13, 6))
bars = plt.barh(classes, f1_scores, color=colors, edgecolor='white')

# Add value labels
for bar, score in zip(bars, f1_scores):
    plt.text(
        bar.get_width() + 0.002,
        bar.get_y() + bar.get_height() / 2,
        f'{score:.4f}',
        va='center', fontsize=9
    )

# Legend
from matplotlib.patches import Patch
legend = [
    Patch(color='#1D9E75', label='F1 ≥ 0.95 (Excellent)'),
    Patch(color='#5DCAA5', label='F1 ≥ 0.90 (Good)'),
    Patch(color='#EF9F27', label='F1 < 0.90 (Needs improvement)'),
]
plt.legend(handles=legend, loc='lower right', fontsize=9)

plt.axvline(x=0.9434, color='red', linestyle='--',
            linewidth=1.5, label=f'Macro F1 (0.9434)')
plt.text(0.9434 + 0.001, -0.8, 'Macro F1\n0.9434',
         color='red', fontsize=8)

plt.title('Per-Class F1 Scores — Test Set\n'
          'Overall Accuracy: 94.32% | Macro F1: 0.9434',
          fontsize=13)
plt.xlabel('F1 Score')
plt.xlim(0.80, 1.02)
plt.gca().invert_yaxis()
plt.tight_layout()

save_path2 = os.path.join(PLOTS_DIR, "per_class_f1.png")
plt.savefig(save_path2, dpi=150, bbox_inches='tight')
print(f"Per-class F1 plot saved to: {save_path2}")

print("\nAll plots generated successfully.")
print("Check results/plots/ folder.")

