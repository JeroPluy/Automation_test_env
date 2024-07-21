import json
import tkinter
from os import path
from typing import Tuple

import customtkinter
from PIL import Image

import customWidgets.customWidgets as cW
import db
from customWidgets.CTkTable.ctktable import CTkTable
from customWidgets.CTkXYFrame.ctk_xyframe import CTkXYFrame

#ctkmessagebox

#ctktooltip
#ctkscrollabledropdown

#ctklistbox
#ctkrangeslider





def load_settings():
    #print(path.join(path.dirname(path.realpath(__file__))))
    with open("settings/settings.json", "r") as json_settings:
        return json.load(json_settings)
    
def load_language(lang):
    with open("settings/appLang.json", "r", encoding="utf8") as json_lang:
        langs = json.load(json_lang)
        selected_lang = {}
        for key in langs:
            selected_lang[key] = langs.get(key)[lang]
        return selected_lang
    
class BlankWindow(customtkinter.CTk):
    """Basic Window for the application  

    Args:
        customtkinter (_type_): standard custom tkinter node for a ctk application
    
    """
    def __init__(self, fg_color: str | Tuple[str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.title("title of the App")
        self.geometry("800x800")
        self.settings = load_settings()
        self.lang = load_language(self.settings["LANG"])
        customtkinter.set_default_color_theme("settings/theme.json")
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
        self.scrollable_frame = CTkXYFrame(self, width=400, height=400)
        self.header_font = customtkinter.CTkFont(weight="bold")
        self.label = customtkinter.CTkLabel(self.scrollable_frame, text="Testlabe", font=self.header_font)
        self.button = customtkinter.CTkButton(self.scrollable_frame, text="testbutton", height=60, command=self.change_theme)
        self.frame = customtkinter.CTkFrame(self)
        self.frame_into_frame = customtkinter.CTkFrame(self.frame)
        self.window_btn = customtkinter.CTkButton(self.scrollable_frame, text="new window", command=self.create_window)
        self.entry = customtkinter.CTkEntry(self.scrollable_frame, placeholder_text="placeholderText")
        self.entry2 = customtkinter.CTkEntry(self.scrollable_frame, placeholder_text="placeholderText")
        self.disabled_btn = customtkinter.CTkButton(self.scrollable_frame, text="diabled", state="disabled")
        self.checkbox = customtkinter.CTkCheckBox(self, text="checkbox text", command=self.disable_it)
        self.checkbox2 = customtkinter.CTkCheckBox(self, text="checkbox 2", command=self.toggle_all)
        self.switch = customtkinter.CTkSwitch(self.scrollable_frame, text="switch text")
        self.radiobtn_test_group = CombinedRadioBtns()
        self.radiobtn = customtkinter.CTkRadioButton(self.scrollable_frame, text="radio text", value=1)
        self.radiobtn2 = customtkinter.CTkRadioButton(self.scrollable_frame, text="radio 2", value=2)
        self.radiobtn_test_group.add_radiobtns([self.radiobtn, self.radiobtn2],1)
        self.select_radio_btn = customtkinter.CTkButton(self.scrollable_frame, text="whats selected?", command=self.radiobtn_test_group.radiobtn_event)
        self.select_radio_btn2 = customtkinter.CTkButton(self.scrollable_frame, text="Get rid of it", command=self.radiobtn_test_group.deselect_all)
        # combo box = option menu with entry field
        self.combo_box = customtkinter.CTkComboBox(self.scrollable_frame, values=["option 1", "option 2"], command=self.combobox_callback)
        self.optionmenu = customtkinter.CTkOptionMenu(self.scrollable_frame, values=["option 1", "option 2"], command=self.optionmenu_callback)
        self.progress_bar = customtkinter.CTkProgressBar(self, mode="determinate", determinate_speed=0.1)
        self.slider = customtkinter.CTkSlider(self, from_=0, to=10, number_of_steps=10, command=self.set_progressbar)
        self.scrollbar = customtkinter.CTkScrollbar(self, orientation="horizontal")
        self.rb_list = CombinedRadioBtns()
        self.rb_frame = customtkinter.CTkScrollableFrame(self, width=200, height=300)
        for i in range(10):
            text_rb = f'Radiobtn {i}'
            rb = customtkinter.CTkRadioButton(self.rb_frame, text=text_rb, value=i)
            rb.pack(pady=10) 
            self.rb_list.add_radiobtns([rb])
        self.not_round_btn = customtkinter.CTkButton(self, text="round btn", corner_radius=6, command=self.rb_list.radiobtn_event)
        self.segment_btn = customtkinter.CTkSegmentedButton(self, )
        self.text_box = customtkinter.CTkTextbox(self, wrap="none", undo=True, maxundo=3)
        self.text_box.bind("<FocusIn>", self.remove_placeholder)
        self.placeholder_text = "Copy YAML here.\n"
        self.text_box.insert("0.0", self.placeholder_text)
        self.text_undo_btn = customtkinter.CTkButton(self, command=self.undo_last_change)

        self.rotating = False
        self.spin = 0
        self.moving_img = customtkinter.CTkImage(light_image=Image.open(path.join(path.dirname(path.realpath(__file__)), "customWidgets/icons/loading_up_b.png")), dark_image=Image.open(path.join(path.dirname(path.realpath(__file__)),"customWidgets/icons/loading_up_w.png")), size=(40,40))
        self.img_label = customtkinter.CTkLabel(self, text="", image=self.moving_img)
        self.button_img = customtkinter.CTkButton(self, text="Load", command=self.toggle_clock)

        table_header = ["overview", "first", "second", "third", "fourth", "fifth"]
        table_data = [[x for x in range(5)] for x in range(10)]
        table_data.insert(0,table_header)
        self.table = CTkTable(self.scrollable_frame, corner_radius=0, wraplength=200 ,values=table_data, header_color="#1D91DA", write=False, hover=True, command=self.select_row_and_data)
        self.selected_tb_data = None

        self.navigation_btns = cW.NavigationButtons(self, values=[self.lang["BACK"], self.lang["NEXT"]])

        self.scrollable_frame.grid(row=0, column=0, rowspan=3)

        self.label.grid(row=0, column=0, sticky="w")
        self.button.grid(row=1, column=0, sticky="w")
        self.window_btn.grid(row=3, column=0, sticky="wn")
        self.toplevel_window = None
        self.entry.grid(row=4, column=0, sticky="wn")
        self.entry2.grid(row=5, column=0, sticky="wn")
        self.disabled_btn.grid(row=6, column=0, sticky="wn")
        self.not_round_btn.grid(row=7, column=0, sticky="wn")
        self.checkbox.grid(row=8, column=1, sticky="wn")
        self.checkbox2.grid(row=9, column=1, sticky="wn")
        self.switch.grid(row=10, column=0, sticky="wn")
        self.radiobtn.grid(row=11, column=0, sticky="wn")
        self.radiobtn2.grid(row=12, column=0, sticky="wn")
        self.select_radio_btn.grid(row=13)
        self.select_radio_btn2.grid(row=14)
        self.combo_box.grid(row=15)
        self.optionmenu.grid(row=16)
        self.table.grid(row=20, column=0)

        self.frame.grid(row=2, column=0, sticky="w")
        self.frame_into_frame.grid(row=0, column=0, sticky="wn", padx=(10,10), pady=(10,10))



        self.text_box.grid(row=1, column=1, sticky="news")
        self.text_undo_btn.grid(row=2,column=1, sticky="news")

        self.progress_bar.grid(row=3, column=1, sticky="ew")
        # set progress bar to start at 0
        self.progress_bar.set(0)
        self.progress_bar.start()

        self.slider.grid(row=4, column=1, sticky="ew")
        self.scrollbar.grid(row=5, column=1, sticky="news")

        self.img_label.grid(row=6, column=1, sticky="news")
        self.button_img.grid(row=7, column=1, sticky="news")

        self.rb_frame.grid(row=8, column=1, sticky="news")

        self.navigation_btns.grid(row=0, column=2)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)


        
        
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
    
    def undo_last_change(self):
        try:
            self.text_box.edit_undo()
        except tkinter.TclError:
            print("nothing to undo")

    def remove_placeholder(self, event):
        print(self.text_box.get("0.0","1.0"))
        if self.text_box.get("0.0","end") == self.placeholder_text +'\n':
            print(True)
            self.text_box.delete("0.0", "end") 

    def rotate_the_clock(self, angle):
           spinning_img_white = Image.open(path.join(path.dirname(path.realpath(__file__)), "customWidgets/icons/loading_up_w.png"))
           spinning_img_black = Image.open(path.join(path.dirname(path.realpath(__file__)), "customWidgets/icons/loading_up_b.png"))
           self.moving_img = customtkinter.CTkImage(light_image=spinning_img_black.rotate(angle), dark_image=spinning_img_white.rotate(angle), size=(40,40))

    def animate_the_clock(self):
        if self.rotating:
            self.spin += 5
            self.rotate_the_clock(self.spin)
            self.img_label = customtkinter.CTkLabel(self, text="", image=self.moving_img)
            self.img_label.grid(row=6, column=1, sticky="news")
            
            self.after(50, self.animate_the_clock)

    def toggle_clock(self):
        self.rotating = not self.rotating
        if self.rotating:
            self.animate_the_clock()
    
    def select_row_and_data(self, data):
        # self.data[i,j] = {"row": i, "column" : j, "value" : value, "args": args}
        if self.selected_tb_data is not None:
            self.table.deselect_row(self.selected_tb_data["row"])
        self.selected_tb_data = data
        print(self.selected_tb_data)
        self.table.select_row(self.selected_tb_data.get("row"))




if __name__ == "__main__":
    # app = AutoamtionAdditon(self.lang["PROJECT"] + "/" + self.lang["NEW_A"])
    app = TestWindow()
    app.mainloop()
