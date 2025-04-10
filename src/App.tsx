import React from 'react';
import { LayoutDashboard, LineChart, Settings, Shield } from 'lucide-react';
import Dashboard from './components/Dashboard';

function App() {
  return (
    <div className="min-h-screen bg-gray-900 flex">
      {/* Sidebar */}
      <div className="w-64 bg-gray-800 shadow-md">
        <div className="p-4">
          <h1 className="text-2xl font-bold text-blue-400">CryptoWatch</h1>
        </div>
        <nav className="mt-4">
          <a href="#" className="flex items-center px-4 py-2 bg-gray-700 text-blue-400">
            <LayoutDashboard className="mr-3" size={20} />
            Dashboard
          </a>
          <a href="#" className="flex items-center px-4 py-2 text-gray-400 hover:bg-gray-700">
            <LineChart className="mr-3" size={20} />
            Trading
          </a>
          <a href="#" className="flex items-center px-4 py-2 text-gray-400 hover:bg-gray-700">
            <Shield className="mr-3" size={20} />
            Risk Analysis
          </a>
          <a href="#" className="flex items-center px-4 py-2 text-gray-400 hover:bg-gray-700">
            <Settings className="mr-3" size={20} />
            Settings
          </a>
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1">
        <header className="bg-gray-800 shadow">
          <div className="px-6 py-4">
            <h2 className="text-xl font-semibold text-gray-100">Dashboard Overview</h2>
          </div>
        </header>

        <main>
          <Dashboard />
        </main>
      </div>
    </div>
  );
}

export default App;