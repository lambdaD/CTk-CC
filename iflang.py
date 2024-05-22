from json import *

def include_settings():
    with open('settings.json', 'r', encoding = 'utf-8') as file:
            settings = load(file)
    return settings

def changeLanguage(lang):
    if lang == 'Ru':
        with open('lang_ru.json', 'r', encoding = 'utf-8') as file:
            lang = load(file)
    return lang