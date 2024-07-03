import pandas as pd
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import os

# Функция для загрузки данных о котировках из Yahoo Finance
def download_stock_data(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    return data

# Функция для сохранения данных в CSV файл
def save_data_to_csv(data, filename):
    data.to_csv(filename)

# Функция для подготовки данных для обучения
def prepare_data(data):
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(data)
    return scaler, scaled_data

# Параметры для загрузки и обработки данных
symbol_for_AAPL = 'AAPL'
symbol_for_MSFT = 'MSFT'
symbol_for_NVDA = 'NVDA'
start_date = '2012-01-01'
end_date = '2023-12-12'
data_filename_for_AAPL= 'data/AAPL_stock_data.csv'
data_filename_for_MSFT= 'data/MSFT_stock_data.csv'
data_filename_for_NVDA= 'data/NVDA_stock_data.csv'
# Загрузка данных
stock_data = download_stock_data(symbol_for_NVDA, start_date, end_date)

# Сохранение данных в CSV файл
save_data_to_csv(stock_data, data_filename_for_NVDA)

