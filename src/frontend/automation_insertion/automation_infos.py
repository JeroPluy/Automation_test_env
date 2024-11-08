from frontend.customWidgets import customWidgets as cW
from frontend.automation_details import automation_details_main as aD

from backend import database as db

from customtkinter import CTkEntry


class AutomationInfosFrame(cW.BasisFrame):
    """
    The frame class displaying the automation information and
    providing the user with the possibility to change them or add new ones
    """

    def __init__(self, app, automation_name, a_id):
        """
        Initialization of the automation information frame

        Args:
            app (customtkinter.CTK): the parent window of the automation information frame
            automation_name (str): the name of the new automation
            a_id (str): the id of the new automation
        """
        super().__init__(app=app, layer=0)

        if app.selected_project is None:
            self.nav_path = automation_name
        else:
            self.nav_path = str(app.selected_project + "/" + automation_name)

        self.nav_bar = cW.NavigationBar(
            self,
            mode=app.settings["MODE"],
            nav_path=self.nav_path,
        )

        self.main_content_frame = cW.BasisFrame(app, self, layer=1)
        # make the content frame resizable depending on the window size
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.info_type_label = cW.CTkLabel(
            self.main_content_frame, text=app.lang["INFO_TYPE"]
        )
        self.info_content_label = cW.CTkLabel(
            self.main_content_frame, text=app.lang["INFO_CONTENT"]
        )

        self.info_list_frame = cW.BasisScrollFrame(
            app, self.main_content_frame, layer=1, scroll_direction="y", border=True
        )
        self.info_list_frame.content_children = []
        # make the info list frame inside the content frame resizable
        self.main_content_frame.columnconfigure(0, weight=1)
        self.main_content_frame.columnconfigure(1, weight=1)
        self.main_content_frame.rowconfigure(1, weight=1)

        # add the project and version info frames to the list as default
        info_frame = self.add_info(removeable=False)
        info_frame.info_type_entry.insert(0, "project")
        if app.selected_project is not None:
            project_str = app.selected_project
        else:
            project_str = ""
        info_frame.info_content_entry.insert(0, project_str)

        info_frame = self.add_info(removeable=False)
        info_frame.info_type_entry.insert(0, "version")
        version_str = app.new_automation.version
        info_frame.info_content_entry.insert(0, version_str)

        self.add_info_btn = cW.AcceptButton(
            self.main_content_frame,
            text=app.lang["ADD_INFO"],
            kind=2,
            command=self.add_info,
            width=260,
        )

        self.nav_btn = Nav_btn(app, self)

        # grid the main elements
        self.nav_bar.grid(row=0, column=0, sticky="we")
        self.main_content_frame.grid(
            row=1, column=0, sticky="news", pady=(15, 10), padx=(25)
        )
        self.nav_btn.grid(row=2, column=0, sticky="we")

        # grid the content frame elements
        self.info_type_label.grid(
            row=0, column=0, sticky="w", padx=(30, 0), pady=(5, 0)
        )
        # TODO: correct the placement of the info_content_label in the frame (it is not aligned with the entry)
        self.info_content_label.grid(row=0, column=1, sticky="w", pady=(5, 0))
        self.info_list_frame.grid(
            row=1, column=0, columnspan=2, sticky="news", pady=(0, 10)
        )
        self.add_info_btn.grid(
            row=2, column=0, columnspan=2, sticky="we", padx=(50), pady=(10, 10)
        )

    def add_info(self, removeable=True):
        """
        Add a new information frame to the information list
        """
        list_frame = self.info_list_frame

        list_frame.add_element_frame(row=len(list_frame.content_children), column=0)
        info_content = InformationFrame(app=self.app, root=list_frame.element_frame, removeable=removeable)
        list_frame.element_frame.columnconfigure(0, weight=1)
        list_frame.element_frame.rowconfigure(0, weight=1)

        info_content.grid(row=0, column=0, sticky="news", padx=(5, 5), pady=(5, 5))

        list_frame.content_children.append(info_content)
        return info_content

    def delete_info(self, info_frame):
        """
        Delete an information frame from the information list

        Args:
            info_frame (InformationFrame): the information frame to be deleted
        """
        list_frame = self.info_list_frame

        info_row = list_frame.content_children.index(info_frame)

        list_frame.delete_content_frame(
            list_frame.content.element_frames[info_row], row=info_row
        )

        list_frame.content_children.remove(info_frame)


class InformationFrame(cW.BasisFrame):
    def __init__(self, app, root, removeable=True):
        self.main_frame = root.root.root.root.root

        super().__init__(app=app, root=root, layer=2)

        self.info_type_entry = CTkEntry(self, height=40)
        self.info_content_entry = CTkEntry(self, height=40)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.delete_btn = cW.DeleteButton(
            self, height=40, width=10, corner_radius=12, command=self.delete_info
        )
        
        if removeable is False:
            self.delete_btn.configure(state="disabled")

        # grid the elements
        self.info_type_entry.grid(row=0, column=0, sticky="we", padx=(0, 10))
        self.info_content_entry.grid(row=0, column=1, sticky="we", padx=(0, 5))
        self.delete_btn.grid(row=0, column=2, sticky="e")

    def delete_info(self):
        self.main_frame.delete_info(self)

    def get_info(self):
        return {
            "info_type": self.info_type_entry.get(),
            "info_content": self.info_content_entry.get(),
        }


class Nav_btn(cW.NavigationButtons):
    def __init__(self, app, root):
        super().__init__(
            root=root,
            objects=1,
            values=[app.lang["FINISH"]],
            pos="center",
            options={"btn_1_type": "accept"},
        )

    def btn_1_func(self):
        infos = []
        for info_frame in self.master.info_list_frame.content_children:
            infos.append(info_frame.get_info())

        db.add_additional_info(
            a_id=self.master.app.new_automation.a_id,
            infos=infos,
        )

        # open the automation details frame for the new automation
        automation = self.master.app.new_automation.config["infos"]
        
        self.master.app.load_new_frame(
            prev_frame=self.master,
            new_frame=aD.AutomationDetailsFrame(
                app=self.master.app,
                a_id=self.master.app.new_automation.a_id,
                automation_name=automation.a_name,
            ),
            returnable=False,
        )

        # reset the new automation object
        self.master.app.new_automation = None
