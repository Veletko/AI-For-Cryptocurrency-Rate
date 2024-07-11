import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import parsing.UsingAI

# Импортируем переводы и настройки для мультиязычности
current_language = 'en'
translations = {
    'en': {
        'Chart': 'Chart',
        'Update': 'Update',
        'week': 'week',
        '2 weeks': '2 weeks',
        'month': 'month',
        'Price/$': 'Price/$',
        'Name': 'Name'
    },
    'fr': {
        'Chart': 'Graphique',
        'Update': 'Mise à jour',
        'week': 'semaine',
        '2 weeks': '2 semaines',
        'month': 'mois',
        'Price/$': 'Prix/$',
        'Name': 'Nom'
    }
}

# Функция для сортировки данных по столбцу
def sort(col, reverse):
    l = [(table.set(k, col), k) for k in table.get_children("")]
    l.sort(reverse=reverse)
    for index, (_, k) in enumerate(l):
        table.move(k, "", index)
    table.heading(col, command=lambda: sort(col, not reverse))

# Функция для обновления графика
def update_plot(number_date, comboboxChoice):
    global canvas
    canvas.get_tk_widget().destroy()
    new_fig = parsing.UsingAI.chart(number_date, comboboxChoice)
    canvas = FigureCanvasTkAgg(new_fig, master=frame_main)
    canvas.draw()
    canvas.get_tk_widget().grid(row=2, column=0, sticky='w')

def languageComboboxCommand(event):
    global current_language
    lang = languageCombobox.get()
    current_language = 'en' if lang == 'English' else 'fr'
    
    for widget in frame_main.winfo_children():
        if isinstance(widget, tk.Button):
            widget.destroy()

    new_button = tk.Button(frame_main, text=translate('Update'), fg="white", bg="#060747", font=('Helvetica', 12))
    new_button.grid(row=1, column=0, padx=100, pady=10, sticky="w")
    window.update()
    
    text.config(text=translate('Chart'))

    button_labels = [translate('week'), translate('2 weeks'), translate('month')]
    for i, label in enumerate(button_labels):
        buttons[i].config(text=label)

    table.heading('Name', text=translate('Name'))
    table.heading('24h/%', text='24h/%')
    table.heading('Price/$', text=translate('Price/$'))

def translate(key):
    return translations[current_language].get(key, key)

def comboboxCommand(event):
    comboboxChoice = combobox.get()
    update_plot(number_date, comboboxChoice)

def change_button_color(button, button_id):
    global number_date
    for b in buttons:
        if b != button:
            b.config(background= "white",foreground="#060747")  
    button.config(bg="#060747", fg= "white")
    number_date = button_id
    update_plot(number_date, combobox.get())

window = tk.Tk()
window.configure(background='#505191')
window.title('Prediction')
window.iconbitmap('icon.ico')

frame_main = tk.Frame(window, width=1600, height=500, bg="#505191")
frame_main.grid(row=0, column=0, sticky="nswe")

comboboxChoice = "Nvidia"
number_date = 2
pairs = ["Apple", "Microsoft", "Nvidia"]

text = ttk.Label(frame_main, text=translate('Chart'), foreground='white', background ='#505191', font=('Helvetica', 14, 'bold'))
text.grid(row=0, column=0, sticky="w", padx=100, pady=10)

fig = parsing.UsingAI.chart(number_date,comboboxChoice)
canvas = FigureCanvasTkAgg(fig, master=frame_main)
canvas.get_tk_widget().grid(row=2, column=0, sticky='w')

styleС = ttk.Style()
styleС.configure("TCombobox", 
                font=('Helvetica', 14, 'bold'), 
                padding=5,                       
                fg= "#060747")  

combobox = ttk.Combobox(frame_main, values=pairs, style="TCombobox")
combobox.bind("<<ComboboxSelected>>", comboboxCommand)
combobox.current(2)
combobox.place(x=250, y=10)

