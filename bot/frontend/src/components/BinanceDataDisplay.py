import os
from binance.client import Client
from datetime import datetime, timedelta

def get_binance_data(symbol, timeframe='1h'):
    # Initialize Binance client
    BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
    BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')
    client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)
    
    # Convert symbol to uppercase and ensure it ends with USDT if not specified
    symbol = symbol.upper()
    if not symbol.endswith('USDT'):
        symbol = f'{symbol}USDT'
    
    # Map timeframe to Binance intervals and lookback period
    timeframe_map = {
        '1m': (Client.KLINE_INTERVAL_1MINUTE, '1 hour'),
        '1h': (Client.KLINE_INTERVAL_1HOUR, '1 day'),
        '1d': (Client.KLINE_INTERVAL_1DAY, '30 days'),
        '30d': (Client.KLINE_INTERVAL_1DAY, '90 days')
    }
    
    interval, lookback = timeframe_map.get(timeframe, (Client.KLINE_INTERVAL_1HOUR, '1 day'))
    
    try:
        # Get ticker information
        ticker = client.get_ticker(symbol=symbol)
        
        # Get historical klines (candlestick) data
        klines = client.get_historical_klines(
            symbol=symbol,
            interval=interval,
            start_str=f"{lookback} ago UTC"
        )
        
        # Process historical data
        historical_data = []
        for k in klines:
            historical_data.append({
                'time': datetime.fromtimestamp(k[0]/1000).strftime('%Y-%m-%d %H:%M:%S'),
                'open': float(k[1]),
                'high': float(k[2]),
                'low': float(k[3]),
                'close': float(k[4]),
                'volume': float(k[5])
            })
        
        # Format the data
        data = {
            'symbol': symbol,
            'current_price': ticker['lastPrice'],
            'price_change': ticker['priceChange'],
            'price_change_percent': ticker['priceChangePercent'],
            '24h_volume': ticker['volume'],
            'timeframe': timeframe,
            'historical_data': historical_data
        }
        
        return data
    except Exception as e:
        return {'error': f'Error fetching data for {symbol}: {str(e)}'}

def print_historical_summary(data):
    if 'historical_data' not in data:
        return
    
    hist = data['historical_data']
    if not hist:
        return
        
    print(f"\nHistorical Data ({data['timeframe']})")
    print(f"First record: {hist[0]['time']}")
    print(f"Last record: {hist[-1]['time']}")
    
    # Calculate some statistics
    high = max(float(x['high']) for x in hist)
    low = min(float(x['low']) for x in hist)
    avg = sum(float(x['close']) for x in hist) / len(hist)
    
    print(f"Highest price: {high:.2f}")
    print(f"Lowest price: {low:.2f}")
    print(f"Average price: {avg:.2f}")
    print(f"Number of records: {len(hist)}")

import json
from pathlib import Path

def get_available_symbols(client):
    """Get and format available USDT trading pairs from Binance with caching"""
    cache_file = Path(__file__).parent / '.symbol_cache.json'
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
    exchange_info = client.get_exchange_info()
    
    # Filter for USDT pairs and extract base symbols
    usdt_symbols = []
    for symbol_info in exchange_info['symbols']:
        if symbol_info['symbol'].endswith('USDT') and symbol_info['status'] == 'TRADING':
            base_symbol = symbol_info['baseAsset']
            if base_symbol not in usdt_symbols:  # Avoid duplicates
                usdt_symbols.append(base_symbol)
    
    # Sort alphabetically
    usdt_symbols.sort()
    
    # Save to cache
    cache_data = {
        'timestamp': datetime.now().isoformat(),
        'symbols': usdt_symbols
    }
    try:
        with open(cache_file, 'w') as f:
            json.dump(cache_data, f)
    except IOError:
        pass  # Ignore cache write failures
    
    return usdt_symbols

def display_available_symbols(symbols, columns=8):
    """Display symbols in a formatted grid"""
    print("\nAvailable symbols:")
    
    # First show popular symbols
    popular = ['BTC', 'ETH', 'SOL', 'BNB', 'XRP', 'ADA', 'DOT', 'DOGE']
    popular_available = [sym for sym in popular if sym in symbols]
    print("\033[1mPopular:\033[0m ", end='')
    for i, sym in enumerate(popular_available):
        print(f"\033[36m{sym}\033[0m", end='')
        if i < len(popular_available) - 1:
            print(", ", end='')
    
    # Then show all symbols in columns
    print("\n\n\033[1mAll available symbols:\033[0m")
    for i in range(0, len(symbols), columns):
        row = symbols[i:i + columns]
        print("  ".join(f"\033[33m{sym:<5}\033[0m" for sym in row))
    print()

if __name__ == '__main__':
    # Initialize client
    BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
    BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')
    client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)
    
    # Get and display available symbols
    symbols = get_available_symbols(client)
    display_available_symbols(symbols)
    
    # Get user input
    symbol = input('Enter symbol from the list above: ')
    timeframe = input('Enter timeframe (1m, 1h, 1d, 30d): ')
    
    data = get_binance_data(symbol, timeframe)
    
    print('\nBinance Data:')
    for key, value in data.items():
        if key not in ['historical_data', 'error']:
            print(f'{key}: {value}')
    
    if 'error' in data:
        print(f"\nError: {data['error']}")
    else:
        print_historical_summary(data)
