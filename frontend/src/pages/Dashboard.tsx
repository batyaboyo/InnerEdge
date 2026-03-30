import { useEffect, useState, FC } from 'react'

interface TradeSummary {
  total_trades: number
  wins: number
  losses: number
  win_rate: number
  total_pnl: number
  avg_win: number
  avg_loss: number
}

const Dashboard: FC = () => {
  const [summary, setSummary] = useState<TradeSummary | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch('/api/journal/trades/analytics/', {
          headers: { Authorization: `Token ${token}` },
        })

        if (response.ok) {
          const data = await response.json()
          setSummary(data)
        }
      } catch (error) {
        console.error('Error fetching dashboard:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchSummary()
  }, [])

  if (loading) {
    return <div className="text-center py-8">Loading...</div>
  }

  if (!summary) {
    return <div className="text-center py-8 text-gray-600">No data available</div>
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-gray-600 text-sm font-medium">Total Trades</h3>
        <p className="text-3xl font-bold mt-2">{summary.total_trades}</p>
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-gray-600 text-sm font-medium">Win Rate</h3>
        <p className="text-3xl font-bold mt-2">{summary.win_rate.toFixed(2)}%</p>
      </div>

      <div className={`bg-white p-6 rounded-lg shadow ${summary.total_pnl >= 0 ? 'border-l-4 border-green-500' : 'border-l-4 border-red-500'}`}>
        <h3 className="text-gray-600 text-sm font-medium">Total P/L</h3>
        <p className={`text-3xl font-bold mt-2 ${summary.total_pnl >= 0 ? 'text-green-600' : 'text-red-600'}`}>
          ${summary.total_pnl.toFixed(2)}
        </p>
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-gray-600 text-sm font-medium">Wins</h3>
        <p className="text-3xl font-bold mt-2 text-green-600">{summary.wins}</p>
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-gray-600 text-sm font-medium">Losses</h3>
        <p className="text-3xl font-bold mt-2 text-red-600">{summary.losses}</p>
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-gray-600 text-sm font-medium">Avg Win / Loss Ratio</h3>
        <p className="text-2xl font-bold mt-2">
          {(summary.avg_win / Math.abs(summary.avg_loss)).toFixed(2)}
        </p>
      </div>
    </div>
  )
}

export default Dashboard
