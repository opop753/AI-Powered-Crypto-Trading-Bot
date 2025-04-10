import requests
from typing import Dict, Any, Optional
from datetime import datetime

class CoinGeckoData:
    def __init__(self, 
                 id: str,
                 symbol: str,
                 name: str,
                 current_price: float,
                 market_cap: float,
                 market_cap_rank: int,
                 price_change_24h: float,
                 price_change_percentage_24h: float,
                 volume_24h: float):
        self.id = id
        self.symbol = symbol
        self.name = name
        self.current_price = current_price
        self.market_cap = market_cap
        self.market_cap_rank = market_cap_rank
        self.price_change_24h = price_change_24h
        self.price_change_percentage_24h = price_change_percentage_24h
        self.volume_24h = volume_24h

def fetch_coingecko_data(symbol: Optional[str] = None, timeframe: str = '1h') -> Dict[str, Any]:
    """
    Fetch cryptocurrency data from CoinGecko API
    
    Args:
        symbol: Optional cryptocurrency symbol (e.g., 'BTC', 'ETH')
        timeframe: Time interval for historical data ('1m', '1h', '1d', '30d')
    
    Returns:
        Dictionary containing cryptocurrency data
    """
    try:
        # Map timeframe to CoinGecko parameters
        timeframe_map = {
            '1m': ('minute', 1),  # 1 minute data for last hour
            '1h': ('hourly', 1),  # Hourly data for last day
            '1d': ('daily', 30),  # Daily data for last 30 days
            '30d': ('daily', 90)  # Daily data for last 90 days
        }
        
        interval, days = timeframe_map.get(timeframe, ('hourly', 1))
        
        # Base API endpoint
        base_url = 'https://api.coingecko.com/api/v3'
        
        if symbol:
            # Convert symbol to CoinGecko ID format
            symbol_to_id = {
                'BTC': 'bitcoin',
                'ETH': 'ethereum',
                'SOL': 'solana',
                'USDT': 'tether',
                'BNB': 'binancecoin'
            }
            
            coin_id = symbol_to_id.get(symbol.upper(), symbol.lower())
            
            # Get specific coin data
            coin_url = f'{base_url}/coins/{coin_id}'
            market_chart_url = f'{coin_url}/market_chart'
            
            # Fetch current data
            response = requests.get(coin_url, params={
                'localization': False,
                'tickers': False,
                'community_data': False,
                'developer_data': False
            })
            coin_data = response.json()
            
            # Fetch historical data
            chart_response = requests.get(market_chart_url, params={
                'vs_currency': 'usd',
                'days': days,
                'interval': interval if interval == 'daily' else None
            })
            chart_data = chart_response.json()
            
            # Process historical data
            historical_data = []
            for price_data in chart_data['prices']:
                timestamp, price = price_data
                historical_data.append({
                    'time': datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d %H:%M:%S'),
                    'price': price
                })
            
            return {
                'id': coin_data['id'],
                'symbol': coin_data['symbol'].upper(),
                'name': coin_data['name'],
                'current_price': coin_data['market_data']['current_price']['usd'],
                'market_cap': coin_data['market_data']['market_cap']['usd'],
                'market_cap_rank': coin_data['market_cap_rank'],
                'price_change_24h': coin_data['market_data']['price_change_24h'],
                'price_change_percentage_24h': coin_data['market_data']['price_change_percentage_24h'],
                'volume_24h': coin_data['market_data']['total_volume']['usd'],
                'timeframe': timeframe,
                'historical_data': historical_data
            }
        else:
            # Get top 100 coins by market cap
            response = requests.get(f'{base_url}/coins/markets', params={
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': 100,
                'page': 1,
                'sparkline': False
            })
            
            coins_data = response.json()
            return [CoinGeckoData(
                id=coin['id'],
                symbol=coin['symbol'].upper(),
                name=coin['name'],
                current_price=coin['current_price'],
                market_cap=coin['market_cap'],
                market_cap_rank=coin['market_cap_rank'],
                price_change_24h=coin['price_change_24h'],
                price_change_percentage_24h=coin['price_change_percentage_24h'],
                volume_24h=coin['total_volume']
            ) for coin in coins_data]
            
    except Exception as e:
        raise Exception(f"Error fetching CoinGecko data: {str(e)}")
