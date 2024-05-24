from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from iflang import *
import pandas as pd


settings = include_settings()
lang = changeLanguage(settings['language']['user_language'])


def create_new_tab_windowSchedulePayments(payments):
    windowSchedulePayments = Toplevel()
    windowSchedulePayments.title(lang['ScheduleTable']['Title'])
    columns = [lang['ScheduleTable']['Num'], 
               lang['ScheduleTable']['Date'], 
               lang['ScheduleTable']['Payment'], 
               lang['ScheduleTable']['Principal'], 
               lang['ScheduleTable']['Interest'], 
               lang['ScheduleTable']['Balance']]
    tableSchedulePayments = ttk.Treeview(windowSchedulePayments, columns=columns, show='headings')
    tableSchedulePayments.heading(lang['ScheduleTable']['Num'], text=lang['ScheduleTable']['Num'], anchor=CENTER)
    tableSchedulePayments.heading(lang['ScheduleTable']['Date'], text=lang['ScheduleTable']['Date'], anchor=CENTER)
    tableSchedulePayments.heading(lang['ScheduleTable']['Payment'], text=lang['ScheduleTable']['Payment'], anchor=CENTER)
    tableSchedulePayments.heading(lang['ScheduleTable']['Principal'], text=lang['ScheduleTable']['Principal'], anchor=CENTER)
    tableSchedulePayments.heading(lang['ScheduleTable']['Interest'], text=lang['ScheduleTable']['Interest'], anchor=CENTER)
    tableSchedulePayments.heading(lang['ScheduleTable']['Balance'], text=lang['ScheduleTable']['Balance'], anchor=CENTER)
    for col in columns:
        tableSchedulePayments.column(col, anchor=CENTER)
    tableSchedulePayments.pack(fill='both', expand=True)
    for payment in payments:
        tableSchedulePayments.insert('', 'end', values=payment)
    export_button = Button(windowSchedulePayments, text='Экспорт', command=lambda: export_to_excel(tableSchedulePayments))
    export_button.pack(pady=10)


def export_to_excel(tree):
    try:
        rows = []
        for row_id in tree.get_children():
            row = tree.item(row_id)['values']
            rows.append(row)
        columns = [tree.heading(col)['text'] for col in tree['columns']]
        df = pd.DataFrame(rows, columns=columns)
        file_path = 'schedule_payments.xlsx'
        df.to_excel(file_path, index=False)
        messagebox.showinfo('Ok', 'Ok')
    except Exception as e:
        messagebox.showerror('Not ok', 'not ok')
