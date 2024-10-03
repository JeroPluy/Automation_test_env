"""
This module is the entry point for the application. It displays the start screen of the application.
"""

from os import path

from backend.database.db_utils import load_automations, load_projects
from frontend import automation_insertion as aI
from frontend import automation_overview as aS
from frontend.customWidgets import customWidgets as cW


class StartFrame(cW.BasisFrame):
    """
    The start frame of the application
    """

    def __init__(self, app, **kwargs):
        """
        Initialization of the start screen frame
        Args:
            master (customtkinter.CTk): the parent frame of the window
        """

        super().__init__(app=app, root=app, layer=0, **kwargs)

        image_path = path.join("src", "frontend", "customWidgets", "icons")
        light_logo = path.join(image_path, "logo_w_txt.png")
        dark_logo = path.join(image_path, "logo_inverted_w_txt.png")

        self.logo_img = cW.IconImage(
            root=self,
            light_theme_img_path=light_logo,
            dark_theme_img_path=dark_logo,
            size=(600, 256),
        )
        self.logo_img.pack(fill="both", expand=True, pady=(0, 20))

        app.selected_project = None

        # # TODO debug -----
        # print(app.projects)
        # delay = 1000
        # self.after(delay, self.next_frame)
        # # TODO debug -----

        self.after(100, self.next_frame)

        # TODO debug: skip to automation creation
        # self.after(100, self.skip_to_automation_creation)

    def next_frame(self):
        projects = load_projects()
        if len(projects) <= 1:
            if len(projects) == 0:
                projects.append("uncategorized")
                project_automations = []
            if projects[0] == "uncategorized":
                project_automations = load_automations()
                self.app.load_new_frame(self, aS.AutomationSelectionFrame(self.app, automations=project_automations))
            else: # only one other project
                self.app.selected_project = projects[0]
                # add the project selection frame to the frame stack
                self.app.frame_stack.append(aS.ProjectSelectionFrame)
                project_automations = load_automations(
                    project=self.app.selected_project
                )
                self.app.load_new_frame(self, aS.AutomationSelectionFrame(self.app, automations=project_automations))
        else:
            self.app.load_new_frame(self, aS.ProjectSelectionFrame(self.app, projects))

    def skip_to_automation_creation(self):
        create_frame = self.app.load_new_frame(
            self, aI.AutomationCreationFrame(self.app)
        )
        create_frame.load_automation(
            automation_path=path.join(
                "test_data",
                "yaml_files",
                "example_automations",
                "2024.08.02",
                "living_room_tv_lighting.yaml",
            ),
        )
