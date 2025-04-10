import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { CryptoData, TimeFrame, DataSource } from '../api/types';
import './Dashboard.css';

const Dashboard: React.FC = () => {
  const { source } = useParams<{ source: string }>();
  const navigate = useNavigate();
  const [dataSource, setDataSource] = useState<DataSource>((source as DataSource) || 'binance');
  const [symbol, setSymbol] = useState<string>('BTC');
  const [timeframe, setTimeframe] = useState<TimeFrame>('1h');
  const [data, setData] = useState<CryptoData | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);



 interface BinanceResponse {
  lastPrice: string;
  priceChangePercent: string;
  volume: string;
}

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      console.log(
        `Loading data for ${symbol} from ${dataSource} with ${timeframe} timeframe`
      );
      if (dataSource === 'binance') {
        const response = await axios.get<BinanceResponse>(
          `https://api.binance.com/api/v3/ticker/24hr?symbol=${symbol.toUpperCase()}USDT`
        );
        setData({
          symbol,
          current_price: parseFloat(response.data.lastPrice || "0"),
          price_change_percentage_24h: parseFloat(response.data.priceChangePercent || "0"),
          volume_24h: parseFloat(response.data.volume || "0")
        });
      } else if (dataSource === 'coingecko') {
        const response = await axios.get<CryptoData>(
          `https://api.coingecko.com/api/v3/coins/${symbol.toLowerCase()}/market_chart?vs_currency=usd&days=${timeframe}`
        );
        setData(response.data);
      }
    } catch (error) {
      setError('Failed to load data');
      console.error(error);
    } finally {
      setLoading(false);
    }
  }, [dataSource, symbol, timeframe]);

  useEffect(() => {
    if (source) {
      setDataSource(source === 'binance' ? 'binance' : 'coingecko');
      setSymbol(source === 'binance' ? 'BTC' : 'ETH');
      setTimeframe(source === 'binance' ? '1h' : '1d');
    } else {
      navigate('/source/binance', { replace: true });
    }
  }, [source, navigate]);

  useEffect(() => {
    loadData();
    const intervalId = setInterval(loadData, 60000); // Refresh every minute
    return () => clearInterval(intervalId);
  }, [loadData]);

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 8
    }).format(price);
  };

  const formatPercentage = (value: number) => {
    return `${value >= 0 ? '+' : ''}${value.toFixed(2)}%`;
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (!data) {
    return <div>No data available</div>;
  }

  return (
    <div>
      <h1>Crypto Dashboard</h1>
      <p>Symbol: {data.symbol}</p>
      <p>Current Price: {formatPrice(data.current_price)}</p>
      <p>Price Change (24h): {formatPercentage(data.price_change_percentage_24h)}</p>
      <p>Volume (24h): {formatPrice(data.volume_24h)}</p>
    </div>
  );
};

export default Dashboard;