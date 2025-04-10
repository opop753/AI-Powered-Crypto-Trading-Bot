export interface CryptoData {
    symbol: string;
    current_price: number;
    price_change_24h?: number;
    price_change_percentage_24h: number;
    volume_24h: number;
    timeframe?: string;
    historical_data?: {
        time: string;
        price: number;
        volume?: number;
    }[];
}

export type TimeFrame = '1m' | '1h' | '1d' | '30d';
export type DataSource = 'binance' | 'coingecko';
