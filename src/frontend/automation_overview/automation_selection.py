from customtkinter import CTkFont, CTkLabel, CTkRadioButton, StringVar

from backend.database import db_utils
from backend.database.db_utils import load_automations
from frontend.automation_details import automation_details_main as aD
from frontend.automation_insertion import AutomationCreationFrame
from frontend.automation_test_case_creation import CaseCreationFrame
from frontend.customWidgets import customWidgets as cW


class AutomationSelectionFrame(cW.BasisFrame):
    """
    AutomationSelection is a frame class that allows the user to select the automation
    """

    def __init__(self, app):
        """
        Initialization of the AutomationSelection frame

        Args:
            app (customtkinter.CTK): the parent window of the automation selection frame
        """

        super().__init__(app=app, layer=0)

        if app.selected_project is not None:
            navigation_text = str(
                app.selected_project + "/" + app.lang["AUTOMATION_OVERVIEW"]
            )
            automations = load_automations(project=self.app.selected_project)
        else:
            navigation_text = str(app.lang["AUTOMATION_OVERVIEW"])

        self.navigation_bar = cW.NavigationBar(
            self, nav_path=navigation_text, mode=app.settings["MODE"]
        )

        self.automation_list_frame = AutomationSelectionList(
            selection_frame=self, app=app, automations=automations
        )

        self.add_automation_btn = cW.AcceptButton(
            self, text=app.lang["NEW_A"], kind=2, command=self.new_automation, width=260
        )

        if app.selected_project is not None:
            self.nav_btns = NavBtns(
                app=app,
                root=self,
                objects=2,
                pos="right",
                values=(app.lang["TEST"], app.lang["BACK"]),
            )
        else:
            self.nav_btns = NavBtns(
                app=app, root=self, objects=1, values=(app.lang["TEST"],), pos="center"
            )

        # --- grid the elements ---

        # grid the main elements
        self.navigation_bar.grid(row=0, column=0, sticky="we")
        self.automation_list_frame.grid(
            row=1, column=0, sticky="news", padx=(15), pady=(15, 15)
        )
        self.add_automation_btn.grid(row=2, column=0, pady=(0, 20))
        self.nav_btns.grid(row=3, column=0, sticky="news")

        # make the selection frame resizable depending on the window size
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

    def new_automation(self):
        """
        Function to handle the New Automation button press
        """
        self.app.load_new_frame(
            self,
            AutomationCreationFrame(self.app),
        )

    def enable_test_automation(self):
        """
        Function to handle the Test Automation button press
        """
        self.nav_btns.btn_1.configure(state="normal")


class AutomationSelectionList(cW.BasisScrollFrame):
    """
    AutomationSelectionList is a frame class that allows the user to select the automation
    """

    def __init__(self, app, selection_frame, automations: list):
        """
        Initialization of the AutomationSelectionList frame

        Args:
            app (customtkinter.CTK): the parent window of the automation selection frame
            selection_frame (cW.BasisFrame): the parent frame of the automation selection list
            automations (list): the list of automations to be displayed
        """

        # Define the italic font
        italic_font = CTkFont(family="Helvetica", size=14, slant="italic")

        super().__init__(
            app=app,
            root=selection_frame,
            layer=1,
            scroll_direction="y",
        )

        # the same variable combines radio buttons so only one is selectable
        self.selected_automation = StringVar(value="none")

        for automation in automations:
            a_id, a_name, a_version = automation
            # TODO: handle long automation names as wrapping text, cutting off the text or using xyframes

            # TODO: add color if tested positive or negative to the element frame
            self.add_element_frame(
                row=automations.index(automation),
                column=0,
            )

            automation_element = CTkRadioButton(
                self.element_frame,
                text=a_name,
                variable=self.selected_automation,
                value=a_id,
                command=self.radiobtn_event,
            )

            automation_version = CTkLabel(
                self.element_frame,
                text=selection_frame.master.lang["VERSION"]
                + " "
                + a_version,  # TODO apply language settings to the version text if "unknown"
                font=italic_font,
                text_color="#bdbdbd",
            )

            more_info_btn = MoreBtns(
                self.element_frame,
                automation_id=a_id,
                text=selection_frame.master.lang["MORE"],
            )

            # --- grid the elements ---

            # grid the elements inside the selection frame
            automation_element.grid(
                row=0,
                column=0,
                sticky="we",
                pady=(10, 10),
                padx=(15, 15),
            )

            automation_version.grid(
                row=0,
                column=1,
                pady=(10, 10),
                padx=(15, 15),
            )

            more_info_btn.grid(
                row=0,
                column=2,
                sticky="e",
                pady=(10, 10),
                padx=(5, 15),
            )

            # make the automation name expandable
            self.element_frame.columnconfigure(0, weight=1)

    def get(self):
        """
        Function to get the selected automation id

        Returns:
            int - the selected automation id
        """
        return self.variable.get()

    def radiobtn_event(self):
        """
        Function to enable the test automation button when an automation is selected
        """
        # TODO check if the test automation button needs to be enabled
        self.master.enable_test_automation()


class MoreBtns(cW.NeutralButton):
    """
    A button class to open the automation infos
    """

    def __init__(self, root, automation_id, text):
        """
        Initialization of the MoreBtns button

        Args:
            root (cW.BasisFrame): the parent frame of the button
            automation_id (int): the id of the automation
            text (str): the text of the button
        """
        super().__init__(
            root,
            width=50,
            text=text,
            kind=2,
            command=self.open_automation_infos,
        )
        self.automation_id = automation_id

    def open_automation_infos(self):
        """
        Function to handle the More button press and open the automation infos
        for the selected automation
        """

        automation_name = db_utils.get_automation_name(self.automation_id)

        self.master.app.load_new_frame(
            prev_frame=self.master,
            new_frame=aD.AutomationDetailsFrame(
                app=self.master.app,
                a_id=self.automation_id,
                automation_name=automation_name,
            ),
            return_btn=True,
        )


class NavBtns(cW.NavigationButtons):
    """
    The child class of NavigationButtons to overwrite the functions
    """

    def __init__(self, app, root, pos, objects: int = 2, values: cW.Tuple[str] = None):
        """
        Initialization of the NavBtns class for the AutomationSelection frame

        Args:
            app (test_environment_app.AppWindow): the application window
            root (cW.BasisFrame): the parent frame of the navigation buttons
            pos (str): the position of the navigation buttons
            objects (int): the number of buttons to be displayed
            values (cW.Tuple[str]): the text values of the buttons
        """
        self.objects = objects

        self.app = app

        super().__init__(root, objects, values, pos)

        self.btn_1.configure(state="disabled")

    def btn_1_func(self):
        """
        Function to handle the test button press
        """

        self.app.selected_automation = (
            self.master.automation_list_frame.selected_automation.get()
        )
        self.app.load_new_frame(
            prev_frame=self.master,
            new_frame=CaseCreationFrame(
                app=self.app,
            ),
            return_btn=True,
        )

    def btn_2_func(self):
        """
        Function to handle the back button press
        """
        self.master.app.go_back(old_frame=self.master)
