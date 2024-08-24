"""
This frontend module is responsible for the automation insertion windows.
"""

from os import path
from typing import Tuple
from tkinter import TclError, filedialog as fd
import customtkinter

from frontend.customWidgets import customWidgets as cW


class BlankToplevelWindow(customtkinter.CTkToplevel):
    """
    Basic top level window for warnings and errors
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


class customNavButtons(cW.NavigationButtons):
    """
    Custom navigation buttons for the automation insertion window
    """

    def __init__(self, master, objects: int = 2, values: Tuple[str] = None):
        super().__init__(master, objects, values)
        self.version_option = customtkinter.CTkOptionMenu(
            self,
            values=master.settings["HA_VERSIONS"],
            width=130,
            height=30,
            command=self.version_select,
        )
        self.version_option.grid(row=0, column=1, padx=(0, 15), sticky="we")

    def nav_back(self):
        print("go back")

    def nav_forwards(self):
        print("go next")

    def version_select(self, choice):
        print("optionmenu dropdown clicked:", str(choice))


class AutoamtionInsertionFrame(customtkinter.CTkFrame):
    """
    Frame for the automation insertion window with a entry for the name, textbox for the automation code and buttons to add and delete the code

    Args:
        customtkinter.CTkFrame (class): extended custom tkinter node for a ctk frame
    """

    def __init__(self, master, **kwargs):
        """
        Initialization of the frame for the automation insertion window with a entry for the name, textbox for the automation code and buttons to add and delete the code

        Args:
            master (customtkinter.CTKFrame): the parent frame of the automation insertion frame
        """
        super().__init__(master, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.textbox = customtkinter.CTkTextbox(
            self,
            width=330,
            height=132,
            font=("Roboto", 16),
            wrap="none",
            undo=True,
            maxundo=3,
        )
        self.textbox.grid(row=0, column=0, sticky="news", rowspan=2, padx=(0, 10))

        self.imp_btn = cW.acceptButton(
            self,
            width=60,
            height=60,
            corner_radius=12,
            kind=0,
            command=self.textbox_load,
        )
        self.window_title = master.lang["CHOOSE_FILE"]
        self.dir_path = path.join("data")
        self.imp_btn.grid(row=0, column=1, sticky="nw", pady=(0, 5))

        self.undo_btn = cW.neutralButton(
            self,
            width=60,
            height=60,
            corner_radius=12,
            kind=0,
            command=self.textbox_undo,
        )
        self.undo_btn.grid(row=1, column=1, sticky="nw", pady=(5, 0))

    def textbox_load(self):
        """
        Loads the text from a yaml file into the textbox
        """
        file_name = fd.askopenfilename(
            filetypes=[("YAML files", "*.yaml")],
            title=self.window_title,
            initialdir=self.dir_path,
        )
        with open(file_name, "r") as file:
            self.textbox.insert("1.0", file.read())

    def textbox_undo(self):
        """
        Undoes the last action in the textbox
        """
        try:
            self.textbox.edit_undo()
        except TclError:
            pass
            # TODD popup warning "Nothing to undo"

    def safe_text(self):
        """
        Saves the text in the textbox
        """
        self.text = self.textbox.get(
            "0.0", "end"
        )  # get text from line 0 character 0 till the end


class AutomationAddition(cW.BlankWindow):
    """
    The base window for adding a new automation to the database with the insertion frame displayed first

    Args:
        cW.BlankWindow (class): custom blank basic window for the application
    """

    def __init__(self, project):
        super().__init__()
        self.title("title of the App")
        self.geometry("600x600")
        self.grid_columnconfigure(0, weight=1)

        self.nav_bar = cW.NavigationBar(
            self,
            mode=self.settings["mode"],
            auto_path=str(project + "/" + self.lang["NEW_A"]),
        )
        self.nav_bar.grid(row=0, column=0, sticky="ew")

        self.entry = customtkinter.CTkEntry(
            self, placeholder_text=self.lang["AUTO_NAME"], font=("Roboto", 16)
        )
        self.entry.grid(row=1, column=0, sticky="we", padx=50, pady=(10, 10))

        self.insertion_frame = AutoamtionInsertionFrame(self)
        self.insertion_frame.grid(
            row=2, column=0, padx=(50, 50), pady=(10, 23), sticky="news"
        )

        self.navigaton_buttons = customNavButtons(
            self, objects=2, values=[self.lang["BACK"], self.lang["NEXT"]]
        )
        self.navigaton_buttons.grid(
            row=3, column=0, padx=(50, 50), pady=(0, 15), sticky="news"
        )
