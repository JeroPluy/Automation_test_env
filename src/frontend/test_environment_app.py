"""
This module is the main module for the test environment application. It is the main module that is run to start the application.
"""

from customtkinter import CTk, set_default_color_theme, set_appearance_mode
from frontend.utils import load_language, load_settings, THEME_PATH

from frontend.automation_overview.application_start import StartFrame


class AppWindow(CTk):
    """
    Class for the window of the application

    Args:
        BlankWindow (class): the blank window class for the application
    """

    def __init__(self, **kwargs):
        """
        Initialization of the start window of the application

        Args:
            master (customtkinter.CTk): the parent frame of the window
        """

        super().__init__()

        self.settings = load_settings()

        # scaling of the application but has a weird rezising issue
        # shortly after the start where the window expands after a few seconds

        # scale_factor = self.settings["SCALE_FACTOR"]
        # set_window_scaling(scale_factor)
        # set_widget_scaling(scale_factor)

        # center the window at the start
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        width = self.settings["WINDOW_SIZE"][0]
        height = self.settings["WINDOW_SIZE"][1]

        x = int(((screen_width / 2) - (width / 2)))
        y = int(((screen_height / 2) - (height / 1.8)))

        geometry = f"{width}x{height}+{x}+{y}"
        self.geometry(geometry)

        self.minsize(520, 340)

        self.lang = load_language(self.settings["LANG"])
        self.title(self.lang["APP_NAME"])
        set_default_color_theme(THEME_PATH)
        set_appearance_mode(self.settings["MODE"])
        
        self.start_frame = StartFrame(self)
        # display the start frame with the logo
        self.load_new_frame(None, self.start_frame)
     
     
    def load_new_frame(self, prev_frame, new_frame):
        """
        Function to load a new frame into the main window
        
        Args:
            prev_frame (customtkinter.CTk): the previous frame before the new frame
            new_frame (customtkinter.CTk): the new frame to be displayed
        """
        if prev_frame is not None:
            prev_frame.destroy()
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        new_frame.grid(row=0, column=0, sticky="news")

if __name__ == "__main__":
    app = AppWindow()
    app.mainloop()
