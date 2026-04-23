'use client'
import { DateTime } from 'luxon'
import HistoryChart from '@/components/charts/HistoryChart'
import { Tooltip } from '@/components/ui/Tooltip'
import { useHistory } from '@/hooks/useHistory'
import Swal from 'sweetalert2'
import { Info, Download, Trash2, Search, Activity, BarChart3, Layers, Clock, Flower } from 'lucide-react'

export default function HistoryPage() {
  const { history, deleteEntry, clearHistory } = useHistory()

  const handleDelete = async (id: string, name: string) => {
    const result = await Swal.fire({
      title: 'Delete Entry?',
      text: `Are you sure you want to remove the ${name} scan from your history?`,
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#BA6E8F',
      cancelButtonColor: '#7B466A',
      confirmButtonText: 'Yes, delete it',
      background: '#0C0420',
      color: '#FFFFFF'
    })

    if (result.isConfirmed) {
      deleteEntry(id)
      Swal.fire({
        title: 'Deleted!',
        text: 'The record has been purged from the registry.',
        icon: 'success',
        background: '#0C0420',
        color: '#FFFFFF',
        timer: 1500,
        showConfirmButton: false
      })
    }
  }

  const handleExport = () => {
    if (history.length === 0) {
      Swal.fire({
        title: 'Export Error',
        text: 'Registry is currently empty. No data to export.',
        icon: 'error',
        background: '#0C0420',
        color: '#FFFFFF',
        confirmButtonColor: '#BA6E8F'
      })
      return
    }

    // Generate CSV content
    const headers = ['ID', 'Flower Name', 'Confidence (%)', 'Timestamp']
    const rows = history.map(item => [
      item.id,
      item.flowerName,
      item.confidence.toFixed(2),
      item.timestamp
    ])
    
    const csvContent = [headers, ...rows].map(e => e.join(",")).join("\n")
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
    const url = URL.createObjectURL(blob)
    
    // Create download link
    const link = document.createElement("a")
    link.setAttribute("href", url)
    link.setAttribute("download", `flower_scan_protocol_${DateTime.now().toFormat('yyyy_MM_dd')}.csv`)
    link.style.visibility = 'hidden'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    Swal.fire({
      title: 'Protocol Exported',
      text: 'Scan history has been saved to your device.',
      icon: 'success',
      background: '#0C0420',
      color: '#FFFFFF',
      timer: 2000,
      showConfirmButton: false
    })
  }

  return (
    <div className="max-w-7xl mx-auto space-y-16 pb-24 relative overflow-hidden px-4">
      {/* Background visual flair */}
      <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-brand-primary/5 blur-[120px] rounded-full -z-10 animate-pulse" />

      {/* Page header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-10 pt-16">
        <div data-aos="fade-right">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-primary/10 border border-brand-primary/20 text-[9px] font-black tracking-widest text-brand-secondary uppercase mb-6 shadow-[0_0_20px_rgba(186,110,143,0.1)]">
             <Clock className="w-3 h-3" /> PERSISTENT SCAN RECORD
          </div>
          <h1 className="text-6xl font-black text-white mb-6 tracking-tighter italic uppercase underline decoration-brand-primary decoration-4 underline-offset-8">
            Scan <span className="text-gradient">Registry</span>
          </h1>
          <p className="text-gray-400 text-lg max-w-xl font-bold italic leading-relaxed">
            A chronological record of every flower sample decrypted by the neural engine. Your local discovery journey starts here.
          </p>
        </div>
        
        <div className="flex gap-4" data-aos="fade-left">
           {history.length > 0 && (
              <button 
                onClick={clearHistory}
                className="glass px-8 py-4 rounded-[1.5rem] flex items-center gap-3 text-red-400 font-black hover:bg-red-500/10 hover:scale-105 active:scale-95 transition-all text-xs uppercase tracking-widest border-red-500/20 shadow-xl"
              >
                <Trash2 className="w-4 h-4" />
                Purge All
              </button>
           )}
           <button 
             onClick={handleExport}
             className="btn-primary px-8 py-4 rounded-[1.5rem] flex items-center gap-3 font-black hover:scale-105 active:scale-95 transition-all text-xs uppercase tracking-widest shadow-xl"
           >
             <Download className="w-4 h-4" />
             Export Protocol
           </button>
        </div>
      </div>

      {/* Analytics Overview (Trends only) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
        <div className="lg:col-span-12 grid grid-cols-1 md:grid-cols-3 gap-8" data-aos="fade-up">
           {[
             { label: 'Total Scans', value: history.length, icon: Activity },
             { label: 'Latest Identity', value: history[0]?.flowerName || 'None', icon: Flower },
             { label: 'Avg Confidence', value: history.length ? `${(history.reduce((a,b)=>a+b.confidence,0)/history.length).toFixed(1)}%` : '0%', icon: Layers },
           ].map((s) => (
             <div key={s.label} className="glass-floral p-8 rounded-[2.5rem] border-white/10 relative overflow-hidden group shadow-2xl">
               <s.icon className="w-8 h-8 text-brand-primary/40 mb-6 group-hover:scale-110 group-hover:text-brand-primary transition-all duration-500" />
               <div className="text-4xl font-black text-white mb-2 tracking-tighter italic">{s.value}</div>
               <div className="text-[9px] font-black text-brand-secondary tracking-[0.3em] uppercase opacity-70 group-hover:opacity-100 transition-opacity">{s.label}</div>
             </div>
           ))}
        </div>

        <div className="lg:col-span-12" data-aos="fade-up">
           <div className="glass p-10 rounded-[3rem] border-white/10 shadow-2xl relative min-h-[400px]">
              <h3 className="text-xl font-black text-white italic uppercase tracking-tighter mb-10 flex items-center gap-2">
                Scan Visualization Trends
              </h3>
              <div className="h-[300px]">
                <HistoryChart />
              </div>
           </div>
        </div>
      </div>

      {/* Live History List */}
      <div className="space-y-10" data-aos="fade-up">
        <div className="flex flex-col md:flex-row md:items-center justify-between px-4 gap-6">
          <h2 className="text-3xl font-black text-white italic uppercase tracking-tighter flex items-center gap-4">
             <Layers className="w-8 h-8 text-brand-primary" />
             Capture Registry
          </h2>
          <div className="relative w-full md:w-[400px] group">
             <div className="absolute inset-0 bg-brand-primary/5 blur-xl group-hover:bg-brand-primary/10 transition-all" />
             <Search className="absolute left-6 top-1/2 -translate-y-1/2 w-4 h-4 text-brand-primary/60 group-hover:text-brand-primary transition-colors" />
             <input type="text" placeholder="PROBE ARCHIVES..." className="w-full glass pl-14 pr-6 py-4 rounded-2xl text-[10px] font-black tracking-[0.3em] text-white placeholder:text-gray-700 focus:border-brand-primary outline-none transition-all shadow-2xl" />
          </div>
        </div>

        {history.length === 0 ? (
           <div className="glass p-20 rounded-[3rem] border-dashed border-white/10 text-center animate-in fade-in duration-700">
              <div className="w-20 h-20 rounded-full bg-white/5 flex items-center justify-center mx-auto mb-8 text-4xl">📭</div>
              <h3 className="text-2xl font-black text-white uppercase italic tracking-tighter mb-4">Registry Empty</h3>
              <p className="text-gray-500 font-bold max-w-sm mx-auto">Upload a flower sample on the Predict page to initialize your neural discovery timeline.</p>
           </div>
        ) : (
          <div className="grid grid-cols-1 gap-8 px-4">
            {history.map((item, i) => (
              <div key={item.id} data-aos="fade-up" data-aos-delay={String(i * 100)} className="glass p-6 rounded-[2.5rem] border-white/10 hover:border-brand-primary/30 transition-all flex flex-col lg:flex-row lg:items-center gap-10 group shadow-2xl hover:-translate-y-1 relative overflow-hidden">
                <div className="absolute top-0 right-0 w-1/2 h-full bg-gradient-to-l from-brand-primary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none" />
                <div className="relative w-full lg:w-48 h-48 rounded-[2rem] overflow-hidden shrink-0 shadow-2xl border border-white/5">
                  {item.imagePath ? (
                    <img src={item.imagePath} alt={item.flowerName} className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-1000" />
                  ) : (
                    <div className="w-full h-full bg-white/5 flex items-center justify-center text-4xl opacity-20">🌸</div>
                  )}
                </div>
                <div className="flex-1 min-w-0 relative z-10">
                  <div className="flex flex-col xl:flex-row xl:items-start justify-between gap-6 mb-8">
                    <div>
                      <h3 className="text-4xl font-black text-white group-hover:text-brand-primary transition-colors truncate italic uppercase tracking-tighter mb-2">{item.flowerName}</h3>
                      <div className="flex items-center gap-4 text-[10px] font-black text-gray-500 uppercase tracking-widest">
                         <span className="text-brand-secondary">{DateTime.fromISO(item.timestamp).toRelative()}</span>
                         <span className="w-1.5 h-1.5 rounded-full bg-white/10" />
                         <span>SCAN-ID: {item.id.slice(0, 8)}</span>
                      </div>
                    </div>
                    <div className="text-right">
                       <div className="text-4xl font-black text-white italic tracking-tighter">{item.confidence.toFixed(1)}%</div>
                       <div className="text-[9px] font-black text-brand-secondary uppercase tracking-[0.3em] opacity-60">Confidence Score</div>
                    </div>
                  </div>
                  <div className="pt-8 border-t border-white/5 flex items-center justify-between">
                     <div className="flex items-center gap-3 text-[10px] font-black uppercase text-gray-400 tracking-[0.2em]">
                        <div className="w-2.5 h-2.5 rounded-full bg-brand-primary animate-pulse shadow-[0_0_12px_rgba(186,110,143,1)]" />
                        Neural Match Verified
                     </div>
                     <button onClick={() => handleDelete(item.id, item.flowerName)} className="w-12 h-12 rounded-2xl glass border-white/5 flex items-center justify-center text-gray-500 hover:text-red-400 hover:bg-red-500/10 hover:border-red-500/20 transition-all">
                        <Trash2 className="w-4 h-4" />
                     </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}