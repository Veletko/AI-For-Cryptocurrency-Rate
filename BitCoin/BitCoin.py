
import tkinter as tk
from tkinter.tix import ComboBox
from tkinter.ttk import Combobox
from tkinter import ttk
from keras.src.backend.tensorflow.trackable import sticky_attribute_assignment
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from cgitb import text
import datetime
import pandas as pd
import yfinance as yf
import numpy as np
from keras._tf_keras.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import parsing.UsingAI







#from parsing import TakeHistoricalData

window = tk.Tk()
window.configure(background='#0f3464')
#window.geometry("600x600")
window.title('My App')

frame_statistic = tk.Frame(window, width=150, height=550, bg = 'gray30')
frame_main = tk.Frame(window, width=600, height=550, bg = "#0f3464")

frame_statistic.grid(row = 0, column = 1, sticky="nswe")
frame_main.grid(row = 0, column = 0,sticky="nswe")

#диаграмма

# style = ttk.Style()
# style.configure("My.TCombobox", background="gray1", foreground='dodgerblue1') 
# style.map("My.TCombobox", background=[('readonly', 'gray1'), ('active', 'dodgerblue1')],
#                    foreground=[('readonly', 'dodgerblue1'), ('active', 'dodgerblue1')])
# combobox = ttk.Combobox(frame_main,values=pairs, style="My.TCombobox")

pairs = ["Apple","Microsoft", "Nvidia"]
combobox = ttk.Combobox(frame_main,values=pairs,background='gray1', foreground='dodgerblue1')
text = ttk.Label(frame_main, text = "Chart", background='gray1',foreground='dodgerblue1')
combobox.current(2)
text.grid(row = 0, column=0, sticky="w", padx = 10,pady =10 ) 
combobox.place(x=60,y=10) 




# ###ГРАФИК 

# Построение графика

# Функция для обновления графика (можно изменить данные или стиль графика)
number_date = 2
fig = parsing.UsingAI.chart(number_date)
canvas = FigureCanvasTkAgg(fig, master=frame_main)
canvas.draw()
canvas.get_tk_widget().grid(row =2, column=0,  sticky='w')


def update_plot(number_date):
    # Очистка текущего холста
    canvas.get_tk_widget().destroy()

    # Создание новой фигуры с обновленными данными
    new_fig = parsing.UsingAI.chart(number_date)
    
    # Создание нового холста с новой фигурой
    new_canvas = FigureCanvasTkAgg(new_fig, master=frame_main)
    new_canvas.draw()
    new_canvas.get_tk_widget().grid(row=2, column=0, sticky='w')


    
# Кнопка для обновления графика
button = tk.Button(frame_main, text = "Update", fg = "white", bg = "gray", command = update_plot) 
button.grid(row=1, column=0, padx = 10,pady =10, sticky= "w")







####ебанные кнопки
def change_button_color(button, button_id):
    # Сбрасываем цвет предыдущей выбранной кнопки
    for b in buttons:
        if b != button:
            b.config(bg="SystemButtonFace")  # Возвращаем стандартный цвет

    # Изменяем цвет выбранной кнопки
    button.config(bg="dodgerblue4")
    number_date = button_id
    update_plot(number_date)
   

      
    


# Создаем кнопки
frame_button = tk.Frame(window,bg = "#0f3464", padx=50)
frame_button.grid(row=5, column=0, sticky="nsew")

buttons = []
button_labels = ["week", "2 weeks", "month"]
for i, label in enumerate(button_labels): 
    button = tk.Button(frame_button, text=label)
    button.config(command=lambda b=button, idx=i: change_button_color(b, idx))  
    button.grid(row=0,column=i, sticky='w', padx=10)
    buttons.append(button)




###таблица
data = [
    ["Apple", "2", "3"],
    ["Microsoft", "5", "6"],
    ["Nvidia", "8", "9"]
]
heads = ['Name', '24h','Price']
table = ttk.Treeview(frame_statistic, show = 'headings')
table['columns']=heads
for header in heads:
    table.heading(header, text=header,anchor='center')
    table.column(header,anchor='center')


for row in data:
     table.insert('', tk.END, values=row)
     
table.pack(expand=tk.YES, fill=tk.BOTH)






















# sales.plot(kind='line', x='Year', y='Units sold(in millions)', 
#            color='orange', grid=True, 
#            title='Pok?mon Game Sales');
# pd.options.plotting.backend = 'holoviews'
# sales.plot(kind='line', x='Year', y='Units sold(in millions)', 
#            color='orange', grid=True, title='Pok?mon Game Sales', hover=False) \
#   * sales.plot(kind='scatter', x='Year', y='Units sold(in millions)', 
#                color='#c70000', hover_cols='Game')






window.mainloop()

