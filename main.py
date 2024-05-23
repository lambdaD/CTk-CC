from customtkinter import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import *
from dateutil.relativedelta import relativedelta

from additionalCalculateCC import *
from tabWindow import * 
from menu_window import *
from iflang import *
from PIL import Image, ImageTk


def Change_Currency():
    for cur in currencies:
        if(currency_default.get() == cur):
            for cur_lb in currency_types_labels_values:
                cur_lb.configure(text = cur)
    currency_types_labels_values[3].configure(text = '%')

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
        amount = float(get_clean_number(main_entries_values[0].get()))
        period = float(get_clean_number(main_entries_values[1].get()))
        rate = float(get_clean_number(main_entries_values[2].get()))
        down_payment = float(get_clean_number(additional_entries_values[0].get()))
        one_time_fee = float(get_clean_number(additional_entries_values[1].get()))
        monthly_fee = float(get_clean_number(additional_entries_values[2].get()))
        first_payment_date = datetime.strptime(date_entry.get(), "%d.%m.%Y")

        Change_Currency()
        period = Change_Period(period_units_default.get(), period)
        rate = Change_Type_Rate(rate_per_units_default.get(), rate)

        if var_type_payment.get() == lang['TypesDebt'][0]:
            monthly_payment, total_payment, overpayment, overpayment_percentage = Annuity.Is_Annuity_Monthly_Payment_Execute(amount, period, rate, down_payment, one_time_fee, monthly_fee)
            payments = calculate_annuity_payments(amount, period, rate, down_payment, monthly_fee, first_payment_date)
        else:
            monthly_payment, total_payment, overpayment, overpayment_percentage = Differentiated.Is_Differentiated_Monthly_Payment_Execute(amount, period, rate, down_payment, one_time_fee, monthly_fee)
            payments = calculate_differentiated_payments(amount, period, rate, down_payment, monthly_fee, first_payment_date)

        try:
            result_labels_values[0].configure(text=str(f'{monthly_payment:.2f}'))
        except:
            result_labels_values[0].configure(text=monthly_payment)
        result_labels_values[1].configure(text=str(f'{total_payment:.2f}'))
        result_labels_values[2].configure(text=str(f'{overpayment:.2f}'))
        result_labels_values[3].configure(text=str(f'{overpayment_percentage:.2f}'))

        create_new_tab_windowSchedulePayments(payments)
    except:
       messagebox.showinfo(lang['Error Messages']['Value Error']['Title'], lang['Error Messages']['Value Error']['Text'])

def calculate_annuity_payments(amount, period, rate, down_payment, monthly_fee, first_payment_date):
    net_amount = amount - down_payment
    annuity_ratio = Annuity.Annuity_Ratio_Calculate(rate, period)
    monthly_payment = Annuity.Annuity_Monthly_Payment_Calculate(net_amount, annuity_ratio)
    monthly_payment_with_fee = monthly_payment + monthly_fee

    payments = []
    balance = net_amount
    for i in range(int(period)):
        interest_payment = balance * rate
        principal_payment = monthly_payment - interest_payment
        balance -= principal_payment

        payment_date = first_payment_date + timedelta(days=i*30)
        payments.append((i+1, payment_date.strftime("%d.%m.%Y"), round(monthly_payment_with_fee, 2), round(principal_payment, 2), round(interest_payment, 2), round(balance, 2)))

    return payments

def calculate_differentiated_payments(amount, period, rate, down_payment, monthly_fee, first_payment_date):
    net_amount = amount - down_payment
    principal_payment = net_amount / period

    payments = []
    balance = net_amount
    for i in range(int(period)):
        interest_payment = balance * rate
        monthly_payment = principal_payment + interest_payment + monthly_fee
        balance -= principal_payment

        payment_date = first_payment_date + timedelta(days=i*30)
        payments.append((i+1, payment_date.strftime("%d.%m.%Y"), round(monthly_payment, 2), round(principal_payment, 2), round(interest_payment, 2), round(balance, 2)))

    return payments

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

def format_number(entry_text):
    # Удаляем все не числовые символы
    value = entry_text.get().replace(',', '').replace(' ', '')
    if value.isdigit():
        formatted_value = '{:,}'.format(int(value)).replace(',', ' ')
        # Отключаем временно обработку для предотвращения бесконечного цикла
        entry_text.trace_vdelete("w", entry_text.trace_id)
        entry_text.set(formatted_value)
        # Восстанавливаем обработчик
        entry_text.trace_id = entry_text.trace("w", lambda name, index, mode, sv=entry_text: format_number(sv))

