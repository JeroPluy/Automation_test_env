from ..customWidgets import customWidgets as cW
from ..automation_insertion import automation_insertion_utils as ai_utils

from tkinter import StringVar
from customtkinter import CTkLabel, CTkCheckBox, CTkEntry, CTkFont

from backend.database import db_utils
from backend.utils.env_helper_classes import Automation


class AutomationDetailsFrame(cW.BasisFrame):
    """
    Main frame class for the automation details window
    """

    def __init__(self, app, a_id, automation_name):
        """
        Initialization of the AutomationDetailsFrame

        Args:
            app (customtkinter.CTK): the parent window of the automation details frame
            a_id (int): the id of the automation which details are displayed
            automation_name (str): the name of the automation
        """

        super().__init__(app=app, layer=0)

        self.nav_bar = cW.NavigationBar(
            self, mode=app.settings["MODE"], nav_path=automation_name
        )

        self.main_frame = AutomationDetailsContent(
            app=app,
            root=self,
            a_id=a_id,
        )

        self.nav_btns = NavBtns(app=app, root=self, a_id=a_id)

        # --- grid the elements ---

        # grid the main elements
        self.nav_bar.grid(row=0, column=0, sticky="ew")
        self.main_frame.grid(row=1, column=0, sticky="news", pady=(0, 10), padx=(0))
        self.nav_btns.grid(row=2, column=0, sticky="news")

        # make the main frame (content) resizable depending on the window size
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)


class AutomationDetailsContent(cW.BasisScrollFrame):
    """
    The class defines the main content frame for the automation details window
    between the navigation bar and the navigation buttons
    """

    def __init__(self, app, root, a_id: int):
        """
        Initialization of the AutomationDetailsContent frame

        Args:
            app (customtkinter.CTK): the parent window of the automation details content frame
            root (cW.BasisFrame): the parent frame of the automation details content frame
            a_id (int): the id of the automation which details are displayed
        """

        self.automation = db_utils.get_automation_data(a_id)

        super().__init__(app, root, scroll_direction="y", layer=0)

        # add the menu btns to the main frame
        self.add_element_frame(row=0, column=0, layer=0)
        self.element_frame.columnconfigure(0, weight=1)

        self.menu_btns_frame = MenuBtns(app, self.element_frame)

        # add the main content frame to the main frame
        self.add_element_frame(row=1, column=0, layer=1)
        self.element_frame.columnconfigure(0, weight=1)

        self.data_frame = cW.BasisFrame(app, self.element_frame, layer=1)

        self.info_labels = InfoLabels(
            app=app, root=self.data_frame, automation=self.automation
        )

        self.entity_params = EntityParamsFrame(app=app, root=self.data_frame, a_id=a_id)

        self.script_path_frame = cW.BasisFrame(app, self.data_frame, layer=2)
        self.script_path_label = CTkLabel(
            master=self.script_path_frame,
            text=app.lang["SCRIPT_PATH"] + ":",
            width=100,
            anchor="w",
        )
        self.script_path_val = CTkLabel(
            master=self.script_path_frame,
            text=self.automation.script,
            anchor="e",
            font=CTkFont(underline=True),
        )

        self.add_info_frame = AddInfoFrame(app, self.data_frame, a_id)

        self.delete_autmation_btn = cW.DeleteButton(
            root=self.data_frame,
            text=app.lang["DELETE_AUTOMATION"],
            height=40,
            width=75,
            kind=0,
            command=self.delete_automation,
        )

        # --- grid the elements ---

        # grid the main frame elements
        self.menu_btns_frame.grid(row=0, column=0, sticky="news")
        self.data_frame.grid(row=1, column=0, sticky="news", padx=(0), pady=(15, 0))

        ## grid the main data frame elements
        self.info_labels.grid(row=0, column=0, sticky="news", padx=(15), pady=(0, 15))
        self.entity_params.grid(row=1, column=0, sticky="news", padx=(15), pady=(0, 15))
        self.script_path_frame.grid(
            row=2, column=0, sticky="news", padx=(15), pady=(0, 15)
        )
        self.add_info_frame.grid(
            row=3, column=0, sticky="news", padx=(15), pady=(0, 15)
        )
        self.delete_autmation_btn.grid(row=4, column=0, sticky="ns", pady=(0, 15))

        self.data_frame.columnconfigure(0, weight=1)

        ### grid the script path elements
        self.script_path_label.grid(
            row=0, column=0, sticky="w", pady=(2, 2), padx=(10, 0)
        )
        self.script_path_val.grid(row=0, column=1, sticky="e", pady=(2, 2), padx=(0, 5))

        self.script_path_frame.columnconfigure(1, weight=1)

    def delete_automation(self):
        """
        Delete the automation from the database
        """

        # TODO delete the automation
        print("Delete automation")


