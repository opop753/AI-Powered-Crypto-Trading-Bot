import sys
import os

#from bot.models.models import models
from keras.layers import Dense, Embedding, Dropout, Bidirectional, SimpleRNN, Conv1D, MaxPooling1D, Flatten, GlobalAveragePooling1D, BatchNormalization, Activation, Input, Dense, LSTM, Dropout, Bidirectional, GRU, SimpleRNN, Conv1D, MaxPooling1D, Flatten, GlobalAveragePooling1D, BatchNormalization, Activation, Input, Dense, LSTM, Dropout, Bidirectional, GRU, SimpleRNN, Conv1D, MaxPooling1D, Flatten, GlobalAveragePooling1D, BatchNormalization, Activation
from keras.models import Sequential, load_model
from keras.optimizers import Adam, RMSprop, Adagrad, Adadelta, Adamax, Nadam
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau, CSVLogger, TensorBoard
#from keras.utils import to_categorical, plot_model, to_categorical, normalize, get_user_data
from bot.models.xgboost import train_xgboost
from bot.models.randomForest import train_random_forest
from bot.models.rnn_lstm import train_RNNLSTM
from bot.models.lstm import train_LSTM


class Model:
    def __init__(self):
        self.model = Sequential()
        self.model.add(LSTM(units=50, return_sequences=True, input_shape=(None, 1)))
        self.model.add(LSTM(units=50))
        self.model.add(Dense(1, activation='sigmoid'))
        
        optimizer = Adam(learning_rate=0.001)
        self.model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
    
    def train(self, X_train, y_train, X_val=None, y_val=None, epochs=100):
        validation_data = (X_val, y_val) if X_val is not None and y_val is not None else None
        self.model.fit(X_train, y_train, epochs=epochs, batch_size=32, verbose=1, validation_data=validation_data)
    
    def predict(self, X):
        return self.model.predict(X)
    
    def evaluate(self, X_test, y_test):
        return self.model.evaluate(X_test, y_test)
    
    def save(self, filename):
        self.model.save(filename)
    
    def load(self, filename):
        self.model = tf.keras.models.load_model(filename)
    
    def summary(self):
        return self.model.summary()

def create_model(train_xgboost, train_random_forest, train_RNNLSTM, train_LSTM):
    if train_xgboost:
        return train_xgboost()
    elif train_random_forest:
        return train_random_forest()
    elif train_RNNLSTM:
        return train_RNNLSTM()
    elif train_LSTM:
        return train_LSTM()
    else:
        print("No model selected")
        return None
