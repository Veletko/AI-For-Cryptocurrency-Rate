import math
import pandas_datareader as web
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras._tf_keras.keras.models import Sequential
from keras._tf_keras.keras.layers import Dense,LSTM
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
file_name_for_AAPL = 'data/AAPL_stock_data.csv'
file_name_for_MSFT = 'data/MSFT_stock_data.csv'
file_name_for_NVDA = 'data/NVDA_stock_data.csv'
df = pd.read_csv(file_name_for_MSFT)
data = df.filter(['Close'])
dataset = data.values
traning_data_len = math.ceil(len(dataset)*.8)
scaler = MinMaxScaler(feature_range=(0,1))
scaler_data = scaler.fit_transform(dataset)
traning_data = scaler_data[0:traning_data_len,:]
x_train = []
y_train = []
for i in range(60,len(traning_data)):
    x_train.append(traning_data[i-60:i,0])
    y_train.append(traning_data[i,0])
x_train,y_train =np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train,(x_train.shape[0],x_train.shape[1],1))
model = Sequential()
model.add(LSTM(100,return_sequences=True,input_shape=(x_train.shape[1],1)))
model.add(LSTM(75,return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))
model.compile(optimizer='adam',loss='mean_squared_error')
model.fit(x_train,y_train,batch_size=1,epochs=1)
#model.save('ai_models/ai_for_MSFT_price_pridiction.h5')


test_data = scaler_data[traning_data_len-60:,:]
x_test=[]
y_test = dataset[traning_data_len:,:]
for i in range(60,len(test_data)):
    x_test.append(test_data[i-60:i,0])
x_test=np.array(x_test)
x_test = np.reshape(x_test,(x_test.shape[0],x_test.shape[1],1))
predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)
# Построение графика
train = data[:traning_data_len]
valid = data[traning_data_len:]
valid['Predictions'] = predictions

plt.figure(figsize=(16,8))
plt.title('Model')
plt.xlabel('Date', fontsize=18)
plt.ylabel('Close Price USD ($)', fontsize=18)
plt.plot(train['Close'])
plt.plot(valid[['Close', 'Predictions']])
plt.legend(['Train', 'Actual', 'Predictions'], loc='lower right')
plt.show()
rmse = np.sqrt(np.mean(predictions - y_test )**2)
print(rmse)
