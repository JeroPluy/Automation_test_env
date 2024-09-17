"""
This module is the entry point for the application. It displays the start screen of the application.
"""

from os import path
from frontend.customWidgets import customWidgets as cW
from frontend import automation_overview as aS

from customtkinter import CTkLabel

from backend.database.db_utils import load_projects, load_automations

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
            light_img_path=light_logo, dark_img_path=dark_logo, size=(600, 256)
        )
        self.image_label = CTkLabel(self, image=self.logo_img, text="")
        self.image_label.pack(fill="both", expand=True, pady=(0, 20))

        app.selected_project = None
        app.projects = load_projects()

        # TODO debug -----
        print(app.projects)
        delay = 1000
        # TODO debug -----
        
        self.after(delay, self.next_frame)


    def next_frame(self):
        if len(self.app.projects) <= 1:
            if len(self.app.projects) == 0:
                self.app.projects.append("uncategorized") 
                self.app.project_automations = []
            if self.app.projects[0] == "uncategorized":
                self.app.project_automations = load_automations()
                self.app.load_new_frame(self, aS.AutomationSelectionFrame(self.app))
        else:
            self.app.load_new_frame(self, aS.ProjectSelectionFrame(self.app))
        