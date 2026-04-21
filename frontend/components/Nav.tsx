"use client"

import Link from 'next/link'
import { usePathname } from 'next/navigation'

const links = [
  { href: '/dashboard', label: 'Dashboard' },
  { href: '/transactions', label: 'Transactions' },
  { href: '/policy-editor', label: 'Policy Editor' },
  { href: '/alerts', label: 'Alerts' }
]

export default function Nav() {
  const pathname = usePathname()

  return (
    <aside className='card p-4 h-fit'>
      <div className='text-sm uppercase tracking-widest text-gray-300 mb-3'>Aegis Layer</div>
      <div className='grid gap-2'>
        {links.map((l) => {
          const active = pathname.startsWith(l.href)
          return (
            <Link key={l.href} href={l.href} className={`px-3 py-2 rounded-md border ${active ? 'border-[#4F8CFF] text-white bg-[#131824]' : 'border-[#1f1f23] text-gray-300'}`}>
              {l.label}
            </Link>
          )
        })}
      </div>
    </aside>
  )
}
