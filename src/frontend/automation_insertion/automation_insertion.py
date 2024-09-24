"""
This frontend module is responsible for the automation insertion windows.
"""

from os import path
from threading import Thread
from tkinter import TclError
from tkinter import filedialog as fd
from typing import Tuple

import customtkinter

from backend import automation_gen as ag
from backend.utils.env_helper_classes import Automation
from frontend.customWidgets import customWidgets as cW

from .automation_entities import AutomationEntityFrame


class AutomationCreationFrame(cW.BasisFrame):
    """
    The window class which combines all the widgets for the automation insertion window

    Args:
        cW.BlankWindow (class): custom blank basic window for the application
    """

    def __init__(self, app):
        """
        Initialization of the automation insertion window with a entry for the name, textbox for the automation code and buttons to add and delete the code

        Args:
            app (customtkinter.CTK): the parent window of the automation insertion frame
            project (str): the name of the project the automation is added to
        """

        # create the basis frame for the automation insertion window
        super().__init__(app=app, layer=0)

        if app.selected_project is None:
            nav_path = str(app.lang["NEW_A"])
        else:
            nav_path = str(app.selected_project + "/" + app.lang["NEW_A"])

        self.grid_columnconfigure(0, weight=1)

        self.nav_bar = cW.NavigationBar(
            self,
            mode=app.settings["MODE"],
            nav_path=nav_path,
        )

        self.nav_bar.grid(row=0, column=0, sticky="ew")

        self.entry = customtkinter.CTkEntry(
            self, placeholder_text=app.lang["AUTO_NAME"], font=("Roboto", 16)
        )
        self.entry.grid(row=1, column=0, sticky="we", padx=50, pady=(15, 5))

        # the textbox for the automation code is below the text insertion tools but needs to be initialized first
        # to be able to reference it in the text insertion tools
        self.textbox = customtkinter.CTkTextbox(
            self,
            font=("Roboto", 16),
            wrap="none",
            undo=True,
            maxundo=3,
        )
        self.textbox.grid(row=3, column=0, sticky="news", padx=50, pady=(0, 23))
        self.grid_rowconfigure(3, weight=1)

        self.text_tool_btns = TextToolBtns(root=self, app=app)
        self.text_tool_btns.grid(
            row=2, column=0, padx=(50, 50), pady=(10, 10), sticky="news"
        )

        self.navigaton_buttons = CustomNavButtons(
            self,
            objects=2,
            values=[app.lang["BACK"], app.lang["NEXT"]],
        )
        self.navigaton_buttons.grid(
            row=4, column=0, padx=(25, 25), pady=(0, 20), sticky="news"
        )

    def load_automation(self, automation_path: str):
        """
        Load the automation data from the automation file

        Args:
            automation_path (str): the path to the automation file
        """
        # if no file is selected, return
        if automation_path == "":
            return

        with open(automation_path, "r") as file:
            # get the name of the automation from the file name
            self.entry.delete(0, "end")
            self.entry.insert(0, path.basename(automation_path).split(".")[0])

            # get the content of the file and insert it into the textbox
            self.textbox.delete("0.0", "end")
            self.textbox.insert("0.0", file.read())


class TextToolBtns(customtkinter.CTkFrame):
    """
    Frame for the automation insertion window with all the buttons for the textbox manipulation.
    Contains buttons for importing, undoing, redoing and saving the automation code.

    Args:
        customtkinter.CTkFrame (class): extended custom tkinter node for a ctk frame
    """

    def __init__(self, app, root, **kwargs):
        """
        Initialization of the frame for the automation insertion window with a entry for the name, textbox for the automation code and buttons to add and delete the code

        Args:
            root (customtkinter.CTKFrame): the parent frame is the automation insertion window
        """
        super().__init__(root, fg_color="transparent", **kwargs)

        self.app = app

        # create the buttons for the automation insertion window
        self.imp_btn = cW.AcceptButton(
            self,
            width=60,
            height=60,
            corner_radius=12,
            kind=0,
            command=self.textbox_load,
        )

        # TODO: add user defined path for loading the configuration files from the file system
        self.dir_path = path.join("data")
        self.imp_btn.grid(row=0, column=0, padx=(0, 15))

        self.undo_btn = cW.NeutralButton(
            self,
            width=60,
            height=60,
            corner_radius=12,
            kind=0,
            command=self.textbox_undo,
        )
        self.undo_btn.grid(row=0, column=1, padx=(0, 15))

        self.redo_btn = cW.NeutralButton(
            self,
            width=60,
            height=60,
            corner_radius=12,
            kind=1,
            command=self.textbox_redo,
        )
        self.redo_btn.grid(row=0, column=2, padx=(0, 15))

        self.save_btn = cW.AcceptButton(
            self,
            width=60,
            height=60,
            corner_radius=12,
            kind=1,
            command=self.textbox_save,
        )
        # TODO: add user defined path for saving the configuration files
        self.dir_path = path.join("data")
        self.save_btn.grid(row=0, column=3, padx=(0, 15))

    def textbox_load(self):
        """
        Loads the text from a yaml file into the textbox

        Args:
            self (TextToolBtns): the frame with the buttons for the textbox manipulation
        """
        file_name = fd.askopenfilename(
            filetypes=[("YAML files", "*.yaml")],
            title=self.app.lang["CHOOSE_FILE"],
            initialdir=self.dir_path,
        )
        self.master.load_automation(file_name)
        # TODO undo imports in the textbox with one undo step

    def textbox_undo(self):
        """
        Undoes the last action in the textbox

        Args:
            self (TextToolBtns): the frame with the buttons for the textbox manipulation
        """
        try:
            self.master.textbox.edit_undo()
        except TclError:
            cW.PopupWarning(
                app=self.app,
                title=self.app.lang["WARNING"],
                message=self.app.lang["NOTHING_UNDO"],
            )

    def textbox_redo(self):
        """
        Redoes the last undo in the textbox

        Args:
            self (TextToolBtns): the frame with the buttons for the textbox manipulation
        """
        try:
            self.master.textbox.edit_redo()
        except TclError:
            cW.PopupWarning(
                app=self.app,
                title=self.app.lang["WARNING"],
                message=self.app.lang["NOTHING_REDO"],
            )

    def textbox_save(self):
        """
        Saves the text in the textbox

        Args:
            self (TextToolBtns): the frame with the buttons for the textbox manipulation
        """

        # get text from line 0 character 0 till the end
        self.text = self.master.textbox.get("0.0", "end")

        # get the name of the automation
        self.auto_name = self.master.entry.get()

        file_name = fd.asksaveasfilename(
            filetypes=[("YAML files", "*.yaml"), ("All files", "*.*")],
            title=self.app.lang["SAVE_FILE"],
            defaultextension=".yaml",
            initialdir=self.dir_path,
            initialfile=self.auto_name,
            confirmoverwrite=True,
        )

        # if no file is selected, return
        if file_name == "":
            return

        with open(file_name, "w") as file:
            file.write(self.text)