button_update = tk.Button(frame_main, text=translate('Update'), fg="white", bg="#060747", font=('Helvetica', 12), command=lambda: update_plot(number_date, comboboxChoice))
button_update.grid(row=1, column=0, padx=100, pady=10, sticky="w")

frame_button = tk.Frame(window, bg="#505191")
frame_button.grid(row=3, column=0, sticky="nswe")

appleData = parsing.UsingAI.get_data_for_period(0, 'AAPL')     
last_two_rowsApple = appleData['Close'].tail(2)
price_lastApple = last_two_rowsApple.iloc[-1]
price_second_lastApple = last_two_rowsApple.iloc[-2]

microsoftData = parsing.UsingAI.get_data_for_period(0, 'MSFT')            
last_two_rowsMicrosoft = microsoftData['Close'].tail(2)
price_lastMicrosoft = last_two_rowsMicrosoft.iloc[-1]
price_second_lastMicrosoft = last_two_rowsMicrosoft.iloc[-2]

nvidiaData = parsing.UsingAI.get_data_for_period(0, 'NVDA')                   
last_two_rowsNvidia = nvidiaData['Close'].tail(2)
price_lastNvidia = last_two_rowsNvidia.iloc[-1]
price_second_lastNvidia = last_two_rowsNvidia.iloc[-2]

buttons = []
button_labels = [translate('week'), translate('2 weeks'), translate('month')]
for i, label in enumerate(button_labels):
    button = tk.Button(frame_button, text=label, font=('Helvetica', 12))
    button.config(background="white", foreground="#060747", command=lambda b=button, idx=i: change_button_color(b, idx))
    button.grid(row=0, column=i, padx=150)
    buttons.append(button)



data = [
    ["Apple", round(((price_lastApple - price_second_lastApple) / price_second_lastApple * 100), 2), round(price_lastApple, 2)],
    ["Microsoft", round(((price_lastMicrosoft - price_second_lastMicrosoft) / price_second_lastMicrosoft * 100), 2), round(price_lastMicrosoft, 2)],
    ["Nvidia", round(((price_lastNvidia - price_second_lastNvidia) / price_second_lastNvidia * 100), 2), round(price_lastNvidia, 2)]
]

frame_statistic = tk.Frame(window, bg='#505191')
frame_statistic.grid(row=0, column=1, sticky="w")

heads = ['Name', '24h/%', 'Price/$']
style = ttk.Style()

style.configure("Treeview",
                background="#060747",
                foreground="#ffffff",
                fieldbackground="#060747",
                font=('Helvetica', 14),
                rowheight=25,
                takefocus=False)
style.map("Treeview", background=[('selected', '#a9aae2')],
          foreground=[('selected', '#060747')])

style.configure("Treeview.Heading",
                background="#a9aae2",
                foreground="#060747",
                font=('Helvetica', 14, 'bold'),
                relief="flat")
style.map("Treeview.Heading", 
          background=[('active', '#a9aae2')],
          foreground=[('active', '#060747')],
          relief=[('active', 'flat')])

table_height = len(data)

table = ttk.Treeview(frame_statistic, show='headings', style="Treeview", height=table_height)
table['columns'] = heads

table.heading('Name', text=translate('Name'), anchor='center', command=lambda: sort(0, False))
table.column('Name', anchor='center', width=100)
table.heading('24h/%', text='24h/%', anchor='center', command=lambda: sort(1, False))
table.column('24h/%', anchor='center', width=100)
table.heading('Price/$', text=translate('Price/$'), anchor='center', command=lambda: sort(2, False))
table.column('Price/$', anchor='center', width=100)

for row in data:
    table.insert('', tk.END, values=row)

table.pack(expand=False, fill='both')

languages = ['English', 'French']
languageCombobox = ttk.Combobox(frame_main, values=languages, style="TCombobox")
languageCombobox.bind("<<ComboboxSelected>>", languageComboboxCommand)
languageCombobox.current(0)
languageCombobox.place(x=430, y=10)

window.mainloop()
