import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

import train_RNNLSTM, evaluate_RNNLSTM, rnn_lstm
import train_xgboost, evaluate_xgboost, XGBoost
import train_random_forest, evaluate_random_forest, randomForest
import train_lstm, evaluate_lstm, lstm

import random_forest
import moving_average_crossover


def train_test_split(X, y, test_size=0.2, random_state=42):
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    return X_train, X_test, y_train, y_test


def train_model(df):
    df = df.load(df)
    X = df.drop('target', axis=1)
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    if model == 'RNNLSTM':
        model = RNNLSTM.RNNLSTM()
        model.train(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f'Accuracy: {accuracy:.2f}')

    elif model == 'XGBoost':
        model = XGBoost.XGBoost()
        model.train(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f'Accuracy: {accuracy:.2f}')

    elif model == 'Random Forest':
        model = randomForest.randomForest()
        model.train(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f'Accuracy: {accuracy:.2f}')

    elif model == 'LSTM':
        model = LSTM.LSTM()
        model.train(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f'Accuracy: {accuracy:.2f}')

    else:
        print('Invalid model')
        return accuracy

    
class Model: 
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.model = None
        self.trained = False
        self.score = 0
    def train(self, data):
        self.model = train_model(self.model, data)
        self.trained = True
    def evaluate(self, data):
        if self.trained:
            self.score = evaluate_model(self.model, data).score
        else:
            self.score = 0
            return self.score
    def get_score(self):
        return self.score
    def get_name(self):
        return self.name
    def get_description(self):
        return self.description
    def get_model(self):
        return self.model
    def __repr__(self):
        return f"Model('{self.name}', '{self.description}')"
        # Create a dictionary of models
        models = {
            "LSTM": lstm(),
            "RNN-LSTM": rnn_lstm(),
            "XGBoost": xgboost(),
            "Random Forest": random_forest(),
            "Moving Average Crossover": moving_average_crossover()
        }
    def to_dict(self):
        return {"name": self.name, "description": self.description}
    def to_json(self):
        return json.dumps(self.to_dict())
    def from_json(self, json_str):
        data = json.loads(json_str)
        self.name = data["name"]
        self.description = data["description"]
    def __str__(self):
        return f"Model('{self.name}', '{self.description}')"
    def __eq__(self, other):
        return self.name == other.name and self.description == other.description
    def __hash__(self):
        return hash((self.name, self.description))
    def __lt__(self, other):
        return self.name < other.name
    def __le__(self, other):
        return self.name <= other.name
    def __gt__(self, other):
        return self.name > other.name
    def __ge__(self, other):
        return self.name >= other.name

models = {
    "LSTM": Model(lstm),
    "RNN-LSTM": Model(rnn_lstm),
    "XGBoost": Model(xgboost),
    "Random Forest": Model(random_forest),
    "Moving Average Crossover": Model(moving_average_crossover)
}
