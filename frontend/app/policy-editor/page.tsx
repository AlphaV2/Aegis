'use client'

import { useState } from 'react'
import { apiPost } from '@/lib/api'

export default function PolicyEditorPage() {
  const [form, setForm] = useState({
    agent_id: '',
    per_tx_limit: '1000',
    daily_limit: '3000',
    monthly_limit: '15000',
    allowed_vendors: 'openai,aws,supabase',
    blocked_categories: 'gambling,adult',
    requires_approval_above: '700'
  })
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState('')

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    try {
      const payload = {
        ...form,
        allowed_vendors: form.allowed_vendors.split(',').map((x) => x.trim()).filter(Boolean),
        blocked_categories: form.blocked_categories.split(',').map((x) => x.trim()).filter(Boolean)
      }
      const res = await apiPost('/policy/set', payload)
      setResult(res)
    } catch (err: any) {
      setError(err.message || 'failed')
    }
  }

  return (
    <section className='grid gap-4'>
      <h1 className='text-2xl font-semibold'>Policy Editor</h1>
      <form onSubmit={onSubmit} className='card p-4 grid gap-3'>
        {Object.entries(form).map(([k, v]) => (
          <div key={k}>
            <label className='text-sm text-gray-300'>{k}</label>
            <input className='input mt-1' value={v} onChange={(e) => setForm((s) => ({ ...s, [k]: e.target.value }))} />
          </div>
        ))}
        <button className='btn mt-2' type='submit'>Save Policy</button>
        {error && <div className='text-red-300 text-sm'>{error}</div>}
      </form>
      <div className='card p-4'>
        <div className='text-sm text-gray-300 mb-2'>JSON view</div>
        <pre className='text-xs overflow-auto'>{JSON.stringify(result, null, 2)}</pre>
      </div>
    </section>
  )
}
