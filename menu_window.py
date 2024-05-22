from customtkinter import *
from iflang import *
from json import *

lang = changeLanguage('Ru')

isWinOpen = False


        
def Create_Menu_Window(label):
    global isWinOpen
    if (label == lang['Header']['Help'][1]) and not isWinOpen:
        about_window = CTkToplevel()
        about_window.title(label)
        about_window.geometry('500x350+1000+0')
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
    elif (label == lang['Header']['Help'][0]) and not isWinOpen:
        help_window = CTkToplevel()
        help_window.title(label)
        help_window.geometry('1000x500+1000+0')
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
    if (label == lang['Header']['Edit'][2]) and not isWinOpen:
        settings = include_settings()

        edit_window = CTkToplevel()
        edit_window.title(label)
        edit_window.geometry('250x120+1000+0')

        frame_native = CTkFrame(edit_window, fg_color='transparent')
        frame_native.grid(row=0, column=0, padx=10, pady=20)

        label_language = CTkLabel(frame_native, text="Язык:", fg_color="transparent")
        label_language.grid(row=0, column=0)

        label_appearance = CTkLabel(frame_native, text="Тема:", fg_color="transparent")
        label_appearance.grid(row=1, column=0)

        optionmenu_lang_var = StringVar(value=settings['language']['user_language'])
        optionmenu_lang = CTkOptionMenu(frame_native, variable=optionmenu_lang_var, values=list(settings['language']['language_list'].values()))
        optionmenu_lang.grid(row=0, column=1, padx=(10, 0))

        optionmenu_theme_var = StringVar(value=lang['default_theme'])
        optionmenu_theme = CTkOptionMenu(frame_native, variable=optionmenu_theme_var, values=list(lang['AppearanceApp'].values()))
        optionmenu_theme.grid(row=1, column=1, padx=(10, 0))


        
        save_btn = CTkButton(frame_native, text=lang['Buttons']['SettingBtnSave'], command=lambda: Additional.optionmenu_lang_callback(settings, optionmenu_lang_var.get()))
        save_btn.grid(row=2, column=1, padx=(10, 0))

class Additional():
    def update_text(article, article_text_area):
        article_text_area.delete(1.0, END)
        article_text_area.insert(END, article)
    
    def optionmenu_lang_callback(settings, var):
        settings['language']['user_language'] = var
        with open('settings.json', 'w', encoding='utf-8') as file:
            dump(settings, file, ensure_ascii=False, indent=4)






  

    