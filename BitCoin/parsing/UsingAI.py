import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import yfinance as yf
from keras._tf_keras.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import mplcursors

def get_data_for_period(period_choice):

    end_date = datetime.datetime.now().strftime('%Y-%m-%d')
    
    if period_choice == 0:  # ��������� ������
        start_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    elif period_choice == 1:  # ��������� ��� ������
        start_date = (datetime.datetime.now() - datetime.timedelta(days=14)).strftime('%Y-%m-%d')
    else:  # ��������� �����
        start_date = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    
    ticker = 'NVDA'  # ������ ������ ����� (NVIDIA)
    data = yf.download(ticker, start=start_date, end=end_date)
    data = data.filter(['Close'])
    
    return data

def chart(period_choice):

    # �������� ��������� ���� �� �����
    model = load_model('ai_models/ai_for_NVDA_price_pridiction.h5')
    scaler = MinMaxScaler()

    def get_prediction(data):
        scaled_data = scaler.fit_transform(data)
        x_test = np.array([scaled_data])
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
        prediction = model.predict(x_test)
        prediction = scaler.inverse_transform(prediction)
        return prediction

    # ��������� ������ �� ��������� ������
    data = get_data_for_period(period_choice)
    
    # ��������������� ��� �� ������ ���� ������� � �� ��������� ����
    predicted_prices = []
    for i in range(len(data)):
        prediction = get_prediction(data.iloc[:i+1])
        predicted_prices.append(prediction[-1][0])

    # ������� �� ��������� ����
    last_days_data = data['Close'].values.reshape(-1, 1)
    prediction = get_prediction(last_days_data)[-1]

    # ���������� ������������ ������ ������������� ��� � ������
    data['Predicted Price'] = predicted_prices

    # ���������� ������� ��� �� ����� �� ������ � �������������� ������ �� ������ ����
    fig, ax = plt.subplots(figsize=(12, 6))

    # ��������� ����� ���� ������� � �� ��� ���������
    fig.patch.set_facecolor('#0f3464')
    ax.set_facecolor('#0B284D')

    # ��������� ������ �������
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # ��������� ����� ��� X � ����������� �� �������
    if period_choice == 0:  # ��������� ������
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))  # ����� ������ ����
    elif period_choice == 1:  # ��������� ��� ������
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))  # ����� ������ ��� ���
    else:  # ��������� �����
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))  # ����� ������ ��� ���

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%y'))  # ������ ����

    # ��������� ����� ��� X � �������������� ���������
    plt.xticks(rotation=0)

    actual_price_plot, = ax.plot(data.index, data['Close'], label='Actual Price', color='black')
    predicted_price_plot, = ax.plot(data.index, data['Predicted Price'], marker='o', markersize=8, label='Predicted Price', color='green')

    # ����� �� ��������� ������������� ���� �� ���������� ���
    next_day_date = data.index[-1] + datetime.timedelta(days=1)
    last_predicted_price = data['Predicted Price'].iloc[-1]
    next_day_prediction = prediction[0]  # ����� ������ �������, ��� ��� prediction ����� ���� ��������

    # �������� ����������� ����� � ���������� ����� ��������
    ax.plot([data.index[-1], next_day_date], [last_predicted_price, next_day_prediction], color='red', zorder=3)

    # ����� ��� ���������� ���
    next_day_point = ax.scatter(next_day_date, next_day_prediction, color='red', label='Prediction for the next day', zorder=5)

    ax.set_title('Price Chart with Prediction', color='black')
    ax.set_xlabel('Date', color='black')  # ���� ��� �������
    ax.set_ylabel('Closing Price', color='black')  # ���� ��� �������
    ax.tick_params(axis='x', colors='black')  # ���� ������� ��� �������
    ax.tick_params(axis='y', colors='black')  # ���� ������� ��� �������
    ax.legend()
    
    # ��������� �����
    ax.grid(color = "#0f3464")

    # ���������� ������������� ���������
    cursor = mplcursors.cursor([actual_price_plot, predicted_price_plot, next_day_point], hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f'{mdates.num2date(sel.target[0]).strftime("Date: %d.%m.%y")}\nPrice: ${sel.target[1]:.2f}'))

    # ���������� ����������� ������� ��� �������� ��������� ��� ������ �������
    def hide_annotation(event):
        if not ax.contains(event)[0]:
            for sel in cursor.selections:
                sel.annotation.set_visible(False)
            fig.canvas.draw_idle()

    fig.canvas.mpl_connect('motion_notify_event', hide_annotation)

    return fig