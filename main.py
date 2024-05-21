from customtkinter import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from json import *
from tkcalendar import DateEntry
from datetime import *
from dateutil.relativedelta import relativedelta
from ttkthemes import ThemedTk

from additionalCalculateCC import *
from tabWindow import * 
from menu_window import *



def Change_Currency():
    for cur in currencies:
        if(currency_default.get() == cur):
            for cur_lb in currency_types_labels_values:
                cur_lb.configure(text = cur)


def Change_Period(period_unit, period):
    if(period_unit == period_units[0]):
        return Calculate.Year_To_Month_Period_Calculate(period)
    elif(period_unit == period_units[1]):
        return period
    elif(period_unit == period_units[2]):
        if(period < 30):
            return period
        else:
            years, days = divmod(period, 365)
            return years * 12 + days // 30
        
    
def Change_Type_Rate(rate_type, rate):
    rate = Calculate.ToPercentCalculate(rate)
    if(rate_type == rate_per_units[0]):
        return Calculate.Year_To_Month_Rate_Calculate(rate)
    elif(rate_type == rate_per_units[1]):
        return rate
    elif(rate_type == rate_per_units[2]):
        return Calculate.Day_To_Month_Rate_Calculate(rate)
    
def Slider_Event(value, entry):
    entry.delete(0, 'end')
    entry.insert(0, int(value))
    

def Execute():
    try:
        amount, period, rate = float(main_entries_values[0].get()), float(main_entries_values[1].get()), float(main_entries_values[2].get())
        Change_Currency()
        period = Change_Period(period_units_default.get(), period)
        rate = Change_Type_Rate(rate_per_units_default.get(), rate)
        if(var_type_payment.get() == 'аннуитетный'):
            monthly_payment, total_payment, overpayment = Annuity.Is_Annuity_Monthly_Payment_Execute(amount, period, rate, float(additional_entries_values[0].get()), float(additional_entries_values[1].get()), float(additional_entries_values[2].get()))
        else:
            monthly_payment, total_payment, overpayment = Differentiated.Is_Differentiated_Monthly_Payment_Execute(amount, period, rate, float(additional_entries_values[0].get()), float(additional_entries_values[1].get()), float(additional_entries_values[2].get()))
        try:
            result_labels_values[0].configure(text=str(round(monthly_payment,2)))
        except TypeError:
            result_labels_values[0].configure(text=monthly_payment)
        result_labels_values[1].configure(text=str(round(total_payment,2)))
        result_labels_values[2].configure(text=str(round(overpayment,2)))
        create_new_tab_window()
    except ValueError:
        messagebox.showinfo('Ошибка данных',('Введите корректные данные в поля'))



def Create_Menu(lang_header):
    header_menu = Menu()
    #------------------------/------------------------#
    file_menu = Menu(tearoff=0, font=('Calibri', 15), fg = '#0E1010', bg = '#808288', activeforeground = '#808288', activebackground = '#0E1010')
    for label in lang_header['File']:
        file_menu.add_command(label=label, command = lambda label = label: File_Activities_Execute(label))
    header_menu.add_cascade(label=lang_header['Menu'][0], menu=file_menu)
    #------------------------/------------------------#
    edit_menu = Menu(tearoff=0, font=('Calibri', 15), fg = '#0E1010', bg = '#808288', activeforeground = '#808288', activebackground = '#0E1010')
    for label in lang_header['Edit']:
        edit_menu.add_command(label=label, command=lambda label=label: Create_Settings_Menu_Window(label))
    header_menu.add_cascade(label=lang_header['Menu'][1], menu=edit_menu)
    #------------------------/------------------------#
    tools_menu = Menu(tearoff=0, font=('Calibri', 15), fg = '#0E1010', bg = '#808288', activeforeground = '#808288', activebackground = '#0E1010')
    for label in lang_header['Tools']:
        tools_menu.add_command(label=label)
    header_menu.add_cascade(label=lang_header['Menu'][2], menu=tools_menu)
    #------------------------/------------------------#
    help_menu = Menu(tearoff=0, font=('Calibri', 15), fg = '#0E1010', bg = '#808288', activeforeground = '#808288', activebackground = '#0E1010')
    for label in lang_header['Help']:
        help_menu.add_command(label=label, command=lambda label=label: Create_Menu_Window(label))
    header_menu.add_cascade(label=lang_header['Menu'][3], menu=help_menu)
    #------------------------/------------------------#
    return header_menu


def Create_Main_Entries_Frame(labels_texts, units_for_combo, default_units_for_combo, master, padxentry, widthentry, widthcombo, maxSlider):
    frame = CTkFrame(master, fg_color='transparent')
    entries = []
    sliders = []
    countRows = 0 
    count = 0
    countRowsforSlider = 1 
    for i in labels_texts:
        label = CTkLabel(frame, text=i, font = ('Century Gothic', 17))
        entry = CTkEntry(frame, font = ('Century Gothic', 14), width = widthentry)
        entries.append(entry)
        combo = CTkComboBox(frame, values = units_for_combo[countRows], variable = default_units_for_combo[countRows], width=widthcombo, state='readonly', font = ('Century Gothic', 13))
        slider = CTkSlider(frame, width = 500)
        sliders.append(slider)
        label.grid(column = 0, row = count, sticky=E)
        entry.grid(column = 1, row = count, padx = (padxentry,0))
        combo.grid(column = 2, row = count, sticky = W)
        slider.grid(column = 0, row = countRowsforSlider, columnspan = 3)
        countRows += 1
        count += 2
        countRowsforSlider +=2
    sliders[0].configure(from_ = 0, to = maxSlider[0], number_of_steps = 100, command = lambda value:  Slider_Event(value, entries[0]))
    sliders[0].set(0)
    sliders[1].configure(from_ = 0, to = maxSlider[1], number_of_steps = 100, command = lambda value:  Slider_Event(value, entries[1]))
    sliders[1].set(0)
    sliders[2].configure(from_ = 0, to = maxSlider[2], number_of_steps = 100, command = lambda value:  Slider_Event(value, entries[2]))
    sliders[2].set(0)
    return frame, entries, sliders


