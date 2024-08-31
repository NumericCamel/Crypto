
import os 
import sys
import pandas as pd 
import numpy as np

from pipeline_crypto_prices import get_prices

# Deep Learning
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense


sys.path.append('P:/6. DSMA/99. Thesis/Github/thesis/scripts')
path = 'C:/Users/mulle/Documents/iCloudDrive\Documents/19. GITHUB/Crypto'
os.chdir(path)


# Get latest prices to feed into model
#btc = get_prices(start_date='2018-01-01')
#btc.to_csv('btc.csv')

btc = pd.read_csv('btc.csv', index_col=0)


def create_sequences(data, target, n_steps_in, n_steps_out):
    X, y = [], []
    for i in range(len(data) - n_steps_in - n_steps_out + 1):
        # Gather input and output parts of the pattern
        end_ix = i + n_steps_in
        seq_x = data[i:end_ix]
        seq_y = target[end_ix:end_ix + n_steps_out]
        X.append(seq_x)
        y.append(seq_y)
    return np.array(X), np.array(y)

# Prepare input and target columns
input_columns = btc.drop(columns=['Close']).values  # Exclude 'Close' if it's not part of inputs
close_prices = btc['Close'].values  # Target variable

n_steps_in, n_steps_out = 30, 7
X, y = create_sequences(input_columns, close_prices, n_steps_in, n_steps_out)

# Define model
model = Sequential([
    LSTM(50, activation='relu', input_shape=(n_steps_in, X.shape[2])),  # Ensure this matches the number of input features
    Dense(n_steps_out)
])
model.compile(optimizer='adam', loss='mse')

# Fit model
model.fit(X, y, epochs=20, verbose=1)

# Prepare the last known sequence (last 30 days)
x_input = X[-1]  # Taking the last available sequence from X
x_input = x_input.reshape((1, n_steps_in, X.shape[2]))  # Match the LSTM input shape

# Predict the next 7 days
predicted_days = model.predict(x_input, verbose=0)
print(predicted_days)




