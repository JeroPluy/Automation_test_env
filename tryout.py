from typing import Any, Tuple
import customtkinter
import appLang
import customWidgets as cW

customtkinter.set_default_color_theme("theme.json")
customtkinter.set_appearance_mode("light")

class customNavigation(cW.NavigationFrame):
    def __init__(self, master, com_backwards, com_forward, objects: int = 2, values: Tuple[str] = ...):
        super().__init__(master, com_backwards, com_forward, objects, values)
        self.version_option = customtkinter.CTkOptionMenu(self, values=appLang.OPTIONS, width=130, height=30, command=self.version_select)
        self.version_option.grid(row=0, column=1, padx=(0,15), sticky="we")

    def version_select(self, choice):
        print("optionmenu dropdown clicked:", str(choice))

        
class AutoamtionInsertionFrame(customtkinter.CTkFrame):
    """_summary_

    Args:
        customtkinter (_type_): _description_
    """
    def __init__(self, master,**kwargs):
        super().__init__(master, fg_color = "transparent",**kwargs)
        self.grid_columnconfigure(0,weight=1)

        self.textbox = customtkinter.CTkTextbox(self, width=330, height=132, font=("Roboto", 16), wrap="none")
        self.textbox.grid(row=0,column=0, sticky="news", rowspan=2, padx=(0,10))

        self.add_btn = cW.acceptButton(self, width=60, height=60, corner_radius=12, kind=1, command=self.textbox_add) 
        self.add_btn.grid(row=0, column=1, sticky="nw", pady=(0,5))

        self.del_btn = cW.deleteButton(self, width=60, height=60, corner_radius=12, kind=0, command=self.textbox_del) 
        self.del_btn.grid(row=1, column=1, sticky="nw", pady=(5,0))
        

    def textbox_del(self):
        self.textbox.delete("0.0", "end")

    def textbox_add(self):
        self.textbox.insert("0.0", " Text ")

    def safe_text(self):
        self.text = self.textbox.get("0.0", "end")  # get text from line 0 character 0 till the end


class AutoamtionAdditon(customtkinter.CTk):
    """_summary_

    Args:
        customtkinter (_type_): _description_
    """
    def __init__(self, title):
        super().__init__()
        self.title("my app")
        self.geometry("600x600")
        self.grid_columnconfigure(0, weight=1)
        self.title = customtkinter.CTkLabel(self, text=title, fg_color="#212226", font=("Roboto", 16), text_color="#D9DADE")
        self.title.grid(row=0, column=0,sticky="ew")

        self.entry = customtkinter.CTkEntry(self, placeholder_text=appLang.NAME[appLang.LANG], font=("Roboto", 16) )
        self.entry.grid(row=1, column=0, sticky="we", padx=50, pady=(10,10))

        self.insertion_frame = AutoamtionInsertionFrame(self)
        self.insertion_frame.grid(row=2, column=0, padx=(50,50),pady=(10,23), sticky="news")

        self.navigaton_frame = customNavigation(self, objects=2, com_backwards=self.backwards, com_forward=self.forwards, values=[appLang.BACK[appLang.LANG], appLang.NEXT[appLang.LANG]])
        self.navigaton_frame.grid(row=3, column=0, padx=(50,50),pady=(0,15), sticky="news")

    def backwards(self):
        print("did nothing")

    def forwards(self):
        print("did nothing")

app = AutoamtionAdditon(appLang.NEWAUTO)
app.mainloop()