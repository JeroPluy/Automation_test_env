
from frontend.customWidgets import customWidgets as cW


class AutomationEntityFrame(cW.BasisFrame):
    """
    The frame class displaying the automation entity with the name and their integration 
    as well as automation mode and the maximum number of script instances
    """

    def __init__(self, app, automation_name):
        """
        The initialization of the automation entity frame
        
        Args:
            app (customtkinter.CTK): the parent window of the automation entity frame
            automation_name (str): the name of the new automation
            project (str): the name of the project of the new automation
        """
        
        super().__init__(app=app, layer=0)
        
        if app.selected_project is None:
            nav_path = automation_name
        else:
            nav_path = str(app.selected_project + "/" + automation_name)
            
        self.grid_columnconfigure(0, weight=1)

        self.nav_bar = cW.NavigationBar(
            self,
            mode=app.settings["MODE"],
            nav_path=nav_path,
        )
        
        self.nav_bar.grid(row=0, column=0, sticky="ew")