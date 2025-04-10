from keras.layers import Dense, Input, Conv1D, Flatten
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from pandas import DataFrame as df

def train_RNNLSTM(X_train, y_train, lookback=730, units=50, epochs=100):
    model = RNNLSTM(units)
    model.train(X_train, y_train, epochs=epochs)
    return model

def train_test_split(X, y, test_size=0.2, random_state=42):
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    return X_train, X_test, y_train, y_test

def predict_RNNLSTM(model, X_test, lookback=730):
    predictions = model.predict(X_test)
    return predictions

def RNNLSTM(df):
    df = df.load(df)
    X = df.drop('target', axis=1)
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = train_RNNLSTM(X_train, y_train)
    accuracy = evaluate_RNNLSTM(model, X_test, y_test)
    return model, accuracy