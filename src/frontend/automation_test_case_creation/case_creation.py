from tkinter import StringVar
from ..customWidgets import customWidgets as cW

from backend.database import db_utils
from backend.utils.env_helper_classes import Entity

from customtkinter import CTkEntry, CTkFont, CTkLabel

from .range_value_creation import RangeValueFrame


class CaseCreationFrame(cW.BasisFrame):
    """
    The base frame for creating a new test case
    """

    def __init__(self, app):
        """
        Initialization of the test case creation frame
        Args:
            app (test_environment_app.AppWindow): the application window
            a_id (int): the id of the automation
        """

        super().__init__(app=app)

        self.app = app

        a_id = app.selected_automation

        automation_name = db_utils.get_automation_name(a_id)

        if app.selected_project is None:
            nav_path = automation_name
        else:
            nav_path = str(app.selected_project) + "/" + automation_name

        self.nav_bar = cW.NavigationBar(
            self, mode=app.settings["MODE"], nav_path=nav_path
        )

        self.nav_btns = NavBtns(app=app, root=self, automation_id=a_id)

        # needs to be initialized here to be able to access the nav_btns from the test case settings frame
        self.main_frame = TestCaseSettings(
            app=app,
            root=self,
            a_id=a_id,
        )

        # --- grid the elements ---

        # grid the main elements
        self.nav_bar.grid(row=0, column=0, sticky="we")
        self.main_frame.grid(
            row=1, column=0, sticky="news", padx=(15, 15), pady=(15, 15)
        )
        self.nav_btns.grid(row=2, column=0, sticky="we")

        # make the test case settings frame expandable
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)


class TestCaseSettings(cW.BasisFrame):
    """
    Subframe for the test case settings like entity values, requirements and priority
    """

    def __init__(self, app, root, a_id):
        """
        Initialization of the test case settings frame

        Args:
            app (test_environment_app.AppWindow): the application window
            root (cW.BasisFrame): the parent frame
            a_id (int): the id of the automation
        """

        super().__init__(app=app, root=root, layer=1)

        self.app = app

        self.entity_value_list = EntityValueList(app=app, root=self, a_id=a_id)

        # TODO: disable the import button if the automation has no other versions available in the database to import from
        self.import_test_case_btn = cW.NeutralButton(
            root=self,
            width=200,
            text=app.lang["IMPORT_TC"],
            command=self.import_test_case,
            state="normal",
        )

        self.add_settings_frame = AddSettingsFrame(app=app, root=self)

        # --- grid the elements ---

        self.entity_value_list.grid(
            row=0, column=0, sticky="news", padx=(15, 15), pady=(15, 15), columnspan=2
        )

        self.import_test_case_btn.grid(
            row=1, column=0, sticky="ew", padx=(15, 35), pady=(25, 25)
        )

        self.add_settings_frame.grid(
            row=1, column=1, sticky="news", padx=(15, 15), pady=(0, 15)
        )

        # make the value list expandable
        self.rowconfigure(0, weight=1)
        # self.columnconfigure(0, weight=1) # TODO check if this is necessary for the entity list
        self.columnconfigure(1, weight=1)

    def import_test_case(self):
        """
        Function to import a test case from another automation

        Args:
            automation_id (int): the id of the automation to import the test case to
        """
        # TODO implement the import of a test case from another automation
        print("Import test case for automation: " + str(self.app.selected_automation))

    def get_inputs(self):
        """
        Function to get the entity values from the entity value list

        Returns:
            list: containing the inputs of the test case
        """

        return self.entity_value_list.get_selected_values()


