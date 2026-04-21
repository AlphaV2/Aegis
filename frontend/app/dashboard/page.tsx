import { apiGet } from '@/lib/api'

type Tx = {
  id: string
  amount: string
  vendor: string
  status: string
  created_at: string
}

type Agent = {
  id: string
  name: string
  status: string
  wallet_balance: string
  currency: string
}

export default async function DashboardPage() {
  let txs: Tx[] = []
  let agents: Agent[] = []
  try {
    txs = await apiGet<Tx[]>('/transactions')
  } catch {
    txs = []
  }
  try {
    agents = await apiGet<Agent[]>('/agents')
  } catch {
    agents = []
  }

  const total = txs.reduce((s, t) => s + Number(t.amount), 0)

  return (
    <section className='grid gap-5'>
      <h1 className='text-2xl font-semibold'>Dashboard</h1>
      <div className='grid sm:grid-cols-3 gap-4'>
        <div className='card p-4'><div className='text-gray-300 text-sm'>Transactions</div><div className='text-2xl font-bold mt-1'>{txs.length}</div></div>
        <div className='card p-4'><div className='text-gray-300 text-sm'>Volume</div><div className='text-2xl font-bold mt-1'>${total.toFixed(2)}</div></div>
        <div className='card p-4'><div className='text-gray-300 text-sm'>Rejected</div><div className='text-2xl font-bold mt-1'>{txs.filter(t => t.status === 'REJECTED').length}</div></div>
      </div>
      <div className='card p-4'>
        <div className='font-semibold mb-3'>Agents and wallets</div>
        <div className='grid gap-2 mb-4'>
          {agents.map((a) => (
            <div key={a.id} className='grid grid-cols-[1fr_160px_120px] text-sm border border-[#1f1f23] rounded px-3 py-2'>
              <div>{a.name}</div>
              <div>{a.currency} {Number(a.wallet_balance).toFixed(2)}</div>
              <div>{a.status}</div>
            </div>
          ))}
          {agents.length === 0 && <div className='text-gray-400 text-sm'>No agents available.</div>}
        </div>

        <div className='font-semibold mb-3'>Recent activity</div>
        <div className='grid gap-2'>
          {txs.slice(0, 8).map((t) => (
            <div key={t.id} className='grid grid-cols-[120px_1fr_120px_180px] text-sm border border-[#1f1f23] rounded px-3 py-2'>
              <div>${Number(t.amount).toFixed(2)}</div>
              <div>{t.vendor}</div>
              <div>{t.status}</div>
              <div className='text-gray-400'>{new Date(t.created_at).toLocaleString()}</div>
            </div>
          ))}
          {txs.length === 0 && <div className='text-gray-400 text-sm'>No transactions yet.</div>}
        </div>
      </div>
    </section>
  )
}
