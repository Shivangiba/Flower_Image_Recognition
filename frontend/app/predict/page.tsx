'use client'
import { useState, useCallback, useRef, useEffect } from 'react'
import Swal from 'sweetalert2'
import PredictionChart from '@/components/charts/PredictionChart'
import ConfidenceGauge from '@/components/charts/ConfidenceGauge'
import { predictFlowerBase64, PredictResponse } from '@/lib/api'
import { toBase64 } from '@/lib/utils'
import { Tooltip } from '@/components/ui/Tooltip'
import { useHistory } from '@/hooks/useHistory'
import { Info, Sparkles, Zap, ShieldCheck, Microscope, Loader2, UploadCloud, CheckCircle2, RefreshCw, Camera } from 'lucide-react'
import { FLOWER_DESCRIPTIONS } from '@/lib/constants'
import AOS from 'aos'
import 'aos/dist/aos.css'
import FlowerScanner from '@/components/FlowerScanner'

export default function PredictPage() {
  const [file, setFile]             = useState<File | null>(null)
  const [preview, setPreview]       = useState<string | null>(null)
  const [result, setResult]         = useState<PredictResponse | null>(null)
  const [isPredicting, setIsPredicting] = useState(false)
  const [dragOver, setDragOver]     = useState(false)
  const [showScanner, setShowScanner] = useState(false)
  
  const fileInputRef = useRef<HTMLInputElement>(null)
  const { addEntry } = useHistory()

  // Refresh AOS when dynamically rendered results appear
  useEffect(() => {
    AOS.init({ duration: 1000, once: true })
  }, [])

  useEffect(() => {
    if (result) {
      AOS.refresh()
    }
  }, [result])


  // Clean up preview URL on unmount to prevent leaks
  useEffect(() => {
    return () => {
      if (preview && preview.startsWith('blob:')) {
        URL.revokeObjectURL(preview)
      }
    }
  }, [preview])

  const handleFile = useCallback((f: File) => {
    console.log('File detected:', f.name, f.type)
    
    if (!f.type.startsWith('image/')) {
      Swal.fire({
        title: 'Input Error',
        text: 'Please select a valid image file (JPG, PNG, or WEBP).',
        icon: 'error',
        background: '#0C0420',
        color: '#FFFFFF',
        confirmButtonColor: '#BA6E8F',
      })
      return
    }

    // Set file state
    setFile(f)
    setResult(null)
    
    // Create preview
    const reader = new FileReader()
    reader.onloadend = () => {
      setPreview(reader.result as string)
    }
    reader.readAsDataURL(f)
  }, [])

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setDragOver(false)
    const f = e.dataTransfer.files[0]
    if (f) handleFile(f)
  }

  const triggerFileInput = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click()
    }
  }

  const handlePredict = useCallback(async (overridingFile?: File) => {
    const fileToPredict = overridingFile || file
    if (!fileToPredict) return

    setIsPredicting(true)
    
    Swal.fire({
      title: 'Neural Link Active',
      html: '<div class="flex flex-col items-center gap-4"><div class="w-10 h-10 border-2 border-brand-primary border-t-transparent rounded-full animate-spin"></div><p>Decoding pixel matrices...</p></div>',
      showConfirmButton: false,
      allowOutsideClick: false,
      background: '#0C0420',
      color: '#FFFFFF'
    })

    try {
      const base64 = await toBase64(fileToPredict)
      const data = await predictFlowerBase64(base64)
      
      setResult(data)
      
      addEntry({
        id: crypto.randomUUID(),
        flowerName: data.predicted,
        confidence: data.confidence,
        timestamp: new Date().toISOString(),
        imagePath: preview || '',
      })

      Swal.close()
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Visual node failure.'
      Swal.fire({
        title: 'Network Error',
        text: message,
        icon: 'error',
        background: '#0C0420',
        color: '#FFFFFF'
      })
    } finally {
      setIsPredicting(false)
    }
  }, [file, preview, addEntry])

  /**
   * handleScanComplete (Callback from FlowerScanner)
   * 
   * Orchestrates the final result delivery after a live scan:
   * 1. Closes the camera modal.
   * 2. Sets the captured File to state (updating simple display).
   * 3. Triggers the prediction pipeline automatically (same as Select Image).
   */
  const handleScanComplete = (f: File) => {
    setShowScanner(false)
    handleFile(f) // Handles preview and file state
    
    // Explicitly call handlePredict with the fresh file immediately
    // This allows the AI analysis to start without waiting for React state update
    setTimeout(() => {
      handlePredict(f)
    }, 100)
  }

  const reset = () => {
    setFile(null)
    setPreview(null)
    setResult(null)
  }

  return (
    <div className="max-w-7xl mx-auto space-y-12 pb-24 relative overflow-hidden">
      
      <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-brand-primary/5 blur-[150px] rounded-full -z-10" />

      <div className="text-center pt-8">
        <h1 className="text-7xl font-black text-white mb-6 uppercase italic tracking-tighter">
          Neural <span className="text-gradient">Vision</span> Lab
        </h1>
        <div className="flex justify-center gap-6">
           <span className="flex items-center gap-2 px-4 py-1.5 rounded-full glass border-white/5 text-[9px] font-black tracking-widest text-brand-secondary uppercase">
             <ShieldCheck className="w-4 h-4" /> Node: Primary
           </span>
           <span className="flex items-center gap-2 px-4 py-1.5 rounded-full glass border-white/5 text-[9px] font-black tracking-widest text-brand-secondary uppercase">
             <RefreshCw className="w-4 h-4 text-brand-primary animate-spin-slow" /> Latency: 42ms
           </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 relative z-10">

        {/* INPUT BOX */}
        <div className="lg:col-span-5 space-y-8">
          
          <div className="glass-floral rounded-[3.5rem] p-10 border-white/10 relative shadow-2xl overflow-hidden group">
            <h2 className="text-2xl font-black text-white italic tracking-tight flex items-center gap-4 mb-8 text-gradient">
              <Microscope className="w-8 h-8" />
              Capture Module
            </h2>

            <div
              onDrop={handleDrop}
              onDragOver={(e) => { e.preventDefault(); setDragOver(true) }}
              onDragLeave={() => setDragOver(false)}
              className={`relative rounded-[3rem] border-2 border-dashed transition-all duration-500 overflow-hidden h-[460px] flex items-center justify-center
                ${dragOver ? 'border-brand-primary bg-brand-primary/5 scale-[1.02]' : 'border-white/5 bg-black/20'}
                ${preview ? 'border-none' : ''}`}
            >
              {preview ? (
                <div className="absolute inset-0">
                  <img src={preview} alt="Preview" className="w-full h-full object-cover" />
                  <div className="absolute inset-0 bg-gradient-to-t from-brand-dark via-transparent to-transparent opacity-90" />
                  <div className="absolute bottom-8 left-0 w-full px-8">
                     <div className="glass p-4 rounded-3xl border-white/10 flex items-center gap-4 animate-in slide-in-from-bottom-5">
                        <CheckCircle2 className="w-6 h-6 text-brand-primary" />
                        <div className="min-w-0">
                           <p className="text-[10px] font-black text-brand-secondary uppercase tracking-widest">Signal Locked</p>
                           <p className="text-white font-bold text-sm truncate">{file?.name}</p>
                        </div>
                     </div>
                  </div>
                </div>
              ) : (
                <div className="flex flex-col items-center gap-8 text-center p-12">
                   <div className="w-24 h-24 rounded-[2.5rem] bg-brand-primary/10 flex items-center justify-center text-5xl">🌸</div>
                   <div className="space-y-3">
                      <p className="text-3xl font-black text-white italic tracking-tight uppercase">Upload Sample</p>
                      <p className="text-gray-500 text-sm font-bold opacity-70">Drag botanical data here</p>
                   </div>
                </div>
              )}
            </div>

            <div className="mt-10 flex flex-col gap-4">
              <input 
                type="file" 
                ref={fileInputRef}
                className="hidden" 
                accept="image/*" 
                onChange={(e) => {
                  const f = e.target.files?.[0]
                  if (f) handleFile(f)
                }} 
              />
              
              {!preview ? (
                <div className="flex flex-col gap-4">
                  <button
                    type="button"
                    onClick={triggerFileInput}
                    className="w-full py-5 btn-primary rounded-[2rem] font-black text-xl tracking-tighter uppercase italic shadow-2xl flex items-center justify-center gap-4 transition-all active:scale-95"
                  >
                    <UploadCloud className="w-6 h-6" />
                    SELECT IMAGE
                  </button>
                  {/* Option 2: Live AI Scanner (WebRTC) */}
                  <button
                    type="button"
                    onClick={() => setShowScanner(true)}
                    className="w-full py-5 btn-scan rounded-[2rem] font-black text-xl tracking-tighter uppercase italic shadow-2xl flex items-center justify-center gap-4 transition-all active:scale-95 animate-scan-pulse"
                  >
                    <Camera className="w-6 h-6" />
                    SCAN FLOWER
                  </button>
                </div>
              ) : (
                <div className="space-y-4">
                  <button
                    onClick={() => handlePredict()}
                    disabled={isPredicting}
                    className="w-full py-5 btn-primary rounded-[2rem] font-black text-xl tracking-tighter uppercase italic shadow-2xl disabled:opacity-30 flex items-center justify-center gap-4 transition-all"
                  >
                    {isPredicting ? <Loader2 className="w-6 h-6 animate-spin" /> : <Zap className="w-6 h-6" />}
                    {isPredicting ? 'SCANNING...' : 'LAUNCH ANALYSIS'}
                  </button>
                  <button
                    onClick={reset}
                    className="w-full py-4 glass text-gray-500 rounded-2xl font-black text-xs uppercase tracking-[0.4em] hover:text-white transition-all"
                  >
                    RESET MODULE
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Scanner Modal */}
        {showScanner && (
          <FlowerScanner 
            onCapture={handleScanComplete}
            onClose={() => setShowScanner(false)}
          />
        )}

        {/* RESULTS AREA */}
        <div className="lg:col-span-7 space-y-10">
          {result ? (
            <div className="space-y-10 animate-in fade-in duration-1000">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                   <div className="glass-floral p-10 rounded-[3.5rem] border-white/10 flex flex-col justify-between min-h-[320px] shadow-2xl overflow-hidden relative">
                      <div>
                         <div className="px-5 py-2 rounded-full bg-brand-primary/10 border border-brand-primary/20 inline-block text-[10px] font-black text-brand-secondary uppercase tracking-[0.3em] mb-10">Result Found</div>
                         <h2 className="text-6xl font-black text-white italic uppercase tracking-tighter leading-none mb-4">{result.predicted}</h2>
                      </div>
                      <div className="pt-10 border-t border-white/5 flex justify-between items-center text-[10px] font-black uppercase text-gray-700">
                         <span>PROCESS TIME</span>
                         <span className="text-brand-primary">{result.processing_time_ms} MS</span>
                      </div>
                   </div>
                   <div className="glass p-10 rounded-[3.5rem] border-white/10 flex items-center justify-center min-h-[320px] shadow-2xl relative">
                      <ConfidenceGauge confidence={result.confidence} />
                   </div>
                </div>

                <div className="glass p-10 md:p-14 rounded-[4rem] border-white/10 shadow-2xl relative">
                   <h3 className="text-2xl font-black text-white italic uppercase tracking-tighter mb-12 flex items-center gap-4">
                      <Sparkles className="w-8 h-8 text-brand-primary" />
                      Probability Distribution
                   </h3>
                   <div style={{ height: '360px' }} className="relative">
                      <PredictionChart data={result.top5} />
                   </div>
                </div>
            </div>

          ) : (
            <div className="glass rounded-[3.5rem] border-dashed border-white/10 flex flex-col items-center justify-center p-24 text-center gap-12 min-h-[700px] shadow-2xl relative overflow-hidden">
               <div className="relative">
                  <div className="w-32 h-32 rounded-[2.5rem] bg-white/2 border border-white/5 flex items-center justify-center text-6xl">📊</div>
                  <div className="absolute -inset-4 bg-brand-primary/5 blur-3xl rounded-full" />
               </div>
               <div className="space-y-5">
                  <h3 className="text-4xl font-black text-white italic tracking-tighter uppercase">No Signal</h3>
                  <p className="text-gray-400 text-lg font-bold max-w-sm mx-auto opacity-60">Upload a sample to initiate the neural vision phase.</p>
               </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}