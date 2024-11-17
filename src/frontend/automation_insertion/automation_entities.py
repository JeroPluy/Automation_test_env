from tkinter import StringVar

from customtkinter import CTkEntry, CTkLabel

from frontend.customWidgets import customWidgets as cW
from .automation_insertion_utils import EntityListFrame
from .antomation_script import AutomationScriptFrame

from backend import database as db


class AutomationEntityFrame(cW.BasisFrame):
    """
    The frame class displaying the automation entity with the name and their integration
    as well as automation mode and the maximum number of script instances
    """

    def __init__(self, app, automation_name):
        """
        The initialization of the automation entity frame

        Args:
            app (customtkinter.CTK): the parent window of the automation entity frame
            automation_name (str): the name of the new automation
            project (str): the name of the project of the new automation
        """

        super().__init__(app=app, layer=0)

        if app.selected_project is None:
            nav_path = automation_name
        else:
            nav_path = str(app.selected_project + "/" + automation_name)

        self.nav_bar = cW.NavigationBar(
            self,
            mode=app.settings["MODE"],
            nav_path=nav_path,
        )

        self.content_frame = cW.BasisFrame(app, self, layer=1)

        # entity list frame
        self.entity_list_frame = EntityListFrame(
            app, self.content_frame, app.new_automation.config["entities"]
        )

        # automation mode frame
        self.a_mode_frame = cW.BasisFrame(app, self.content_frame, layer=2)

        self.a_mode_label = CTkLabel(
            self.a_mode_frame, text=app.lang["AUTOMATION_MODE"]
        )

        # get the automation mode from the config
        autom_mode = app.new_automation.config["infos"].autom_mode
        autom_mode_str = app.lang["SINGLE"]

        if autom_mode == 1:
            autom_mode_str = app.lang["RESTART"]
        elif autom_mode == 2:
            autom_mode_str = app.lang["QUEUED"]
        elif autom_mode == 3:
            autom_mode_str = app.lang["PARALLEL"]

        self.a_mode_dropdown = cW.FramedOptionMenu(
            root=self.a_mode_frame,
            values=[
                app.lang["SINGLE"],
                app.lang["RESTART"],
                app.lang["QUEUED"],
                app.lang["PARALLEL"],
            ],
            default_value=autom_mode_str,
        )

        # automation instances frame
        self.script_instance_frame = cW.BasisFrame(app, self.content_frame, layer=2)

        self.script_instance_label = CTkLabel(
            self.script_instance_frame, text=app.lang["SCRIPT_INSTANCES"]
        )

        self.script_instances = StringVar(
            value=app.new_automation.config["infos"].max_instances
        )

        self.script_instance_entry = CTkEntry(
            self.script_instance_frame,
            textvariable=self.script_instances,
            justify="right",
        )

        # create the navigation buttons for the window
        self.navigation_buttons = NavBtns(
            root=self, values=(app.lang["BACK"], app.lang["CONTINUE"])
        )

        # --- grid the elements ---

        # grid the main elements
        self.nav_bar.grid(row=0, column=0, sticky="ew")
        self.content_frame.grid(
            row=1, column=0, sticky="news", pady=(15, 10), padx=(25)
        )
        self.navigation_buttons.grid(row=2, column=0, sticky="ew")

        # make the content frame resizable depending on the window size
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        ## grid the elements inside the content frame
        self.entity_list_frame.grid(
            row=0, column=0, sticky="news", padx=(10), pady=(10)
        )
        self.a_mode_frame.grid(
            row=1, column=0, sticky="ew", padx=(10, 10), pady=(0, 10)
        )
        self.script_instance_frame.grid(
            row=2, column=0, sticky="ew", padx=(10), pady=(0, 10)
        )

        ## make the entity list frame inside the content frame resizable
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)

        ### grid the elements inside the automation mode frame
        self.a_mode_label.grid(row=0, column=0, sticky="w", pady=(5, 5), padx=(10, 0))
        self.a_mode_dropdown.grid(
            row=0, column=1, sticky="e", pady=(5, 5), padx=(0, 10)
        )

        ### make the automation mode label inside a_mode_frame resizable
        self.a_mode_frame.columnconfigure(0, weight=1)

        ### grid the elements inside the script instance frame
        self.script_instance_label.grid(
            row=0, column=0, sticky="w", pady=(5, 5), padx=(10, 0)
        )
        self.script_instance_entry.grid(
            row=0, column=1, sticky="e", pady=(5, 5), padx=(0, 10)
        )

        ### make the script instance label inside script_instance_frame resizable
        self.script_instance_frame.columnconfigure(0, weight=1)


class NavBtns(cW.NavigationButtons):
    def __init__(self, root, values):
        """
        Initialization of the navigation buttons for the automation entity frame

        Args:
            root (BasisFrame): root frame for the navigation buttons
            values (Tuple[str]): values of the navigation buttons
        """
        self.root = root
        super().__init__(root=root, values=values)

    def btn_1_func(self):
        """
        Function to handle the back button
        """
        self.root.app.go_back(self)
        # TODO load last automation

    def btn_2_func(self):
        """
        Function to handle the continue button by saving the automation and loading the script frame
        """
        
        # save the automation instance from the entry field
        self.root.app.new_automation.config["infos"].max_instances = int(
            self.root.script_instances.get()
        )
        
        # save the automation mode from the dropdown
        autom_value = self.root.a_mode_dropdown.get()
        if autom_value == self.root.app.lang["SINGLE"]:
            autom_mode = 0 
        elif autom_value == self.root.app.lang["RESTART"]:
            autom_mode = 1
        elif autom_value == self.root.app.lang["QUEUED"]:
            autom_mode = 2
        elif autom_value == self.root.app.lang["PARALLEL"]:
            autom_mode = 3
        
        self.root.app.new_automation.config["infos"].autom_mode = autom_mode
        
        
        # TODO apply the integration changes to the script creation and the entity structure

        self.root.app.new_automation.a_id, self.root.app.new_automation.version = (
            db.add_automation(self.root.app.new_automation.config)
        )

        automation = self.master.app.new_automation.config["infos"]

        self.root.app.load_new_frame(
            self.root,
            new_frame=AutomationScriptFrame(
                self.root.app,
                automation_name=automation.a_name,
            ),
            returnable=False,
        )
