import pandas as pd
import numpy as np
import plotly.graph_objects as go
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
import os
import pathlib

class MovingAverageCrossover:
    def __init__(self, data, short_window=50, long_window=200):
        self.data = data
        self.short_window = short_window
        self.long_window = long_window
        self.signals = pd.DataFrame(index=data.index)
        self.signals['price'] = data['close']
        self.signals['SMA50'] = data['close'].rolling(window=self.short_window, min_periods=1).mean()
        self.signals['SMA200'] = data['close'].rolling(window=self.long_window, min_periods=1).mean()
        self.signals['signal'] = 0.0

    def calculate_indicators(self):
        # Calculate Exponential Moving Averages
        self.signals['EMA50'] = self.signals['price'].ewm(span=50, adjust=False).mean()
        self.signals['EMA200'] = self.signals['price'].ewm(span=200, adjust=False).mean()
        # Calculate RSI
        rsi = RSIIndicator(close=self.signals['price'], window=14)
        self.signals['RSI'] = rsi.rsi()
        # Calculate Bollinger Bands
        bollinger = BollingerBands(close=self.signals['price'], window=20, window_dev=2)
        self.signals['Bollinger_High'] = bollinger.bollinger_hband()
        self.signals['Bollinger_Low'] = bollinger.bollinger_lband()
        self.calculate_indicators()  # Calculate indicators before generating signals
        self.signals.loc[self.short_window:, 'signal'] = \
            np.where(self.signals['SMA50'][self.short_window:] > self.signals['SMA200'][self.short_window:], 1.0, 0.0)   
        self.signals['positions'] = self.signals['signal'].diff()  # Use .loc for assignment

    def backtest(self, initial_capital=10000, commission=0.002):
        self.calculate_indicators()  # Calculate indicators before generating signals
        self.signals.loc[self.short_window:, 'signal'] = \
            np.where(self.signals['SMA50'][self.short_window:] > self.signals['SMA200'][self.short_window:], 1.0, 0.0)   
        self.signals['positions'] = self.signals['signal'].diff()  # Use .loc for assignment
        self.plot_results()  # Call the plot function after backtesting
        self.signals['holdings'] = (self.signals['positions'] * self.signals['price']).cumsum()
        self.signals['cash'] = initial_capital - (self.signals['positions'] * self.signals['price']).cumsum()
        self.signals['total'] = self.signals['cash'] + self.signals['holdings']
        self.signals['returns'] = self.signals['total'].pct_change()
        self.signals['strategy_returns'] = self.signals['returns'] - commission
        return self.signals

    def plot_results(self):
        # Create a directory for plots in the user's home directory if it doesn't exist
        home_dir = str(pathlib.Path.home())
        plots_dir = os.path.join(home_dir, 'plots')
        if not os.path.exists(plots_dir):
            os.makedirs(plots_dir)
        fig = go.Figure()
        # Plot the price data
        fig.add_trace(go.Scatter(x=self.data.index, y=self.data['close'], mode='lines', name='Price', line=dict(color='blue')))
        # Plot the short and long moving averages
        fig.add_trace(go.Scatter(x=self.signals.index, y=self.signals['SMA50'], mode='lines', name='SMA50', line=dict(color='orange')))
        fig.add_trace(go.Scatter(x=self.signals.index, y=self.signals['SMA200'], mode='lines', name='SMA200', line=dict(color='red')))
        # Plot EMA lines
        fig.add_trace(go.Scatter(x=self.signals.index, y=self.signals['EMA50'], mode='lines', name='EMA50', line=dict(color='purple')))
        fig.add_trace(go.Scatter(x=self.signals.index, y=self.signals['EMA200'], mode='lines', name='EMA200', line=dict(color='brown')))
        # Plot RSI
        fig.add_trace(go.Scatter(x=self.signals.index, y=self.signals['RSI'], mode='lines', name='RSI', line=dict(color='cyan')))
        # Plot Bollinger Bands
        fig.add_trace(go.Scatter(x=self.signals.index, y=self.signals['Bollinger_High'], mode='lines', name='Bollinger High', line=dict(color='green', dash='dash')))
        fig.add_trace(go.Scatter(x=self.signals.index, y=self.signals['Bollinger_Low'], mode='lines', name='Bollinger Low', line=dict(color='red', dash='dash')))
        # Plot buy signals
        buy_signals = self.signals[self.signals['positions'] == 1]
        fig.add_trace(go.Scatter(x=buy_signals.index, y=buy_signals['price'], mode='markers', name='Buy Signal', marker=dict(color='green', size=10)))
        # Plot sell signals
        sell_signals = self.signals[self.signals['positions'] == -1]
        fig.add_trace(go.Scatter(x=sell_signals.index, y=sell_signals['price'], mode='markers', name='Sell Signal', marker=dict(color='red', size=10)))
        # Update layout
        fig.update_layout(title='Moving Average Crossover Strategy', xaxis_title='Date', yaxis_title='Price', legend_title='Legend')
        # Add your name to the plot
        fig.add_annotation(
            text="OnlyForward0613",
            xref="paper", yref="paper",
            x=0.5, y=1.05,
            showarrow=False,
            font=dict(size=16)
        )
        # Save the plot as an HTML file in the user's home directory
        fig.write_html(os.path.join(plots_dir, 'moving_average_crossover_plot.html'))  # Save the plot as an HTML file
