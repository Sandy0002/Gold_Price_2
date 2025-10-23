# In this program we will be training data by taking inputs from sequence_creator.py 

import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import matplotlib.pyplot as plt
from src.sequence_creator import prepare_data


def training():
    # Getting data from sequence_creator
    xTrain,xTest,yTrain,yTest,scaler = prepare_data()

    model = Sequential([
        # IN layer 1: 50 : Number of neurons, input_shape: timesteps,features, dropout is to remove some neurons randomly to avoid overfitting, return_sequence is for  outputs the entire sequence to the next LSTM layer (needed when stacking LSTMs).
        LSTM(50, return_sequences=True, input_shape=(xTrain.shape[1], 1)), Dropout(0.2),
        LSTM(50, return_sequences=False), Dropout(0.2),

        # Fully connected layer with 25 neurons. ReLU helps capture non-linear relationships between past and future prices.
        Dense(25, activation='relu'),
        Dense(1)
    ])

    model.compile(optimizer='adam', loss='mean_squared_error')
    # model.summary()


    # ===== 5. Train =====
    # here batch_size gives how many samples (sequences) the model processes before updating weights during training.
    history = model.fit(xTrain, yTrain, epochs=20, batch_size=32, validation_data=(xTest, yTest), verbose=1)

    os.makedirs("models", exist_ok=True)  # create folder if it doesn't exist
    model.save("models\\gold_lstm_model.h5")

    return xTest,yTest,scaler