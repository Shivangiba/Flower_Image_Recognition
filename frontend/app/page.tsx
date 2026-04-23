import Link from 'next/link'

/**
 * HomePage Component
 * 
 * The landing page for the FlowerAI platform. 
 * Designed with a "Premium Dark" aesthetic to showcase the intersection 
 * of botanical science and deep learning.
 */

// Key features displayed in the middle section
const features = [
  {
    title: 'Petal Precision',
    desc: 'Analyzes flower anatomy with deep EfficientNet features to detect species.',
    icon: '🌸',
  },
  {
    title: 'Instant Scan',
    desc: 'Predictive inference in milliseconds for a split-second identification.',
    icon: '⚡',
  },
  {
    title: 'Trend Insights',
    desc: 'Personal scan history visualizing your flower discovery journey.',
    icon: '📋',
  },
]

// Real-time project statistics for credibility
const stats = [
  { value: '13', label: 'FLOWER SPECIES' }, // Total classes the model is trained on
  { value: '94.3%', label: 'ACCURACY' },    // Test accuracy from training results
  { value: '<1S', label: 'SPEED' },         // Typical inference latency
  { value: '∞', label: 'FREE API' },        // Pricing model
]

export default function HomePage() {
  return (
    <div className="space-y-32">
      {/* 
          Hero Section:
          Provides the "WOW" factor using radial gradients and high-contrast typography.
          The primary entry point to the prediction engine.
      */}
      <section className="relative flex flex-col items-center justify-center pt-24 pb-12 overflow-hidden">
        {/* Background glow effects to create depth */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-brand-primary/10 blur-[120px] rounded-full -z-10" />
        <div className="absolute bottom-0 right-0 w-[300px] h-[300px] bg-brand-accent/10 blur-[100px] rounded-full -z-10" />

        {/* Version Badge: Indicates active neural node */}
        <div
          data-aos="fade-down"
          className="inline-flex items-center gap-2 text-xs font-bold tracking-[0.2em] px-5 py-2 rounded-full glass border-brand-primary/20 text-brand-secondary mb-10 uppercase transition-all hover:bg-white/5 cursor-default"
        >
          <div className="w-1.5 h-1.5 rounded-full bg-brand-primary animate-pulse" />
          Neural Engine v2.0
        </div>

        {/* Main Value Proposition */}
        <h1
          data-aos="fade-up"
          className="text-7xl md:text-8xl font-black text-white text-center mb-8 tracking-tighter leading-none"
        >
          Identify the <br />
          <span className="text-gradient">Unknown Petals</span>
        </h1>

        <p
          data-aos="fade-up"
          data-aos-delay="100"
          className="text-xl text-gray-400 max-w-2xl text-center mb-12 font-medium leading-relaxed px-4"
        >
          An "Organic Tech" vision tool for botanical research. 
          Upload a high-res photo and let our deep learning model decode the species in seconds.
        </p>

        {/* Action Buttons */}
        <div
          data-aos="fade-up"
          data-aos-delay="200"
          className="flex flex-col sm:flex-row items-center justify-center gap-6"
        >
          <Link
            href="/predict"
            className="px-10 py-4 btn-primary rounded-2xl font-bold tracking-tight text-lg shadow-xl shadow-brand-primary/20"
          >
            Start Analyzing →
          </Link>
          <Link
            href="/history"
            className="px-10 py-4 glass text-white border-white/5 rounded-2xl font-bold tracking-tight text-lg hover:bg-white/5 transition-all"
          >
            Past Discoveries
          </Link>
        </div>
      </section>

      {/* 
          Stats Section:
          Social proof and technical performance data.
      */}
      <section className="grid grid-cols-2 md:grid-cols-4 gap-6 px-4" data-aos="fade-up">
        {stats.map((s) => (
          <div
            key={s.label}
            className="glass-floral rounded-3xl p-8 text-center border-white/5 hover:border-white/10 transition-all group"
          >
            <div className="text-4xl font-black text-white mb-2 group-hover:scale-110 transition-transform">{s.value}</div>
            <div className="text-[10px] font-bold text-brand-secondary tracking-[0.2em] uppercase">{s.label}</div>
          </div>
        ))}
      </section>

      {/* 
          Features Grid:
          Uses AOS (Animate On Scroll) to create a dynamic reading experience.
      */}
      <section className="relative">
        <div className="text-center mb-16">
          <h2 data-aos="fade-up" className="text-5xl font-black text-white mb-6 tracking-tight">
            Advanced Insights
          </h2>
          <p data-aos="fade-up" data-aos-delay="100" className="text-gray-400 max-w-lg mx-auto font-medium">
            Bridging the gap between organic beauty and digital intelligence.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 px-4">
          {features.map((f, i) => (
            <div
              key={f.title}
              data-aos="fade-up"
              data-aos-delay={String(i * 120)}
              className="glass p-10 rounded-[2.5rem] border-white/5 hover:border-brand-primary/30 transition-all hover:-translate-y-2 group"
            >
              <div className="w-16 h-16 rounded-3xl bg-brand-primary/10 flex items-center justify-center text-4xl mb-8 group-hover:scale-110 transition-transform">
                {f.icon}
              </div>
              <h3 className="text-2xl font-bold text-white mb-4 tracking-tight group-hover:text-brand-primary transition-colors">
                {f.title}
              </h3>
              <p className="text-gray-400 text-sm leading-relaxed font-medium">
                {f.desc}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* 
          Tech Breakdown Section:
          Explains the backend logic in user-friendly steps.
      */}
      <section className="bg-white/5 rounded-[3rem] border border-white/5 p-16 mx-4 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-[200px] h-[200px] bg-brand-secondary/5 blur-[80px] rounded-full -z-10" />
        
        <h2 data-aos="fade-up" className="text-4xl font-black text-white text-center mb-16 tracking-tight">
          How the Engine Works
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-12 relative">
          {[
            { step: '01', title: 'Input Capture', desc: 'Secure upload to our high-speed botanical cloud processing nodes.' },
            { step: '02', title: 'Neural Scan', desc: 'Running EfficientNet-B0 features to extract petal & stem patterns.' },
            { step: '03', title: 'Visual Report', desc: 'Generate multi-metric charts and probabilistic confidence maps.' },
          ].map((item, i) => (
            <div key={item.step} data-aos="fade-up" data-aos-delay={String(i * 120)} className="flex flex-col items-center text-center">
              <div className="w-16 h-16 rounded-full bg-brand-primary text-white text-xl font-black flex items-center justify-center mb-8 shadow-lg shadow-brand-primary/30">
                {item.step}
              </div>
              <h3 className="text-xl font-bold text-white mb-4 tracking-tight">{item.title}</h3>
              <p className="text-gray-400 text-sm leading-relaxed font-medium">{item.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Final Call To Action (CTA) */}
      <section
        data-aos="zoom-in"
        className="mx-4 mb-24 relative rounded-[3rem] p-20 text-center overflow-hidden border border-white/5"
      >
        {/* Background gradient for high contrast */}
        <div className="absolute inset-0 bg-gradient-to-br from-brand-primary to-brand-accent opacity-90" />
        {/* Subtle noise texture to prevent banding in the gradient */}
        <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20" />
        
        <div className="relative z-10">
          <h2 className="text-5xl font-black text-white mb-6 tracking-tight">
            Ready to Pulse the Petals?
          </h2>
          <p className="text-white/80 mb-12 text-xl font-medium max-w-xl mx-auto">
            Experience the intersection of botany and deep learning. 
            Upload your first flower today for free.
          </p>
          <Link
            href="/predict"
            className="inline-block px-12 py-5 bg-white text-brand-dark rounded-2xl font-black text-lg hover:scale-105 transition-all shadow-2xl hover:shadow-brand-dark/20"
          >
            Start Predicting →
          </Link>
        </div>
      </section>
    </div>
  )
}