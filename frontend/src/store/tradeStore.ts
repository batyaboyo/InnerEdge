import { create } from 'zustand'

interface Trade {
  id: number
  asset: string
  direction: 'LONG' | 'SHORT'
  entry_price: number
  exit_price: number
  status: 'OPEN' | 'CLOSED'
  pnl_account_currency: number
  opened_at: string
}

interface TradeStore {
  trades: Trade[]
  loading: boolean
  error: string | null
  fetchTrades: () => Promise<void>
  addTrade: (trade: Trade) => void
  removeTrade: (id: number) => void
}

export const useTradeStore = create<TradeStore>((set) => ({
  trades: [],
  loading: false,
  error: null,

  fetchTrades: async () => {
    set({ loading: true, error: null })
    try {
      const token = localStorage.getItem('token')
      const response = await fetch('/api/journal/trades/', {
        headers: { Authorization: `Token ${token}` },
      })

      if (!response.ok) throw new Error('Failed to fetch trades')

      const data: Trade[] = await response.json()
      set({ trades: data, loading: false })
    } catch (error) {
      set({ error: String(error), loading: false })
    }
  },

  addTrade: (trade: Trade) => {
    set((state: TradeStore) => ({ trades: [...state.trades, trade] }))
  },

  removeTrade: (id: number) => {
    set((state: TradeStore) => ({ trades: state.trades.filter((t: Trade) => t.id !== id) }))
  },
}))
