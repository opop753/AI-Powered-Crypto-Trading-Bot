import pandas as pd  # Importing pandas for DataFrame operations
from binance import Client as BinanceClient  # Importing BinanceClient for API access
# Import necessary functions
from data.fetchBinanceWithBacktesting import fetch_binance_data
from data.fetchBitvavoWithBacktesting import fetch_bitvavo_data

def fetch_combined_data(symbol_binance='BTCUSDT', symbol_bitvavo='BTC-EUR', symbol_alpaca='AAPL', symbol_coingecko='bitcoin', interval='1h', lookback='730 days ago UTC'):
    # Fetch data from Binance
    binance_data = fetch_binance_data(symbol=symbol_binance, interval=interval, lookback=lookback)
    
    # Fetch data from Bitvavo
    bitvavo_data = fetch_bitvavo_data(symbol=symbol_bitvavo, interval=interval)

    # Fetch data from Alpaca
    alpaca_data = fetch_alpaca_data(symbol=symbol_alpaca, interval=interval)

    # Fetch data from Coingecko
    coingecko_data = fetch_coingecko_data(symbol=symbol_coingecko, interval=interval)

    # Import necessary functions
    from alpaca_data.fetchAlpacaWithBacktesting import fetch_alpaca_data
    from coingecko_data.fetchCoingeckoWithBacktesting import fetch_coingecko_data
    import pandas as pd
    from utils.display_data import display_data
    from binance_data.fetchBinanceWithBacktesting import fetch_binance_data
    from bitvavo_data.fetchBitvavoWithBacktesting import fetch_bitvavo_data

def fetch_combined_data(symbol_binance='BTCUSDT', symbol_bitvavo='BTC-EUR', symbol_alpaca='AAPL', symbol_coingecko='bitcoin', interval='1h', lookback='730 days ago UTC'): 
    # Combine the data
    combined_data = pd.concat([ fetch_binance_data(symbol="BTCUSDT", interval="1h", lookback="730 days ago UTC"),
                                fetch_alpaca_data(symbol="AAPL", interval="1h"),
                                fetch_coingecko_data(symbol="bitcoin", interval="1h"),
                                fetch_bitvavo_data(symbol="BTC-EUR", interval='1h')], axis=1) # pd.DataFrame([(fetch_binance_data(symbol='BTCUSDT', interval='1h', lookback='730 days ago UTC')], axis=1)", interval=interval)], axis=1)
    
    return combined_data

if __name__ == "__main__":
    combined_data = fetch_combined_data()
    display_data(combined_data)