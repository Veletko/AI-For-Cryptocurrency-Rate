
import tkinter as tk
from tkinter.tix import ComboBox
from tkinter.ttk import Combobox
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from cgitb import text

window = tk.Tk()
#window.configure(background='gray1')
#window.geometry("600x600")
window.title('My App')

frame_statistic = tk.Frame(window, width=150, height=550, bg = 'gray30')
frame_main = tk.Frame(window, width=600, height=550, bg = "#0f3464")

frame_statistic.grid(row = 0, column = 1, sticky="nswe")
frame_main.grid(row = 0, column = 0,sticky="nswe")

#диаграмма
pairs = ["BTC/USD","ETH/USD"]
# style = ttk.Style()
# style.configure("My.TCombobox", background="gray1", foreground='dodgerblue1') 
# style.map("My.TCombobox", background=[('readonly', 'gray1'), ('active', 'dodgerblue1')],
#                    foreground=[('readonly', 'dodgerblue1'), ('active', 'dodgerblue1')])
# combobox = ttk.Combobox(frame_main,values=pairs, style="My.TCombobox")


combobox = ttk.Combobox(frame_main,values=pairs,background='gray1', foreground='dodgerblue1')
text = ttk.Label(frame_main, text = "Chart", background='gray1',foreground='dodgerblue1')
combobox.current(0)
text.grid(row = 0, column=0, sticky="w", padx = 10,pady =10 ) 
combobox.place(x=80,y=10) 




# ###ГРАФИК 

fig = Figure(figsize=(5, 4), dpi=100)
plot = fig.add_subplot(1, 1, 1)
plot.plot([1, 2, 3, 4], [1, 4, 9, 16])  # Пример данных для графика

# Кнопка для обновления графика
button = tk.Button(frame_main, text = "Update", fg = "white", bg = "gray") #command = update_plot
button.grid(row=1, column=0, padx = 10,pady =10, sticky= "w")


# # Создаем холст для отображения графика в Tkinter
canvas = FigureCanvasTkAgg(fig, master= frame_main)
canvas.draw()
canvas.get_tk_widget().grid(row=2, column=0, rowspan=3, sticky="nsew")

# Функция для обновления графика (можно изменить данные или стиль графика)
def update_plot():
    plot.clear()
    plot.plot([1, 2, 3, 4], [1, 8, 27, 64], 'r--')  # Новые данные для графика
    canvas.draw()





####ебанные кнопки
def change_button_color(button):
    # Сбрасываем цвет предыдущей выбранной кнопки
    for b in buttons:
        if b != button:
            b.config(bg="SystemButtonFace")  # Возвращаем стандартный цвет

    # Изменяем цвет выбранной кнопки
    button.config(bg="dodgerblue4")


# Создаем кнопки
frame_button = tk.Frame(window,bg = "#0f3464", padx=50)
frame_button.grid(row=5, column=0, sticky="nsew")

buttons = []
button_labels = ["week", "month", "year"]
for i, label in enumerate(button_labels): 
    button = tk.Button(frame_button, text=label)
    button.config(command=lambda b=button: change_button_color(b))    
    button.grid(row=0,column=i, sticky='w', padx=10)
    buttons.append(button)




###таблица
data = [
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"]
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

