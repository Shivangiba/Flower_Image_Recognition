/**
 * API Service Module
 * 
 * Handles all communication between the Next.js frontend and the FastAPI backend.
 * Uses standard fetch API with async/await for predictable network management.
 */

// Centralized API Base URL (Supports environment variables for production deployment)
const BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

/**
 * Interface representing a single inference result (class + confidence)
 */
export interface Prediction {
  class: string
  probability: number
}

/**
 * Interface representing the full response from the /predict endpoints
 */
export interface PredictResponse {
  predicted: string         // The top-1 class name
  confidence: number        // The confidence percentage (0-100)
  top5: Prediction[]       // List of top 5 most likely classes
  processing_time_ms: number // Server-side inference time
  filename: string          // Name of the processed image
}

/**
 * Standard Image Upload Prediction
 * Sends a raw binary file using multipart/form-data.
 */
export async function predictFlower(file: File): Promise<PredictResponse> {
  const formData = new FormData()
  formData.append('file', file)

  const res = await fetch(`${BASE}/predict`, {
    method: 'POST',
    body: formData,
  })

  // Basic error handling for server outages or model failures
  if (!res.ok) {
    const err = await res.json()
    throw new Error(err.detail || 'Prediction failed')
  }

  return res.json()
}

/**
 * Base64 Image Prediction
 * Sends a base64 encoded string as JSON.
 * High-speed alternative for webcam scanning frames.
 */
export async function predictFlowerBase64(base64Image: string): Promise<PredictResponse> {
  const res = await fetch(`${BASE}/predict-base64`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image: base64Image }),
  })

  if (!res.ok) {
    const err = await res.json()
    throw new Error(err.detail || 'Base64 prediction failed')
  }

  return res.json()
}

/**
 * Performance Metrics Data
 */
export interface MetricsResponse {
  accuracy: number
  f1_score: number
  precision: number
  recall: number
  classes: number
  confusion_matrix_url: string
  training_history_url: string
  per_class_f1_url: string
  report_raw?: string
}

/**
 * Fetches the global model training metrics and evaluation plots.
 */
export async function getMetrics(): Promise<MetricsResponse> {
  const res = await fetch(`${BASE}/metrics`, { cache: 'no-store' })
  if (!res.ok) throw new Error('Could not fetch model metrics')
  const data = await res.json()
  
  // Normalize URLs to ensure they point to the backend server assets
  return {
    ...data,
    confusion_matrix_url: `${BASE}${data.confusion_matrix_url}`,
    training_history_url: `${BASE}${data.training_history_url}`,
    per_class_f1_url: `${BASE}${data.per_class_f1_url}`,
  }
}

/**
 * Simple Health Check
 * Used by the UI to show connection status or node readiness.
 */
export async function checkHealth(): Promise<boolean> {
  try {
    const res = await fetch(`${BASE}/`, { cache: 'no-store' })
    return res.ok
  } catch {
    return false
  }
}