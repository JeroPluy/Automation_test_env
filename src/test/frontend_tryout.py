"""
This is a test file to try out the custom tkinter widgets and the custom tkinter package for the application frontend

If the dont work properly, because some modules are not found, please run the following commands in the terminal:

$env:PYTHONPATH = "..\\src"

In some environments, the PYTHONPATH needs to be set to the src directory.
"""

import tkinter
from os import path
from typing import Tuple

import customtkinter
from PIL import Image

from frontend.customWidgets import customWidgets as cW
from frontend.customWidgets.CTkTable import CTkTable
from frontend.customWidgets.CTkXYFrame import CTkXYFrame
from frontend.utils import ICON_PATH, THEME_PATH, load_language, load_settings

# untested widgets which could be useful in the future
# ctkmessagebox
# ctktooltip
# ctkscrollabledropdown
# ctklistbox
# ctkrangeslider


class BlankWindow(customtkinter.CTk):
    """
    Basic Window for the application

    Args:
        customtkinter (_type_): standard custom tkinter node for a ctk application

    """

    def __init__(self, fg_color: str | Tuple[str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.title("title of the App")
        self.geometry("500x500")
        self.settings = load_settings()
        self.lang = load_language(self.settings["LANG"])
        customtkinter.set_default_color_theme(THEME_PATH)
        customtkinter.set_appearance_mode(self.settings["MODE"])


class ToplevelWindow(customtkinter.CTkToplevel):
    """
    Basic Toplevel window for the application to be used as a popup 
    for example for error messages

    Args:
        customtkinter (_type_): standard custom tkinter node for a ctk toplevel window
    """
    
    def __init__(self, root=customtkinter.CTk, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Testwindow")
        self.resizable(False, False)
        self.attributes("-topmost", True)

        # center the toplevel window
        x = root.winfo_x() + root.winfo_width() // 2 - self.winfo_width() // 2
        y = root.winfo_y() + root.winfo_height() // 2 - self.winfo_height() // 2
        self.geometry(f"+{x}+{y}")


class CombinedRadioBtns:
    """
    Combine radio buttons to only select one at a time
    """
    def __init__(self):
        # the same variable combines radio buttons so only one is selectable
        self.variable = customtkinter.StringVar(value="nothing")

    def add_radiobtns(
        self, radiobtns: Tuple[customtkinter.CTkRadioButton], preselected: int = None
    ):
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
    """
    Test Window for the application to try out the custom tkinter widgets

    Args:
        BlankWindow (class): standard blank window class for the application
    """
    
    def __init__(self, fg_color: str | Tuple[str] | None = None, **kwargs):
        """
        Initialize the TestWindow

        Args:
            fg_color (str | Tuple[str] | None, optional): set the theme color of the window. Defaults to None.
        """
        
        super().__init__(fg_color, **kwargs)
        self.scrollable_frame = CTkXYFrame(self, width=800, height=800)
        self.header_font = customtkinter.CTkFont(weight="bold")
        self.label = customtkinter.CTkLabel(
            self.scrollable_frame, text="Testlabe", font=self.header_font
        )
        self.button = customtkinter.CTkButton(
            self.scrollable_frame,
            text="testbutton",
            height=60,
            command=self.change_theme,
        )
        self.frame = customtkinter.CTkFrame(self)
        self.frame_into_frame = customtkinter.CTkFrame(self.frame)
        self.window_btn = customtkinter.CTkButton(
            self.scrollable_frame, text="new window", command=self.create_window
        )        
        
        self.entry = customtkinter.CTkEntry(
            self.scrollable_frame, placeholder_text="placeholderText"
        )
        self.entry2 = customtkinter.CTkEntry(
            self.scrollable_frame, placeholder_text="placeholderText"
        )
        self.disabled_btn = customtkinter.CTkButton(
            self.scrollable_frame, text="diabled", state="disabled"
        )
        self.checkbox = customtkinter.CTkCheckBox(
            self, text="checkbox text", command=self.disable_it
        )
        self.checkbox2 = customtkinter.CTkCheckBox(
            self, text="checkbox 2", command=self.toggle_all
        )
        self.switch = customtkinter.CTkSwitch(self.scrollable_frame, text="switch text")
        self.radiobtn_test_group = CombinedRadioBtns()
        self.radiobtn = customtkinter.CTkRadioButton(
            self.scrollable_frame, text="radio text", value=1
        )
        self.radiobtn2 = customtkinter.CTkRadioButton(
            self.scrollable_frame, text="radio 2", value=2
        )
        self.radiobtn_test_group.add_radiobtns([self.radiobtn, self.radiobtn2], 1)
        self.select_radio_btn = customtkinter.CTkButton(
            self.scrollable_frame,
            text="whats selected?",
            command=self.radiobtn_test_group.radiobtn_event,
        )
        self.select_radio_btn2 = customtkinter.CTkButton(
            self.scrollable_frame,
            text="Get rid of it",
            command=self.radiobtn_test_group.deselect_all,
        )
        # combo box = option menu with entry field
        self.combo_box = customtkinter.CTkComboBox(
            self.scrollable_frame,
            values=["option 1", "option 2"],
            command=self.combobox_callback,
        )

        self.option_menu_frame = cW.BasisFrame(self, self.scrollable_frame, border_width=10, border_color="red", fg_color="red")
        self.optionmenu = customtkinter.CTkOptionMenu(
            self.option_menu_frame,
            values=["option 1", "option test"],
            command=self.optionmenu_callback,
        )
        self.optionmenu.grid(row=0, column=0, sticky="w")

        self.progress_bar = customtkinter.CTkProgressBar(
            self, mode="determinate", determinate_speed=0.1
        )
        self.slider = customtkinter.CTkSlider(
            self, from_=0, to=10, number_of_steps=10, command=self.set_progressbar
        )
        self.scrollbar = customtkinter.CTkScrollbar(self, orientation="horizontal")
        self.rb_list = CombinedRadioBtns()
        self.rb_frame = customtkinter.CTkScrollableFrame(self, width=200, height=300)
        for i in range(10):
            text_rb = f"Radiobtn {i}"
            rb = customtkinter.CTkRadioButton(self.rb_frame, text=text_rb, value=i)
            rb.pack(pady=10)
            self.rb_list.add_radiobtns([rb])
        self.not_round_btn = customtkinter.CTkButton(
            self.scrollable_frame, text="round btn", corner_radius=6, command=self.rb_list.radiobtn_event
        )
        self.segment_btn = customtkinter.CTkSegmentedButton(
            self,
        )
        self.text_box = customtkinter.CTkTextbox(
            self, wrap="none", undo=True, maxundo=3
        )
        self.text_box.bind("<FocusIn>", self.remove_placeholder)
        self.placeholder_text = "Copy YAML here.\n"
        self.text_box.insert("0.0", self.placeholder_text)
        self.text_undo_btn = customtkinter.CTkButton(
            self, command=self.undo_last_change
        )

        self.rotating = False
        self.spin = 0
        self.moving_img = customtkinter.CTkImage(
            light_image=Image.open(
                path.join(
                    ICON_PATH,
                    "loading_up_b.png",
                )
            ),
            dark_image=Image.open(
                path.join(
                    ICON_PATH,
                    "loading_up_w.png",
                )
            ),
            size=(40, 40),
        )
        self.img_label = customtkinter.CTkLabel(self, text="", image=self.moving_img)
        self.button_img = customtkinter.CTkButton(
            self, text="Load", command=self.toggle_clock
        )

        table_header = ["overview", "first", "second", "third", "fourth", "fifth"]
        table_data = [[x for x in range(5)] for x in range(10)]
        table_data.insert(0, table_header)
        self.table = CTkTable(
            self.scrollable_frame,
            corner_radius=0,
            wraplength=200,
            values=table_data,
            write=False,
            hover=True,
            multi_select=True,
            command=self.select_row_and_data,
        )
        self.selected_tb_data = None

        self.navigation_btns = TestNavBtns(self, ("Button 1", "Button 2"))  
        


        # grid the widgets
        
        # first row of the grid
        self.scrollable_frame.grid(row=0, column=0, rowspan=4)
        self.label.grid(row=0, column=0, sticky="w")
        self.button.grid(row=1, column=0, sticky="w")
        self.window_btn.grid(row=3, column=0, sticky="wn")
        self.toplevel_window = None
        self.entry.grid(row=4, column=0, sticky="wn")
        self.entry2.grid(row=5, column=0, sticky="wn")
        self.disabled_btn.grid(row=6, column=0, sticky="wn")
        self.not_round_btn.grid(row=7, column=0, sticky="wn")
        self.switch.grid(row=10, column=0, sticky="wn")
        self.radiobtn.grid(row=11, column=0, sticky="wn")
        self.radiobtn2.grid(row=12, column=0, sticky="wn")
        self.select_radio_btn.grid(row=13)
        self.select_radio_btn2.grid(row=14)
        # self.combo_box.grid(row=15)
        self.option_menu_frame.grid(row=16)
        self.scrollable_frame.rowconfigure(16, weight=1)
        self.table.grid(row=20, column=0)
        
        self.checkbox.grid(row=4, column=0, sticky="wn")
        self.checkbox2.grid(row=5, column=0, sticky="wn")

        # self.frame.grid(row=2, column=3, sticky="w")
        # self.frame_into_frame.grid(
        #     row=0, column=0, sticky="wn", padx=(10, 10), pady=(10, 10)
        # )

        self.text_box.grid(row=1, column=1, sticky="news")
        self.text_undo_btn.grid(row=2, column=1, sticky="news")

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

        self.columnconfigure((0, 1), weight=1)

    def change_theme(self):
        """
        Change the theme of the application
        """
        self.current_theme = self.settings["MODE"]
        if self.current_theme == "light":
            self.settings["MODE"] = "dark"
        else:
            self.settings["MODE"] = "light"
        customtkinter.set_appearance_mode(self.settings["MODE"])

    def create_window(self):
        """
        Create a new toplevel window and disable the main window
        """
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(root=self)
            # disables other main window until its closed
            self.toplevel_window.grab_set()
        else:
            self.toplevel_window.focus()

    def disable_it(self):
        """
        Disable the checkbox
        """
        self.checkbox.configure(state="disabled")

    def toggle_all(self):
        """
        Toggle the state of the checkbox
        """
        # weird interaction between the disable command and toggle, because its only in normal state available
        self.checkbox.deselect()

    def combobox_callback(self, choice):
        """
        Print the choice of the combobox if clicked

        Args:
            choice (_type_): the choice of the combobox
        """
        print("combobox dropdown clicked:", choice)

    def optionmenu_callback(self, choice):
        """
        Print the choice of the optionmenu if clicked

        Args:
            choice (_type_): the choice of the optionmenu
        """
        print("option box dropdown clicked:", choice)

    def set_progressbar(self, value: int | float):
        """
        Set the progress bar to a specific value

        Args:
            value (int | float): the value to set the progress bar to
        """
        self.progress_bar.set(int(value) / 10)

    def undo_last_change(self):
        """
        Undo the last change in the textbox
        """
        try:
            self.text_box.edit_undo()
        except tkinter.TclError:
            print("nothing to undo")

    def remove_placeholder(self):
        """
        Remove the placeholder text if the textbox is clicked
        """
        print(self.text_box.get("0.0", "1.0"))
        if self.text_box.get("0.0", "end") == self.placeholder_text + "\n":
            print(True)
            self.text_box.delete("0.0", "end")

    def rotate_the_clock(self, angle: int):
        """
        Rotate the clock image by a specific angle to animate it spinning

        Args:
            angle (int): the angle to rotate the image to 0 - 360
        """
        spinning_img_white = Image.open(
            path.join(
                ICON_PATH,
                "loading_up_w.png",
            )
        )
        spinning_img_black = Image.open(
            path.join(
                ICON_PATH,
                "loading_up_b.png",
            )
        )
        self.moving_img = customtkinter.CTkImage(
            light_image=spinning_img_black.rotate(angle),
            dark_image=spinning_img_white.rotate(angle),
            size=(40, 40),
        )

    def animate_the_clock(self):
        """
        Animate the clock image spinning by 5 degrees every 50ms
        """
        if self.rotating:
            self.spin += 5
            self.rotate_the_clock(self.spin)
            self.img_label = customtkinter.CTkLabel(
                self, text="", image=self.moving_img
            )
            self.img_label.grid(row=6, column=1, sticky="news")

            self.after(50, self.animate_the_clock)

    def toggle_clock(self):
        """
        Toggle the clock image spinning animation
        """
        self.rotating = not self.rotating
        if self.rotating:
            self.animate_the_clock()

    def select_row_and_data(self, data: dict):
        """
        Select a row in the table and get the data of the selected row to print

        Args:
            data (dict): the data of the selected row in the table as a dictionary 
                        contains: {"row": i, "column" : j, "value" : value, "args": args}
        """
        # self.data[i,j] = {"row": i, "column" : j, "value" : value, "args": args}
        # if self.selected_tb_data is not None:
        #     self.table.deselect_row(row)
        self.table.select_row(data.get("row"))
    


class TestNavBtns(cW.NavigationButtons):
    def __init__(self, root, values):
        super().__init__(root=root, values=values)
        self.root = root

    def btn_1_func(self):
        print("Button 1 clicked")
        print(self.root.table.get_selected_rows())
        
    def btn_2_func(self):
        print("Button 2 clicked")

class TestWindow2(BlankWindow):
    def __init__(self):
        super().__init__()
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)


        self.base_frame = cW.BasisFrame(self, self, layer=0)
        self.base_frame.grid(row=0, column=0, sticky="news")
        self.base_frame.columnconfigure(0, weight=1)
        
        self.btn = customtkinter.CTkButton(self.base_frame, text="test")
        self.btn.grid(row=0, column=0)
        

        self.scrollable_frame = cW.BasisScrollFrame(app=self, root=self.base_frame, layer=1)
        self.scrollable_frame.grid(row=1, column=0, sticky="news")
        self.scrollable_frame.columnconfigure(0, weight=1)
        
        self.text_box = customtkinter.CTkTextbox(
            self.scrollable_frame.content, wrap="none", undo=True, maxundo=3
        )
        
        self.text_box.grid(row=0, column=0, sticky="news")
        
        self.header_font = customtkinter.CTkFont(weight="bold")
        self.label = customtkinter.CTkLabel(
            self.scrollable_frame.content, text="Testlabe", font=self.header_font
        )
        self.label.grid(row=1, column=0, sticky="w")
        
        self.button = customtkinter.CTkButton(
            self.scrollable_frame.content,
            text="testbutton",
            height=60,
        )
        self.button.grid(row=2, column=0, sticky="w")

        self.layer_3_frame = cW.BasisFrame(self, self.base_frame, layer=4)
        self.layer_3_frame.grid(row=3, column=0, sticky="news")

        self.optionmenu = customtkinter.CTkOptionMenu(
            self.layer_3_frame,
            values=["option 1", "option test"],
        )
        self.optionmenu.grid(row=0, column=0, sticky="news")

        self.optionmenu2 = cW.FramedOptionMenu(
            root=self.layer_3_frame,
            values=["option 1", "option test"],
            default_value="option 1",
        )
        self.optionmenu2.grid(row=1, column=0, sticky="news")




if __name__ == "__main__":

    # app = AutoamtionAdditon(self.lang["PROJECT"] + "/" + self.lang["NEW_A"])
    app = TestWindow()
    app.mainloop()
