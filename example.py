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