
from backend.database.db_utils import load_automations
from frontend.customWidgets import customWidgets as cW

from .automation_selection import AutomationSelectionFrame


class ProjectSelectionFrame(cW.BasisFrame):
    """
    ProjectSelection is a frame class that allows the user to select the project
    """

    def __init__(
        self,
        app,
    ):
        super().__init__(
            app,
            root=None,
            layer=0,
        )

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.navigation_bar = cW.NavigationBar(
            self, nav_path=app.lang["PROJECT_OVERVIEW"], mode=app.settings["MODE"]
        )
        self.navigation_bar.grid(row=0, column=0, sticky="we")

        self.project_list_frame = cW.BasisScrollFrame(
            app, self, layer=1, border=False, scroll_direction="x"
        )
        self.project_list_frame.grid(row=1, column=0, sticky="news", pady=(15, 15), padx=(15, 15))

        uncatogarized_automations = ProjectFrame(app, self.project_list_frame.content, app.lang["UNCATEGORIZED"])
        uncatogarized_automations.grid(row=0, column=0, padx=(15, 15))

        for project in app.projects:
            project_frame = ProjectFrame(app, self.project_list_frame.content, project)
            project_frame.grid(row=0, column=len(self.project_list_frame.content.winfo_children())+1, padx=(0, 15))
            
        self.navigation_btn = cW.NavigationButtons(self, objects=1, values=(app.lang["OPEN"],), pos="right")
        self.navigation_btn.grid(row=2, column=0, sticky="news", pady=(0, 20), padx=(25, 25))

    def open_project(self, project):
        self.app.selected_project = project
        self.app.project_automations = load_automations(project)
        self.app.load_new_frame(self, AutomationSelectionFrame(self.app))


class ProjectFrame(cW.BasisFrame):
    """
    ProjectFrame is a frame class that contains the project icon and the project name
    """

    def __init__(
        self,
        app,
        root,
        project_name,
        project_icon_white: str = "home_48dpWhite.png",
        project_icon_black: str = "home_48dp_black.png",
    ):
        """
        Intialization of the project frame

        Args:
            app (customtkinter.CTk): the parent window of the project frame
            root (customtkinter.CTk): the parent frame of the project frame
            project_name (str): the name of the project
            project_icon_white (str): the name of the white project icon
            project_icon_black (str): the name of the black project icon
        """
        super().__init__(app=app, root=root, layer=1)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # white square icon button with the label below and blue hover effect 
        self.project_button = cW.CTkButton()

        # self.project_icon = cW.IconImage(
        #     root=self,
        #     light_theme_img_path=path.join(ICON_PATH, project_icon_black),
        #     dark_theme_img_path=path.join(ICON_PATH, project_icon_white),
        #     size=(48, 48),
        # )
        # self.project_icon.grid(row=0, column=0, sticky="news", pady=(5, 5), padx=(5, 5))

        self.project_name = cW.CTkLabel(
            self,
            text=project_name,
            font=("Roboto", 16),
            wraplength=100,
        )
        self.project_name.grid(row=1, column=0, sticky="ew", pady=(5, 5), padx=(5, 5))

    def project_btn_press(self):
        pass
        # self.app.selected_project = self.project_name