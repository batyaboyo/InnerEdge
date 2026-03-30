import { useEffect, useState, FC } from 'react'

interface Plan {
  id: number
  code: string
  name: string
  price_monthly_cents: number
  features: Record<string, any>
}

interface Subscription {
  id: number
  plan: number
  status: string
  period_start: string
  period_end: string
  cancel_at_period_end: boolean
}

const Billing: FC = () => {
  const [plans, setPlans] = useState<Plan[]>([])
  const [subscription, setSubscription] = useState<Subscription | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = localStorage.getItem('token')

        // Fetch plans
        const plansResponse = await fetch('/api/billing/plans/', {
          headers: { Authorization: `Token ${token}` },
        })
        if (plansResponse.ok) {
          const plansData = await plansResponse.json()
          setPlans(plansData)
        }

        // Fetch current subscription
        const subResponse = await fetch('/api/billing/subscriptions/', {
          headers: { Authorization: `Token ${token}` },
        })
        if (subResponse.ok) {
          const subData = await subResponse.json()
          if (Array.isArray(subData) && subData.length > 0) {
            setSubscription(subData[0])
          }
        }
      } catch (error) {
        console.error('Error fetching billing data:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  const handleCheckout = async (planId: number) => {
    try {
      const token = localStorage.getItem('token')
      const response = await fetch('/api/billing/subscriptions/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Token ${token}`,
        },
        body: JSON.stringify({ plan: planId }),
      })

      if (response.ok) {
        const data = await response.json()
        if (data.checkout_url) {
          window.location.href = data.checkout_url
        }
      }
    } catch (error) {
      console.error('Error initiating checkout:', error)
    }
  }

  if (loading) {
    return <div className="text-center py-8">Loading billing info...</div>
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Billing & Plans</h1>

      {subscription && (
        <div className="bg-green-50 border border-green-200 p-6 rounded-lg mb-8">
          <h2 className="text-xl font-semibold mb-2">Current Subscription</h2>
          <p className="text-gray-700">
            Status: <span className="font-semibold">{subscription.status}</span>
          </p>
          <p className="text-gray-700">
            Renews: <span className="font-semibold">{new Date(subscription.period_end).toLocaleDateString()}</span>
          </p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {plans.map((plan) => (
          <div key={plan.id} className="bg-white rounded-lg shadow hover:shadow-lg transition">
            <div className="p-6 border-b">
              <h3 className="text-2xl font-bold">{plan.name}</h3>
              <p className="text-3xl font-bold text-blue-600 mt-2">
                ${(plan.price_monthly_cents / 100).toFixed(2)}/mo
              </p>
            </div>

            <div className="p-6">
              <ul className="space-y-3 mb-6">
                {Object.entries(plan.features).map(([key, value]) => (
                  <li key={key} className="flex items-center">
                    <span className="text-green-500 mr-2">✓</span>
                    <span>{key}: {String(value)}</span>
                  </li>
                ))}
              </ul>

              <button
                onClick={() => handleCheckout(plan.id)}
                className="w-full bg-blue-500 hover:bg-blue-600 text-white py-2 rounded font-semibold"
              >
                {subscription ? 'Upgrade' : 'Subscribe'}
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Billing
