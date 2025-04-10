import os  # fetch historical data from Binance, returns a dataframe
from binance.client import Client as BinanceClient
import backtesting as bt
from datetime import datetime, timedelta, timezone
import pandas as pd

# Set Binance API keys
api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')
client = BinanceClient(api_key, api_secret)

# Function to fetch historical data
def fetch_historical_data(symbol, interval, start_str, end_str):
    klines = client.get_historical_klines(symbol, interval, start_str, end_str)
    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'SMA', 'EMA', 'RSI', 'target'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)
    df['volume'] = df['volume'].astype(float)
    return df

# Define trading signals
def target_price(data, window=14):
    data['SMA'] = data['close'].rolling(window).mean()
    data['EMA'] = data['close'].ewm(span=window, adjust=False).mean()
    data['RSI'] = bt.RSI(data['close'], 14)  # Use backtesting package for RSI
    data['target'] = data['close'] + (data['close'] - data['SMA']).shift(1) * 0.05
    return data

# Define trading signals
def generate_signals(data):
    data['SMA'] = data['close'].rolling(14).mean()
    data['EMA'] = data['close'].ewm(span=14, adjust=False).mean()
    data['RSI'] = bt.RSI(data['close'], 14)  # Use backtesting package for RSI
    data['target'] = 0.0
    data.loc[(data['SMA'] > data['EMA']) & (data['SMA'].shift(1) <= data['EMA'].shift(1)), 'target'] = 1.0  # Buy signal
    data.loc[(data['SMA'] < data['EMA']) & (data['SMA'].shift(1) >= data['EMA'].shift(1)), 'target'] = -1.0  # Sell signal
    return data

# Define trading strategy
def strategy(data):
    data['SMA'] = data['close'].rolling(14).mean()
    data['EMA'] = data['close'].ewm(span=14, adjust=False).mean()
    data['RSI'] = bt.RSI(data['close'], 14)  # Use backtesting package for RSI
    data['target'] = 0.0
    data.loc[(data['SMA'] > data['EMA']) & (data['SMA'].shift(1) <= data['EMA'].shift(1)), 'target'] = 1.0  # Buy signal
    data.loc[(data['SMA'] < data['EMA']) & (data['SMA'].shift(1) >= data['EMA'].shift(1)), 'target'] = -1.0  # Sell signal
    return data['SMA'] > data['EMA']  # Buy when SMA crosses above EMA

def fetch_binance_data(symbol='BTCUSDT', interval='1h', lookback='730 days ago UTC'):
    binance_client = BinanceClient(os.getenv("BINANCE_API_KEY"), os.getenv("BINANCE_API_SECRET"))
    klines = binance_client.get_historical_klines(symbol, BinanceClient.KLINE_INTERVAL_1DAY, lookback)
    data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'SMA', 'EMA', 'RSI', 'target'])
    data['close'] = pd.to_numeric(data['close'], errors='coerce')
    data['close'] = data['close'].astype(float)
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    data.set_index('timestamp', inplace=True)
    return data

def fetchBinanceWithBacktesting(symbol, interval, start, end):
    # Fetch data from Binance
    data = fetch_historical_data(symbol, interval, start, end)
    if data is None:
        return None

    # Prepare data for backtesting
    data = pd.DataFrame(data, columns=['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    data['open'] = data['open'].astype(float)
    data['high'] = data['high'].astype(float)
    data['low'] = data['low'].astype(float)
    data['close'] = data['close'].astype(float)
    data['volume'] = data['volume'].astype(float)
    data['open_time'] = pd.to_datetime(data['open_time'], unit='ms')
    data.set_index('open_time', inplace=True)

    # Define Strategy
    strategy = bt.SmaCross(20, 50)  # Use backtesting package for SmaCross
    backtest = bt.Backtest(strategy, data)  # Use backtesting package for Backtest
    backtest.run()
    backtest.plot()
    return data
