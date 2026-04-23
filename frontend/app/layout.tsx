import type { Metadata } from 'next'
import './globals.css'
import Navbar from '@/components/layout/Navbar'
import AOSInit from '@/components/layout/AOSInit'

export const metadata: Metadata = {
  title: 'FlowerAI',
  description: 'Flower image recognition powered by deep learning',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-brand-dark min-h-screen text-white antialiased selection:bg-brand-primary selection:text-white">
        <AOSInit />
        <Navbar />
        <main className="max-w-7xl mx-auto px-6 py-12 relative z-10">
          {children}
        </main>
        <footer className="w-full py-12 px-6 flex justify-center items-center border-t border-white/5 bg-black/20">
           <div className="text-[10px] font-black text-[#7B466A]/40 tracking-[0.4em] uppercase italic select-none">
             Made by Shivangiba Jadeja
           </div>
        </footer>

      </body>
    </html>
  )
}