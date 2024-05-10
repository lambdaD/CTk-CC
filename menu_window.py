from customtkinter import *
from json import *


isWinOpen = False

with open('menu_config_lang_ru.json', 'r', encoding = 'utf-8') as file:
        lang = load(file)
        
def Create_Menu_Window(label):
    global isWinOpen
    if (label == lang['Header']['Help'][1]) and not isWinOpen:
        about_window = CTkToplevel()
        about_window.title(label)
        about_window.geometry('500x350+1000+500')
        about_window.resizable(False, False)
        textbox = CTkTextbox(about_window,  wrap = 'word', width=500, height = 350, font = ('Courier', 15))
        textbox.insert(1.0, lang['About_us_Text']['Name'])
        textbox.insert(END, f' {lang['About_us_Text']['Version']}')
        textbox.insert(END, f'\n{lang['About_us_Text']['Object']}')
        textbox.insert(END, f'\n{lang['About_us_Text']['License']}')
        textbox.insert(END, f'\n{lang['About_us_Text']['Github']}')
        textbox.insert(END, f'\n{lang['About_us_Text']['Thanks']}')
        textbox.configure(state = 'disabled')
        textbox.grid(row = 0, column = 0)
        about_window.protocol("WM_DELETE_WINDOW", lambda: Dismiss_Menu_Window(about_window))
    elif (label == lang['Header']['Help'][0]):
        help_window = CTkToplevel()
        help_window.title(label)
        help_window.geometry('1000x500+1000+500')
        help_window.resizable(False, False)
        title_frame = CTkFrame(help_window)
        title_frame.pack(side = LEFT, fill = Y)
        text_frame = CTkFrame(help_window)
        text_frame.pack(side = RIGHT, fill = BOTH, expand = True)
        for header, text in lang['Help_Text'].items():
             label = CTkLabel(title_frame, text = text['Header'], padx = 10, pady = 5)
             label.pack(fill = X)
             label.bind("<Button-1>", lambda event, article=text['Article']: Additional.update_text(article, article_text_area)) 
        article_text_area = CTkTextbox(text_frame, wrap = 'word')
        article_text_area.pack(fill = BOTH, expand = True)
        help_window.protocol("WM_DELETE_WINDOW", lambda: Dismiss_Menu_Window(help_window))
    isWinOpen = True


def Dismiss_Menu_Window(window):
    global isWinOpen
    isWinOpen = False
    window.destroy()


def File_Activities_Execute(label):
    pass

def Create_Settings_Menu_Window(label):
    pass

class Additional():
    def update_text(article, article_text_area):
        article_text_area.delete(1.0, END)
        article_text_area.insert(END, article)
    






  

    