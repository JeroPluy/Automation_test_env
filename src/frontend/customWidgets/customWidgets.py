from abc import abstractmethod
from os import path
from typing import Any, Callable, Tuple

from customtkinter import (
    CTkButton,
    CTkFont,
    CTkFrame,
    CTkImage,
    CTkLabel,
    Variable,
    CTk,
    set_appearance_mode,
    set_default_color_theme,
)

from frontend.utils import load_language, load_settings, THEME_PATH

from PIL import Image


class BlankWindow(CTk):
    """
        Basic Window for the application

    Args:
        customtkinter (_type_): standard custom tkinter node for a ctk application

    """

    def __init__(self, fg_color: str | Tuple[str] | None = None, **kwargs):
        """
        Initialization of the basic window for the application

        Args:
            fg_color (str | Tuple[str] | None, optional): foreground color of the application. Defaults to None so its taken from the theme.
        """
        super().__init__(fg_color, **kwargs)
        self.title("title of the App")
        self.geometry("600x600")
        self.settings = load_settings()
        self.lang = load_language(self.settings["LANG"])
        set_default_color_theme(THEME_PATH)
        set_appearance_mode(self.settings["mode"])


class acceptButton(CTkButton):
    """
    custom button for the application to accept all the changes to the form

    Args:
        CTkButton (_type_):  standard custom tkinter node for a ctk button
    """

    def __init__(
        self,
        master: Any,
        width: int = 140,
        height: int = 28,
        corner_radius: int | None = None,
        border_width: int | None = None,
        border_spacing: int = 2,
        bg_color: str | Tuple[str] = "transparent",
        fg_color: str | Tuple[str] | None = "#227F6D",
        hover_color: str | Tuple[str] | None = "#1D5249",
        border_color: str | Tuple[str] | None = None,
        text_color: str | Tuple[str] | None = None,
        text_color_disabled: str | Tuple[str] | None = None,
        background_corner_colors: Tuple[str | Tuple[str]] | None = None,
        round_width_to_even_numbers: bool = True,
        round_height_to_even_numbers: bool = True,
        text: str = None,
        font: Tuple | CTkFont | None = None,
        textvariable: Variable | None = None,
        image: CTkImage | Any | None = None,
        state: str = "normal",
        hover: bool = True,
        command: Callable[[], Any] | None = None,
        compound: str = "left",
        anchor: str = "center",
        kind: int = None,
        **kwargs,
    ):
        """
        Initialization of the custom button for the application to accept all the changes to the form

        Args:
            master (Any): master frame for the button
            width (int, optional): width of the button. Defaults to 140.
            height (int, optional): height of the button. Defaults to 28.
            corner_radius (int | None, optional): corner radius of the button. Defaults to None so its taken from the theme. 
            border_width (int | None, optional): border width of the button. Defaults to None so its taken from the theme.
            border_spacing (int, optional): border spacing of the button. Defaults to 2.
            bg_color (str | Tuple[str], optional): background color of the button. Defaults to "transparent".
            fg_color (str | Tuple[str] | None, optional): foreground color of the button. Defaults to "#227F6D". (green) 
            hover_color (str | Tuple[str] | None, optional): hover color of the button. Defaults to "#1D5249". (dark green)
            border_color (str | Tuple[str] | None, optional): border color of the button. Defaults to None so its taken from the theme.
            text_color (str | Tuple[str] | None, optional): text color of the button. Defaults to None so its taken from the theme.
            text_color_disabled (str | Tuple[str] | None, optional): text color of the button when disabled. Defaults to None so its taken from the theme.
            background_corner_colors (Tuple[str  |  Tuple[str]] | None, optional): background corner colors of the button. Defaults to None.
            round_width_to_even_numbers (bool, optional): round width to even numbers of the button. Defaults to True.
            round_height_to_even_numbers (bool, optional): round height to even numbers of the button. Defaults to True.
            text (str, optional): text of the button. Defaults to None so its just an icon.
            font (Tuple | CTkFont | None, optional): font of the button. Defaults to None so its taken from the theme.
            textvariable (Variable | None, optional): textvariable of the button. Defaults to None.
            image (CTkImage | Any | None, optional): image of the button. Defaults to None so its the default white checkmark.
            state (str, optional): state of the button. Defaults to "normal".
            hover (bool, optional): hover of the button. Defaults to True.
            command (Callable[[], Any] | None, optional): command of the button. Defaults to None.
            compound (str, optional): compound of the button. Defaults to "left".
            anchor (str, optional): anchor of the button. Defaults to "center".
            kind (int, optional): kind of the button. Defaults to None so its taken from the theme.
        """
        image_path = path.join(path.dirname(path.realpath(__file__)), "icons")
        if kind == 0:
            ICON = "import_white.png"
        else:
            ICON = "check_white.png"

        image = CTkImage(Image.open(path.join(image_path, ICON)), size=(24, 24))

        super().__init__(
            master,
            width,
            height,
            corner_radius,
            border_width,
            border_spacing,
            bg_color,
            fg_color,
            hover_color,
            border_color,
            text_color,
            text_color_disabled,
            background_corner_colors,
            round_width_to_even_numbers,
            round_height_to_even_numbers,
            text,
            font,
            textvariable,
            image,
            state,
            hover,
            command,
            compound,
            anchor,
            **kwargs,
        )


