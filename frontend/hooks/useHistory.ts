/**
 * useHistory Hook
 * 
 * Manages the persistence and retrieval of local scan data. 
 * Enables the "Recent Discovered Flowers" registry.
 */

'use client'
import { useState, useEffect } from 'react'

/**
 * RunHistory Interface
 * Defines the structure for each botanical scan captured.
 */
export interface RunHistory {
  id: string        // Unique record ID (UUID format)
  flowerName: string // Top prediction from the model
  confidence: number // Confidence % (0-100)
  timestamp: string // ISO string for chronological sorting
  imagePath: string // Data URL / Local Blob URL for preview
}

/**
 * Main History Logic Hook
 * Synchronizes React state with local browser storage.
 */
export function useHistory() {
  const [history, setHistory] = useState<RunHistory[]>([])

  /**
   * Loads historical data from localStorage on first-load.
   * This allows the discovery record to persist even after browser refreshes.
   */
  useEffect(() => {
    // Unique key to prevent collision with other web apps on localhost
    const stored = localStorage.getItem('flower_history')
    if (stored) {
      try {
        setHistory(JSON.parse(stored))
      } catch (e) {
        console.error('Failed to parse scan history', e)
      }
    }
  }, [])

  /**
   * Adds a new scan log to the registry.
   * Prepends to the list so most recent discovery appears first.
   */
  const addEntry = (entry: RunHistory) => {
    const updated = [entry, ...history]
    setHistory(updated)
    // Persist to browser memory
    localStorage.setItem('flower_history', JSON.stringify(updated))
  }

  /**
   * Permanently deletes a specific scan entry from the local record.
   */
  const deleteEntry = (id: string) => {
    const updated = history.filter((e) => e.id !== id)
    setHistory(updated)
    // Synchronize local storage with the filtered set
    localStorage.setItem('flower_history', JSON.stringify(updated))
  }

  /**
   * Wipes the entire discovery registry.
   * Irreversible action.
   */
  const clearHistory = () => {
    setHistory([])
    localStorage.removeItem('flower_history')
  }

  // Expose methods and state to high-level components (HistoryPage, PredictPage)
  return { history, addEntry, deleteEntry, clearHistory }
}
