# fetch historical data from Binance, returns a dataframe
def fetch_binance_data(symbol='BTCUSDT', interval='1h', lookback='730 days ago UTC', strategy='MovingAverageCrossover'):
    binance_client = BinanceClient(BINANCE_API_KEY, BINANCE_API_SECRET)
    klines = binance_client.get_historical_klines(symbol, BinanceClient.KLINE_INTERVAL_1DAY, lookback)
    data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'SMA', 'EMA', 'RSI', 'target'])
    data['close'] = pd.to_numeric(data['close'], errors='coerce')
    data['close'] = data['close'].astype(float)
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    binance_data = data
# Run Backtest
    bt = Backtest(data, strategy, cash=10_000, commission=0.002)
    stats = bt.run()

# Display Results
    print(stats)
    bt.plot()
    return data
