# 🌸 Flower Image Recognition — Project Summary

This document provides a comprehensive technical overview of the Flower Image Recognition project, covering the model architecture, data pipeline, training configuration, and performance results.

---

## 1. 📌 Project Overview
*   **Project Name**: Flower Image Recognition
*   **Goal**: To build a robust deep learning system capable of identifying various flower species from digital images with high precision.
*   **Problem Statement**: Automating the classification of 13 specific flower species (primarily common in South Asia/Bangladesh) to assist in botanical research or consumer-grade flower identification apps.
*   **Type of Task**: Multi-class Image Classification (13 classes).
*   **Dataset**:
    *   **Name**: data_combined (Custom Dataset)
    *   **Total Images**: 8,100
    *   **Number of Classes**: 13
    *   **Split**: Stratified split (70% Train, 15% Validation, 15% Test)
        *   **Train**: 5,670 images
        *   **Validation**: 1,215 images
        *   **Test**: 1,215 images

---

## 2. 🏗️ Model Architecture
*   **Model Type**: Transfer Learning with Fine-tuning.
*   **Base Model**: **EfficientNet-B0** (Pre-trained on ImageNet-1K).
*   **Architecture Breakdown**:
    *   **Backbone**: EfficientNet-B0 (1280-dimensional feature vector).
    *   **Internal Hidden Architecture**: EfficientNet-B0 consists of **9 Stages** of processing:
        - **Stage 1**: $3 \times 3$ Initial Convolution (32 output channels).
        - **Stages 2-8**: **16 MBConv** (Mobile Inverted Bottleneck Convolution) blocks that progressively expand and shrink features (Squeeze-and-Excitation).
        - **Stage 9**: $1 \times 1$ Conv + Global Average Pooling (the final feature bottleneck).
    *   **Key Design Principle**: **Compound Scaling** (Scaling depth, width, and resolution together for maximum efficiency).
    *   **Total Depth**: **237 layers** (including convolutions, batch normalization, and activations).
    *   **Hidden Layers in Head**: **0** (The head uses a direct mapping from 1,280 features to 13 output logits).
    *   **Why 0 Hidden Layers?**: A "linear probe" strategy was chosen because the EfficientNet-B0 backbone already extracts highly complex, non-linear features. Additional hidden layers in the classifier would increase the risk of overfitting on the specialized flower dataset.
    *   **Dropout Layer**: Probability $p=0.4$ to mitigate overfitting.
    *   **Classification Head**: A simple **torch.nn.Sequential** block containing:
        1.  **Dropout**: (0.4) — Randomly zeroes 40% of input elements.
        2.  **Linear Layer**: (1280 → 13) — Maps global average pooled features to class scores.
    *   **Activation**: Logits are converted to probabilities via **Softmax** during inference.
*   **Neuron Breakdown**:
    *   **Input Layer**: **150,528** neurons (224 × 224 × 3 RGB pixels).
    *   **Feature Bottleneck**: **1,280** neurons (Highest-level feature representation).
    *   **Output Layer**: **13** neurons (One per flower species).
*   **Parameter Count**:
    *   **Total Parameters**: ~5.3 Million
    *   **Trainable (Stage 1)**: 16,653 (Classifier Head only)
    *   **Trainable (Stage 2)**: 5.3 Million (Entire network unfrozen)
*   **Input Shape**: 224 × 224 × 3 (RGB)
*   **Output Classes**: 13

---

## 3. 🔧 Technical Stack
*   **Framework**: **PyTorch 2.x**
*   **Core Libraries**:
    *   `timm`: For state-of-the-art EfficientNet backbone.
    *   `torchvision`: For image transforms and utilities.
    *   `scikit-learn`: For stratified dataset splitting and performance metrics.
    *   `Pillow`: For image loading and preprocessing.
    *   `FastAPI`: For backend API serving.
    *   `Next.js`: For frontend user interface.
*   **Infrastructure**:
    *   **Python Version**: 3.9+
    *   **Hardware**: CUDA-enabled GPU (NVIDIA) recommended; CPU fallback supported.

---

## 4. 📊 Data Pipeline
*   **Preprocessing Steps**:
    1.  Resize to 224x224 (B0 requirement).
    2.  Conversion to RGB.
    3.  Normalization using ImageNet stats: Mean `[0.485, 0.456, 0.406]`, Std `[0.229, 0.224, 0.225]`.
