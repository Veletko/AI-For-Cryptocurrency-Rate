import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import yfinance as yf
from keras._tf_keras.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import mplcursors



def get_data_for_period(period_choice,ticker):

    end_date = datetime.datetime.now().strftime('%Y-%m-%d')
    
    if period_choice == 0:  # Последняя неделя
        start_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    elif period_choice == 1:  # Последние две недели
        start_date = (datetime.datetime.now() - datetime.timedelta(days=14)).strftime('%Y-%m-%d')
    else:  # Последний месяц
        start_date = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    
   
    data = yf.download(ticker, start=start_date, end=end_date)
    data = data.filter(['Close'])
    return data
  


def chart(period_choice,comboboxChoice):

    if comboboxChoice=="Apple":
       model = load_model('ai_models/ai_for_AAPL_price_pridiction.h5')
       ticker='AAPL'
       
    elif comboboxChoice =="Microsoft":
       model=load_model('ai_models/ai_for_MSFT_price_pridiction.h5')
       ticker='MSFT'
    else:
       model=load_model('ai_models/ai_for_NVDA_price_pridiction.h5')
       ticker='NVDA'
    scaler = MinMaxScaler()

    def get_prediction(data):
       scaled_data = scaler.fit_transform(data)
       x_test = np.array([scaled_data])
       x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
       prediction = model.predict(x_test)
       prediction = scaler.inverse_transform(prediction)
       
       return prediction
    
    
    # Получение данных за указанный период
    
    data = get_data_for_period(period_choice,ticker)
    
    # Прогнозирование цен на каждый день периода и на следующий день
    predicted_prices = []
    for i in range(len(data)):
        prediction = get_prediction(data.iloc[:i+1])
        predicted_prices.append(prediction[-1][0])

    # Прогноз на следующий день
    last_days_data = data['Close'].values.reshape(-1, 1)
    prediction = get_prediction(last_days_data)[-1]

    # Добавление обновленного списка предсказанных цен к данным
    data['Predicted Price'] = predicted_prices

    # Построение графика цен на акции за период с предсказанными ценами на каждый день
    fig, ax = plt.subplots(figsize=(12, 6))

    # Настройка цвета фона графика и за его пределами
    fig.patch.set_facecolor('#505191')
    ax.set_facecolor('#a9aae2')

    # Настройка границ графика
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Настройка меток оси X в зависимости от периода
    if period_choice == 0:  # Последняя неделя
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))  # Метки каждый день
    elif period_choice == 1:  # Последние две недели
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))  # Метки каждые два дня
    else:  # Последний месяц
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))  # Метки каждые три дня

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%y'))  # Формат даты

    # Оставляем метки оси X в горизонтальном положении
    plt.xticks(rotation=0)

    actual_price_plot, = ax.plot(data.index, data['Close'], label='Actual Price', color='#912324')
    predicted_price_plot, = ax.plot(data.index, data['Predicted Price'], marker='o', markersize=8, label='Predicted Price', color='#e69f29')

    # Линия от последней предсказанной цены до следующего дня
    next_day_date = data.index[-1] + datetime.timedelta(days=1)
    last_predicted_price = data['Predicted Price'].iloc[-1]
    next_day_prediction = prediction[0]  # Берем первый элемент, так как prediction может быть массивом

    # Создание непрерывной линии и добавление точки прогноза
    ax.plot([data.index[-1], next_day_date], [last_predicted_price, next_day_prediction], color='#fbfc84', zorder=3)

    # Точка для следующего дня
    next_day_point = ax.scatter(next_day_date, next_day_prediction, color='#fbfc84', label='Prediction for the next day', zorder=5)

    # # ax.set_xlabel('Date', color='#060747')  # Цвет оси абсцисс
    ax.set_ylabel('$', color='#060747')  # Цвет оси ординат
    ax.tick_params(axis='x', colors='#060747')  # Цвет делений оси абсцисс
    ax.tick_params(axis='y', colors='#060747')  # Цвет делений оси ординат
    ax.legend()
    
    # Настройка сетки
    ax.grid(color = "#505191")

    # Добавление интерактивных подсказок
    cursor = mplcursors.cursor([actual_price_plot, predicted_price_plot, next_day_point], hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f'{mdates.num2date(sel.target[0]).strftime("Date: %d.%m.%y")}\nPrice: ${sel.target[1]:.2f}'))

    # Добавление обработчика событий для удаления аннотации при выходе курсора
    def hide_annotation(event):
        if not ax.contains(event)[0]:
            for sel in cursor.selections:
                sel.annotation.set_visible(False)
            fig.canvas.draw_idle()

    fig.canvas.mpl_connect('motion_notify_event', hide_annotation)

    return fig