class deleteButton(CTkButton):
    """
    custom button for the application to delete all the changes to the form

    Args:
        CTkButton (_type_): standard custom tkinter node for a ctk button
    """

    def __init__(
        self,
        master: Any,
        width: int = 140,
        height: int = 28,
        corner_radius: int | None = None,
        border_width: int | None = None,
        border_spacing: int = 2,
        bg_color: str | Tuple[str] = "transparent",
        fg_color: str | Tuple[str] | None = "#D64C2C",
        hover_color: str | Tuple[str] | None = "#95351F",
        border_color: str | Tuple[str] | None = None,
        text_color: str | Tuple[str] | None = None,
        text_color_disabled: str | Tuple[str] | None = None,
        background_corner_colors: Tuple[str | Tuple[str]] | None = None,
        round_width_to_even_numbers: bool = True,
        round_height_to_even_numbers: bool = True,
        text: str = None,
        font: Tuple | CTkFont | None = None,
        textvariable: Variable | None = None,
        image: CTkImage | Any | None = None,
        state: str = "normal",
        hover: bool = True,
        command: Callable[[], Any] | None = None,
        compound: str = "left",
        anchor: str = "center",
        kind: int = None,
        **kwargs,
    ):
        image_path = path.join(path.dirname(path.realpath(__file__)), "icons")
        if kind == 0:
            ICON = "delete_white.png"

        image = CTkImage(Image.open(path.join(image_path, ICON)), size=(24, 24))

        super().__init__(
            master,
            width,
            height,
            corner_radius,
            border_width,
            border_spacing,
            bg_color,
            fg_color,
            hover_color,
            border_color,
            text_color,
            text_color_disabled,
            background_corner_colors,
            round_width_to_even_numbers,
            round_height_to_even_numbers,
            text,
            font,
            textvariable,
            image,
            state,
            hover,
            command,
            compound,
            anchor,
            **kwargs,
        )


class neutralButton(CTkButton):
    """
    custom button for the application to accept all the changes to the form

    Args:
        CTkButton (_type_):  standard custom tkinter node for a ctk button
    """

    def __init__(
        self,
        master: Any,
        width: int = 140,
        height: int = 28,
        corner_radius: int | None = None,
        border_width: int | None = None,
        border_spacing: int = 2,
        bg_color: str | Tuple[str] = "transparent",
        fg_color: str | Tuple[str] | None = "#1D91DA",
        hover_color: str | Tuple[str] | None = "#0F73BA",
        border_color: str | Tuple[str] | None = None,
        text_color: str | Tuple[str] | None = None,
        text_color_disabled: str | Tuple[str] | None = None,
        background_corner_colors: Tuple[str | Tuple[str]] | None = None,
        round_width_to_even_numbers: bool = True,
        round_height_to_even_numbers: bool = True,
        text: str = None,
        font: Tuple | CTkFont | None = None,
        textvariable: Variable | None = None,
        image: CTkImage | Any | None = None,
        state: str = "normal",
        hover: bool = True,
        command: Callable[[], Any] | None = None,
        compound: str = "left",
        anchor: str = "center",
        kind: int = None,
        **kwargs,
    ):
        """
        Initialization of the custom button for the application to accept all the changes to the form

        Args:
            master (Any): master frame for the button
            width (int, optional): width of the button. Defaults to 140.
            height (int, optional): height of the button. Defaults to 28.
            corner_radius (int | None, optional): corner radius of the button. Defaults to None so its taken from the theme. 
            border_width (int | None, optional): border width of the button. Defaults to None so its taken from the theme.
            border_spacing (int, optional): border spacing of the button. Defaults to 2.
            bg_color (str | Tuple[str], optional): background color of the button. Defaults to "transparent".
            fg_color (str | Tuple[str] | None, optional): foreground color of the button. Defaults to "#227F6D". (green) 
            hover_color (str | Tuple[str] | None, optional): hover color of the button. Defaults to "#1D5249". (dark green)
            border_color (str | Tuple[str] | None, optional): border color of the button. Defaults to None so its taken from the theme.
            text_color (str | Tuple[str] | None, optional): text color of the button. Defaults to None so its taken from the theme.
            text_color_disabled (str | Tuple[str] | None, optional): text color of the button when disabled. Defaults to None so its taken from the theme.
            background_corner_colors (Tuple[str  |  Tuple[str]] | None, optional): background corner colors of the button. Defaults to None.
            round_width_to_even_numbers (bool, optional): round width to even numbers of the button. Defaults to True.
            round_height_to_even_numbers (bool, optional): round height to even numbers of the button. Defaults to True.
            text (str, optional): text of the button. Defaults to None so its just an icon.
            font (Tuple | CTkFont | None, optional): font of the button. Defaults to None so its taken from the theme.
            textvariable (Variable | None, optional): textvariable of the button. Defaults to None.
            image (CTkImage | Any | None, optional): image of the button. Defaults to None so its the default white checkmark.
            state (str, optional): state of the button. Defaults to "normal".
            hover (bool, optional): hover of the button. Defaults to True.
            command (Callable[[], Any] | None, optional): command of the button. Defaults to None.
            compound (str, optional): compound of the button. Defaults to "left".
            anchor (str, optional): anchor of the button. Defaults to "center".
            kind (int, optional): kind of the button. Defaults to None so its taken from the theme.
        """
        image_path = path.join(path.dirname(path.realpath(__file__)), "icons")
        if kind == 0:
            ICON = "undo_w.png"
        else:
            ICON = "check_white.png"

        image = CTkImage(Image.open(path.join(image_path, ICON)), size=(24, 24))

        super().__init__(
            master,
            width,
            height,
            corner_radius,
            border_width,
            border_spacing,
            bg_color,
            fg_color,
            hover_color,
            border_color,
            text_color,
            text_color_disabled,
            background_corner_colors,
            round_width_to_even_numbers,
            round_height_to_even_numbers,
            text,
            font,
            textvariable,
            image,
            state,
            hover,
            command,
            compound,
            anchor,
            **kwargs,
        )    

