from tkinter import StringVar

from customtkinter import CTkEntry, CTkLabel

from backend.database.db_utils import load_integrations
from frontend.customWidgets import customWidgets as cW
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
        # make the content frame resizable depending on the window size
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # entity list frame
        self.entity_list_frame = EntityListFrame(app, self.content_frame)
        # make the entity list frame inside the content frame resizable
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)

        # automation mode frame
        self.a_mode_frame = cW.BasisFrame(app, self.content_frame, layer=2)

        self.a_mode_label = CTkLabel(
            self.a_mode_frame, text=app.lang["AUTOMATION_MODE"]
        )
        # make the automation mode label inside a_mode_frame resizable
        self.a_mode_frame.columnconfigure(0, weight=1)

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
        # make the script instance label inside script_instance_frame resizable
        self.script_instance_frame.columnconfigure(0, weight=1)

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

        # grid the main elements
        self.nav_bar.grid(row=0, column=0, sticky="ew")
        self.content_frame.grid(
            row=1, column=0, sticky="news", pady=(15, 10), padx=(25)
        )
        self.navigation_buttons.grid(row=2, column=0, sticky="ew")

        # grid the elements inside the content frame
        self.entity_list_frame.grid(
            row=0, column=0, sticky="news", padx=(10), pady=(10)
        )
        self.a_mode_frame.grid(
            row=1, column=0, sticky="ew", padx=(10, 10), pady=(0, 10)
        )
        self.script_instance_frame.grid(
            row=2, column=0, sticky="ew", padx=(10), pady=(0, 10)
        )

        # grid the elements inside the automation mode frame
        self.a_mode_label.grid(row=0, column=0, sticky="w", pady=(5, 5), padx=(10, 0))
        self.a_mode_dropdown.grid(
            row=0, column=1, sticky="e", pady=(5, 5), padx=(0, 10)
        )

        # grid the elements inside the script instance frame
        self.script_instance_label.grid(
            row=0, column=0, sticky="w", pady=(5, 5), padx=(10, 0)
        )
        self.script_instance_entry.grid(
            row=0, column=1, sticky="e", pady=(5, 5), padx=(0, 10)
        )


class EntityListFrame(cW.BasisScrollFrame):
    """
    Class to display the list of entities in the automation entity frame
    """

    def __init__(self, app, root):
        super().__init__(app, root, layer=1, border=True, scroll_direction="y")

        self.entity_list: list = app.new_automation.config["entities"]
        integration_list = load_integrations()
        integration_list.sort()

        integration_list.append(app.lang["NEW_INTEGRATION"])

        self.entity_frame_list: list = []

        for entity in self.entity_list:
            entity_name = entity.entity_name
            preselect_type = entity.integration

            self.add_content_frame(row=len(self.entity_frame_list), column=0)
            entity_frame = EntityFrame(
                app=app,
                root=self.element_frame,
                entity_num=len(self.entity_frame_list),
                entity_name=entity_name,
                integration_list=integration_list,
                preselect_type=preselect_type,
            )
            self.element_frame.columnconfigure(0, weight=1)
            self.element_frame.rowconfigure(0, weight=1)

            self.entity_frame_list.append(entity_frame)

            entity_frame.grid(
                row=len(self.entity_frame_list),
                column=0,
                sticky="news",
                padx=(5, 5),
                pady=(2, 2),
            )


class EntityFrame(cW.BasisFrame):
    """
    Class for to display a single entity in the entity list frame
    """

    def __init__(
        self, app, root, entity_num, entity_name, integration_list, preselect_type
    ):
        """
        Initialization of the entity frame

        Args:
        """

        super().__init__(app=app, root=root, layer=3)

        self.entity_num = entity_num

        self.entity_name_label = CTkLabel(self, text=entity_name)
        # the entity name is expandable with the window size
        self.columnconfigure(0, weight=1)

        self.entity_integration_select = cW.FramedOptionMenu(
            root=self,
            values=integration_list,
            default_value=preselect_type,
            command=self.change_integration,
        )

        # grid the elements inside the entity frame
        self.entity_name_label.grid(
            row=0, column=0, sticky="w", pady=(8, 8), padx=(10, 0)
        )
        self.entity_integration_select.grid(
            row=0, column=1, sticky="e", pady=(8, 8), padx=(0, 10)
        )

    def change_integration(self, value):
        """
        Function to handle the changing of the integration of an entity

        Args:
            value (str): the value of the dropdown menu
        """
        if value == self.app.lang["NEW_INTEGRATION"]:
            # TODO open mask for creating a new integration and add it to the database
            print("new integration selected")
        else:
            print(
                "Entity "
                + str(self.entity_num)
                + " integration changed  form: "
                + self.app.new_automation.config["entities"][
                    self.entity_num
                ].integration
                + " to: "
                + value
            )
            self.app.new_automation.config["entities"][
                self.entity_num
            ].integration = value


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
        Function to handle the continue button
        """
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
            returnable=True,
        )
