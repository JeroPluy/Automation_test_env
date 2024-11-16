from frontend.customWidgets import customWidgets as cW 


class SettingsFrame(cW.BasisFrame):
    """
    Class for the settings frame that allows the user to change the settings of the application
    """
    
    def __init__(app, root):
        
        super().__init__(app=app, root=root, layer=0)