def Create_Radio_Frame(label_text, default_option, *radio_options):
    frame = CTkFrame(root, fg_color='transparent')
    label = CTkLabel(frame,text=label_text, font = ('Century Gothic', 17))
    label.grid(column=0, row=0, sticky = E)
    var = StringVar(value=default_option)
    countRow = 0
    for option in radio_options:
        radio_button = CTkRadioButton(frame,text=option,value=option, variable=var, font = ('Century Gothic', 13))
        radio_button.grid(column=1, row=countRow, sticky = W, padx = (50, 0), pady = 5)
        countRow += 1
    return frame, var


def Create_Additional_Parameters():
    frame = CTkFrame(root, fg_color='transparent')
    label_date = CTkLabel(frame, text=lang['DateEntry']['labeldate'], font = ('Century Gothic', 17))
    label_date.grid(column = 0, row = 0, sticky = E)
    first_day_next_month = (date.today() + relativedelta(months=1)).replace(day = 1)
    date_entry = DateEntry(frame, year=first_day_next_month.year, month=first_day_next_month.month,day=first_day_next_month.day, font = ('Century Gothic', 17), locale= lang['DateEntry']['locale'], state = 'readonly')
    date_entry.grid(column = 1, row = 0, sticky = W, pady = (0, 10), padx = (10, 0))

    add_parametrs_combo = StringVar(value = 'у.е.')
    # Фрейм, массив энтрей, массив слайдеров
    add_entries, add_entries_values, add_sliders = Create_Main_Entries_Frame(lang["LabelsForAdditionalEntries"], [[add_parametrs_combo.get(),'% от суммы кредита'], [add_parametrs_combo.get(),'% от суммы кредита'], [add_parametrs_combo.get(),'% от суммы кредита']], [add_parametrs_combo, add_parametrs_combo, add_parametrs_combo], frame, 10, 170, 100, [100000, 30000, 30000])
    add_entries.grid(column = 0, row = 1, columnspan = 2)
    return frame, add_entries_values

def Create_Result_Labels(*labels_texts):
    frame = CTkFrame(root, fg_color='transparent')
    labels_results = []
    labels_add = []
    countRow = 0
    for i in labels_texts:
        label = CTkLabel(frame, text = i, font = ('Century Gothic', 17))
        label_result = CTkLabel(frame, text='0', font = ('Century Gothic', 17))
        labels_results.append(label_result)
        label_add = CTkLabel(frame, text = currency_default.get(), font = ('Century Gothic', 17))
        labels_add.append(label_add)
        label.grid(column=0, row = countRow, sticky = E)
        label_result.grid(column=1, row = countRow, padx = 10)
        label_add.grid(column = 2, row = countRow)
        countRow += 1
    return frame, labels_results, labels_add



root = CTk()
root.geometry('550x650')
root.minsize(550, 650)
root.maxsize(1050, 650)
with open('menu_config_lang_ru.json', 'r', encoding = 'utf-8') as file:
    lang = load(file)
root.title(lang['Title'])
root.iconbitmap(default="ico/usd.ico")
set_appearance_mode("light")
set_default_color_theme("yellow-black.json") 
#------------------------Main entries units------------------------#
currencies = lang['Currencies']
period_units = lang['Period_units']
rate_per_units = lang['Rate_per_units']
units_for_main_entries = [currencies, period_units, rate_per_units]

currency_default = StringVar(value=currencies[0])
period_units_default = StringVar(value=period_units[1])
rate_per_units_default = StringVar(value=rate_per_units[0])
default_units_for_main_entries = [currency_default, period_units_default, rate_per_units_default]
#------------------------/------------------------#
# Header
header_menu = Create_Menu(lang["Header"])
# Фрейм, Массив полей для ввода
main_entries, main_entries_values, main_sliders = Create_Main_Entries_Frame(lang["LabelsForMainEntries"], units_for_main_entries, default_units_for_main_entries, root, 100, 170, 100, [500000, 50, 99])





# Фрейм, StringVar radiobutton
change_type_payment, var_type_payment = Create_Radio_Frame(lang['LabelForTypeDebt'],lang['TypesDebt'][0],lang['TypesDebt'][0],lang['TypesDebt'][1])
# Фрейм
additional_entries, additional_entries_values = Create_Additional_Parameters()
# 
execute_btn = CTkButton(root, text=lang['Buttons']['mainExecute'], command=Execute)
# Фрейм, лейблы результаты, единицы валюты лейблы
result_labels, result_labels_values, currency_types_labels_values = Create_Result_Labels(lang['MainResults']['monthly_payment'], lang['MainResults']['total_payment'], lang['MainResults']['overpayment'])

#------------------------Верстка------------------------#
root.config(menu = header_menu)
main_entries.grid(row = 0, column = 0, sticky = "nsew", padx = (15,0), pady = 10)
change_type_payment.grid(row = 1, column = 0, sticky = "nsew", padx = (15,0), pady = 10)
additional_entries.grid(row = 2, column = 0, sticky = "nsew", padx = (10,0), pady = 10)
execute_btn.grid(row = 3, column = 0, pady = 10)
result_labels.grid(row = 4, column = 0, sticky = "nsew", padx = (10,0), pady = 10)
#------------------------/------------------------#


root.mainloop()

