from customtkinter import CTkFont, CTkLabel, CTkRadioButton, StringVar

from frontend.automation_insertion import AutomationCreationFrame
from frontend.customWidgets import customWidgets as cW


class AutomationSelectionFrame(cW.BasisFrame):
    """
    AutomationSelection is a frame class that allows the user to select the automation
    """

    def __init__(self, app):
        """
        Initialization of the AutomationSelection frame
        """

        super().__init__(app=app, layer=0)

        # create the navigation bar
        if app.selected_project is not None:
            navigation_text = str(
                app.selected_project + "/" + app.lang["AUTOMATION_OVERVIEW"]
            )
        else:
            navigation_text = str(app.lang["AUTOMATION_OVERVIEW"])

        self.navigation_bar = cW.NavigationBar(
            self, nav_path=navigation_text, mode=app.settings["MODE"]
        )

        # create the automation list frame with the automation selection
        self.automation_list_frame = AutomationSelectionList(
            selection_frame=self, app=app, automations=app.project_automations
        )

        # create the button to add a new automation
        self.add_automation_btn = cW.AcceptButton(
            self, text=app.lang["NEW_A"], kind=2, command=self.new_automation, width=260
        )

        # create the navigation buttons for the window and set overwrite the functions
        if app.selected_project is not None:
            self.nav_btns = NavBtns(
                self, objects=2, values=(app.lang["TEST"], app.lang["BACK"])
            )
        else:
            self.nav_btns = NavBtns(
                self, objects=1, values=(app.lang["TEST"],), pos="center"
            )

        # make the selection frame resizable depending on the window size
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # grid the elements
        self.navigation_bar.grid(row=0, column=0, sticky="we")
        self.automation_list_frame.grid(
            row=1, column=0, sticky="news", padx=(15), pady=(15, 15)
        )
        self.add_automation_btn.grid(row=2, column=0, pady=(0, 20))
        self.nav_btns.grid(row=3, column=0, sticky="news", pady=(0, 20), padx=(25, 25))

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
            self.add_content_frame(
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
                text=selection_frame.master.lang["VERSION"] + " " + a_version,
                font=italic_font,
                text_color="#bdbdbd",
            )

            more_info_btn = MoreBtns(
                self.element_frame,
                automation_id=a_id,
                text=selection_frame.master.lang["MORE"],
            )

            # make the automation name expandable
            self.element_frame.columnconfigure(0, weight=1)

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

    Args:
        cW.NeutralButton: the basic button class for blue buttons for more information or other actions
    """

    def __init__(self, master, automation_id, text):
        super().__init__(
            master,
            width=50,
            text=text,
            kind=2,
            command=self.open_automation_infos,
        )
        self.automation_id = automation_id

    def open_automation_infos(self):
        # TODO open the automation infos window
        print("open automation infos for automation id:" + str(self.automation_id))


class NavBtns(cW.NavigationButtons):
    """
    The child class of NavigationButtons to overwrite the functions
    """

    def __init__(self, master, pos, objects: int = 2, values: cW.Tuple[str] = None):
        self.objects = objects
        super().__init__(master, objects, values, pos)

        self.btn_1.configure(state="disabled")

    def btn_1_func(self):
        """
        Function to handle the test button press
        """
        # TODO open the test case selection window
        print(self.master.automation_list_frame.selected_automation.get())

    def btn_2_func(self):
        """
        Function to handle the back button press
        """
        self.app.go_back(old_frame=self.master)
