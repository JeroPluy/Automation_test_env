from frontend.customWidgets import customWidgets as cW
from frontend.automation_details import automation_details_main as aD
from .automation_insertion_utils import (
    clear_automation_insertion_frames,
    AdditionalInfoListFrame,
)

from backend import database as db


class AutomationInfosFrame(cW.BasisFrame):
    """
    The frame class displaying the automation information and
    providing the user with the possibility to change them or add new ones
    """

    def __init__(self, app, automation_name, a_id):
        """
        Initialization of the automation information frame

        Args:
            app (customtkinter.CTK): the parent window of the automation information frame
            automation_name (str): the name of the new automation
            a_id (str): the id of the new automation
        """
        super().__init__(app=app, layer=0)

        if app.selected_project is None:
            self.nav_path = automation_name
        else:
            self.nav_path = str(app.selected_project + "/" + automation_name)

        self.nav_bar = cW.NavigationBar(
            self,
            mode=app.settings["MODE"],
            nav_path=self.nav_path,
        )

        # add the project and version info frames to the list as default
        if app.selected_project is not None:
            project_str = app.selected_project
        else:
            project_str = "uncategorized"

        version_str = app.new_automation.version

        # preselect the project and version info frames and mark them as not removable
        preselected_infos = [
            ("project", project_str, False),
            ("version", version_str, False),
        ]

        self.main_content_frame = AdditionalInfoListFrame(
            app=app, root=self, add_infos=preselected_infos
        )

        self.nav_btn = Nav_btn(app, self)

        # grid the main elements
        self.nav_bar.grid(row=0, column=0, sticky="we")
        self.main_content_frame.grid(
            row=1, column=0, sticky="news", pady=(15, 10), padx=(25)
        )

        self.nav_btn.grid(row=2, column=0, sticky="we")

        # make the content frame resizable depending on the window size
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)


class Nav_btn(cW.NavigationButtons):
    def __init__(self, app, root):
        super().__init__(
            root=root,
            objects=1,
            values=[app.lang["FINISH"]],
            pos="center",
            options={"btn_1_type": "accept"},
        )

    def btn_1_func(self):
        """
        Function to finish the automation creation process
        """

        db.add_additional_info(
            a_id=self.master.app.new_automation.a_id,
            infos=self.master.main_content_frame.get_infos(),
        )

        # open the automation details frame for the new automation
        automation = self.master.app.new_automation.config["infos"]

        clear_automation_insertion_frames(self.master.app.frame_stack)

        self.master.app.load_new_frame(
            prev_frame=self.master,
            new_frame=aD.AutomationDetailsFrame(
                app=self.master.app,
                a_id=self.master.app.new_automation.a_id,
                automation_name=automation.a_name,
            ),
            returnable=True,
        )

        # reset the new automation object
        self.master.app.new_automation = None
