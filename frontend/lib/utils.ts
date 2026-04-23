import { DateTime } from "luxon";

/**
 * Utility Service Module
 * 
 * Provides global helper functions for the entire frontend application. 
 * Centralizing these logic snippets ensures consistency across separate pages.
 */

/**
 * timeAgo (Relative Date Formatter)
 * 
 * Converts an ISO 8601 timestamp into a human-readable "relative" format 
 * (e.g., "5 minutes ago", "2 hours ago").
 * 
 * Uses 'luxon' for high-precision time zone mapping.
 */
export function timeAgo(isoString: string): string {
  return DateTime.fromISO(isoString).toRelative() ?? "Unknown time";
}

/**
 * fullDateTime (Localized Date Formatter)
 * 
 * Returns a full localized date and time string (e.g., "Oct 24, 2023, 10:30 PM").
 */
export function fullDateTime(isoString: string): string {
  return DateTime.fromISO(isoString).toLocaleString(DateTime.DATETIME_MED);
}

/**
 * toBase64 (Image Pipeline Bridge)
 * 
 * High-performance converter to transform a browser 'File' object into a base64 string.
 * This is essential for:
 * 1. Sending image data to the /predict-base64 API endpoint as JSON.
 * 2. Visualizing selected images before they are sent to the model.
 * 
 * @param file - The raw File object from an <input type="file">
 * @returns - A promise resolving to the base64-encoded pixel string (data-prefix removed)
 */
export function toBase64(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const result = reader.result as string;
      // Extract only the base64 string (discard the "data:image/jpeg;base64," prefix)
      // This allows the model server to decode it directly using standard libraries.
      resolve(result.split(",")[1]);
    };
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}
