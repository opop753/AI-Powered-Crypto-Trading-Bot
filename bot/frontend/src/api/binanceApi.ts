export interface BinanceData {
  // Define your data structure here
  symbol: string;
  price: number;
  // ... other fields
}

const API_BASE_URL = 'http://localhost:5000'; // Single API base URL

export async function fetchBinanceData(): Promise<BinanceData[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/binance-data`);
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(`API error: ${response.status} - ${errorData.error || 'Unknown error'}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching Binance data:', error);
    throw error;
  }
}
