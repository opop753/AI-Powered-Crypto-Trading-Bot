export interface Cryptocurrency {
  id: string;
  name: string;
  symbol: string;
  currentPrice: number;
  priceChange24h: number;
  marketCap: number;
  riskScore: number;
}

export interface WatchRule {
  id: string;
  cryptoId: string;
  condition: 'above' | 'below';
  price: number;
  action: 'buy' | 'sell';
  amount: number;
  active: boolean;
}

export interface Trade {
  id: string;
  cryptoId: string;
  type: 'buy' | 'sell';
  amount: number;
  price: number;
  timestamp: Date;
}

export interface WalletBalance {
  cryptoId: string;
  amount: number;
  averageBuyPrice: number;
}