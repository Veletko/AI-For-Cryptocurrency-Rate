import datetime
import pandas as pd
import yfinance as yf
import numpy as np
from keras._tf_keras.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# Загрузка нейронной сети из файла
model = load_model('ai_models/ai_for_NVDA_price_pridiction.h5')
scaler = MinMaxScaler()

def get_prediction(data):
    scaled_data = scaler.fit_transform(data)
    x_test = np.array([scaled_data])
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    prediction = model.predict(x_test)
    prediction = scaler.inverse_transform(prediction)
    return prediction

# Получение данных за 1 месяц, начиная с сегодняшней даты
end_date = datetime.datetime.now().strftime('%Y-%m-%d')
start_date = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
ticker = 'NVDA'  # Пример тикера акции (Apple)
data = yf.download(ticker, start=start_date, end=end_date)
data = data.filter(['Close'])

# Прогнозирование цен на каждый день месяца и на следующий день
predicted_prices = []
for i in range(len(data)):
    prediction = get_prediction(data.iloc[:i+1])
    predicted_prices.append(prediction[-1][0])

# Прогноз на следующий день
last_30_days_data = data['Close'].values.reshape(-1, 1)
prediction = get_prediction(last_30_days_data)[-1]

# Добавление обновленного списка предсказанных цен к данным
data['Predicted Price'] = predicted_prices

# Построение графика цен на акции за месяц с предсказанными ценами на каждый день
plt.figure(figsize=(12, 6))
plt.plot(data.index, data['Close'], label='Actual Price')
plt.plot(data.index, data['Predicted Price'], marker='o', markersize=8, label='Predicted Price', color='red')
plt.title('Stock Prices for '+ticker)
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()

# Добавление точки с предсказанием на следующий день
plt.scatter(data.index[-1] + datetime.timedelta(days=1), prediction, color='g', label='Предсказание на следующий день')

plt.title('График цен на месяц с предсказанием')
plt.xlabel('Дата')
plt.ylabel('Цена закрытия')
plt.legend()
plt.grid()
plt.show()

plt.show()