*   **Data Augmentation (Training Only)**:
    *   `RandomResizedCrop`: Scale 0.7 to 1.0.
    *   `RandomHorizontalFlip`: $p=0.5$.
    *   `RandomVerticalFlip`: $p=0.2$.
    *   `RandomRotation`: $\pm 30$ degrees.
    *   `ColorJitter`: Randomly adjust brightness, contrast, saturation, and hue.
    *   `RandomGrayscale`: $p=0.1$.
*   **Configuration**:
    *   **Batch Size**: 16
    *   **Image Resolution**: 224 × 224
    *   **Data Loaders**: PyTorch `DataLoader` with $0$ workers (Windows safety).

---

## 5. ⚙️ Training Configuration
*   **Loss Function**: `CrossEntropyLoss` (Standard for multi-class).
*   **Optimizer**: `AdamW` (Weight decay $1 \times 10^{-4}$).
*   **Learning Rate Strategy**:
    *   **Stage 1 (Frozen Backbone)**: $1 \times 10^{-3}$ for 5 epochs.
    *   **Stage 2 (Fine-tuning)**: $1 \times 10^{-4}$ for up to 25 epochs.
*   **Metrics Tracked**: Accuracy, Loss, Per-class F1-Score, Confusion Matrix.
*   **Callbacks**:
    *   **ModelCheckpoint**: Saves weights to `best_model.pth` whenever validation accuracy improves.
    *   **EarlyStopping**: 10-epoch patience based on validation loss.
    *   **ReduceLROnPlateau**: Factor 0.5, Patience 3 epochs.

---

## 6. 📈 Model Performance
Based on the final test set evaluation (1,215 images):

| Metric | Measured Value |
| :--- | :--- |
| **Final Test Accuracy** | **94.32%** |
| **Macro F1-Score** | **0.9434** |
| **Macro Precision** | 0.9452 |
| **Macro Recall** | 0.9433 |

### Per-Class F1-Score Highlights:
*   **Top Performance**: **Sunflower (0.99)**, Marigold (0.97), Cosmos flower (0.97).
*   **Lowest Performance**: **Rose (0.85)** — noted for high visual variance in varieties.

---

## 7. 🗂️ Project Structure
```text
Flower_Image_Recognition/
├── Flower_Image_Recognition_Modal/   # Deep Learning Core
│   ├── src/                          # Modular source code
│   │   ├── config.py                 # Central configurations
│   │   ├── model.py                  # Architecture definition
│   │   ├── train.py                  # Training loops
│   │   └── evaluate.py               # Evaluation logic
│   ├── results/                      # Saved checkpoints/plots
│   ├── main.py                       # Orchestration script
│   └── eda.py                        # Data analysis script
├── backend/                          # FastAPI Web Server
│   └── main.py                       # API endpoints (/predict)
├── frontend/                         # Next.js Web App
│   └── app/                          # User interface pages
└── data_combined/                    # Raw Dataset (13 classes)
```

---

## 8. 🚀 Inference & Deployment
*   **Format**: Model weights are saved as PyTorch State Dict (`.pth`).
*   **Inference CLI**:
    ```powershell
    python main.py --mode predict --image "path/to/flower.jpg"
    ```
* **REST API**: FastAPI server providing a `/predict` endpoint for multipart images and `/predict-base64` for scanning. 
* **Frontend**: Next.js dashboard featuring the **"Neural Vision Lab"** with drag-and-drop, real-time **"Live Flower Scanner"** (Google Lens style), and dynamic history visualization.

---

## 10. 📸 Live Flower Scanner Architecture
The project now includes a high-performance, real-time flower scanning module inspired by Google Lens.
The Live Flower Scanner follows a sophisticated real-time processing pipeline:

🛠️ Technologies Used
Deep Learning Pipeline: EfficientNet-B0 (PyTorch) served via FastAPI.
Media Streaming: WebRTC (getUserMedia) for low-latency video feed.
Image Bridge: HTML5 Canvas API used as a high-performance frame buffer to "freeze" pixels without quality loss.
Animations: CSS3-driven scan-line and viewfinder-pulse animations for a state-of-the-art UX.
⚙️ Technical Flow 
The Stream: The frontend initializes a secure 1280x720 video feed, targeting the environment (rear) camera on mobile.
The Capture: When the user taps the shutter, the current video frame is instantly mapped 1:1 onto a hidden canvas element.
The Conversion: The canvas is serialized into a JPEG Blob (quality 0.92) and wrapped in a standard 

File
 object.
The Prediction: This file is passed to the Neural Vision Lab's ingestion pipeline. It follows a multi-part POST request to the FastAPI backend, where the EfficientNet-B0 model performs a single forward pass over the pixel matrix.
The Feedback: Within milliseconds, the API returns the top-5 species matches. These are rendered as dynamic, color-coded visual gauges and interactive treemaps.
The project is now fully documented with the latest features, ensuring clarity on both the AI and the web architectu