class EntityValueList(cW.BasisScrollFrame):
    """
    Subframe for the list of entity values
    """

    def __init__(self, app, root, a_id):
        """
        Initialization of the entity value list frame

        Args:
            app (test_environment_app.AppWindow): the application window
            root (cW.BasisFrame): the parent frame
            a_id (int): the id of the automation
        """

        super().__init__(app=app, root=root, scroll_direction="y")

        self.app = app

        self.a_id = a_id

        self.selected_options: int = 0

        self.entities: list = db_utils.get_automation_entities(
            automation_id=a_id, only_inputs=True
        )

        if not hasattr(self.app, "entity_value_frame_dict"):
            # dictionary to store the entity value frames for each entity
            self.app.entity_value_frame_dict = {}

        if self.app.entity_value_frame_dict is None:
            self.app.entity_value_frame_dict = {}

        row_counter = 0

        # get for each entity the possible values and create a frame for it
        for entity in self.entities:
            self.add_element_frame(row=row_counter, column=0)

            if entity.entity_id is None:
                raise Exception("Entity not found in the database")

            # if the entities are not already in the test case entity values, load them from the database and add them to the test case entity values
            if len(self.app.entity_value_frame_dict) < len(self.entities):
                # TODO differentiate between different types of possible value categories
                possible_values_dict = db_utils.get_entity_possible_values(
                    entity.entity_id
                )

                possible_values = [app.lang["MULTIPLE_VALS"]] + list(
                    possible_values_dict.keys()
                )

                entity_value_frame = EntityValueFrame(
                    app=app,
                    root=self.element_frame,
                    entity=entity,
                    possible_values=possible_values,
                )

                self.app.entity_value_frame_dict[entity.entity_id] = entity_value_frame

            else:
                # display the entity value frame with the selected value from the test case entity values
                old_entity_value_frame = self.app.entity_value_frame_dict[
                    entity.entity_id
                ]
                selected_value: str = old_entity_value_frame.get_selected_value()[
                    "shown_value"
                ]

                if selected_value == self.app.lang["MULTIPLE_VALS"]:
                    selected_value = "-"

                # rebind the entity value frame to the element frame
                entity_value_frame = EntityValueFrame(
                    app=app,
                    root=self.element_frame,
                    entity=entity,
                    possible_values=[app.lang["MULTIPLE_VALS"]]
                    + old_entity_value_frame.possible_values,
                    default_value=selected_value,
                )

                # if the entity value frame has a selected value, mark it as selected
                if selected_value != "-":
                    entity_value_frame.set_and_further_specification_type(
                        selected_value
                    )
                    # set the list from the incoming range value frame as the test value
                    entity_value_frame.test_value = old_entity_value_frame.test_value

            # --- grid the elements ---

            entity_value_frame.grid(
                row=row_counter,
                column=0,
                sticky="news",
                padx=(5, 5),
                pady=(2, 2),
            )

            self.element_frame.columnconfigure(0, weight=1)
            self.element_frame.rowconfigure(0, weight=1)

            row_counter += 1

    def unlock_create_btn(self):
        """
        Function to unlock the create button if for all entities a value is selected
        """
        self.selected_options += 1

        if self.selected_options == len(self.app.entity_value_frame_dict):
            self.root.root.nav_btns.btn_2.configure(state="normal")

    def get_selected_values(self) -> list:
        """
        Function to get all the selected values of the entities from the entity value frames

        Returns:
            list: containing the selected values of the entities and their entity id
        """

        selected_values = []

        for entity_id in self.app.entity_value_frame_dict:
            selected_values.append(
                self.app.entity_value_frame_dict[entity_id].get_selected_value()
            )

        return selected_values


