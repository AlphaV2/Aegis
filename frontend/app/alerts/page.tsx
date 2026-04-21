import { apiGet } from '@/lib/api'

export default async function AlertsPage() {
  const rows = await apiGet<any[]>('/audit-logs').catch(() => [])

  return (
    <section className='grid gap-4'>
      <h1 className='text-2xl font-semibold'>Alerts and Activity</h1>
      <div className='grid gap-3'>
        {rows.map((r) => (
          <div key={r.id} className='card p-3 border-l-2 border-l-[#4F8CFF]'>
            <div className='text-sm text-gray-300'>{r.event_type}</div>
            <div className='text-xs text-gray-400 mt-1'>{new Date(r.timestamp).toLocaleString()}</div>
            <pre className='text-xs mt-2 text-gray-200 overflow-auto'>{JSON.stringify(r.payload, null, 2)}</pre>
          </div>
        ))}
        {rows.length === 0 && <div className='text-gray-400'>No activity logs yet.</div>}
      </div>
    </section>
  )
}
