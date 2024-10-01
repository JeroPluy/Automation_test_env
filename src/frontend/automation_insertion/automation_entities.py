
from tkinter import StringVar

from customtkinter import CTkEntry, CTkLabel

from backend.utils.env_helper_classes import Entity
from frontend.customWidgets import customWidgets as cW


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
            
        self.grid_columnconfigure(0, weight=1)

        self.nav_bar = cW.NavigationBar(
            self,
            mode=app.settings["MODE"],
            nav_path=nav_path,
        )
        self.nav_bar.grid(row=0, column=0, sticky="ew")

        self.content_frame = cW.BasisFrame(app, self, layer=1)
        self.content_frame.grid(row=1, column=0, sticky="news", pady=(15, 0), padx=(15, 15))
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)

        # entity list frame
        self.entity_list_frame = cW.BasisScrollFrame(app, self.content_frame, layer=1, border=True, scroll_direction="y")
        self.entity_list_frame.grid(row=0, column=0, sticky="ew", padx=(50), pady=(10))

        entity_list: list = app.new_automation_config["entities"]
        entity_frame_list: list = []

        for entity in entity_list:
            entity_frame = EntityFrame(self.app, self.entity_list_frame.content, entity)
            entity_frame.grid(row=len(entity_frame_list), column=0, sticky="ew")
            entity_frame_list.append(entity_frame)

        # automation mode frame
        self.a_mode_frame = cW.BasisFrame(app, self.content_frame, layer=2)
        self.a_mode_frame.grid(row=1, column=0, sticky="ew")

        self.a_mode_frame.columnconfigure(0, weight=1)

        self.a_mode_label = CTkLabel(self.a_mode_frame, text=app.lang["AUTOMATION_MODE"])
        self.a_mode_label.grid(row=0, column=0, sticky="w", pady=(5,5), padx=(10,0))

        autom_mode = app.new_automation_config["infos"].autom_mode
        autom_mode_str = app.lang["SINGLE"]

        if autom_mode == 1:
            autom_mode_str = app.lang["RESTART"]
        elif autom_mode == 2:
            autom_mode_str = app.lang["QUEUED"]
        elif autom_mode == 3:
            autom_mode_str = app.lang["PARALLEL"]

        self.a_mode_dropdown = cW.FramedOptionMenu(
            root=self.a_mode_frame,
            values=[app.lang["SINGLE"], app.lang["RESTART"], app.lang["QUEUED"], app.lang["PARALLEL"]],
            default_value=autom_mode_str,
        )
        self.a_mode_dropdown.grid(row=0, column=1, sticky="e",pady=(5,5), padx=(0,10))

        # automation instances frame
        self.script_instance_frame = cW.BasisFrame(app, self.content_frame, layer=2)
        self.script_instance_frame.grid(row=2, column=0, sticky="ew")

        self.script_instance_frame.columnconfigure(0, weight=1)

        self.script_instance_label = CTkLabel(self.script_instance_frame, text=app.lang["SCRIPT_INSTANCES"])
        self.script_instance_label.grid(row=0, column=0, sticky="w", pady=(5,5), padx=(10,0))

        self.script_instances = StringVar(value=app.new_automation_config["infos"].max_instances)

        self.script_instance_entry = CTkEntry(self.script_instance_frame, textvariable=self.script_instances,justify="right")
        self.script_instance_entry.grid(row=0, column=1, sticky="e", pady=(5,5), padx=(0,10))

class EntityFrame(cW.BasisFrame):
    """
    The frame class displaying one automation entity in scrollable list frame
    """
    
    def __init__(self, app, root, entity: Entity):
        super().__init__(app=app, root=root, layer=3)

        self.dummy_label = CTkLabel(self, text=entity.entity_name)
        self.dummy_label.grid(row=0, column=0, sticky="w", pady=(5,5), padx=(10,0))
    