### 🛠️ Technology Stack (Scanner)
*   **WebRTC (`getUserMedia`)**: Used to capture the real-time video stream from the user's camera (supports both front/selfie and back/environment modes).
*   **HTML5 Canvas**: Acts as the bridge between video and image. It captures a high-resolution frame from the video track, applies visual logic (like aspect ratio correction), and converts it to a `Blob` (image/jpeg).
*   **Lucide React**: Provides the vector-based iconography for the scanner UI (camera, flip, close, scan).
*   **CSS3 Animations**: Power the scanning frame pulse, the vertical scan line, and the shutter flash for a premium UX feel.

### ⚙️ Implementation Flow
1.  **Initialization**: User clicks "SCAN FLOWER", triggering the `FlowerScanner` modal. The app requests camera permissions and initializes a 1280x720 video feed.
2.  **Viewfinder**: A custom overlay displays a "scanning frame" with pulsing corners and a moving laser line.
3.  **Capture**: When the shutter is pressed, the current video frame is drawn onto a hidden canvas. A white flash animation provides immediate visual feedback.
4.  **Processing**: The canvas image is converted to a `Blob`, then wrapped in a standard JavaScript `File` object.
5.  **Pipeline Integration**: The file is passed back to the main `PredictPage` state, updating the preview area.
6.  **Inference**: The file is automatically sent to the `/predict-base64` or `/predict` backend endpoint. The model (EfficientNet-B0) processes the pixel matrix and returns the top 5 predictions and confidence scores.
7.  **Result Rendering**: The UI dynamically updates the Results Panel with a confidence gauge and probability distribution chart.

---

11. 📊 Data Export Protocol (CSV Engine)
The application includes a zero-dependency, client-side data export system for scan registries.

### 🛠️ Technology Stack (Export)
*   **Blob (Binary Large Object)**: An immutable object representing raw data. It stores the CSV-serialized string in the browser's memory without requiring a server-side file system.
*   **URL.createObjectURL**: Creates a transient URL (a "pointer") that allows the browser's download manager to address the memory block.
*   **Programmatic Anchor Injection**: A dynamically-created `<a>` element with the `download` attribute is used to force-trigger the device's native download dialog.
*   **DOM Lifecycle Cleanup**: Immediate invocation of `URL.revokeObjectURL` and `document.body.removeChild` ensures no memory leaks are left in the browser.

### ⚙️ Implementation Components
| Component | Role | Technical Implementation |
| :--- | :--- | :--- |
| **Data Format** | Universal Standard | Comma Separated Values (CSV) with UTF-8 encoding |
| **Storage Bridge** | Memory Object | **`Blob` API** encapsulates the raw string |
| **Download Link** | Transience | Virtual Anchor (`<a>`) with the `download` attribute |
| **Trigger Agent** | Programmatic | Native `.click()` invocation on the hidden element |

---

## 12. ⚠️ Challenges & Observations
*   **No Overfitting**: Validation loss remained lower than training loss in Stage 1, indicating excellent generalization.
*   **Rose Variance**: The Rose class remains the most challenging due to its diverse petal shapes and colors compared to highly distinct species like Sunflowers.
*   **Environment Rigidity**: Early versions had hardcoded Windows paths; these were refactored to use dynamic `os.path` for portability.
*   **Windows Multiprocessing**: PyTorch `num_workers > 0` caused crashes on Windows, resolved by pinning to `0`.
*   **Registry Memory Safety**: Fixed a React initialization bug where empty image paths caused redundant network requests; added stylized flower placeholders for legacy data entries.
*   **Code Documentation**: Standardized on JSDoc-style comments for the `FlowerScanner` module to improve maintainability and technical clarity.
*   **Data Portability**: Integrated a "Protocol Export" system allowing users to download their scan history as locally-browsable CSV files.
*   **Visual Insights**: Replaced mock data in the `HistoryChart` with real-time confidence trend analysis from the `useHistory` local state.

---

## 10. 🔮 Future Improvements
1.  **Weighted Loss**: Implementing weighted CrossEntropy to boost performance on "difficult" classes like Rose.
2.  **ONNX Export**: Converting the model to ONNX format for faster browser-side or mobile inference.
3.  **TTA (Test-Time Augmentation)**: Implementing TTA during inference to gain an estimated 0.5–1% accuracy boost.
4.  **Mixed Precision**: Enabling `torch.cuda.amp` to halve training time on RTX series GPUs.
