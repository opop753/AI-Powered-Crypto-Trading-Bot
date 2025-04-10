from pandas import DataFrame as df
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def train_LSTM(X_train, y_train, lookback=730, units=50, epochs=100):
    timesteps=400           # dimensionality of the input sequence
    features=3            # dimensionality of each input representation in the sequence
    LSTMoutputDimension = 2 # dimensionality of the LSTM outputs (Hidden & Cell states)


def evaluate_lstm(model, X_test, y_test):
    predictions = model.predict(X_test)
    return accuracy_score(y_test, predictions)

def LSTM(df):
    df = df.load(df)
    X = df.drop('target', axis=1)
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = train_lstm(X_train, y_train)
    accuracy = evaluate_lstm(model, X_test, y_test)
    return model, accuracy
