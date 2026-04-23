export interface Prediction {
  class: string
  probability: number
}

export interface PredictResponse {
  predicted: string
  confidence: number
  top5: Prediction[]
  processing_time_ms: number
  filename: string
}