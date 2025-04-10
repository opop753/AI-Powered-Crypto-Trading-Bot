import React from 'react';
import { CoinGeckoData } from '../api/coinGeckoApi';

interface CoinGeckoDataDisplayProps {
  data: CoinGeckoData | null;
}

const CoinGeckoDataDisplay: React.FC<CoinGeckoDataDisplayProps> = ({ data }) => {
  if (!data) {
    return <p>No data available</p>;
  }

  return (
    <div>
      <h3>CoinGecko Data</h3>
      <h4>Prices</h4>
      <ul>
        {data.prices.map((price, index) => (
          <li key={index}>
            Time: {new Date(price[0]).toLocaleString()} - Price: ${price[1].toFixed(2)}
          </li>
        ))}
      </ul>
      <h4>Market Caps</h4>
      <ul>
        {data.market_caps.map((marketCap, index) => (
          <li key={index}>
            Time: {new Date(marketCap[0]).toLocaleString()} - Market Cap: ${marketCap[1].toFixed(2)}
          </li>
        ))}
      </ul>
      <h4>Total Volumes</h4>
      <ul>
        {data.total_volumes.map((volume, index) => (
          <li key={index}>
            Time: {new Date(volume[0]).toLocaleString()} - Volume: ${volume[1].toFixed(2)}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CoinGeckoDataDisplay;
