import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Conv1D, Flatten, Dropout
from collections import deque
import random

# Load Data
def load_data(filename):
    df = pd.read_csv(filename)
    df.dropna(inplace=True)
    return df

# Split Data
def split_data(df, features, target):
    X = df[features]
    y = df[target].replace(-1, 0)  # Convert -1 to 0 for binary classification
    return train_test_split(X, y, test_size=0.2, shuffle=False)

# Train Random Forest
def train_Random_Forest(X_train, y_train, n_estimators=100):
    model = RandomForestClassifier(n_estimators=n_estimators)
    model.fit(X_train, y_train)
    return model

# Train XGBoost
def train_xgboost(X_train, y_train):
    model = xgb.XGBClassifier(objective='binary:logistic', use_label_encoder=False, eval_metric='logloss')
    model.fit(X_train, y_train)
    return model

# Visualization Functions
def plot_signals(df, predictions):
    df['Decision'] = predictions
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Price'))
    fig.add_trace(go.Scatter(x=df[df['Decision'] == 1].index, y=df[df['Decision'] == 1]['Close'], mode='markers', marker=dict(color='green', size=8), name='BUY'))
    fig.add_trace(go.Scatter(x=df[df['Decision'] == -1].index, y=df[df['Decision'] == -1]['Close'], mode='markers', marker=dict(color='red', size=8), name='SELL'))
    fig.update_layout(title='Trading Signals', xaxis_title='Time', yaxis_title='Price')
    fig.show()

def plot_feature_importance(model, features):
    importance = model.feature_importances_
    plt.figure(figsize=(10, 5))
    sns.barplot(x=importance, y=features)
    plt.title('Feature Importance')
    plt.show()

def plot_cumulative_returns(df, predictions):
    df['Strategy Returns'] = df['Returns'] * predictions
    df['Cumulative Returns'] = (1 + df['Strategy Returns']).cumprod()
    plt.figure(figsize=(10, 5))
    plt.plot(df['Cumulative Returns'], label='Strategy')
    plt.title('Cumulative Returns')
    plt.legend()
    plt.show()

def plot_exchange_data(data, exchange_name, color, model, features, predictions):
    fig, ax1 = plt.subplots(figsize=(12, 6))
    # Plot price data
    ax1.plot(data['timestamp'], data['close'], label=f'{exchange_name} BTC', color=color)
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price')
    ax1.legend(loc='upper left')
    
    # Plot key indicators on a secondary y-axis
    ax2 = ax1.twinx()
    if exchange_name == "binance":
        ax2.plot(data['timestamp'], data['SMA'], label='SMA', linestyle='dashed', color='pink')
    else:
        ax2.plot(data['timestamp'], data['SMA14'], label='SMA14', linestyle='dashed', color='pink')
    
    ax2.plot(data['timestamp'], data['EMA14'], label='EMA14', linestyle='dotted', color='yellow')
    ax2.plot(data['timestamp'], data['MACD'], label='MACD', linestyle='dashed', color='orange')
    ax2.plot(data['timestamp'], data['RSI'], label='RSI', linestyle='dashdot', color='aquamarine')
    ax2.plot(data['timestamp'], data['UpperBand'], label='UpperBand', linestyle=(0, (5, 2)), color='fuchsia')
    ax2.plot(data['timestamp'], data['MiddleBand'], label='MiddleBand', linestyle=(0, (5, 10)), color='darkgoldenrod')
    ax2.plot(data['timestamp'], data['LowerBand'], label='LowerBand', linestyle=(0, (10, 5)), color='gold')
    ax2.set_ylabel('Indicators')
    ax2.legend(loc='upper right')
    plt.title(f'Historical Crypto Data: {exchange_name}')
    plt.show()
    
    # Additional Visualizations
    plot_signals(data, predictions)
    plot_feature_importance(model, features)
    plot_cumulative_returns(data, predictions)

# Main Execution
if __name__ == "__main__":
    df = load_data('data/historical_data.csv')
    plot_exchange_data(df, "binance", "blue", model=None, features=None, predictions=None)
