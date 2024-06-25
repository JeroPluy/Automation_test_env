import json
from os import path
from typing import Any, Tuple

import customtkinter

import customWidgets.customWidgets as cW


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

class BlankToplevelWindow(customtkinter.CTkToplevel):
    """
        Basic top level window for warnings and errors
    """
    def __init__(self, root=customtkinter.CTk, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Testwindow")  
        self.resizable(False, False)   
        self.attributes("-topmost",True)  

        # center the toplevel window
        x = root.winfo_x() + root.winfo_width()//2 - self.winfo_width()//2
        y = root.winfo_y() + root.winfo_height()//2 - self.winfo_height()//2
        self.geometry(f"+{x}+{y}")


class customNavButtons(cW.NavigationButtons):
    def __init__(self, master, com_backwards, com_forward, objects: int = 2, values: Tuple[str] = ...):
        super().__init__(master, com_backwards, com_forward, objects, values)
        self.version_option = customtkinter.CTkOptionMenu(self, values=master.settings["HA_VERSIONS"], width=130, height=30, command=self.version_select)
        self.version_option.grid(row=0, column=1, padx=(0,15), sticky="we")

    def version_select(self, choice):
        print("optionmenu dropdown clicked:", str(choice))



class AutoamtionInsertionFrame(customtkinter.CTkFrame):
    """_summary_

    Args:
        customtkinter (_type_): _description_
    """
    def __init__(self, master,**kwargs):
        super().__init__(master, fg_color = "transparent",**kwargs)
        self.grid_columnconfigure(0,weight=1)

        self.textbox = customtkinter.CTkTextbox(self, width=330, height=132, font=("Roboto", 16), wrap="none")
        self.textbox.grid(row=0,column=0, sticky="news", rowspan=2, padx=(0,10))

        self.add_btn = cW.acceptButton(self, width=60, height=60, corner_radius=12, kind=1, command=self.textbox_add) 
        self.add_btn.grid(row=0, column=1, sticky="nw", pady=(0,5))

        self.del_btn = cW.deleteButton(self, width=60, height=60, corner_radius=12, kind=0, command=self.textbox_del) 
        self.del_btn.grid(row=1, column=1, sticky="nw", pady=(5,0))
        

    def textbox_del(self):
        self.textbox.delete("0.0", "end")

    def textbox_add(self):
        self.textbox.insert("0.0", " Text ")

    def safe_text(self):
        self.text = self.textbox.get("0.0", "end")  # get text from line 0 character 0 till the end



class AutoamtionAdditon(BlankWindow):
    """_summary_

    Args:
        customtkinter (_type_): _description_
    """
    def __init__(self, project):
        super().__init__()
        self.title("title of the App")
        self.geometry("600x600")
        self.grid_columnconfigure(0, weight=1)

        self.nav_bar = cW.NavigationBar(self, mode=self.settings["mode"], auto_path=str(project + "/" + self.lang["NEW_A"]))
        self.nav_bar.grid(row=0, column=0,sticky="ew")

        self.entry = customtkinter.CTkEntry(self, placeholder_text=self.lang["AUTO_NAME"], font=("Roboto", 16) )
        self.entry.grid(row=1, column=0, sticky="we", padx=50, pady=(10,10))

        self.insertion_frame = AutoamtionInsertionFrame(self)
        self.insertion_frame.grid(row=2, column=0, padx=(50,50),pady=(10,23), sticky="news")

        self.navigaton_buttons = customNavButtons(self, objects=2, com_backwards=self.backwards, com_forward=self.forwards, values=[self.lang["BACK"], self.lang["NEXT"]])
        self.navigaton_buttons.grid(row=3, column=0, padx=(50,50),pady=(0,15), sticky="news")

    def backwards(self):
        print("did nothing")

    def forwards(self):
        print("did nothing")

if __name__ == "__main__":
    app = AutoamtionAdditon(project="project1")
    app.mainloop()