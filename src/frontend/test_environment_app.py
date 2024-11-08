"""
This module is the main module for the test environment application. It is the main module that is run to start the application.
"""

from customtkinter import CTk, set_appearance_mode, set_default_color_theme

from frontend.automation_overview.application_start import StartFrame
from frontend.utils import THEME_PATH, load_language, load_settings


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

        # init the frame history stack and the start frame
        self.frame_stack = []
        self.start_frame = StartFrame(self)
        # display the start frame with the logo
        self.load_new_frame(None, self.start_frame, returnable=False)

    def load_new_frame(self, prev_frame, new_frame, returnable=True):
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
        if returnable:  
            self.frame_stack.append(new_frame.__class__)

        # TODO debug
        for frame in self.frame_stack:
            print(frame)
        print("-----------------")

        return new_frame

    def go_back(self, old_frame):
        """
        Function to go back to the previous frame

        Args:
            old_frame (customtkinter.CTk): the current frame before going back
        """
        if len(self.frame_stack) > 1:
            self.frame_stack.pop()

            new_frame_class = self.frame_stack[-1]
            new_frame = new_frame_class(self)
            self.load_new_frame(old_frame, new_frame)
            self.frame_stack.pop()
        else:
            print("Error: No previous frame found")


if __name__ == "__main__":
    app = AppWindow()
    app.mainloop()
