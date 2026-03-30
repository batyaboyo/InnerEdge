import { useEffect, useState, FC } from 'react'

interface Trade {
  id: number
  asset: string
  direction: 'LONG' | 'SHORT'
  entry_price: number
  exit_price: number
  status: 'OPEN' | 'CLOSED'
  pnl_account_currency: number
  opened_at: string
  closed_at?: string
}

const TradeJournal: FC = () => {
  const [trades, setTrades] = useState<Trade[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)

  useEffect(() => {
    const fetchTrades = async () => {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch('/api/journal/trades/', {
          headers: { Authorization: `Token ${token}` },
        })

        if (response.ok) {
          const data = await response.json()
          setTrades(data)
        }
      } catch (error) {
        console.error('Error fetching trades:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchTrades()
  }, [])

  if (loading) {
    return <div className="text-center py-8">Loading trades...</div>
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Trade Journal</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
        >
          {showForm ? 'Cancel' : 'Add Trade'}
        </button>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full bg-white rounded-lg shadow">
          <thead className="bg-gray-100">
            <tr>
              <th className="px-6 py-3 text-left text-sm font-semibold">Asset</th>
              <th className="px-6 py-3 text-left text-sm font-semibold">Direction</th>
              <th className="px-6 py-3 text-left text-sm font-semibold">Entry</th>
              <th className="px-6 py-3 text-left text-sm font-semibold">Exit</th>
              <th className="px-6 py-3 text-left text-sm font-semibold">Status</th>
              <th className="px-6 py-3 text-left text-sm font-semibold">P/L</th>
              <th className="px-6 py-3 text-left text-sm font-semibold">Date</th>
            </tr>
          </thead>
          <tbody>
            {trades.map((trade) => (
              <tr key={trade.id} className="border-t hover:bg-gray-50">
                <td className="px-6 py-4">{trade.asset}</td>
                <td className="px-6 py-4">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                    trade.direction === 'LONG' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {trade.direction}
                  </span>
                </td>
                <td className="px-6 py-4">{trade.entry_price.toFixed(5)}</td>
                <td className="px-6 py-4">{trade.exit_price?.toFixed(5) || '-'}</td>
                <td className="px-6 py-4">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                    trade.status === 'OPEN' ? 'bg-yellow-100 text-yellow-800' : 'bg-gray-100 text-gray-800'
                  }`}>
                    {trade.status}
                  </span>
                </td>
                <td className={`px-6 py-4 font-semibold ${trade.pnl_account_currency >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  ${trade.pnl_account_currency.toFixed(2)}
                </td>
                <td className="px-6 py-4 text-sm text-gray-600">
                  {new Date(trade.opened_at).toLocaleDateString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default TradeJournal
