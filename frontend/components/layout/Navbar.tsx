'use client'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

const navLinks = [
  { href: '/',        label: 'Home'    },
  { href: '/predict', label: 'Predict' },
  { href: '/history', label: 'History' },
  { href: '/about',   label: 'About'   },
]


export default function Navbar() {
  const pathname = usePathname()

  return (
    <nav className="w-full border-b border-white/10 bg-brand-dark/80 backdrop-blur-lg sticky top-0 z-50 px-6 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">

        {/* Logo */}
        <Link href="/" className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-brand-primary to-brand-accent flex items-center justify-center shadow-lg shadow-brand-primary/20 hover:scale-110 transition-transform">
            <span className="text-white text-lg font-bold">F</span>
          </div>
          <span className="font-bold text-white text-xl tracking-tight">
            Flower<span className="text-brand-primary">AI</span>
          </span>
        </Link>

        {/* Links */}
        <div className="flex items-center gap-2 p-1 bg-white/5 rounded-2xl border border-white/5">
          {navLinks.map(({ href, label }) => {
            const isActive = pathname === href
            return (
              <Link
                key={href}
                href={href}
                className={`px-5 py-2 rounded-xl text-sm font-semibold transition-all duration-300 ${
                  isActive
                    ? 'bg-brand-primary text-white shadow-md'
                    : 'text-gray-400 hover:text-white hover:bg-white/5'
                }`}
              >
                {label}
              </Link>
            )
          })}
        </div>

        {/* Badge */}
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-2 px-4 py-1.5 rounded-full bg-green-500/10 border border-green-500/20 text-green-400 font-bold text-xs">
            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
            LIVE
          </div>
        </div>

      </div>
    </nav>
  )
}