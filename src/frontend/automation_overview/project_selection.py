from os import path

from backend.database.db_utils import load_projects
from frontend.customWidgets import customWidgets as cW
from frontend.utils import ICON_PATH

from .automation_selection import AutomationSelectionFrame


class ProjectSelectionFrame(cW.BasisFrame):
    """
    ProjectSelection is a frame class that allows the user to select the project
    """

    def __init__(
        self,
        app,
        projects: list = None,
    ):
        """
        Initialization of the project selection frame

        Args:
            app (CTk): the parent window of the project selection frame
            projects (list): the list of projects. Standard is None.
        """
        super().__init__(
            app,
            root=None,
            layer=0,
        )

        self.navigation_bar = cW.NavigationBar(
            self, nav_path=app.lang["PROJECT_OVERVIEW"], mode=app.settings["MODE"]
        )

        self.project_list_frame = ProjectListFrame(app, self, projects)

        self.navigation_btn = NavBtn(root=self, value=(app.lang["OPEN"],))

        # --- grid the elements ---

        # grid the main elements
        self.navigation_bar.grid(row=0, column=0, sticky="we")
        self.project_list_frame.grid(
            row=1, column=0, sticky="news", pady=(15, 15), padx=(15, 15)
        )
        self.navigation_btn.grid(row=2, column=0, sticky="news")

        # make the project list frame resizable depending on the window size
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)


class ProjectListFrame(cW.BasisScrollFrame):
    """
    ProjectListFrame is a scroll frame class that contains all the project frames
    """

    def __init__(self, app, root, projects: list):
        """
        Initialization of the project list frame

        Args:
            app (CTk): the parent window of the project list frame
            root (ProjectSelectionFrame): the parent frame of the project list frame
            projects (list): the list of projects. If None, the projects will be loaded from the database
        """
        super().__init__(app, root, layer=1, border=False, scroll_direction="x")

        self.content.choosen_project = None
        self.content.selected_frame = None

        uncatogarized_automations = ProjectFrame(
            app, self.content, app.lang["UNCATEGORIZED"]
        )
        uncatogarized_automations.grid(row=0, column=0, padx=(15, 15))

        if projects is None:
            projects = load_projects()

        for project in projects:
            if project == "uncategorized":
                continue
            project_frame = ProjectFrame(app, self.content, project)
            project_frame.grid(
                row=0,
                column=len(self.content.winfo_children()) + 1,
                padx=(0, 15),
            )


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
        self.root = root

        super().__init__(app=app, root=root, layer=1)

        # white square icon button with the label below and blue hover effect
        self.project_button = ProjectButton(
            self, project_icon_white, project_icon_black
        )

        self.project_name = cW.CTkLabel(
            self,
            text=project_name,
            wraplength=100,
        )

        # --- grid the elements ---

        # grid the elements of the project frame
        self.project_button.grid(
            row=0, column=0, sticky="news", pady=(5, 5), padx=(5, 5)
        )
        self.project_name.grid(row=1, column=0, sticky="ew", pady=(5, 5), padx=(5, 5))

        # make the project button resizable depending on the window size
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


class ProjectButton(cW.CTkButton):
    """
    ProjectButton is a button class that contains the project icon as a selectable button
    """

    def __init__(
        self,
        root,
        project_icon_white: str = "home_48dpWhite.png",
        project_icon_black: str = "home_48dp_black.png",
    ):
        """
        Initialization of the project button

        Args:
            root (customtkinter.CTk): the parent frame of the project button
            project_icon_white (str): the name of the white project icon
            project_icon_black (str): the name of the black project icon
        """

        self.selected = False

        image = cW.CTkImage(
            light_image=cW.Image.open(path.join(ICON_PATH, project_icon_black)),
            dark_image=cW.Image.open(path.join(ICON_PATH, project_icon_white)),
            size=(150, 150),
        )

        super().__init__(
            master=root,
            image=image,
            text="",
            fg_color=["#FCFCFC", "#343446"],
            command=self.project_btn_press,
        )

    def project_btn_press(self):
        """
        Function to select the project button
        """
        self.selected = True

        # reset the previous selected project / button
        if self.master.root.choosen_project is not None:
            self.master.root.selected_frame.project_button.selected = False
            self.master.root.selected_frame.project_button.configure(
                fg_color=["#FCFCFC", "#343446"]
            )
            self.master.root.choosen_project = None
            self.master.root.selected_frame = None

        if self.selected:
            self.configure(fg_color="#1D91DA")
            self.master.root.choosen_project = self.master.project_name.cget("text")
            self.master.root.selected_frame = self.master


class NavBtn(cW.NavigationButtons):
    """
    NavBtn is a button class that defines the navigation button for the project selection frame
    """

    def __init__(self, root, value):
        """
        Initialization of the navigation button

        Args:
            root (ProjectSelectionFrame): the parent frame of the navigation button
            value (str): the value of the navigation button
        """

        self.root = root

        super().__init__(root, objects=1, values=value, pos="right")

    def btn_1_func(self):
        """
        Function to open the selected project and load the automation selection frame
        """
        app = self.root.app

        project = self.root.project_list_frame.content.choosen_project
        if project is None:
            project = "uncategorized"
        app.selected_project = project
        app.load_new_frame(self, AutomationSelectionFrame(app))
