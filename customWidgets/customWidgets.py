from abc import abstractmethod
from os import path
from typing import Any, Callable, Tuple

from customtkinter import (CTkButton, CTkFont, CTkFrame, CTkImage, CTkLabel,
                           Variable)
from PIL import Image


class acceptButton(CTkButton):
    def __init__(self, master: Any, width: int = 140, height: int = 28, corner_radius: int | None = None, border_width: int | None = None, border_spacing: int = 2, bg_color: str | Tuple[str] = "transparent", fg_color: str | Tuple[str] | None = "#227F6D", hover_color: str | Tuple[str] | None = "#1D5249", border_color: str | Tuple[str] | None = None, text_color: str | Tuple[str] | None = None, text_color_disabled: str | Tuple[str] | None = None, background_corner_colors: Tuple[str | Tuple[str]] | None = None, round_width_to_even_numbers: bool = True, round_height_to_even_numbers: bool = True, text: str = None, font: Tuple | CTkFont | None = None, textvariable: Variable | None = None, image: CTkImage | Any | None = None, state: str = "normal", hover: bool = True, command: Callable[[], Any] | None = None, compound: str = "left", anchor: str = "center", kind: int = None, **kwargs):
        image_path = path.join(path.dirname(path.realpath(__file__)), "icons")
        if kind == 0 :
            ICON = "import_white.png"
        else:
            ICON = "check_white.png"

        image = CTkImage(Image.open(path.join(image_path, ICON)), size=(24,24))
        
        super().__init__(master, width, height, corner_radius, border_width, border_spacing, bg_color, fg_color, hover_color, border_color, text_color, text_color_disabled, background_corner_colors, round_width_to_even_numbers, round_height_to_even_numbers, text, font, textvariable, image, state, hover, command, compound, anchor, **kwargs)

class deleteButton(CTkButton):
    def __init__(self, master: Any, width: int = 140, height: int = 28, corner_radius: int | None = None, border_width: int | None = None, border_spacing: int = 2, bg_color: str | Tuple[str] = "transparent", fg_color: str | Tuple[str] | None = "#D64C2C", hover_color: str | Tuple[str] | None = "#95351F", border_color: str | Tuple[str] | None = None, text_color: str | Tuple[str] | None = None, text_color_disabled: str | Tuple[str] | None = None, background_corner_colors: Tuple[str | Tuple[str]] | None = None, round_width_to_even_numbers: bool = True, round_height_to_even_numbers: bool = True, text: str = None, font: Tuple | CTkFont | None = None, textvariable: Variable | None = None, image: CTkImage | Any | None = None, state: str = "normal", hover: bool = True, command: Callable[[], Any] | None = None, compound: str = "left", anchor: str = "center", kind: int = None, **kwargs):
        image_path = path.join(path.dirname(path.realpath(__file__)), "icons")
        if kind == 0 :
            ICON = "delete_white.png"

        image = CTkImage(Image.open(path.join(image_path, ICON)), size=(24,24))
        
        super().__init__(master, width, height, corner_radius, border_width, border_spacing, bg_color, fg_color, hover_color, border_color, text_color, text_color_disabled, background_corner_colors, round_width_to_even_numbers, round_height_to_even_numbers, text, font, textvariable, image, state, hover, command, compound, anchor, **kwargs)

class NavigationButtons(CTkFrame):
    """_summary_

    Args:
        customtkinter (_type_): _description_
    """
    def __init__(self, master, objects:int = 2, values: Tuple[str] = None):
        super().__init__(master, fg_color = "transparent")
        self.values = values
        self.grid_columnconfigure((0,1,2),weight=1)
        if (objects >= 1):
            self.back_btn = CTkButton(self, text=self.values[0], width=130, height=30, command=self.nav_back)
            self.back_btn.grid(row=0, column=0, padx=(0,15), sticky="w")
        if (objects >= 2):
            self.next_btn = CTkButton(self, text=self.values[1], width=130, height=30, command=self.nav_forwards)
            self.next_btn.grid(row=0, column=2, padx=(0,0), sticky="e")

    @abstractmethod
    def nav_back():
        pass
    @abstractmethod
    def nav_forwards():
        pass

class NavigationBar(CTkLabel):
        def __init__(self, master: Any, width: int = 0, height: int = 28, corner_radius: int | None = None, bg_color: str | Tuple[str] = "transparent", fg_color = None, text_color = None, text_color_disabled = None, text = None, font: Tuple | CTkFont | None = None, image = None, compound: str = "center", anchor: str = "center", wraplength: int = 0, auto_path: str | Tuple[str] = "undefined", mode:str = "light", **kwargs):
            if mode == "light":
                fg_color = "#DCDCDC"
                text_color = "#3D3D3D"
            else: 
                fg_color = "#212226"
                text_color = "#D9DADE"
            text = auto_path
            super().__init__(master, width, height, corner_radius, bg_color, fg_color, text_color, text_color_disabled, text, font, image, compound, anchor, wraplength, **kwargs)