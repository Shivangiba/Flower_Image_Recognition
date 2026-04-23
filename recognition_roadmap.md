# Flower AI: Precision Recognition Analysis & Roadmap

This document provides a step-by-step analysis of your current model architecture, data workflow, and the technical requirements to transition from **Flower Classification** to **Flower Recognition (Google Lens style)**.

---

## 1. Current Model Workflow (Step-by-Step)

Your current system is built as a **Global Image Classifier**. Here is how the data flows:

### Step A: Data Preparation (`dataset.py`)
- **Structure**: Data is organized by folders (e.g., `rose/`, `tulip/`). The folder name is the "Ground Truth" label.
- **Preprocessing**: Images are resized, centered, and normalized using ImageNet statistics (Mean/Std).
- **Assumption**: The model assumes there is **exactly one** primary flower in the image.

### Step B: Neural Architecture (`model.py`)
- **Backbone**: **EfficientNet-B0**. This is a state-of-the-art "Feature Extractor" known for being very lightweight and fast.
- **Head**: A custom linear layer reduces the 1280 features from EfficientNet down to your **13 flower classes**.
- **Output**: A probability distribution (Softmax). If the model sees 90% Rose and 10% Tulip, it ignores the Tulip and labels it "Rose".

### Step C: Inference & Camera Feed (`FlowerScanner.tsx` + `main.py`)
- **Process**: When you "Scan," the camera takes a static snapshot (Snapshot Mode).
- **Communication**: The frontend sends the image as a Base64 string or File to the `/predict-base64` endpoint.
- **Result**: The API returns the top class (single result) which the UI displays as a card.

---

## 2. Recommended Performance Improvements

Before changing the model type, here are 3 ways to improve the current accuracy:

1.  **Test-Time Augmentation (TTA)**: During prediction, run the image through the model 3-5 times with slight rotations/crops and average the results. This often boosts accuracy by 1-2%.
2.  **Class Weights**: If some flowers (e.g., "Lotus") have fewer images than others, add `weight` to your `CrossEntropyLoss` during training to focus on the rare classes.
3.  **Resolution Scaling**: EfficientNet-B0 is trained on 224x224. If your flowers are small in the frame, increasing `IMAGE_SIZE` to 300x300 and using **EfficientNet-B3** would significantly improve detail recognition.

---

## 3. Transitioning to "Flower Recognition" (Google Lens Style)

"Recognition" implies **Object Detection** (finding multiple objects in one frame) rather than just "Classification."

### The Key Difference
| Feature | Current (Classification) | New (Recognition / Detection) |
| :--- | :--- | :--- |
| **Output** | "This image is a Rose." | "There is a Rose at [x1,y1] and a Tulip at [x2,y2]." |
| **Model** | EfficientNet-B0 | **YOLOv12**, **SSD**, or **Faster R-CNN** |
| **Data Requirements** | Image + Folder Label | Image + **Bounding Box Coordinates** |

### Necessary Changes to Achieve This:

#### 1. Data Re-Labeling (The Biggest Task)
You cannot use the folder-based labels anymore. You will need to annotate your images with "Bounding Boxes" using tools like **CVAT** or **LabelImg**. 
- Instead of just `label: rose`, you need `label: rose, x: 100, y: 150, w: 50, h: 50`.

#### 2. Swap the Neural Engine
I recommend switching to **YOLOv11** or **YOLOv12** (if available). 
- It is designed for real-time mobile/web performance.
- It can detect 50+ flowers in a single frame in milliseconds.

#### 3. Backend API Update
The response format must change from a single object to a list of detections:
```json
{
  "detections": [
    { "label": "Rose", "box": [10, 20, 100, 150], "conf": 0.98 },
    { "label": "Tulip", "box": [200, 50, 80, 120], "conf": 0.85 }
  ]
}
```

#### 4. Frontend "Live Lens" Implementation
- **Real-time Loop**: Instead of a "Shutter button," the `FlowerScanner.tsx` will use a `setInterval` to send a frame every 300-500ms.
- **Bounding Box Overlay**: Add a transparent `<canvas>` over the `<video>` element. When the backend sends coordinates, use Javascript `ctx.strokeRect()` to draw boxes around the flowers in real-time.

---

## 4. Google Lens Implementation Strategy

To make it feel exactly like Google Lens:

1.  **Continuous Scanning**: Use Web Workers to process frames in the background so the UI never lags.
2.  **Smooth Tracking**: Implement a simple "Centroid Tracker" on the frontend. If a flower moves slightly, the box should follow it smoothly rather than flickering.
3.  **Interactive Dots**: Instead of just boxes, place "pulsing dots" on the flowers. When the user taps a dot, it expands to show details.

---

> [!TIP]
> **Low-Code Shortcut**: If re-labeling thousands of images with bounding boxes sounds too difficult, you can use **Auto-Labeling**. Use a pre-trained model like CLIP or a generic YOLO model to "suggest" boxes, and then you just verify them.

**Would you like me to start by preparing a "Multi-label" version of the current model (no boxes, just listing all flowers seen) or go straight to the Object Detection (YOLO) plan?**
