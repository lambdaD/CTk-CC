from tkinter import *
from tkinter import ttk

# Функция для создания нового окна
def create_new_tab_window(payments):
    window = Toplevel()
    window.title("Payment Schedule")

    tree = ttk.Treeview(window, columns=('№', 'Date', 'Payment', 'Principal', 'Interest', 'Balance'), show='headings')
    tree.heading('№', text='№')
    tree.heading('Date', text='Date')
    tree.heading('Payment', text='Payment')
    tree.heading('Principal', text='Principal')
    tree.heading('Interest', text='Interest')
    tree.heading('Balance', text='Balance')

    for payment in payments:
        tree.insert('', 'end', values=payment)

    tree.pack(expand=True, fill='both')