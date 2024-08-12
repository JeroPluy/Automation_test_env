"""
This module contains utility functions for the frontend.
"""

from os import path
import json

# paths to the settings files
SETTING_PATH = path.join("src", "frontend", "settings", "settings.json")
LANG_PATH = path.join("src", "frontend", "settings", "appLang.json")
THEME_PATH = path.join("src", "frontend", "settings", "theme.json")

# path to the icons directory for the custom widgets images
ICON_PATH = path.join("src", "frontend", "customWidgets", "icons")

def load_settings():
    #print(path.join(path.dirname(path.realpath(__file__))))
    with open(SETTING_PATH, "r") as json_settings:
        return json.load(json_settings)
    
def load_language(lang):
    with open(LANG_PATH, "r", encoding="utf8") as json_lang:
        langs = json.load(json_lang)
        selected_lang = {}
        for key in langs:
            selected_lang[key] = langs.get(key)[lang]
        return selected_lang 
    

  