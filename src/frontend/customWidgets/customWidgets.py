from abc import abstractmethod
from os import path
from tkinter import StringVar
from typing import Any, Callable, Tuple

from customtkinter import (
    CTkButton,
    CTkFrame,
    CTkImage,
    CTkLabel,
    CTkOptionMenu,
    CTkScrollableFrame,
    CTkToplevel,
    Variable,
)
from PIL import Image

from frontend.customWidgets.CTkXYFrame import CTkXYFrame


class BasisFrame(CTkFrame):
    """
    The basic frame for the application to hold all the widgets for different views
    """

    def __init__(
        self,
        app: Any,
        root: Any = None,
        layer: int = 0,
        fg_color: str | Tuple[str] | None = None,
        border_width: int | str | None = None,
        border_color: str | Tuple[str] | None = None,
        **kwargs,
    ):
        """
        Initialization of the basic frame for the application to hold all the widgets for different views
        and with different background colors for the different layers

        Args:
            app (AppWindow): the application object
            root (Any, optional): root frame for the basic frame
            layer (int, optional): layer of the basic frame. Defaults to 0.
            fg_color (str | Tuple[str] | None, optional): (Debugging purposes) foreground color of the basic frame. Defaults to None so its taken from the theme.
            border_width (int | str | None, optional): (Debugging purposes) border width of the basic frame. Defaults to None so its taken from the theme.
            border_color (str | Tuple[str] | None, optional): (Debugging purposes) border color of the basic frame. Defaults to None so its taken from the theme.
        """

        # provide the link to application instance for the frame
        self.app = app

        # link the application settings and language texts to the frame instance
        self.settings = app.settings
        self.lang = app.lang

        # if the root is not given then the root is the application window
        if root is None:
            self.root = app

        self.layer = layer
        color_mode = self.settings["MODE"]

        # depending on the layer the basic frame has different colors and round corners
        round_corners = None

        # base color for the first layer of the window
        if self.layer == 0:
            if color_mode == "light":
                fg_color = "#EFEFEF"
            else:
                fg_color = "#1E1E29"
            round_corners = 0

        # basic frame color
        elif self.layer == 1:
            if color_mode == "light":
                fg_color = "#f5f5f5"
            else:
                fg_color = "#252532"

        # secondary frame color on top of a basic frame
        elif self.layer == 2:
            if color_mode == "light":
                fg_color = "#FCFCFC"
            else:
                fg_color = "#343446"

        else:
            # debug coloring
            fg_color = fg_color
            round_corners = 0

        super().__init__(
            master=root,
            border_width=border_width,
            fg_color=fg_color,
            border_color=border_color,
            corner_radius=round_corners,
            **kwargs,
        )


class BasisScrollFrame(BasisFrame):
    """
    This is a basic scroll frame for the application which can be altered in the scroll direction
    to fit the needs of the application.
    Its based on the CTkXYFrame or CTkScrollableFrame with a BasisFrame as root element.
    """

    def __init__(
        self,
        app,
        root: Any,
        layer: int = 1,
        border: bool = False,
        scroll_direction: str = "both",
    ):
        """
        Initialization of the basic scroll frame based on a CTkXYFrame or CTkScrollableFrame in a BasisFrame.

        Args:
            app (Any): the application object
            root (Any): root frame for the basic scroll frame
            layer (int, optional): layer of the basic scroll frame. Defaults to 1.
            scroll_direction (str, optional): direction of the scroll. Defaults to "both".
        """

        if border:
            border_width = 2
            border_color = ["#989898", "#565B5E"]
        else:
            border_width = 0

        # create the basic frame for the scroll frame base
        super().__init__(app, root, layer=layer,border_width=border_width, border_color=border_color)

        # set the basic frame as wide as the root frame allows
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # create the scroll frame inside of the basic frame as a container for the content
        if scroll_direction == "y":
            self.content = CTkScrollableFrame(self, orientation="vertical")
            self.content.columnconfigure(0, weight=1)
        elif scroll_direction == "x":
            self.content = CTkScrollableFrame(self, orientation="horizontal")
            self.content.rowconfigure(0, weight=1)
        else:
            self.content = CTkXYFrame(self)

        # add the basis variables for the scroll frame
        self.content.layer = layer
        self.content.settings = app.settings
        self.content.lang = app.lang

        # set the scroll frame as wide as the basic frame allows
        self.content.grid(row=0, column=0, sticky="news", pady=(2,2), padx=(2,2))

    def add_content_frame(self, row: int = 0, column: int = 0):
        """
        Function to add a content frame to the scroll frame to hold the widgets and elements of the application.

        Args:
            row (int, optional): row position of the content. Defaults to 0.
            column (int, optional): column position of the content. Defaults to 0.
        """

        # NOTE: if the scroll frame is an XYFrame the content frame is only as wide as its content plus padding
        #       the expansion through the columnconfigure or pack(fill="both", expand=True) is not possible as far as I tested it

        self.element_frame = BasisFrame(
            app=self.app,
            root=self.content,
            layer=self.layer + 1,
        )

        self.element_frame.grid(
            row=row,
            column=column,
            sticky="we",
            pady=(5, 5),
            padx=(15, 15),
        )


