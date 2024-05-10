from tkinter import *
from tkinter import ttk

# Функция для создания нового окна
def create_new_tab_window():
    new_window = Toplevel()  
    new_window.title("Расчет")  
    label = Label(new_window, text="")  
    label.pack()  
    tree = ttk.Treeview(new_window, columns=('Count', 'DateTime', 'Amount', 'MainDebt', 'RatioDebt', 'RestDebt'))
    tree.heading('Count', text='Count')
    tree.heading('DateTime', text='Count')
    tree.heading('Amount', text='Count')
    tree.heading('MainDebt', text='Count')
    tree.heading('RatioDebt', text='Count')
    tree.heading('RestDebt', text='Count')

    tree.pack()