def get_clean_number(entry_text):
    # Удаляем пробелы из строки и возвращаем число
    return entry_text.replace(' ', '')

def Create_Main_Entries_Frame(labels_texts, units_for_combo, default_units_for_combo, master, padxentry, widthentry, widthcombo, maxSlider):
    frame = CTkFrame(master, fg_color='transparent')
    entries = []
    sliders = []
    countRows = 0 
    count = 0
    countRowsforSlider = 1 
    for i in labels_texts:
        label = CTkLabel(frame, text=i, font = ('Century Gothic', 17))
        entry_text = StringVar()
        entry_text.trace_id = entry_text.trace("w", lambda name, index, mode, sv=entry_text: format_number(sv))
        entry = CTkEntry(frame, font = ('Century Gothic', 14), width = widthentry, textvariable=entry_text)
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
    sliders[0].configure(from_ = 0, to = maxSlider[0], number_of_steps = 300, command = lambda value:  Slider_Event(value, entries[0]))
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

    add_parametrs_combo = StringVar(value = lang['CombosForAdditionalEntries'][0])
    # Фрейм, массив энтрей, массив слайдеров
    add_entries, add_entries_values, add_sliders = Create_Main_Entries_Frame(lang["LabelsForAdditionalEntries"], [[add_parametrs_combo.get(),lang['CombosForAdditionalEntries'][1]], [add_parametrs_combo.get(),lang['CombosForAdditionalEntries'][1]], [add_parametrs_combo.get(),lang['CombosForAdditionalEntries'][1]]], [add_parametrs_combo, add_parametrs_combo, add_parametrs_combo], frame, 10, 170, 100, [100000, 30000, 30000])
    add_entries.grid(column = 0, row = 1, columnspan = 2)
    return frame, add_entries_values, date_entry

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
root.geometry('1050x650')
root.minsize(550, 650)
root.maxsize(1050, 650)
settings = include_settings()
lang = changeLanguage(settings['language']['user_language'])
root.title(lang['Title'])
root.iconbitmap(default="ico/usd.ico")
Additional.optionmenu_themes_callback('Светлая') 



my_image = CTkImage(light_image=Image.open("img/Lambda.png"), dark_image=Image.open("img/Bern.png"),size=(500, 500))
image_label = CTkLabel(root, image=my_image, text="")
image_label.place(relx=1.0, rely=1.0, anchor='se')

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
main_entries, main_entries_values, main_sliders = Create_Main_Entries_Frame(lang["LabelsForMainEntries"], units_for_main_entries, default_units_for_main_entries, root, 100, 170, 100, [5000000, 120, 99])





# Фрейм, StringVar radiobutton
change_type_payment, var_type_payment = Create_Radio_Frame(lang['LabelForTypeDebt'],lang['TypesDebt'][0],lang['TypesDebt'][0],lang['TypesDebt'][1])
# Фрейм
additional_entries, additional_entries_values, date_entry = Create_Additional_Parameters()
# 
execute_btn = CTkButton(root, text=lang['Buttons']['mainExecute'], command=Execute)
# Фрейм, лейблы результаты, единицы валюты лейблы
result_labels, result_labels_values, currency_types_labels_values = Create_Result_Labels(lang['MainResults']['monthly_payment'], lang['MainResults']['total_payment'], lang['MainResults']['overpayment'],lang['MainResults']['overpayment_percantage'])
currency_types_labels_values[3].configure(text = '%')

#------------------------Верстка------------------------#
root.config(menu = header_menu)
main_entries.grid(row = 0, column = 0, sticky = "nsew", padx = (15,0), pady = 10)
change_type_payment.grid(row = 1, column = 0, sticky = "nsew", padx = (15,0), pady = 10)
additional_entries.grid(row = 2, column = 0, sticky = "nsew", padx = (10,0), pady = 10)
execute_btn.grid(row = 3, column = 0, pady = 10)
result_labels.grid(row = 4, column = 0, sticky = "nsew", padx = (10,0), pady = 10)
#------------------------/------------------------#


root.mainloop()

