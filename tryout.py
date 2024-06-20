import json
from os import path
from typing import Any, Tuple

import customtkinter

import customWidgets as cW


def load_settings():
    #print(path.join(path.dirname(path.realpath(__file__))))
    with open("settings.json", "r") as json_settings:
        return json.load(json_settings)
    
def load_language(lang):
    with open("appLang.json", "r", encoding="utf8") as json_lang:
        langs = json.load(json_lang)
        selected_lang = {}
        for key in langs:
            selected_lang[key] = langs.get(key)[lang]
        print(selected_lang)
        return selected_lang
    
class BlankWindow(customtkinter.CTk):
    """
        Basic Window for the application  

    Args:
        customtkinter (_type_): standard custom tkinter node for a ctk application
    
    """
    def __init__(self, fg_color: str | Tuple[str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.title("title of the App")
        self.geometry("600x600")
        self.settings = load_settings()
        self.lang = load_language(self.settings["LANG"])
        customtkinter.set_default_color_theme("theme.json")
        customtkinter.set_appearance_mode(self.settings["mode"])   

        
class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, root=customtkinter.CTk, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Testwindow")  
        self.resizable(False, False)   
        self.attributes("-topmost",True)  

        # center the toplevel window
        x = root.winfo_x() + root.winfo_width()//2 - self.winfo_width()//2
        y = root.winfo_y() + root.winfo_height()//2 - self.winfo_height()//2
        self.geometry(f"+{x}+{y}")


class TestWindow(BlankWindow):
    def __init__(self, fg_color: str | Tuple[str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.label = customtkinter.CTkLabel(self, text="Testlabe")
        self.button = customtkinter.CTkButton(self, text="testbutton", command=self.change_theme)
        self.frame = customtkinter.CTkFrame(self)
        self.frame_into_frame = customtkinter.CTkFrame(self.frame)
        self.window_btn = customtkinter.CTkButton(self, text="new window", command=self.createWindow)
        self.entry = customtkinter.CTkEntry(self, placeholder_text="placeholderText")
        self.entry2 = customtkinter.CTkEntry(self, placeholder_text="placeholderText")
        self.disabled_btn = customtkinter.CTkButton(self, text="diabled", state="disabled")
        self.round_btn = customtkinter.CTkButton(self, text="new window", corner_radius=13)
        self.label.grid(row=0, column=0, sticky="we")
        self.button.grid(row=1, column=0, sticky="we")
        self.frame.grid(row=2, column=0, sticky="we")
        self.frame_into_frame.grid(row=0, column=0, sticky="n", padx=(10,10), pady=(10,10))
        self.window_btn.grid(row=3, column=0, sticky="n")
        self.toplevel_window = None
        self.entry.grid(row=4, column=0, sticky="n")
        self.entry2.grid(row=5, column=0, sticky="n")
        self.disabled_btn.grid(row=6, column=0, sticky="n")
        self.round_btn.grid(row=7, column=0, sticky="n")

        
        
    def change_theme(self):
        self.current_theme = self.settings["mode"]
        if self.current_theme == "light":
            self.settings["mode"] = "dark"
        else:
            self.settings["mode"] = "light"
        customtkinter.set_appearance_mode(self.settings["mode"])

    def createWindow(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(root=self)
            # disables other main window until its closed
            self.toplevel_window.grab_set()
        else:
            self.toplevel_window.focus()

if __name__ == "__main__":
    #app = AutoamtionAdditon(self.lang["PROJECT"] + "/" + self.lang["NEW_A"])
    app = TestWindow()
    app.mainloop()