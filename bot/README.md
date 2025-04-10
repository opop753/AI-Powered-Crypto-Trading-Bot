# Trading Bot Documentation

## Overview
This trading bot implements various trading strategies using historical data from Binance and Bitvavo. It includes a moving average crossover strategy, along with several technical indicators.

## Features
- Fetch historical data from Binance and Bitvavo.
- Implement moving average crossover strategy.
- Calculate various technical indicators (SMA, EMA, RSI, Bollinger Bands).
- Backtest strategies and visualize results.

## Features
- Fetch historical data from Binance and Bitvavo.
- Implement moving average crossover strategy.
- Calculate various technical indicators (SMA, EMA, RSI, Bollinger Bands).
- Backtest strategies and visualize results.

## Installation
1. Clone the repository.
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
- To fetch data and run backtests, use the following command:
  ```bash
  python data/fetchBinanceWithBacktesting.py
- To test the data fetching functionality, run:
  ```bash
  python bot/data/test_fetchBitvavo.py
  ```

## Contributing
Feel free to submit issues or pull requests for improvements or new features.

## License
This project is licensed under the MIT License.
