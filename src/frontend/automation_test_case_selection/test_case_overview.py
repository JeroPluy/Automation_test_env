from ..customWidgets import customWidgets as cW
from ..customWidgets.CTkTable import CTkTable

from frontend.automation_test_case_creation import CaseCreationFrame

from backend.database import db_utils

from backend.automation_testing import test_execution

from backend.utils.env_helper_classes import Automation

from customtkinter import CTkCheckBox, StringVar


class TestCaseSelectionFrame(cW.BasisFrame):
    """
    Class for the frame that displays the test cases for the test execution
    """

    def __init__(self, app):
        """
        Constructor for the TestCaseSelectionFrame
        """

        super().__init__(app=app)

        test_cases = db_utils.load_test_cases(self.app.selected_automation)

        if len(test_cases) == 0:
            app.go_back(self)
            return

        # if there are test cases, display the test case selection frame

        automation_name = db_utils.get_automation_name(app.selected_automation)

        if app.selected_project is None:
            nav_path = automation_name
        else:
            nav_path = str(app.selected_project) + "/" + automation_name

        self.nav_bar = cW.NavigationBar(
            self,
            mode=app.settings["MODE"],
            nav_path=nav_path,
        )

        self.content_frame = ContentFrame(app=app, root=self, test_cases=test_cases)

        self.nav_btns = NavBtns(
            root=self,
            values=(app.lang["BACK"], app.lang["START_TEST"]),
        )

        # --- grid the elements ---

        self.nav_bar.grid(row=0, column=0, sticky="ew")
        self.content_frame.grid(row=1, column=0, sticky="news")
        self.nav_btns.grid(row=2, column=0, sticky="ew")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)


class ContentFrame(cW.BasisScrollFrame):
    """
    Subframe class for the content of the test cases
    """

    def __init__(self, app, root, test_cases):
        """
        Constructor for the ContentFrame class

        Args:
            app (test_environment_app.AppWindow): the main application
            root (customtkinter.CTK): the parent frame
            test_cases (list): the list of test cases
        """

        super().__init__(app=app, root=root, layer=0, scroll_direction="y")

        self.app = app

        automation: Automation = db_utils.get_automation_data(app.selected_automation)

        self.script_path = automation.script
        self.autom_mode = automation.autom_mode
        self.max_instances = automation.max_instances

        self.table_frame = self.add_element_frame(row=0, column=0, layer=1, expand=True)

        self.test_case_table = TestCaseTable(
            app=app, root=self.table_frame, test_cases=test_cases
        )

        self.add_element_frame(row=1, column=0, layer=1)

        self.add_test_case_btn = cW.AcceptButton(
            self.element_frame,
            text=app.lang["NEW_TC"],
            kind=2,
            command=self.add_new_test_case,
            width=260,
        )

        self.selection_content_frame = self.add_element_frame(row=2, column=0, layer=2)
        self.selection_content_frame.columnconfigure(0, weight=1)
        self.selection_content_frame.rowconfigure(0, weight=1)

        self.selection_frame = SelectionFrame(
            app=app, root=self.selection_content_frame, autom_mode=self.autom_mode
        )

        # --- grid the elements ---

        self.test_case_table.grid(row=0, column=0, sticky="news", padx=2, pady=5)
        self.table_frame.columnconfigure(0, weight=1)
        self.table_frame.rowconfigure(0, weight=1)

        self.add_test_case_btn.grid(row=0, column=0, pady=(5), padx=50, sticky="we")

        self.selection_frame.grid(row=0, column=0, sticky="ews")

    def add_new_test_case(self):
        """
        Function to add a new test case to the automation
        """

        self.app.load_new_frame(
            prev_frame=self.root,
            new_frame=CaseCreationFrame(
                app=self.app,
            ),
            return_btn=True,
        )

    def get_selected_test_cases(self):
        """
        Function to get the selected test cases
        
        Returns:
            list: the selected test cases as dictionaries with the test case id and the input values
        """

        return self.test_case_table.get_selected_test_cases()