class MenuBtns(cW.BasisFrame):
    """
    Class to display the menu buttons for navigating to the test case collection and the test results
    """

    def __init__(self, app, root):
        """
        Initialization of the MenuBtns frame

        Args:
            app (customtkinter.CTK): the parent window of the menu buttons frame
            root (cW.BasisFrame): the parent frame of the menu buttons frame
        """

        super().__init__(app, root, layer=0)

        self.test_case_coll_btn = cW.NeutralButton(
            self,
            text=app.lang["TEST_CASE_COLLECTION"],
            width=350,
            height=40,
            command=self.open_test_case_coll,
        )

        self.test_results_btn = cW.NeutralButton(
            self,
            text=app.lang["TEST_RESULTS"],
            width=350,
            height=40,
            command=self.open_test_results,
        )

        # --- grid the elements ---

        self.test_case_coll_btn.grid(row=0, column=0, sticky="w", padx=(15, 5))
        self.test_results_btn.grid(row=0, column=1, sticky="e", padx=(5, 15))

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def open_test_case_coll(self):
        # TODO open the test case collection
        print("Open test case collection")

    def open_test_results(self):
        # TODO open the test results
        print("Open test results")


class InfoLabels(cW.BasisFrame):
    """
    Class to display the information labels block of the automation details window
    """

    def __init__(self, app, root, automation: Automation):
        """
        Initialization of the InfoLabels frame

        Args:
            app (customtkinter.CTK): the parent window of the info labels frame
            root (cW.BasisFrame): the parent frame of the info labels frame
            automation (Automation): the automation data to display
        """

        super().__init__(app, root, layer=1)

        locked_state = "disabled" if automation.error is not None else "normal"

        # created frame
        self.created_frame = cW.BasisFrame(app, self, layer=2)

        self.created_label = CTkLabel(
            master=self.created_frame,
            text=app.lang["CREATED"] + ":",
            anchor="w",
        )

        self.created_date = CTkLabel(
            master=self.created_frame,
            text=automation.created,
        )

        # automation mode frame
        self.a_mode_frame = cW.BasisFrame(app, self, layer=2)

        self.a_mode_label = CTkLabel(
            master=self.a_mode_frame,
            text=app.lang["AUTOMATION_MODE"] + ":",
            anchor="w",
        )

        autom_mode = automation.autom_mode

        if autom_mode == 0:
            autom_mode_str = app.lang["SINGLE"]
        elif autom_mode == 1:
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
            state=locked_state,
        )

        # error frame
        # TODO better coloring and theme mode handling
        if automation.error == 1:
            error_color = "red"
        elif automation.error == 0:
            error_color = "green"
        else:
            error_color = "#FCFCFC"

        self.error_frame = cW.BasisFrame(app, self, layer=-1, fg_color=error_color)
        self.error_frame.configure("rounded_corners=6")

        self.error_label = CTkLabel(
            master=self.error_frame,
            text=app.lang["ERROR_DETECT"] + ":",
        )

        # TODO change Checkbox to a framed icon with ❌, ✔️ and ❓
        self.error_checkbox = CTkCheckBox(
            master=self.error_frame,
            text="",
            variable=automation.error,
            state="disabled",  # should not be changed
        )

        # max instances frame
        self.max_inst_frame = cW.BasisFrame(app, self, layer=2)

        self.max_instances_label = CTkLabel(
            master=self.max_inst_frame,
            text=app.lang["MAX_INSTANCES"] + ":",
        )

        max_inst_value_str = StringVar(value=automation.max_instances)

        # TODO gray out the entry field if the state is locked
        self.max_instances_value = CTkEntry(
            master=self.max_inst_frame,
            textvariable=max_inst_value_str,
            state=locked_state,
            width=50,
            justify="right",
        )

        # --- grid the elements ---

        # grid the label frames
        self.created_frame.grid(row=0, column=0, sticky="we", padx=(0, 5), pady=(0, 5))
        self.a_mode_frame.grid(row=0, column=1, sticky="we", padx=(5, 0), pady=(0, 5))
        self.error_frame.grid(row=1, column=0, sticky="we", padx=(0, 5), pady=(5))
        self.max_inst_frame.grid(row=1, column=1, sticky="we", padx=(5, 0), pady=(5))

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        ## grid the created elements
        self.created_label.grid(row=0, column=0, sticky="w", pady=(2, 2), padx=(10, 2))
        self.created_date.grid(row=0, column=1, sticky="e", pady=(2, 2), padx=(0, 5))

        self.created_frame.columnconfigure(1, weight=1)

        ## grid the error elements
        self.error_label.grid(row=0, column=0, sticky="w", pady=(2, 2), padx=(10, 2))
        self.error_checkbox.grid(row=0, column=1, sticky="e", pady=(2, 2), padx=(0, 5))

        self.error_frame.columnconfigure(1, weight=1)

        ## grid the automation mode elements
        self.a_mode_label.grid(row=0, column=0, sticky="w", pady=(2, 2), padx=(10, 2))
        self.a_mode_dropdown.grid(row=0, column=1, sticky="e", pady=(2, 2), padx=(0, 5))

        self.a_mode_frame.columnconfigure(1, weight=1)

        ## grid the max instances elements
        self.max_instances_label.grid(
            row=0, column=0, sticky="w", pady=(2, 2), padx=(10, 2)
        )
        self.max_instances_value.grid(
            row=0, column=1, sticky="e", pady=(2, 2), padx=(0, 5)
        )

        self.max_inst_frame.columnconfigure(1, weight=1)


