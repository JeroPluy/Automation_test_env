from frontend.customWidgets import customWidgets as cW

from frontend.automation_details import automation_details_main as aD

from backend import database as db

from .automation_infos import AutomationInfosFrame
from .automation_insertion_utils import clear_automation_insertion_frames

from customtkinter import CTkTextbox, CTkFont


class AutomationScriptFrame(cW.BasisFrame):
    """
    The frame class displaying the automation script and the path to the script
    """

    def __init__(self, app, automation_name):
        """
        Initialization of the automation script frame

        Args:
            app (customtkinter.CTK): the parent window of the automation script frame
            automation_name (str): the name of the new automation
        """
        # TODO clear the creation frames form the frame stack

        super().__init__(app=app, layer=0)

        # Define the underline font
        underline_font = CTkFont(family="Roboto", size=16, underline=True)

        if app.selected_project is None:
            self.nav_path = automation_name
        else:
            self.nav_path = str(app.selected_project + "/" + automation_name)

        self.nav_bar = cW.NavigationBar(
            self,
            mode=app.settings["MODE"],
            nav_path=self.nav_path,
        )

        self.main_content_frame = cW.BasisFrame(app, self, layer=1)

        self.path_label_frame = cW.BasisFrame(app, self.main_content_frame, layer=2)

        self.script_path_label = cW.CTkLabel(
            self.path_label_frame,
            text=app.lang["SCRIPT_PATH"] + ":",
        )

        self.path_label = cW.CTkLabel(
            self.path_label_frame,
            text=app.new_automation.config["infos"].script,
            font=underline_font,
            wraplength=600,
        )

        self.script_content = CTkTextbox(
            master=self.main_content_frame, font=("Lucida Console", 16)
        )
        self.load_automation_script(
            app.new_automation.config["infos"].script, self.script_content
        )

        self.nav_btns = self.navigation_buttons = NavBtns(
            root=self, values=(app.lang["FINISH"], app.lang["ADD_INFO"])
        )
        
        # --- grid the elements ---

        # grid the main elements
        self.nav_bar.grid(row=0, column=0, sticky="ew")
        self.main_content_frame.grid(
            row=1, column=0, sticky="news", pady=(15, 10), padx=(25)
        )
        self.navigation_buttons.grid(row=2, column=0, sticky="ew")
        
        # make the content frame resizable depending on the window size
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        ## grid the elements inside the content frame
        self.path_label_frame.grid(row=0, column=0, sticky="ew", padx=(10), pady=(10))
        self.script_content.grid(
            row=1, column=0, sticky="news", padx=(10), pady=(0, 10)
        )
        
        ## make the script textbox inside the content frame resizable
        self.main_content_frame.columnconfigure(0, weight=1)
        self.main_content_frame.rowconfigure(1, weight=1)

        
        ## grid the elements inside the path label frame
        self.script_path_label.grid(
            row=0, column=0, sticky="w", padx=(10, 0), pady=(10)
        )
        self.path_label.grid(row=0, column=1, sticky="ew", padx=(5, 10), pady=(10))
        
        ## make the path inside the path label frame resizable
        self.path_label_frame.columnconfigure(1, weight=1)



    def load_automation_script(self, script_path: str, textbox: CTkTextbox):
        """
        Load the sript content from the script file

        Args:
            script_path (str): the path to the script file
            textbox (CTkTextbox): the textbox to display the script content
        """
        # if no file is selected, return
        if script_path == "":
            return

        with open(script_path, "r") as file:
            # get the content of the file and insert it into the textbox
            textbox.delete("0.0", "end")
            textbox.insert("0.0", file.read())
            textbox.configure(state="disabled")


class NavBtns(cW.NavigationButtons):
    def __init__(self, root, values):
        """
        Initialization of the navigation buttons for the automation information frame

        Args:
            root (customtkinter.CTK): the root frame of the navigation buttons
            values (Tuple[str]): the values of the navigation buttons
        """
        self.root = root
        super().__init__(root, values=values, options={"btn_1_type": "accept"})

    def btn_1_func(self):
        """
        Functionality of the first navigation button (finish the automation creation)
        """

        automation = self.master.app.new_automation.config["infos"]

        db.add_additional_info(self.root.app.new_automation.a_id)

        clear_automation_insertion_frames(stack=self.master.app.frame_stack)

        self.root.app.load_new_frame(
            prev_frame=self.root,
            new_frame=aD.AutomationDetailsFrame(
                app=self.root.app,
                a_id=self.root.app.new_automation.a_id,
                automation_name=automation.a_name,
            ),
            returnable=True,
        )

    def btn_2_func(self):
        """
        Functionality of the second navigation button (add more information to the automation)
        """
        automation = self.master.app.new_automation.config["infos"]

        self.root.app.load_new_frame(
            prev_frame=self.root,
            new_frame=AutomationInfosFrame(
                app=self.root.app,
                automation_name=automation.a_name,
                a_id=self.root.app.new_automation.a_id,
            ),
            returnable=False,
        )