class CustomNavButtons(cW.NavigationButtons):
    """
    Custom navigation buttons for the automation insertion window
    """

    def __init__(self, root, objects: int = 2, values: Tuple[str] = None):
        super().__init__(root, objects, values)

        self.version_option = customtkinter.CTkOptionMenu(
            self,
            values=root.app.settings["HA_VERSIONS"],
            width=130,
            height=30,
            command=self.version_select,
        )
        self.version_option.grid(row=0, column=1, padx=(0, 15), sticky="we")

    def btn_1_func(self):
        self.master.app.go_back(old_frame=self.master)

    def btn_2_func(self):
        # save the automation data to a yaml file
        with open("data/automation.yaml", "w") as file:
            file.write(self.master.textbox.get("0.0", "end"))

        def validate_and_load():
            # validate and load the new automation data
            self.master.app.curr_automation_config = ag.load_new_automation_data(
                "data/automation.yaml"
            )

        def check_thread(thread):
            if thread.is_alive():
                self.master.app.after(100, check_thread, thread)
            else:
                after_loading()

        def after_loading():
            if self.master.app.curr_automation_config is None:
                new_frame = self.master.app.go_back(old_frame=self.master)
                new_frame.load_automation("data/automation.yaml")
                cW.PopupWarning(
                    app=self.master.app,
                    title=self.master.app.lang["WARNING"],
                    message=self.master.app.lang["INVALID_AUTOMATION"],
                    # TODO: add the error / exception message to the popup
                )
            else:
                # load the automation entity frame for selecting the integrations for the entities of the automation
                automation: Automation =  self.master.app.curr_automation_config["infos"]
                self.master.app.load_new_frame(
                    prev_frame=self.master,
                    
                    new_frame=AutomationEntityFrame(
                        self.master.app,
                        automation_name=automation.a_name,
                    ),
                )

        # Start the validation and loading thread to prevent the GUI from freezing
        validate_thread = Thread(target=validate_and_load)
        validate_thread.start()

        # Run the loading screen on the main thread
        self.master.app.load_new_frame(
            prev_frame=self.master, new_frame=LoadingFrame(self.master.app)
        )

        # Check if the thread is still running
        self.master.app.after(100, check_thread, validate_thread)

    def version_select(self, choice):
        print("optionmenu dropdown clicked:", str(choice))
        print("optionmenu dropdown clicked:", str(choice))


class LoadingFrame(cW.BasisFrame):
    def __init__(self, app):
        super().__init__(app=app, layer=0)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.loading_context = LoadingContext(app=self.app, root=self)

        self.loading_context.grid(
            row=0, column=0, pady=(50, 0), padx=(50, 50), sticky="news"
        )

        self.cancel_btn = cW.DeleteButton(
            self,
            text=self.app.lang["CANCEL"],
            command=self.cancel_loading,
        )

        self.cancel_btn.grid(row=1, column=0, pady=(20, 50), padx=(50, 50), sticky="ns")

    def cancel_loading(self):
        automation_ins_frame = self.app.go_back(old_frame=self)
        # reload the automation from before the loading screen
        automation_ins_frame.load_automation("data/automation.yaml")


class LoadingContext(cW.BasisFrame):
    def __init__(self, app, root):
        super().__init__(app=app, root=root, layer=1)

        self.binding_frame = customtkinter.CTkFrame(self)
        self.binding_frame.columnconfigure(0, weight=1)
        self.binding_frame.grid(row=0, column=0, sticky="ew")

        # TODO wrap the text in the label if the window is too small
        self.loading_label = customtkinter.CTkLabel(
            self.binding_frame,
            text=app.lang["LOADING_AUTOMATION"],
            font=("Roboto", 16),
        )
        self.loading_label.grid(row=1, column=0, sticky="we", padx=50, pady=(15, 5))

        self.loading_bar = customtkinter.CTkProgressBar(
            self.binding_frame, mode="indeterminate", determinate_speed=0.1
        )
        self.loading_bar.grid(row=2, column=0, sticky="we", padx=50, pady=(15, 5))
        self.loading_bar.set(0)
        self.loading_bar.start()

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
