import json
from os import path
import tkinter
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
        self.geometry("600x800")
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


class CombinedRadioBtns():
    def __init__(self):
        # the same variable combines radio buttons so only one is selectable
        self.variable = customtkinter.StringVar(value="nothing")

    def add_radiobtns(self, radiobtns: Tuple[customtkinter.CTkRadioButton], preselected:int=None):
        for btn in radiobtns:
            btn.configure(variable=self.variable)
        if preselected:
            try:
                radiobtns[preselected].select()
            except IndexError:
                print("NOT in the list")

    def get(self):
        return self.variable.get()      
    
    def radiobtn_event(self):
        print(self.get())
    
    def deselect_all(self):
        self.variable.set("nothing")
      

class TestWindow(BlankWindow):
    def __init__(self, fg_color: str | Tuple[str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.label = customtkinter.CTkLabel(self, text="Testlabe")
        self.button = customtkinter.CTkButton(self, text="testbutton", height=60, command=self.change_theme)
        self.frame = customtkinter.CTkFrame(self)
        self.frame_into_frame = customtkinter.CTkFrame(self.frame)
        self.window_btn = customtkinter.CTkButton(self, text="new window", command=self.create_window)
        self.entry = customtkinter.CTkEntry(self, placeholder_text="placeholderText")
        self.entry2 = customtkinter.CTkEntry(self, placeholder_text="placeholderText")
        self.disabled_btn = customtkinter.CTkButton(self, text="diabled", state="disabled")
        self.checkbox = customtkinter.CTkCheckBox(self, text="checkbox text", command=self.disable_it)
        self.checkbox2 = customtkinter.CTkCheckBox(self, text="checkbox 2", command=self.toggle_all)
        self.switch = customtkinter.CTkSwitch(self, text="switch text")
        self.radiobtn_test_group = CombinedRadioBtns()
        self.radiobtn = customtkinter.CTkRadioButton(self, text="radio text", value=1)
        self.radiobtn2 = customtkinter.CTkRadioButton(self, text="radio 2", value=2)
        self.radiobtn_test_group.add_radiobtns([self.radiobtn, self.radiobtn2],1)
        self.select_radio_btn = customtkinter.CTkButton(self, text="whats selected?", command=self.radiobtn_test_group.radiobtn_event)
        self.select_radio_btn2 = customtkinter.CTkButton(self, text="Get rid of it", command=self.radiobtn_test_group.deselect_all)
        # combo box = option menu with entry field
        self.combo_box = customtkinter.CTkComboBox(self, values=["option 1", "option 2"], command=self.combobox_callback)
        self.optionmenu = customtkinter.CTkOptionMenu(self, values=["option 1", "option 2"], command=self.optionmenu_callback)
        self.progress_bar = customtkinter.CTkProgressBar(self, mode="determinate", determinate_speed=0.1)
        self.slider = customtkinter.CTkSlider(self, from_=0, to=10, number_of_steps=10, command=self.set_progressbar)
        self.scrollbar = customtkinter.CTkScrollbar(self, orientation="horizontal")
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, width=200, height=200)
        self.rb_list = CombinedRadioBtns()
        for i in range(10):
            text_rb = f'Radiobtn {i}'
            rb = customtkinter.CTkRadioButton(self.scrollable_frame, text=text_rb, value=i)
            rb.pack(pady=10) 
            self.rb_list.add_radiobtns([rb])
        self.not_round_btn = customtkinter.CTkButton(self, text="round btn", corner_radius=6, command=self.rb_list.radiobtn_event)
        self.segment_btn = customtkinter.CTkSegmentedButton(self, )



        self.label.grid(row=0, column=0, sticky="we")
        self.button.grid(row=1, column=0, sticky="we")
        self.frame.grid(row=2, column=0, sticky="we")
        self.frame_into_frame.grid(row=0, column=0, sticky="n", padx=(10,10), pady=(10,10))
        self.window_btn.grid(row=3, column=0, sticky="n")
        self.toplevel_window = None
        self.entry.grid(row=4, column=0, sticky="n")
        self.entry2.grid(row=5, column=0, sticky="n")
        self.disabled_btn.grid(row=6, column=0, sticky="n")
        self.not_round_btn.grid(row=7, column=0, sticky="n")
        self.checkbox.grid(row=8, column=1, sticky="n")
        self.checkbox2.grid(row=9, column=1, sticky="n")
        self.switch.grid(row=10, column=0, sticky="n")
        self.radiobtn.grid(row=11, column=0, sticky="n")
        self.radiobtn2.grid(row=12, column=0, sticky="n")
        self.select_radio_btn.grid(row=13)
        self.select_radio_btn2.grid(row=14)
        self.combo_box.grid(row=15)
        self.optionmenu.grid(row=16)
        self.progress_bar.grid(row=1, column=1)
        # set progress bar to start at 0
        self.progress_bar.set(0)
        self.progress_bar.start()

        self.slider.grid(row=2, column=1)
        self.scrollbar.grid(row=3, column=1)
        self.scrollable_frame.grid(row=4, column=1)




        
        
    def change_theme(self):
        self.current_theme = self.settings["mode"]
        if self.current_theme == "light":
            self.settings["mode"] = "dark"
        else:
            self.settings["mode"] = "light"
        customtkinter.set_appearance_mode(self.settings["mode"])

    def create_window(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(root=self)
            # disables other main window until its closed
            self.toplevel_window.grab_set()
        else:
            self.toplevel_window.focus()
    
    def disable_it(self):
        self.checkbox.configure(state="disabled")

    def toggle_all(self):
        # weird interaction between the disable command and toggle, because its only in normal state available
        self.checkbox.deselect()    
    
    def combobox_callback(self, choice):
        print("combobox dropdown clicked:", choice)

    def optionmenu_callback(self, choice):
        print("option box dropdown clicked:", choice)

    def set_progressbar(self, value):
        self.progress_bar.set(int(value)/10)

        
            

if __name__ == "__main__":
    #app = AutoamtionAdditon(self.lang["PROJECT"] + "/" + self.lang["NEW_A"])
    app = TestWindow()
    app.mainloop()