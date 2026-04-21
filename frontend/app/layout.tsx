import './globals.css'
import type { Metadata } from 'next'
import Nav from '@/components/Nav'

export const metadata: Metadata = {
  title: 'Aegis Layer',
  description: 'Control and governance system for AI agent payments'
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang='en'>
      <body>
        <div className='min-h-screen p-6 md:p-8'>
          <div className='max-w-7xl mx-auto grid md:grid-cols-[240px_1fr] gap-5'>
            <Nav />
            <main>{children}</main>
          </div>
        </div>
      </body>
    </html>
  )
}
