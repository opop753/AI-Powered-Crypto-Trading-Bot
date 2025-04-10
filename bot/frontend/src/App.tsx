import { Settings } from 'lucide-react';
import { BrowserRouter, Routes, Route, Link, Navigate } from 'react-router-dom';
import Dashboard from './components/Dashboard';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-900 flex">
        {/* Sidebar */}
        <div className="w-64 bg-gray-800 shadow-md fixed h-full">
          <div className="p-4">
            <h1 className="text-2xl font-bold text-blue-400">CryptoWatch</h1>
          </div>
          <nav className="mt-4">
            <Link to="/source/binance" className="flex items-center px-4 py-2 text-gray-400 hover:bg-gray-700 hover:text-blue-400">
              <span className="mr-3">₿</span>
              Binance
            </Link>
            <Link to="/source/coingecko" className="flex items-center px-4 py-2 text-gray-400 hover:bg-gray-700 hover:text-green-400">
              <span className="mr-3">🦎</span>
              CoinGecko
            </Link>
            <Link to="#" className="flex items-center px-4 py-2 text-gray-400 hover:bg-gray-700">
              <Settings className="mr-3" size={20} />
              Settings
            </Link>
          </nav>
        </div>

        {/* Main Content */}
        <div className="flex-1 pl-64">
          <header className="bg-gray-800 shadow">
            <div className="px-6 py-4">
              <h2 className="text-xl font-semibold text-gray-100">Dashboard Overview</h2>
            </div>
          </header>

          <main className="p-6">
            <Routes>
              <Route path="/source/:source" element={<Dashboard />} />
              <Route path="*" element={<Navigate to="/source/binance" replace />} />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