class BlankToplevelWindow(CTkToplevel):
    """
    Basic top level window for warnings and errors.
    """

    def __init__(self, app, title: str = ""):
        """
        Initialization of the basic top level window for warnings and errors.

        Args:
            app (Any): the application object
            title (str, optional): title of the top level window. Defaults to "".
        """

        # create the toplevel window
        super().__init__()

        # set the title of the toplevel window
        self.title(title)

        # set toplevel window properties
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.minsize(280, 150)

        # center the toplevel window in the middle of the application window
        x: int = int(app.winfo_x() + app.winfo_width() / 2 - self.winfo_width() / 2)
        y: int = int(app.winfo_y() + app.winfo_height() / 2 - self.winfo_height() / 2)
        geometry = f"+{x}+{y}"
        self.geometry(geometry)


class PopupWarning(BlankToplevelWindow):
    """
    Custom toplevel window for popup warnings in the application.
    """

    # TODO the application window should not be usable when the popup is open

    def __init__(self, app, message: str, title: str = None):
        """
        Initialization of the custom toplevel window for popup warnings in the application.

        Args:
            app (Any): the application object
            message (str): message of the warning
            title (str, optional): title of the warning. Defaults to None.
        """

        # create the toplevel window for the warning with the title
        super().__init__(app=app, title=title)

        self.image = IconImage(
            root=self,
            light_theme_img_path=path.join(
                path.dirname(path.realpath(__file__)), "icons", "warning_black.png"
            ),
            dark_img_path=path.join(
                path.dirname(path.realpath(__file__)), "icons", "warning_white.png"
            ),
            size=(30, 30),
        )
        self.image.pack(pady=(15, 0))

        # create place the warning label with the message in the toplevel window
        self.warning_label = CTkLabel(
            self,
            text=message,
            wraplength=400,
            compound="left",
            anchor="center",
        )

        self.warning_label.pack(padx=15, pady=15, fill="both", expand=True)
        self.warning_label.rowconfigure(0, weight=1)

        # create and place the ok button to close the warning
        self.back_btn = NeutralButton(
            self,
            text=app.lang["OK"],
            kind=-1,
            width=130,
            height=30,
            command=self.destroy,
        )

        self.back_btn.pack(
            pady=15,
        )


class IconImage(CTkLabel):
    """
    Custom image class for icons in the application which has a light and dark form
    """

    def __init__(
        self,
        root: Any,
        light_theme_img_path: str,
        dark_theme_img_path: str = None,
        size: Tuple[int] = (30, 30),
    ):
        """
        Initialization of the custom image icon for the application

        Args:
            light_theme_img_path (str): path to the dark image
            dark_theme_img_path (str, optional): path to the bright image. Defaults to None.
            size (Tuple[int], optional): size of the image. Defaults to (30, 30).
        """

        # if the dark image path is not given then the dark image is the same as the light image
        if dark_theme_img_path is None:
            dark_theme_img_path = light_theme_img_path

        self.image = CTkImage(
            light_image=Image.open(light_theme_img_path),
            dark_image=Image.open(dark_theme_img_path),
            size=size,
        )

        super().__init__(
            master=root,
            text="",
            image=self.image,
        )


