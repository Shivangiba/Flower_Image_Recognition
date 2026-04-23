# ============================================================
# main.py — FastAPI Backend Server
#
# This server acts as the bridge between the React frontend and 
# the PyTorch deep learning model. It handles image processing,
# binary encoding, and performance monitoring.
#
# CORE STACK:
# - FastAPI: High-performance async web framework.
# - Pydantic: Data validation for API requests.
# - model_loader: Custom module that wraps the EfficientNet-B0 model.
# ============================================================

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import time
from fastapi.staticfiles import StaticFiles
import os

# Internal import for the prediction logic (wrapping PyTorch/EfficientNet-B0)
from model_loader import predict

# ------------------------------------------------------------
# INITIALIZE FASTAPI APP
# ------------------------------------------------------------
app = FastAPI(
    title="FlowerAI Neural API",
    description="EfficientNet-B0 flower classification node — Optimized for 13 species",
    version="2.0.0"
)

# ------------------------------------------------------------
# CORS MIDDLEWARE
# 
# Critical for development: Allows the Next.js frontend (Port 3000)
# to communicate with this backend (Port 8000) without browser blocks.
# ------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # Development: allow all. Production: restrict to frontend URL.
    allow_methods=["*"],    # Allow GET, POST, OPTIONS, etc.
    allow_headers=["*"],
)

# ------------------------------------------------------------
# HEALTH CHECK
# GET /
# Used for heartbeat monitoring and cloud deployment readiness.
# ------------------------------------------------------------
@app.get("/")
def health_check():
  return {
    "status": "online",
    "model": "EfficientNet-B0",
    "classes": 13,
    "timestamp": time.time(),
    "node": "primary-vision-lab"
  }

# ------------------------------------------------------------
# MULTIPART IMAGE PREDICTION
# POST /predict
#
# Handles traditional file uploads (drag-n-drop/file selector).
# Efficient for high-resolution images sent from the browser.
# ------------------------------------------------------------
@app.post("/predict")
async def predict_flower(file: UploadFile = File(...)):
  """
  Receives a raw image file, validates it, and runs the neural engine.
  """
  # Security: Restrict to common image formats
  allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/webp"]
  if file.content_type not in allowed_types:
    raise HTTPException(
      status_code=400,
      detail=f"Unsupported format. AI requires: JPG, PNG, or WEBP."
    )

  # Asynchronous read to prevent blocking the worker thread
  image_bytes = await file.read()

  if len(image_bytes) == 0:
    raise HTTPException(status_code=400, detail="Null payload received.")

  # Execute Neural Inference
  start_time = time.time()
  try:
    result = predict(image_bytes)
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Inference Engine Error: {str(e)}")

  # Calculate latency for frontend performance monitoring
  processing_time = round((time.time() - start_time) * 1000)

  return {
    "predicted": result["predicted"],
    "confidence": result["confidence"],
    "top5": result["top5"],
    "processing_time_ms": processing_time,
    "filename": file.filename
  }

# ------------------------------------------------------------
# BASE64 IMAGE PREDICTION
# POST /predict-base64
#
# Optimized for the "Live Scanner" (WebRTC frames).
# Browser canvas snapshots are natively base64; sending them directly
# saves memory and reduces serialization overhead.
# ------------------------------------------------------------
class Base64Request(BaseModel):
  image: str # The encoded string (includes data:image/jpeg;base64 prefix)

@app.post("/predict-base64")
async def predict_flower_base64(request: Base64Request):
  """
  Decodes a base64 frame from the live scanner and runs prediction.
  """
  try:
    image_data = request.image
    # Strip the Data-URL metadata prefix if the browser includes it
    if "," in image_data:
      image_data = image_data.split(",")[1]

    # Convert base64 string back to binary pixel data for the model
    image_bytes = base64.b64decode(image_data)
  except Exception:
    raise HTTPException(status_code=400, detail="Malformed base64 sequence.")

  # Execute Neural Inference
  start_time = time.time()
  try:
    result = predict(image_bytes)
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Inference Engine Error: {str(e)}")

  processing_time = round((time.time() - start_time) * 1000)

  return {
    "predicted": result["predicted"],
    "confidence": result["confidence"],
    "top5": result["top5"],
    "processing_time_ms": processing_time
  }

# ------------------------------------------------------------
# STATIC ASSETS & METRICS
#
# Serves training logs and evaluation plots (Confusion Matrix, Loss curves)
# ------------------------------------------------------------
RESULTS_BASE = os.path.abspath(os.path.join(os.getcwd(), "..", "Flower_Image_Recognition_Modal", "results"))
METRICS_PATH = os.path.join(RESULTS_BASE, "metrices", "classification_report.txt")
PLOTS_DIR = os.path.join(RESULTS_BASE, "plots")

# Expose the training plots directory as static assets accessible via URL
if os.path.exists(PLOTS_DIR):
  app.mount("/plots", StaticFiles(directory=PLOTS_DIR), name="plots")

@app.get("/metrics")
async def get_metrics():
  """
  Aggregates final model validation metrics for the frontend stats page.
  """
  # Base performance data (from local test set evaluation)
  metrics = {
    "accuracy": 94.32,
    "f1_score": 0.9434,
    "precision": 0.9452,
    "recall": 0.9432,
    "classes": 13,
    "confusion_matrix_url": "/plots/confusion_matrix.png",
    "training_history_url": "/plots/training_history.png",
    "per_class_f1_url": "/plots/per_class_f1.png"
  }
  
  # Inject raw text classification report if available on disk
  if os.path.exists(METRICS_PATH):
    try:
      with open(METRICS_PATH, "r") as f:
        metrics["report_raw"] = f.read()
    except Exception:
      pass
      
  return metrics