class EntityParamsFrame(cW.BasisFrame):
    """
    Class to display the entity parameter list of the automation
    """

    def __init__(self, app, root, a_id, locked=False):
        """
        Initialization of the EntityParamsFrame by loading the entity parameters from the database

        Args:
            app (customtkinter.CTK): the parent window of the entity params frame
            root (cW.BasisFrame): the parent frame of the entity params frame
            a_id (int): the id of the automation which entity parameters are displayed
            locked (bool): determines if the entity parameters are locked
        """

        super().__init__(app, root, layer=1)

        autoamtion_entities = db_utils.get_automation_entities(a_id)

        self.param_header_label = CTkLabel(
            master=self,
            text=app.lang["ENTITY_PARAMS"] + ":",
            font=CTkFont(weight="bold"),
        )

        self.param_list = ai_utils.EntityListFrame(
            app, self, autoamtion_entities, locked, height=200
        )

        # --- grid the elements ---

        # grid the Entity Params Frame
        self.param_header_label.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 10),
        )
        self.param_list.grid(row=1, column=0, sticky="news")

        self.columnconfigure(0, weight=1)

    def get_entity_params(self) -> list:
        """
        Function to get the entity parameters from the entity list frame

        Returns:
            list: the entity parameters as a list of dictionaries
        """

        return self.param_list.get_entity_integrations()


class AddInfoFrame(cW.BasisFrame):
    """
    Frame class to display the additional information of the automation
    """

    def __init__(self, app, root, a_id):
        """
        Initialization of the AddInfoFrame by loading the additional information from the database

        Args:
            app (customtkinter.CTK): the parent window of the add info frame
            root (cW.BasisFrame): the parent frame of the add info frame
            a_id (int): the id of the automation which additional information is displayed
        """

        additional_infos = db_utils.get_additional_inforamtion(a_id)

        super().__init__(app, root, layer=1)

        self.add_info_header_label = CTkLabel(
            master=self,
            text=app.lang["ADDITIONAL_INFORMATION"] + ":",
            font=CTkFont(weight="bold"),
        )

        self.add_info_list = ai_utils.AdditionalInfoListFrame(
            app, self, add_infos=additional_infos
        )

        # --- grid the elements ---

        # grid the Add Info Frame
        self.add_info_header_label.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 10),
        )
        self.add_info_list.grid(row=1, column=0, sticky="news")

        self.columnconfigure(0, weight=1)

    def get_additional_info(self) -> list:
        """
        Function to get the additional information from the additional info list frame as a list of dictionaries
        """

        return self.add_info_list.get_infos()


class NavBtns(cW.NavigationButtons):
    """
    Class to display the navigation buttons for the automation details window
    """

    def __init__(self, app, root, a_id):
        """
        Initialization of the NavBtns frame with the delete and save buttons for the automation details window

        Args:
            app (customtkinter.CTK): the parent window of the navigation buttons
            root (cW.BasisFrame): the parent frame of the navigation buttons
            a_id (int): the id of the automation which details are displayed
        """

        self.root = root
        self.a_id = a_id

        super().__init__(
            root=root,
            values=(app.lang["DISCARD"], app.lang["SAVE"]),
            options={"btn_1_type": "delete", "btn_2_type": "accept"},
        )

    def btn_1_func(self):
        """
        Button 1 function to discard the changes and go back to the automation selection overview
        """
        self.root.app.go_back(self.root)

    def btn_2_func(self):
        """
        Button 2 function to save the changes to the automation details in the database
        and go back to the automation selection overview
        """

        entity_config = self.root.main_frame.entity_params.get_entity_params()
        # TODO change the integration and the script depending on the new entity config

        additional_info = self.root.main_frame.add_info_frame.get_additional_info()
        db_utils.update_additional_infos(self.a_id, additional_info)

        self.btn_1_func()