class EntityValueFrame(cW.BasisFrame):
    """
    Subframe for an entity with its value/s
    """

    def __init__(
        self, app, root, entity: Entity, possible_values: list, default_value: str = "-"
    ):
        """
        Initialization of the entity value frame

        Args:
            app (test_environment_app.AppWindow): the application window
            root (cW.BasisFrame): the parent frame
            entity (Entity): the entity to be displayed
            possible_values (list): the possible values for the entity
            default_value (str): the default value for the entity
        """

        super().__init__(app=app, root=root, layer=2)

        self.entity = entity

        self.test_value = default_value

        entity_pos = entity.position
        entity_name = entity.entity_name
        entity_type = (
            app.lang["TRIGGER"]
            if entity.parameter_role == 0
            else app.lang["CONDITION"]
            if entity.parameter_role == 1
            else app.lang["ACTION"]
        )

        # remove the "Range of values" from the deposited possible values for the entity value frame
        self.possible_values = possible_values[1:]
        self.specified_value = False
        self.changed = False

        self.list_frame = self.root.root.root

        self.entity_position_label = CTkLabel(
            self, text=entity_type + " " + str(entity_pos), font=CTkFont(weight="bold")
        )

        self.entity_name_label = CTkLabel(self, text=entity_name)

        self.entity_value_selection = cW.FramendComboBox(
            root=self,
            values=possible_values,
            default_value=default_value,
            command=self.set_and_further_specification_type,
        )

        # --- grid the elements ---

        self.entity_position_label.grid(
            row=0, column=0, sticky="w", pady=(8, 0), padx=(10, 0)
        )

        self.entity_name_label.grid(
            row=1, column=0, sticky="w", pady=(0, 8), padx=(10, 0)
        )

        self.entity_value_selection.grid(
            row=1, column=1, sticky="e", pady=(0, 8), padx=(0, 10)
        )

        # the entity name label should be expandable
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

    def set_and_further_specification_type(self, value):
        """
        Function to specify the selected entity value further

        Args:
            value (str): the selected value of the OptionMenu
        """

        if value == self.app.lang["MULTIPLE_VALS"]:
            # load the range value frame
            self.app.load_new_frame(
                prev_frame=self.list_frame.root.root,
                new_frame=RangeValueFrame(
                    app=self.app,
                    entity_id=self.entity.entity_id,
                    entity_name=self.entity.entity_name,
                    nav_path=self.list_frame.root.root.nav_bar.get_nav_path(),
                    possible_values=self.possible_values,
                ),
                return_btn=True,
            )
        else:
            if value in db_utils.specification_p_values:
                self.specified_value = True

                self.specify_edit = CTkEntry(
                    master=self,
                    width=200,
                    height=40,
                    justify="right",
                )

                self.specify_edit.grid(
                    row=1, column=3, sticky="ew", pady=(0, 8), padx=(10, 10)
                )
            else:
                self.specified_value = False

                self.test_value = value

                if hasattr(self, "specify_edit"):
                    self.specify_edit.destroy()

            if not self.changed:
                self.changed = True
                self.list_frame.unlock_create_btn()

            self.app.entity_value_frame_dict[self.entity.entity_id] = self

    def get_selected_value(self) -> dict:
        """
        Function to get the selected value of the entity

        Returns:
            dict: containing the entity id and the selected value
        """

        if self.specified_value:
            return {
                "entity_id": self.entity.entity_id,
                "value": self.specify_edit.get(),
            }
        else:
            return {
                "entity_id": self.entity.entity_id,
                "value": self.test_value,
                "shown_value": self.entity_value_selection.get(),
            }


class AddSettingsFrame(cW.BasisFrame):
    """
    Subframe for the additional settings (requirement and priority) of the test case
    """

    def __init__(self, app, root):
        """
        Initialization of the additional settings frame with requirement and priority

        Args:
            app (test_environment_app.AppWindow): the application window
            root (cW.BasisFrame): the parent frame
        """
        super().__init__(app=app, root=root, layer=1)

        self.requirement_label = CTkLabel(self, text=app.lang["REQUIREMENT"])

        self.req_string = StringVar(value="")

        self.requirement_entry = CTkEntry(
            master=self,
            textvariable=self.req_string,
            height=40,
            width=80,
            justify="right",
        )

        self.priority_label = CTkLabel(self, text=app.lang["PRIORITY"])

        self.prio_value = StringVar(value="")

        self.priority_entry = CTkEntry(
            master=self,
            textvariable=self.prio_value,
            height=40,
            width=80,
            justify="right",
        )

        # --- grid the elements ---

        self.requirement_label.grid(
            row=0, column=0, sticky="e", pady=(2, 7), padx=(10, 25)
        )
        self.requirement_entry.grid(
            row=0, column=1, sticky="e", pady=(7, 2), padx=(0, 10)
        )

        self.priority_label.grid(
            row=1, column=0, sticky="e", pady=(2, 7), padx=(10, 25)
        )
        self.priority_entry.grid(row=1, column=1, sticky="e", pady=(7, 2), padx=(0, 10))

        self.columnconfigure(0, weight=1)


class NavBtns(cW.NavigationButtons):
    """
    Class for the navigation buttons of the test case creation frame
    """

    def __init__(self, app, root, automation_id):
        """
        Initialization of the navigation buttons

        Args:
            app (test_environment_app.AppWindow): the application window
            root (cW.BasisFrame): the parent frame
            automation_id (int): the id of the automation
        """

        super().__init__(
            root=root,
            objects=2,
            values=(app.lang["BACK"], app.lang["CREATE"]),
            options=({"btn_1_type": "neutral", "btn_2_type": "accept"}),
        )

        self.btn_2.configure(state="disabled")

        self.root = root

        self.automation_id = automation_id

    def btn_1_func(self):
        self.root.app.go_back(self.root)
        del self.root.app.entity_value_frame_dict

    def btn_2_func(self):
        # TODO create test case and hand over the values to the table overview frame
        print("Create test case for automation: " + str(self.automation_id))
        print(self.root.main_frame.get_inputs())