class AcceptButton(CTkButton):
    """
    Custom button for the application to to accept inputs and changes or
    confirm actions. The button has a green color.
    """

    def __init__(
        self,
        root: Any,
        width: int = 140,
        height: int = 28,
        text: str = None,
        textvariable: Variable | None = None,
        state: str = "normal",
        hover: bool = True,
        corner_radius: int = None,
        command: Callable[[], Any] | None = None,
        kind: int = None,
    ):
        """
        Initialization of the custom button for the application to to accept inputs and changes or
        confirm actions. The button has a green color.

        Args:
            root (Any): root frame for the button
            width (int, optional): width of the button. Defaults to 140.
            height (int, optional): height of the button. Defaults to 28.
            text (str, optional): text of the button. Defaults to None so its just an icon.
            textvariable (Variable | None, optional): textvariable of the button. Defaults to None.
            state (str, optional): state of the button (if it is clickable). Defaults to "normal".
            hover (bool, optional): hover of the button. Defaults to True.
            corner_radius (int, optional): corner radius of the button. Defaults to None so its taken from the theme.
            command (Callable[[], Any] | None, optional): command of the button. Defaults to None.
            kind (int, optional): kind of the button.
            Defaults to None = check icon, 0 = import icon, 1 = save icon, 2 = add icon, -1 = no icon.
        """

        image_path = path.join(path.dirname(path.realpath(__file__)), "icons")
        if kind == 0:
            icon = "import_white.png"
        elif kind == 1:
            icon = "save_white.png"
        elif kind == 2:
            icon = "add_white.png"
        elif kind == -1:
            icon = None
        else:
            icon = "check_white.png"

        if icon is not None:
            image = CTkImage(Image.open(path.join(image_path, icon)), size=(24, 24))
        else:
            image = None

        super().__init__(
            root,
            width,
            height,
            fg_color="#227F6D",
            hover_color="#1D5249",
            text=text,
            textvariable=textvariable,
            image=image,
            state=state,
            hover=hover,
            corner_radius=corner_radius,
            command=command,
        )


class DeleteButton(CTkButton):
    """
    Custom button for the application to delete entries or decline actions.
    The button has a red color.
    """

    def __init__(
        self,
        root: Any,
        width: int = 140,
        height: int = 28,
        text: str = None,
        textvariable: Variable | None = None,
        state: str = "normal",
        hover: bool = True,
        corner_radius: int = None,
        command: Callable[[], Any] | None = None,
        kind: int = None,
    ):
        """
        Initialization of the custom button for the application to delete entries or decline actions.

        Args:
            root (Any): root frame for the button
            width (int, optional): width of the button. Defaults to 140.
            height (int, optional): height of the button. Defaults to 28.
            text (str, optional): text of the button. Defaults to None so its just an icon.
            textvariable (Variable | None, optional): textvariable of the button. Defaults to None.
            state (str, optional): state of the button (if it is clickable). Defaults to "normal".
            hover (bool, optional): hover of the button. Defaults to True.
            corner_radius (int, optional): corner radius of the button. Defaults to None so its taken from the theme.
            command (Callable[[], Any] | None, optional): command of the button. Defaults to None.
            kind (int, optional): kind of the button. Defaults to None = close icon, 0 = trash delete icon.
        """

        # select the icon for the button based on the kind
        image_path = path.join(path.dirname(path.realpath(__file__)), "icons")
        if kind == 0:
            icon = "delete_white.png"
        elif kind == -1:
            icon = None
        else:
            icon = "close_white.png"

        if icon is not None:
            image = CTkImage(Image.open(path.join(image_path, icon)), size=(24, 24))
        else:
            image = None

        super().__init__(
            root,
            width,
            height,
            fg_color="#D64C2C",
            hover_color="#95351F",
            text=text,
            textvariable=textvariable,
            image=image,
            state=state,
            hover=hover,
            corner_radius=corner_radius,
            command=command,
        )


class NeutralButton(CTkButton):
    """
    Custom button for the application to access more information, navigation or other actions.
    The button has a blue color.
    """

    def __init__(
        self,
        root: Any,
        width: int = 140,
        height: int = 28,
        text: str = None,
        textvariable: Variable | None = None,
        state: str = "normal",
        hover: bool = True,
        corner_radius: int = None,
        command: Callable[[], Any] | None = None,
        kind: int = None,
    ):
        """
        Initialization of the custom button for the application  to access more information, navigation or other actions.
        The button has a blue color.

        Args:
            root (Any): root frame for the button
            width (int, optional): width of the button. Defaults to 140.
            height (int, optional): height of the button. Defaults to 28.
            text (str, optional): text of the button. Defaults to None so its just an icon.
            textvariable (Variable | None, optional): textvariable of the button. Defaults to None.
            state (str, optional): state of the button (if it is clickable). Defaults to "normal".
            hover (bool, optional): hover of the button. Defaults to True.
            corner_radius (int, optional): corner radius of the button. Defaults to None so its taken from the theme.
            command (Callable[[], Any] | None, optional): command of the button. Defaults to None.
            kind (int, optional): kind of the button.
            Defaults to None = no icon, 0 = white undo icon, 1 = white redoicon, 2 = white info icon.
        """

        # select the icon for the button based on the kind
        image_path = path.join(path.dirname(path.realpath(__file__)), "icons")
        if kind == 0:
            icon = "undo_w.png"
        elif kind == 1:
            icon = "redo_w.png"
        elif kind == 2:
            icon = "info_white.png"
        else:
            icon = None

        if icon is not None:
            image = CTkImage(Image.open(path.join(image_path, icon)), size=(24, 24))
        else:
            image = None

        super().__init__(
            root,
            width,
            height,
            fg_color="#1D91DA",
            hover_color="#0F73BA",
            text=text,
            textvariable=textvariable,
            image=image,
            state=state,
            hover=hover,
            corner_radius=corner_radius,
            command=command,
        )


