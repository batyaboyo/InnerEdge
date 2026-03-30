import { useEffect, useState, FC } from 'react'

interface Alert {
  id: number
  title: string
  message: string
  level: 'INFO' | 'WARNING' | 'ERROR'
  is_read: boolean
  created_at: string
}

const Alerts: FC = () => {
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch('/api/alerts/events/', {
          headers: { Authorization: `Token ${token}` },
        })

        if (response.ok) {
          const data = await response.json()
          setAlerts(data)
        }
      } catch (error) {
        console.error('Error fetching alerts:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchAlerts()
    const interval = setInterval(fetchAlerts, 5000) // Refresh every 5 seconds

    return () => clearInterval(interval)
  }, [])

  const markAsRead = async (alertId: number) => {
    try {
      const token = localStorage.getItem('token')
      await fetch(`/api/alerts/events/${alertId}/mark-read/`, {
        method: 'POST',
        headers: { Authorization: `Token ${token}` },
      })

      setAlerts(alerts.map((a) => (a.id === alertId ? { ...a, is_read: true } : a)))
    } catch (error) {
      console.error('Error marking alert as read:', error)
    }
  }

  if (loading) {
    return <div className="text-center py-8">Loading alerts...</div>
  }

  const getLevelColor = (level: string) => {
    switch (level) {
      case 'INFO':
        return 'bg-blue-100 text-blue-800'
      case 'WARNING':
        return 'bg-yellow-100 text-yellow-800'
      case 'ERROR':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Alerts & Notifications</h1>

      {alerts.length === 0 ? (
        <div className="bg-white p-8 rounded-lg shadow text-center text-gray-600">
          No alerts yet
        </div>
      ) : (
        <div className="space-y-4">
          {alerts.map((alert) => (
            <div
              key={alert.id}
              className={`bg-white p-6 rounded-lg shadow ${!alert.is_read ? 'border-l-4 border-blue-500' : ''}`}
            >
              <div className="flex justify-between items-start">
                <div>
                  <div className="flex items-center gap-3">
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${getLevelColor(alert.level)}`}>
                      {alert.level}
                    </span>
                    <h3 className="text-lg font-semibold">{alert.title}</h3>
                  </div>
                  <p className="text-gray-600 mt-2">{alert.message}</p>
                  <p className="text-sm text-gray-500 mt-2">
                    {new Date(alert.created_at).toLocaleString()}
                  </p>
                </div>
                {!alert.is_read && (
                  <button
                    onClick={() => markAsRead(alert.id)}
                    className="text-sm bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded"
                  >
                    Mark Read
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default Alerts
