import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import TradeJournal from './pages/TradeJournal'
import Alerts from './pages/Alerts'
import Billing from './pages/Billing'
import Login from './pages/Login'
import Navbar from './components/Navbar'
import { useAuthStore } from './store/authStore'

function App() {
  const { token } = useAuthStore()

  if (!token) {
    return <Login />
  }

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <main className="container mx-auto py-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/journal" element={<TradeJournal />} />
            <Route path="/alerts" element={<Alerts />} />
            <Route path="/billing" element={<Billing />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
