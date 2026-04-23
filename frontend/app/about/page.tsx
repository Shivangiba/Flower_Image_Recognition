'use client'
import { useEffect, useState } from 'react'
import { getMetrics, MetricsResponse } from '@/lib/api'
import { Info, BarChart3, Zap, Binary, Layers, BrainCircuit, Cpu, Network, ShieldCheck } from 'lucide-react'
import { Tooltip } from '@/components/ui/Tooltip'

export default function AboutPage() {
  const [metrics, setMetrics] = useState<MetricsResponse | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getMetrics()
      .then(setMetrics)
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="max-w-7xl mx-auto space-y-16 pb-24 relative overflow-hidden px-4">
      {/* Background visual flair */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-brand-primary/5 blur-[120px] rounded-full -z-10 animate-pulse" />

      {/* Page header */}
      <div className="text-center pt-16" data-aos="zoom-out">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-primary/10 border border-brand-primary/20 text-[9px] font-black tracking-widest text-brand-secondary uppercase mb-6 shadow-[0_0_20px_rgba(186,110,143,0.1)]">
           <BrainCircuit className="w-3 h-3" /> NEURAL ENGINE TOPOLOGY
        </div>
        <h1 className="text-6xl font-black text-white mb-6 tracking-tighter italic uppercase italic">
          About the <span className="text-gradient">Model</span>
        </h1>
        <p className="text-gray-400 text-lg max-w-2xl mx-auto font-bold italic leading-relaxed">
          The core architecture leverages EfficientNet-B0 with deep feature extraction and botanical transfer learning.
        </p>
      </div>

      {/* Primary Analytics Section */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-8" data-aos="fade-up">
         {[
           { label: 'Neural Accuracy', value: metrics ? `${metrics.accuracy}%` : '---', icon: BarChart3, delay: 0 },
           { label: 'F1 Harmony', value: metrics ? metrics.f1_score.toFixed(4) : '---', icon: Layers, delay: 100 },
           { label: 'Precision Node', value: metrics ? metrics.precision.toFixed(4) : '---', icon: Zap, delay: 200 },
           { label: 'Species Range', value: metrics ? metrics.classes : '---', icon: Binary, delay: 300 },
         ].map((s, i) => (
           <div key={s.label} className="glass-floral p-8 rounded-[2.5rem] border-white/10 relative overflow-hidden group shadow-2xl">
             <s.icon className="w-8 h-8 text-brand-primary/40 mb-6 group-hover:scale-110 group-hover:text-brand-primary transition-all duration-500" />
             <div className="text-4xl font-black text-white mb-2 tracking-tighter italic">{s.value}</div>
             <div className="text-[9px] font-black text-brand-secondary tracking-[0.3em] uppercase opacity-70 group-hover:opacity-100 transition-opacity">{s.label}</div>
           </div>
         ))}
      </div>

      {/* Model Architecture Info */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
        <div className="lg:col-span-12 glass p-10 md:p-16 rounded-[3rem] border-white/10 shadow-2xl relative overflow-hidden" data-aos="fade-up">
           <div className="absolute top-0 right-0 w-[400px] h-[400px] bg-brand-primary/5 blur-[100px] rounded-full -z-10" />
           <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
              <div className="space-y-8">
                 <h2 className="text-4xl font-black text-white italic uppercase tracking-tighter flex items-center gap-4">
                    <Cpu className="w-10 h-10 text-brand-primary" />
                    EfficientNet-B0 Base
                 </h2>
                 <p className="text-gray-400 text-lg font-bold leading-relaxed italic">
                    Our model uses **Transfer Learning** from the ImageNet database. This means the neural network already knows how to detect edges, curves, and basic textures, which we then specialized for the botanical domain.
                 </p>
                 <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-6">
                    {[
                      { title: 'Fine-Tuning', desc: 'The last layers are specialized for 13 distinct flower classes.' },
                      { title: 'Augmentation', desc: 'Rotation, zoom, and flip transforms were used for robustness.' },
                      { title: 'Drop-Out', desc: 'Preventing overfitting with regularized neural dropout.' },
                      { title: 'Hyper-Param', desc: 'Optimized with AdamW optimizer at 1e-4 learning rate.' },
                    ].map((idx) => (
                      <div key={idx.title} className="flex gap-4 p-4 rounded-2xl bg-white/5 border border-white/10 group hover:border-brand-primary/40 transition-all">
                        <div className="w-2 h-2 rounded-full bg-brand-primary mt-1.5 shrink-0 shadow-[0_0_10px_rgba(186,110,143,1)]" />
                        <div>
                          <div className="text-xs font-black text-white uppercase mb-1 tracking-widest">{idx.title}</div>
                          <div className="text-[10px] text-gray-500 font-bold leading-tight">{idx.desc}</div>
                        </div>
                      </div>
                    ))}
                 </div>
              </div>
              <div className="glass-floral p-10 rounded-[3rem] border-white/10 relative overflow-hidden group">
                 <h3 className="text-xl font-black text-white italic uppercase tracking-tighter mb-10 flex items-center justify-between">
                    Confusion Matrix Overview
                    <Tooltip content="Analysis of predicted vs actual classes, showing clear convergence on the target set.">
                      <div className="w-8 h-8 rounded-full glass border-white/5 flex items-center justify-center cursor-help">
                        <Info className="w-4 h-4 text-brand-secondary" />
                      </div>
                    </Tooltip>
                 </h3>
                 <div className="relative rounded-2xl overflow-hidden group shadow-inner border border-white/5">
                    {metrics ? (
                      <img src={metrics.confusion_matrix_url} alt="Confusion Matrix" className="w-full h-auto brightness-90 contrast-110 group-hover:scale-110 transition-transform duration-[3s]" />
                    ) : (
                      <div className="w-full aspect-video bg-black/40 animate-pulse flex items-center justify-center text-gray-700 italic">SYNCING NEURAL LOGS...</div>
                    )}
                 </div>
              </div>
           </div>
        </div>
      </div>

      {/* Tech Stack */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8" data-aos="fade-up">
         {[
           { title: 'Data Pipeline', desc: 'Python-based preprocessing with PyTorch transforms and EfficientNet backbone.', icon: Network },
           { title: 'Inference Engine', desc: 'FastAPI backend optimized for real-time sub-second botanical classification.', icon: Network },
           { title: 'Interface Logic', desc: 'Next.js Frontend with Chart.js visualization and AOS micro-animations.', icon: Network },
         ].map((t) => (
           <div key={t.title} className="glass p-10 rounded-[3rem] border-white/10 group shadow-2xl hover:border-brand-primary/20 transition-all">
              <t.icon className="w-8 h-8 text-brand-primary/20 mb-8 group-hover:text-brand-primary transition-colors" />
              <h3 className="text-xl font-black text-white italic uppercase mb-4 tracking-tighter">{t.title}</h3>
              <p className="text-gray-500 text-sm font-bold leading-relaxed italic">{t.desc}</p>
           </div>
         ))}
      </div>

    </div>
  )
}
