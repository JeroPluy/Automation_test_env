from ..customWidgets import customWidgets as cW
from ..customWidgets.CTkTable import CTkTable

from backend.automation_testing import test_case_gen


class NewCaseOverview(cW.BasisFrame):
    """
    The frame class displaying all the test cases for the automation before finally added to the database
    """

    def __init__(self, app, navigation_path: str, test_case_value_list: list, test_case_infos: dict):
        """
        Constructor for the NewCaseOverview frame

        Args:
            app (test_environment_app.AppWindow): the main application
            navigation_path (str): the path of the navigation bar
            test_case_value_list (list): the list of test case values
            test_case_infos (dict): the list of test case information dictionaries with the test case requirement and priority
        """

        super().__init__(app)

        self.app = app

        self.test_case_value_list = test_case_value_list

        self.nav_bar = cW.NavigationBar(
            self,
            mode=app.settings["MODE"],
            nav_path=navigation_path,
        )

        self.table_frame = TableFrame(
            app=app,
            root=self,
            value_list=test_case_value_list,
            additional_infos=test_case_infos,
        )

        self.Nav_btns = NavBtns(
            app=app,
            root=self,
            automation_id=self.app.selected_automation,
        )
        
        # --- grid the elements ---
        
        self.nav_bar.grid(row=0, column=0, sticky="ew")
        self.table_frame.grid(row=1, column=0, sticky="news")
        self.Nav_btns.grid(row=2, column=0, sticky="ew")
        
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)


class TableFrame(cW.BasisScrollFrame):
    """
    Subframe class for the table of the test cases
    """

    def __init__(self, app, root, value_list: list, additional_infos: dict):
        """
        Constructor for the TableFrame class

        Args:
            app (test_environment_app.AppWindow): the main application
            root (customtkinter.CTk): the parent frame of the table
            value_list (list): contains information about the test cases and their values
                    [{'entity': Entity, ..., 'test_value': str | list}]
            additional_infos (dict): the additional information for the test cases
        """
        
        super().__init__(app=app, root=root, layer=0)
        
        # get the entity names
        entity_names = []
        for value in value_list:
            if len(value["entity"].entity_name.split(".")[1]) > 30:
                entity_names.append(value["entity"].entity_name.replace('.', '.\n')[:30] + '...')
            else:
                entity_names.append(value["entity"].entity_name.replace('.', '.\n'))
        
        # create the header values
        header_values = ["ID"] + entity_names + [app.lang["REQUIREMENT_SHORT"], app.lang["PRIORITY_SHORT"]]
        
        # create the combined case values for the table body
        combined_case_values = test_case_gen.create_test_case_input_combinations(
            value_list
        )
        
        # combine the header and the body values
        table_values = [header_values] + self.add_row_ids_and_infos(
            combined_case_values, additional_infos
        )

        # calculate the column width
        col_width = [40] + [140] * len(value_list) + [80, 40]
        
        # create the table content frame
        self.table_content = self.add_element_frame(expand=True)

        self.table = CTkTable(
            master=self.table_content,
            values=table_values,
            write=True,
            col_width=col_width,
            padx=10,
            pady=10,
            header_col = True,
        )
        
        # --- grid the elements ---
        
        self.table.grid(row=0, column=0, sticky="news", padx=10, pady=10)


    def get_table_values(self):
        """
        Get the values of the table

        Returns:
            list: the values of the table
        """   
        # get the values of the table body without the header row and the first column
        values = [row[1:] for row in self.table.values[1:]]  
        return values
    
    def add_row_ids_and_infos(self, ccombined_case_vals: list, additional_infos: dict):
        """
        Add the row ids and additional information to the table
        
        Args:
            ccombined_case_vals (list): the combined case values
            additional_infos (dict): the additional information for the test cases
        """
        
        for i, row in enumerate(ccombined_case_vals):
            row.insert(0, i+1)
            row.append(additional_infos["requirement"])
            row.append(additional_infos["priority"])
        
        return ccombined_case_vals
        


class NavBtns(cW.NavigationButtons):
    def __init__(self, app, root, automation_id: int):
        """
        Constructor for the NavBtns class

        Args:
            app (test_environment_app.AppWindow): the main application
            root (customtkinter.CTk): the parent frame of the navigation buttons
            automation_id (int): the id of the automation
        """

        super().__init__(
            root=root,
            objects=2,
            values=(app.lang["DISCARD"], app.lang["FINISH"]),
            options={"btn_1_type": "delete", "btn_2_type": "accept"},
        )

        self.root = root
        self.automation_id = automation_id

    def btn_1_func(self):
        self.root.app.go_back(old_frame=self.root)

    def btn_2_func(self):
        table_values: list = self.root.table_frame.get_table_values()
        case_input_values = [value[:-2] for value in table_values]
        requirements = [value[-2] for value in table_values]
        priorities = [value[-1] for value in table_values]

        test_case_gen.add_test_cases_to_db(
            automation_id=self.root.app.selected_automation,
            combination_of_test_inputs=case_input_values,
            input_value_list=self.root.test_case_value_list,
            reqiurements=requirements,
            case_priorities=priorities,
        )
        
        self.root.app.entity_value_frame_dict = {}
        
        # remove the current frame from the frame stack to go back to the previous frame 
        # before the test case creation after the test cases are added to the database
        self.root.app.frame_stack.pop()
        self.root.app.go_back(old_frame=self.root)
        
        
