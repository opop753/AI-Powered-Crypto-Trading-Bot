import os
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
import requests

# Add the parent directory to Python path to allow relative imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.coinGeckoApi import fetch_coingecko_data

def get_available_symbols():
    """Get and format available symbols from CoinGecko with caching"""
    cache_file = Path(__file__).parent / '.coingecko_symbol_cache.json'
    cache_max_age = timedelta(hours=1)  # Cache valid for 1 hour
    
    # Try to load from cache first
    if cache_file.exists():
        try:
            with open(cache_file) as f:
                cache_data = json.load(f)
                cache_time = datetime.fromisoformat(cache_data['timestamp'])
                if datetime.now() - cache_time < cache_max_age:
                    return cache_data['symbols']
        except (json.JSONDecodeError, KeyError, ValueError):
            pass
    
    # If cache miss or invalid, fetch from API
    try:
        response = requests.get('https://api.coingecko.com/api/v3/coins/list')
        response.raise_for_status()
        coins = response.json()
        
        # Extract and format symbols
        symbols = [{
            'symbol': coin['symbol'].upper(),
            'id': coin['id'],
            'name': coin['name']
        } for coin in coins]
        
        # Sort by symbol
        symbols.sort(key=lambda x: x['symbol'])
        
        # Save to cache
        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'symbols': symbols
        }
        try:
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f)
        except IOError:
            pass  # Ignore cache write failures
        
        return symbols
    except Exception as e:
        print(f"Error fetching symbols: {e}")
        return []

def display_available_symbols(symbols, columns=6):
    """Display symbols in a formatted grid"""
    print("\nAvailable symbols:")
    
    # First show popular symbols
    popular_ids = ['bitcoin', 'ethereum', 'solana', 'binancecoin', 'ripple', 'cardano', 'polkadot', 'dogecoin']
    popular = [s for s in symbols if s['id'] in popular_ids]
    
    print("\033[1mPopular:\033[0m ")
    for i, sym in enumerate(popular):
        print(f"\033[36m{sym['symbol']}\033[0m", end='')
        if i < len(popular) - 1:
            print(", ", end='')
    
    # Then show all symbols in columns
    print("\n\n\033[1mAll available symbols:\033[0m")
    # Create rows of symbols
    for i in range(0, len(symbols), columns):
        row = symbols[i:i + columns]
        # Format each symbol with its name
        formatted_row = [f"\033[33m{s['symbol']:<8}\033[0m" for s in row]
        print("  ".join(formatted_row))
    print()

def get_coingecko_data(symbol=None, timeframe='1h'):
    try:
        data = fetch_coingecko_data(symbol, timeframe)
        return data
    except Exception as e:
        return {'error': str(e)}

def print_historical_summary(data):
    if 'historical_data' not in data:
        return
    
    hist = data['historical_data']
    if not hist:
        return
        
    print(f"\nHistorical Data ({data['timeframe']})")
    print(f"First record: {hist[0]['time']}")
    print(f"Last record: {hist[-1]['time']}")
    
    prices = [float(x['price']) for x in hist]
    high = max(prices)
    low = min(prices)
    avg = sum(prices) / len(prices)
    
    print(f"Highest price: {high:.2f}")
    print(f"Lowest price: {low:.2f}")
    print(f"Average price: {avg:.2f}")
    print(f"Number of records: {len(hist)}")

if __name__ == '__main__':
    # Get and display available symbols
    print("Fetching available symbols...")
    symbols = get_available_symbols()
    display_available_symbols(symbols)
    
    # Get user input
    symbol = input('\nEnter symbol from the list above: ').upper()
    timeframe = input('Enter timeframe (1m, 1h, 1d, 30d): ')
    
    # Find the coin id for the entered symbol
    coin_info = next((s for s in symbols if s['symbol'] == symbol), None)
    if not coin_info:
        print(f"\n\033[31mError: Symbol {symbol} not found!\033[0m")
        sys.exit(1)
    
    print(f"\nFetching data for {coin_info['name']} ({symbol})...")
    data = get_coingecko_data(coin_info['id'], timeframe)
    
    print('\nCoinGecko Data:')
    if isinstance(data, dict):
        if 'error' in data:
            print(f"\033[31mError: {data['error']}\033[0m")
        else:
            for key, value in data.items():
                if key not in ['historical_data']:
                    print(f'\033[1m{key}:\033[0m {value}')
            
            print_historical_summary(data)
    else:
        # Handle list of coins case
        for coin in data[:10]:  # Show first 10 coins
            print(f"\n{coin.name} ({coin.symbol})")
            print(f"Price: ${coin.current_price:,.2f}")
            print(f"24h Change: {coin.price_change_percentage_24h:.2f}%")
