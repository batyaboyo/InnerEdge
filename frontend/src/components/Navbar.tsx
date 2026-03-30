import { FC } from 'react'
import { Link } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'

const Navbar: FC = () => {
  const { logout } = useAuthStore()

  return (
    <nav className="bg-white shadow-sm">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <Link to="/" className="text-2xl font-bold text-blue-600">
          InnerEdge
        </Link>

        <div className="flex gap-8">
          <Link to="/" className="text-gray-600 hover:text-gray-900">
            Dashboard
          </Link>
          <Link to="/journal" className="text-gray-600 hover:text-gray-900">
            Trade Journal
          </Link>
          <Link to="/alerts" className="text-gray-600 hover:text-gray-900">
            Alerts
          </Link>
          <Link to="/billing" className="text-gray-600 hover:text-gray-900">
            Billing
          </Link>
        </div>

        <button
          onClick={() => {
            logout()
            window.location.reload()
          }}
          className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded"
        >
          Logout
        </button>
      </div>
    </nav>
  )
}

export default Navbar