class NavigationButtons(CTkFrame):
    """
    Custom frame for two navigation buttons in the application.
    For a consistent look and feel of the application the frame
    should be placed with the following parameters: pady=(0, 20), padx=(25, 25)
    """

    def __init__(
        self, root, objects: int = 2, values: Tuple[str] = None, pos: str = "left"
    ):
        """
        Initialization of the custom frame and the two navigation buttons in the application

        Args:
            root (CTkFrame): root frame for the navigation button frame
            objects (int, optional): number of buttons. Defaults to 2.
            values (Tuple[str], optional): Values / Text of the buttons. Defaults to None.
            pos (str, optional): Variable to determine the position of the first button.
                                 Defaults to left meaning the first button is in the bottom left corner.
        """
        super().__init__(root, fg_color="transparent")
        self.values = values
        self.columnconfigure((0, 1, 2), weight=1)  # make all columns expandable
        if objects >= 1:
            self.btn_1 = CTkButton(
                self,
                text=self.values[0],
                width=130,
                height=30,
                compound="left",
                command=self.btn_1_func,
            )
            if pos == "left":
                self.btn_1.grid(row=0, column=0, sticky="nw", padx=(25,0), pady=(0, 20))
            elif pos == "center":
                self.btn_1.grid(row=0, column=1)
            else:
                self.btn_1.grid(row=0, column=2, sticky="ne", padx=(0,25), pady=(0, 20))
        if objects >= 2:
            self.btn_2 = CTkButton(
                self,
                text=self.values[1],
                width=130,
                height=30,
                command=self.btn_2_func,
            )
            if pos == "left":
                self.btn_2.grid(row=0, column=2, sticky="ne", padx=(0,25), pady=(0, 20))
            else:
                self.btn_2.grid(row=0, column=0, sticky="nw", padx=(25,0), pady=(0, 20))

    @abstractmethod
    def btn_1_func(self):
        pass

    @abstractmethod
    def btn_2_func(self):
        pass


class NavigationBar(CTkLabel):
    """
    Custom label for the navigation bar in the application
    """

    def __init__(
        self,
        root: Any,
        wraplength: int = 0,
        nav_path: str | Tuple[str] = "undefined",
        mode: str = "light",
    ):
        """
        Initialization of the custom label for the navigation bar in the application

        Args:
            root (Any): root frame for the navigation bar
            wraplength (int, optional): wraplength of the navigation bar. Defaults to 0.
            nav_path (str | Tuple[str], optional): navigation path of the frame. Defaults to "undefined".
            mode (str, optional): mode of the navigation bar. Defaults to "light".
        """
        if mode == "light":
            fg_color = "#DCDCDC"
            text_color = "#3D3D3D"
        else:
            fg_color = "#212226"
            text_color = "#D9DADE"

        super().__init__(
            root,
            width=0,
            height=28,
            corner_radius=None,
            fg_color=fg_color,
            text_color=text_color,
            text=nav_path,
            image=None,
            compound="center",
            anchor="center",
            wraplength=wraplength,
        )


class FramedOptionMenu(BasisFrame):
    """
    Custom option menu for the application with a frame around the menu for better visibility.
    """

    def __init__(
        self,
        root,
        values: list,
        default_value: str,
        command: Callable[[str], Any] | None = None,
    ):
        """
        Initialization of the custom option menu for the application with a frame around the menu for better visibility.

        Args:
            root (BasisFrame): root frame for the option menu
            values (list): values of the option menu
            default_variable (str): default value of the option menu and the variable
            command (Callable[[str], Any]): command of the option menu
        """
        self.app = root.app
        if self.app.settings["MODE"] == "light":
            border_color = "#989898"
        elif self.app.settings["MODE"] == "dark":
            border_color = "#565B5E"

        super().__init__(
            app=self.app, root=root, layer=1, border_color=border_color, border_width=1
        )
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.variable = StringVar(value=default_value)
        option_menu = CTkOptionMenu(
            self, values=values, variable=self.variable, command=command
        )
        option_menu.grid(row=0, column=0, sticky="ew", padx=(2), pady=(2))
