import React, { useEffect, useState } from 'react';
import fetchCoinGeckoDataDisplay from '../api/coinGeckoApi.tsx';
import CoinGeckoChart from '../components/CoinGeckoChart.tsx';
import CoinGeckoTable from '../components/CoinGeckoTable.tsx';
import CoinGeckoHeader from '../components/CoinGeckoHeader.tsx';
import './CoinGeckoDataDisplay.css'; // We'll create this file for styling

// Define a type for the CoinGecko data
interface CoinGeckoData {
  prices: number[][]; // Adjust this type based on the actual structure of the data
}

const CoinGeckoDataDisplay: React.FC = () => {
  const [data, setData] = useState<CoinGeckoData | null>(null); // Use the defined type
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        const CoinGeckoDataDisplay = await fetchCoinGeckoDataDisplay();
        console.log("Fetched CoinGecko Data:", CoinGeckoDataDisplay); // Log the fetched data
        setData(CoinGeckoDataDisplay);
        setError(null);
      } catch (err) {
        setError('Failed to load data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  return (
    <div>
      <h1>CoinGecko Data Display</h1>
      {loading && <p>Loading data...</p>}
      {error && <p>Error: {error}</p>}
      {!loading && !error && data && data.prices.length > 0 && (
        <CoinGeckoChart data={data} /> // Render the CoinGeckoChart component
      )}
      {!loading && !error && data && data.prices.length === 0 && <p>No data available</p>}
    </div>
  );
};

export default CoinGeckoDataDisplay;