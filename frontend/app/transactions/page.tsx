import { apiGet } from '@/lib/api'

export default async function TransactionsPage() {
  const rows = await apiGet<any[]>('/transactions').catch(() => [])

  return (
    <section className='grid gap-4'>
      <h1 className='text-2xl font-semibold'>Transactions</h1>
      <div className='card p-4 overflow-x-auto'>
        <table className='w-full text-sm'>
          <thead>
            <tr className='text-gray-400'>
              <th className='text-left p-2'>Time</th>
              <th className='text-left p-2'>Agent</th>
              <th className='text-left p-2'>Vendor</th>
              <th className='text-left p-2'>Amount</th>
              <th className='text-left p-2'>Status</th>
              <th className='text-left p-2'>Reason</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.id} className='border-t border-[#1f1f23]'>
                <td className='p-2'>{new Date(r.created_at).toLocaleString()}</td>
                <td className='p-2'>{String(r.agent_id).slice(0, 8)}</td>
                <td className='p-2'>{r.vendor}</td>
                <td className='p-2'>${Number(r.amount).toFixed(2)}</td>
                <td className='p-2'>{r.status}</td>
                <td className='p-2 text-gray-300'>{r.reason}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {rows.length === 0 && <div className='text-gray-400'>No transactions found.</div>}
      </div>
    </section>
  )
}
