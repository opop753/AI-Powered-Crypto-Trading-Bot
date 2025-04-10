import React from 'react';
import { XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from 'recharts';
import { Activity, Wallet, Eye, AlertTriangle, TrendingUp, TrendingDown } from 'lucide-react';
//import { formatDistanceToNow } from 'date-fns';
import useSWR from 'swr';

interface CryptoData {
  id: string;
  symbol: string;
  name: string;
  image: string;
  current_price: number;
  market_cap: number;
  market_cap_rank: number;
  total_volume: number;
  high_24h: number;
  low_24h: number;
  price_change_24h: number;
  price_change_percentage_24h: number;
  market_cap_change_24h: number;
  market_cap_change_percentage_24h: number;
  circulating_supply: number;
  total_supply: number;
  ath: number;
  ath_change_percentage: number;
}

const fetcher = (url: string) => fetch(url).then((res) => res.json());

const Dashboard: React.FC = () => {
  const { data: cryptoData, error } = useSWR<CryptoData[]>(
    'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1&sparkline=true',
    fetcher,
    {
      refreshInterval: 30000 // Refresh every 30 seconds
    }
  );

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(price);
  };

  const formatLargeNumber = (num: number) => {
    if (num >= 1e12) return (num / 1e12).toFixed(2) + 'T';
    if (num >= 1e9) return (num / 1e9).toFixed(2) + 'B';
    if (num >= 1e6) return (num / 1e6).toFixed(2) + 'M';
    return num.toLocaleString();
  };

  if (error) return <div className="text-red-500">Failed to load cryptocurrency data</div>;
  if (!cryptoData) return <div className="text-gray-400">Loading...</div>;

  // Create chart data
  const chartData = cryptoData.map(coin => ({
    name: coin.symbol.toUpperCase(),
    price: coin.current_price,
    marketCap: coin.market_cap,
    volume: coin.total_volume,
    change24h: coin.price_change_percentage_24h
  }));

  return (
    <div className="p-6 space-y-6 bg-gray-900 text-gray-100">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-gray-800 p-6 rounded-lg shadow-md">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold text-gray-300">Total Market Cap</h3>
            <Wallet className="text-blue-400" />
          </div>
          <p className="text-2xl font-bold mt-2 text-gray-100">
            ${formatLargeNumber(cryptoData.reduce((acc, coin) => acc + coin.market_cap, 0))}
          </p>
          <p className="text-green-400 text-sm">
            {cryptoData[0]?.market_cap_change_percentage_24h.toFixed(2)}% 24h
          </p>
        </div>

        <div className="bg-gray-800 p-6 rounded-lg shadow-md">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold text-gray-300">24h Volume</h3>
            <Activity className="text-purple-400" />
          </div>
          <p className="text-2xl font-bold mt-2 text-gray-100">
            ${formatLargeNumber(cryptoData.reduce((acc, coin) => acc + coin.total_volume, 0))}
          </p>
          <p className="text-gray-400 text-sm">Across all pairs</p>
        </div>

        <div className="bg-gray-800 p-6 rounded-lg shadow-md">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold text-gray-300">BTC Dominance</h3>
            <Eye className="text-green-400" />
          </div>
          <p className="text-2xl font-bold mt-2 text-gray-100">
            {((cryptoData[0]?.market_cap / cryptoData.reduce((acc, coin) => acc + coin.market_cap, 0)) * 100).toFixed(2)}%
          </p>
          <p className="text-gray-400 text-sm">Market share</p>
        </div>

        <div className="bg-gray-800 p-6 rounded-lg shadow-md">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold text-gray-300">Active Cryptocurrencies</h3>
            <AlertTriangle className="text-yellow-400" />
          </div>
          <p className="text-2xl font-bold mt-2 text-gray-100">{cryptoData.length}</p>
          <p className="text-gray-400 text-sm">Top by market cap</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-gray-800 p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-bold mb-4 text-gray-100">Market Overview</h2>
          <div className="h-[400px]">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData}>
                <defs>
                  <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#60A5FA" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#60A5FA" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="name" stroke="#9CA3AF" />
                <YAxis stroke="#9CA3AF" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1F2937',
                    border: 'none',
                    borderRadius: '0.5rem',
                    color: '#F3F4F6',
                  }}
                />
                <Area
                  type="monotone"
                  dataKey="price"
                  stroke="#60A5FA"
                  fillOpacity={1}
                  fill="url(#colorPrice)"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-gray-800 p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-bold mb-4 text-gray-100">Top Cryptocurrencies</h2>
          <div className="space-y-4">
            {cryptoData.map((crypto) => (
              <div
                key={crypto.id}
                className="flex items-center justify-between p-3 bg-gray-700 rounded-lg hover:bg-gray-600 transition-colors"
              >
                <div className="flex items-center space-x-3">
                  <img src={crypto.image} alt={crypto.name} className="w-8 h-8" />
                  <div>
                    <p className="font-medium text-gray-100">{crypto.name}</p>
                    <p className="text-sm text-gray-400">
                      Vol: ${formatLargeNumber(crypto.total_volume)}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="font-medium text-gray-100">{formatPrice(crypto.current_price)}</p>
                  <div className="flex items-center justify-end space-x-1">
                    {crypto.price_change_percentage_24h >= 0 ? (
                      <TrendingUp size={14} className="text-green-400" />
                    ) : (
                      <TrendingDown size={14} className="text-red-400" />
                    )}
                    <span
                      className={`text-sm ${
                        crypto.price_change_percentage_24h >= 0 ? 'text-green-400' : 'text-red-400'
                      }`}
                    >
                      {crypto.price_change_percentage_24h.toFixed(2)}%
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;