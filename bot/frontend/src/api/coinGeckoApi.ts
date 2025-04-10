import axios from 'axios';
import CoinGeckoData from '../components/CoinGeckoDataDisplay';
export interface CoinGeckoData {
  // Define your data structure based on CoinGecko response
  prices: [number, number][];
  market_caps: [number, number][];
  total_volumes: [number, number][];
}

const API_BASE_URL = 'http://localhost:5001'; // Updated base URL to port 5001

export async function fetchCoinGeckoData(
  vsCurrency: string = 'usd',
  days: string = '30'
): Promise<CoinGeckoData> {
  try {
    const response = await fetch(
      `${API_BASE_URL}/api/coingecko?vs_currency=${vsCurrency}&days=${days}`
    );
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(`API error: ${response.status} - ${errorData.error || 'Unknown error'}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching CoinGecko data:', error);
    throw error;
  }
}
export const fetchCoinGeckoDataDisplay = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/api/coingecko`, {
            params: { vs_currency: 'usd', days: '30' }
        });
        return response.data;
    } catch (error) {
        console.error("Error fetching CoinGecko data:", error);
        throw error;
    } finally {
        console.log("CoinGecko data fetch completed.");
    }
};