class TestCaseTable(cW.BasisScrollFrame):
    """
    Subframe class for the table of the test cases in a scroll frame
    """

    def __init__(self, app, root, test_cases):
        """
        Constructor for the TestCaseTable class

        Args:
            app (test_environment_app.AppWindow): the main application
            root (customtkinter.CTK): the parent frame
            test_cases (list): the list of test cases
        """

        self.app = app

        self.test_cases = test_cases

        # get the entity names
        entity_names = []
        self.entity_roles = []

        for input in test_cases[0]["case_inputs"]:
            self.entity_roles.append(input["p_role"])
            if len(input["e_name"].split(".")[1]) > 30:
                entity_names.append(input["e_name"].replace(".", ".\n")[:30] + "...")
            else:
                entity_names.append(input["e_name"].replace(".", ".\n"))

        # create the header values
        header_values = (
            ["ID", app.lang["CREATED"]]
            + entity_names
            + [app.lang["REQUIREMENT_SHORT"], app.lang["PRIORITY_SHORT"]]
        )

        test_case_values = []

        for test_case in test_cases:
            test_case_inputs = [
                input["test_value"] for input in test_case["case_inputs"]
            ]
            test_case_values.append(
                [
                    test_case["case_id"],
                    test_case["timestamp"],
                ]
                + test_case_inputs
                + [test_case["requirement"], test_case["priority"]]
            )

        # create the table values
        table_values = [header_values] + test_case_values

        table_height = len(table_values) * 40 + 20

        super().__init__(
            app=app, root=root, layer=1, scroll_direction="x", height=table_height
        )

        # calculate the column width
        col_width = [40, 80] + [140] * len(entity_names) + [80, 40]

        # create the table content frame
        self.table_content = self.add_element_frame(expand=True, layer=2)

        self.table = CTkTable(
            master=self.table_content,
            values=table_values,
            height=40,
            col_width=col_width,
            header_col=True,
            multi_select=True,
            corner_radius=0,
            command=self.select_row,
        )

        # --- grid the elements ---

        self.table.grid(row=0, column=0, sticky="news")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def select_row(self, data: dict):
        """
        Select a row in the table and get the data of the selected row

        Args:
            data (dict): the data of the selected row in the table as a dictionary
                        contains: {"row": i, "column" : j, "value" : value, "args": args}
        """
        self.table.select_row(data.get("row"))

    def get_selected_test_cases(self):
        """
        Function to get the selected test values
        """

        selected_test_cases = self.table.get_selected_rows()

        test_cases = []

        for test_case in selected_test_cases:
            input_values = [[], [], []]
            tc_id = test_case[0]

            for i, input in enumerate(test_case[2:-2]):
                input_values[self.entity_roles[i]].append(input)

            test_cases.append({"id": tc_id,"input_values": input_values})

        return test_cases


class SelectionFrame(cW.BasisFrame):
    """
    Subframe class for the selection of the test cases
    """

    def __init__(self, app, root, autom_mode):
        """
        Constructor for the SelectionFrame class

        Args:
            app (test_environment_app.AppWindow): the main application
            root (customtkinter.CTK): the parent frame
            autom_mode (int): the automation mode
        """

        autom_mode_str = (
            app.lang["SINGLE"]
            if autom_mode == 0
            else (
                app.lang["RESTART"]
                if autom_mode == 1
                else (app.lang["QUEUED"] if autom_mode == 2 else app.lang["PARALLEL"])
            )
        )

        super().__init__(app=app, root=root, layer=2)

        self.app = app

        self.preselect_btn = cW.NeutralButton(
            self,
            text=app.lang["PRESELECT"],
            command=self.preselect_test_cases,
            width=260,
        )

        self.save_colletion_btn = cW.NeutralButton(
            self,
            text=app.lang["SAVE_COLLECTION"],
            command=self.save_collection,
            width=260,
        )

        self.simultan_bool = StringVar(value=False)

        self.simultan_checkbox = CTkCheckBox(
            master=self,
            text=app.lang["SIMULTAN"]
            + "\n"
            + app.lang["AUTOMATION_MODE"]
            + ": "
            + autom_mode_str,
            variable=self.simultan_bool,
        )

        # --- grid the elements ---

        self.preselect_btn.grid(
            row=0, column=0, pady=(20, 10), padx=(25, 0), sticky="w"
        )

        self.save_colletion_btn.grid(
            row=0, column=2, pady=(20, 10), padx=(0, 25), sticky="e"
        )

        self.simultan_checkbox.grid(
            row=1, column=1, pady=(0, 20), padx=(15), sticky="ew"
        )

        self.columnconfigure((0, 2), weight=1)
        self.rowconfigure(0, weight=1)

    def preselect_test_cases(self):
        """
        Function to preselect the test cases
        """

        print("preselect test cases")

    def save_collection(self):
        """
        Function to save the collection of the test cases
        """

        print("save collection")


class NavBtns(cW.NavigationButtons):
    """
    Subclass of the NavigationButtons class for the navigation buttons of the frame
    """

    def __init__(self, root, values):
        """
        Constructor for the NavBtns class

        Args:
            root (customtkinter.CTK): the parent frame
            values (tuple): the values of the navigation buttons
        """

        super().__init__(root=root, values=values)

        self.root = root

    def btn_1_func(self):
        """
        Function for the back button
        """

        self.root.app.go_back(self.root)

    def btn_2_func(self):
        """
        Function for the start test button
        """
        test_cases_list = self.root.content_frame.get_selected_test_cases()

        test_cases = []
        for test_case in test_cases_list:
            test_case["script_path"] = self.root.content_frame.script_path
            test_cases.append(test_case)
            

        if self.root.content_frame.selection_frame.simultan_checkbox.get():
            results = test_execution.run_simultaneous_automations(
                test_cases,
                self.root.content_frame.autom_mode,
                max_instances=self.root.content_frame.max_instances,
            )
        else:
            results = test_execution.run_distinct_automations(
                test_cases,
                self.root.content_frame.autom_mode,
            )

        print("results: ", results)