class NavigationButtons(CTkFrame):
    """
    custom frame for the navigation buttons in the application

    Args:
        CTkFrame (_type_): standard custom tkinter node for a ctk frame
    """

    def __init__(self, master, objects: int = 2, values: Tuple[str] = None):
        super().__init__(master, fg_color="transparent")
        self.values = values
        self.grid_columnconfigure((0, 1, 2), weight=1)
        if objects >= 1:
            self.back_btn = CTkButton(
                self, text=self.values[0], width=130, height=30, command=self.nav_back
            )
            self.back_btn.grid(row=0, column=0, padx=(0, 15), sticky="w")
        if objects >= 2:
            self.next_btn = CTkButton(
                self,
                text=self.values[1],
                width=130,
                height=30,
                command=self.nav_forwards,
            )
            self.next_btn.grid(row=0, column=2, padx=(0, 0), sticky="e")

    @abstractmethod
    def nav_back(self):
        pass

    @abstractmethod
    def nav_forwards(self):
        pass


class NavigationBar(CTkLabel):
    """
    custom label for the navigation bar in the application

    Args:
        CTkLabel (_type_): standard custom tkinter node for a ctk label
    """

    def __init__(
        self,
        master: Any,
        width: int = 0,
        height: int = 28,
        corner_radius: int | None = None,
        bg_color: str | Tuple[str] = "transparent",
        fg_color=None,
        text_color=None,
        text_color_disabled=None,
        text=None,
        font: Tuple | CTkFont | None = None,
        image=None,
        compound: str = "center",
        anchor: str = "center",
        wraplength: int = 0,
        auto_path: str | Tuple[str] = "undefined",
        mode: str = "light",
        **kwargs,
    ):
        """
        Initialization of the custom label for the navigation bar in the application

        Args:
            master (Any): master frame for the navigation bar
            width (int, optional): width of the navigation bar. Defaults to 0.
            height (int, optional): height of the navigation bar. Defaults to 28.
            corner_radius (int | None, optional): corner radius of the navigation bar. Defaults to None.
            bg_color (str | Tuple[str], optional): background color of the navigation bar. Defaults to "transparent".
            fg_color (_type_, optional): foreground color of the navigation bar. Defaults to None.
            text_color (_type_, optional): text color of the navigation bar. Defaults to None.
            text_color_disabled (_type_, optional): text color of the navigation bar when disabled. Defaults to None.
            text (_type_, optional): text of the navigation bar. Defaults to None.
            font (Tuple | CTkFont | None, optional): font of the navigation bar. Defaults to None.
            image (_type_, optional): image of the navigation bar. Defaults to None.
            compound (str, optional): compound of the navigation bar. Defaults to "center".
            anchor (str, optional): anchor of the navigation bar. Defaults to "center".
            wraplength (int, optional): wraplength of the navigation bar. Defaults to 0.
            auto_path (str | Tuple[str], optional): path to the image of the navigation bar. Defaults to "undefined".
            mode (str, optional): mode of the navigation bar. Defaults to "light".
        """
        if mode == "light":
            fg_color = "#DCDCDC"
            text_color = "#3D3D3D"
        else:
            fg_color = "#212226"
            text_color = "#D9DADE"
        text = auto_path
        super().__init__(
            master,
            width,
            height,
            corner_radius,
            bg_color,
            fg_color,
            text_color,
            text_color_disabled,
            text,
            font,
            image,
            compound,
            anchor,
            wraplength,
            **kwargs,
        )
