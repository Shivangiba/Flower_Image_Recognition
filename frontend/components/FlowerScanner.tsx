'use client'

/**
 * FlowerScanner Component
 * 
 * A Google Lens-style live camera interface designed for automated flower recognition.
 * It provides a real-time viewfinder, scanning animations, and frame capture logic.
 */

import React, { useState, useRef, useEffect, useCallback } from 'react'
import { X, RefreshCcw, Camera, AlertCircle, Loader2 } from 'lucide-react'
import styles from './FlowerScanner.module.css'

interface FlowerScannerProps {
  onCapture: (file: File) => void // Callback when image is captured
  onClose: () => void           // Callback when scanner is closed
}

const FlowerScanner: React.FC<FlowerScannerProps> = ({ onCapture, onClose }) => {
  // State for camera management
  const [stream, setStream] = useState<MediaStream | null>(null)
  const [facingMode, setFacingMode] = useState<'user' | 'environment'>('environment') // Toggle between front/back
  const [error, setError] = useState<string | null>(null)
  
  // State for UI feedback
  const [isCapturing, setIsCapturing] = useState(false)
  const [showFlash, setShowFlash] = useState(false)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  
  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)

  /**
   * Stops all active camera tracks to release the hardware.
   * Crucial for battery life and privacy.
   */
  const stopTracks = useCallback(() => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop())
      setStream(null)
    }
  }, [stream])

  /**
   * Initializes the camera stream using navigator.mediaDevices.getUserMedia.
   * Requests 720p resolution for high-fidelity scanning without lag.
   */
  const startCamera = useCallback(async () => {
    stopTracks() // Clear any existing stream before starting new one
    setError(null)

    const constraints: MediaStreamConstraints = {
      video: {
        facingMode, // "environment" uses the rear camera (ideal for flowers)
        width: { ideal: 1280 },
        height: { ideal: 720 }
      }
    }

    try {
      // Validate browser support for camera APIs
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        throw new Error('Live scanning requires a secure connection (HTTPS) and a modern browser.')
      }

      const newStream = await navigator.mediaDevices.getUserMedia(constraints)
      setStream(newStream)
      
      // Attach the stream to our video element
      if (videoRef.current) {
        videoRef.current.srcObject = newStream
      }
    } catch (err: any) {
      console.error('Camera access error:', err)
      // Map specific browser errors to user-friendly messages
      if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
        setError('Camera access denied. Please allow camera permissions in your browser settings.')
      } else {
        setError(err.message || 'Could not access camera. Please try again.')
      }
    }
  }, [facingMode, stopTracks])

  // Re-start camera whenever the facing mode (front/back) changes
  useEffect(() => {
    startCamera()
    return () => stopTracks() // Cleanup on component unmount
  }, [facingMode])

  const toggleCamera = () => {
    setFacingMode(prev => prev === 'user' ? 'environment' : 'user')
  }

  /**
   * Core logic for freezing the frame and converting it to a usable image.
   * 1. Draws the current frame from the <video> to a hidden <canvas>.
   * 2. Triggers a UI flash animation.
   * 3. Converts canvas content to a JPEG Blob.
   * 4. Passes the Blob as a File object to the parent component.
   */
  const captureImage = async () => {
    if (!videoRef.current || !canvasRef.current || isCapturing) return

    setIsCapturing(true)
    setShowFlash(true) // Trigger the white flash overlay

    // Clear flash after 300ms
    setTimeout(() => setShowFlash(false), 300)

    const video = videoRef.current
    const canvas = canvasRef.current
    const context = canvas.getContext('2d')

    if (context) {
      // Synchronize canvas dimensions with the actual video feed resolution
      canvas.width = video.videoWidth
      canvas.height = video.videoHeight
      
      // Draw the exact current pixel data from video onto canvas
      context.drawImage(video, 0, 0, canvas.width, canvas.height)
      
      // Show "Analyzing..." spinner to give the user time to realize capture happened
      setIsAnalyzing(true)
      
      // Artificial delay (500ms) for UX - makes the "scan" feel more scientific
      setTimeout(() => {
        canvas.toBlob((blob) => {
          if (blob) {
            // Package the blob as a standard JS File object
            const file = new File([blob], `scan_${Date.now()}.jpg`, { type: 'image/jpeg' })
            onCapture(file) // Send back to PredictPage
            stopTracks()    // Release camera immediately after success
          }
          setIsAnalyzing(false)
          setIsCapturing(false)
        }, 'image/jpeg', 0.92) // 92% quality offers best balance of speed and clarity
      }, 500)
    }
  }

  return (
    <div className={styles.modalOverlay}>
      {/* Navigation Controls */}
      <button className={styles.closeBtn} onClick={onClose} aria-label="Close scanner">
        <X size={24} />
      </button>

      <div className={styles.videoContainer}>
        {error ? (
          // Error State: Displayed if camera fails
          <div className={styles.errorMessage}>
            <AlertCircle size={48} color="#ba6e8f" className="mx-auto mb-4" />
            <p className="font-bold text-lg">{error}</p>
            <p className="mt-4 text-sm opacity-70">Make sure you are using HTTPS and have granted permission.</p>
          </div>
        ) : (
          <>
            {/* Live Feed: The core camera view */}
            <video 
              ref={videoRef} 
              autoPlay 
              playsInline 
              className={styles.videoFeed}
            />
            
            {/* Scanner Overlays: Purely visual elements for the "AI Lens" look */}
            <div className={styles.scannerOverlay}>
              <div className={styles.label}>
                <i>Point at a flower to scan</i>
              </div>
              
              <div className={styles.scanFrame}>
                {/* Viewfinder Corners (Pulsing via CSS) */}
                <div className={`${styles.corner} ${styles.topLeft}`} />
                <div className={`${styles.corner} ${styles.topRight}`} />
                <div className={`${styles.corner} ${styles.bottomLeft}`} />
                <div className={`${styles.corner} ${styles.bottomRight}`} />
                
                {/* The "Laser" Scan Line (Moving via CSS) */}
                <div className={styles.scanLine} />
              </div>
            </div>

            {/* Switch Camera Button */}
            <button className={styles.flipBtn} onClick={toggleCamera} aria-label="Flip camera">
              <RefreshCcw size={24} />
            </button>

            {/* Capture Shutter Button */}
            <div className={styles.controls}>
              <button 
                className={styles.shutterBtn} 
                onClick={captureImage}
                disabled={isCapturing || !!error}
                aria-label="Capture flower"
              >
                <div className={styles.shutterInner} />
              </button>
            </div>
          </>
        )}
      </div>

      {/* Hidden processing canvas */}
      <canvas ref={canvasRef} style={{ display: 'none' }} />
      
      {/* Visual Feedback Animations */}
      {showFlash && <div className={`${styles.flashOverlay} ${styles.flashActive}`} />}
      
      {isAnalyzing && (
        <div className={styles.loadingOverlay}>
          <div className={styles.spinner} />
          <p className="font-black text-brand-secondary uppercase tracking-widest animate-pulse">Analyzing...</p>
        </div>
      )}
    </div>
  )
}

export default FlowerScanner
