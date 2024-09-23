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
            app, root=None, layer = 0,
        )
        
        self.navigation_bar = cW.NavigationBar(
            self, nav_path=app.lang["PROJECT_OVERVIEW"], mode=app.settings["MODE"]
        )
    
    def open_project(self, project):
        self.app.selected_project = project
        self.app.project_automations = load_automations(project)
        self.app.load_new_frame(self, AutomationSelectionFrame(self.app))
