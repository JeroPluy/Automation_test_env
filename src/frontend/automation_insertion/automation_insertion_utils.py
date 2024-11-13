from frontend.customWidgets import customWidgets as cW

from customtkinter import CTkLabel, CTkEntry

from backend.database.db_utils import load_integrations


class EntityListFrame(cW.BasisScrollFrame):
    """
    Class to display the list of entities in the automation entity frame
    """

    def __init__(self, app, root, entity_list: list, locked=False, height=200):
        """
        Initialization of the entity list frame

        Args:
            app (customtkinter.CTK): the parent window of the entity list frame
            root (customtkinter.CTK): the root frame of the entity list frame
            entity_list (list): the list of entities to be displayed
            locked (bool): the state of the entity frames in the list
            height (int): the height of the entity list frame
        """
        super().__init__(
            app, root, layer=1, height=height, border=True, scroll_direction="y"
        )

        self.entity_list = entity_list
        integration_list = load_integrations()
        integration_list.sort()

        integration_list.append(app.lang["NEW_INTEGRATION"])

        self.entity_frame_list: list = []

        for entity in self.entity_list:
            entity_name = entity.entity_name
            preselect_type = entity.integration

            self.add_element_frame(row=len(self.entity_frame_list), column=0)
            entity_frame = EntityFrame(
                app=app,
                root=self.element_frame,
                entity_num=len(self.entity_frame_list),
                entity_name=entity_name,
                integration_list=integration_list,
                preselect_type=preselect_type,
                locked=locked,
            )
            self.element_frame.columnconfigure(0, weight=1)
            self.element_frame.rowconfigure(0, weight=1)

            self.entity_frame_list.append(entity_frame)

            entity_frame.grid(
                row=len(self.entity_frame_list),
                column=0,
                sticky="news",
                padx=(5, 5),
                pady=(2, 2),
            )

    def get_entity_integrations(self) -> list:
        """
        Get the list of

        Returns:
            list: the list of entities
        """
        entity_integrations = []

        for entity_frame in self.entity_frame_list:
            entity_integrations.append(entity_frame.get_integration())

        return entity_integrations


class EntityFrame(cW.BasisFrame):
    """
    Class for to display a single entity in the entity list frame
    """

    def __init__(
        self,
        app,
        root,
        entity_num: int,
        entity_name: str,
        integration_list: list,
        preselect_type: str,
        locked: bool,
    ):
        """
        Initialization of the entity frame

        Args:
            app (customtkinter.CTK): the parent window of the entity frame
            root (EntityListFrame): the root frame of the entity frame
            entity_num (int): the number of the entity in the list
            entity_name (str): the name of the entity
            integration_list (list): the list of possible integrations
            preselect_type (str): the preselected integration of the entity
            locked (bool): defines if the entity frame can be deleted
        """

        super().__init__(app=app, root=root, layer=3)

        self.entity_num = entity_num

        self.entity_frame_list = self.root.root.root.entity_frame_list

        self.integration = preselect_type

        self.entity_name_label = CTkLabel(self, text=entity_name)
        # the entity name is expandable with the window size
        self.columnconfigure(0, weight=1)

        self.entity_integration_select = cW.FramedOptionMenu(
            root=self,
            values=integration_list,
            default_value=preselect_type,
            command=self.change_integration,
            state="disabled" if locked else "normal",
        )

        # grid the elements inside the entity frame
        self.entity_name_label.grid(
            row=0, column=0, sticky="w", pady=(8, 8), padx=(10, 0)
        )
        self.entity_integration_select.grid(
            row=0, column=1, sticky="e", pady=(8, 8), padx=(0, 10)
        )

    def change_integration(self, value):
        """
        Function to handle the changing of the integration of an entity

        Args:
            value (str): the value of the dropdown menu
        """

        if value == self.app.lang["NEW_INTEGRATION"]:
            # TODO open mask for creating a new integration and add it to the database
            print("new integration selected")
        else:
            print(
                "Entity "
                + str(self.entity_num)
                + " integration changed  form: "
                + self.entity_frame_list[self.entity_num].integration
                + " to: "
                + value
            )

        self.entity_frame_list[self.entity_num].integration = value

        # TODO realise the integration change in the database and in the automation script
        self.popup_info = cW.PopupWarning(
            app=self.app,
            message="This feature is not implemented yet and your changes will not be saved",
            title="Not implemented",
        )

    def get_integration(self):
        """
        Get the integration of the entity

        Returns:
            dict: the entity information as dictionary {"entity_num": int, "integration": str}
        """
        return {"entity_num": self.entity_num, "integration": self.integration}


class AdditionalInfoListFrame(cW.BasisFrame):
    """
    Class to display a list of additional information in the automation entity frame
    """

    def __init__(
        self,
        app,
        root,
        add_infos,
        scroll_direction="y",
        layer=1,
        broder=True,
        height=200,
    ):
        """
        Initialization of the additional information list frame

        Args:
            app (customtkinter.CTK): the parent window of the additional information list frame
            root (customtkinter.CTK): the root frame of the additional information list frame
            add_infos (list): the list of additional information to be displayed
            scroll_direction (str): the direction of the scroll bar
            layer (int): the layer of the additional information list frame
            broder (bool): the state of the border of the additional information list frame
            height (int): the height of the additional information list frame
        """
        super().__init__(app=app, root=root, layer=layer, height=height)

        self.info_type_label = cW.CTkLabel(self, text=app.lang["INFO_TYPE"], width=260)
        self.info_content_label = cW.CTkLabel(self, text=app.lang["INFO_CONTENT"])

        self.info_list_frame = cW.BasisScrollFrame(
            app, self, layer=layer, scroll_direction=scroll_direction, border=broder
        )
        self.info_list_frame.content_children = []

        for information in add_infos:
            info_type, info, removable = information
            info_frame = self.add_info(removeable=removable)
            info_frame.info_type_entry.insert(0, info_type)
            info_frame.info_content_entry.insert(0, info)

        self.add_info_btn = cW.AcceptButton(
            self,
            text=app.lang["ADD_INFO"],
            kind=2,
            command=self.add_info,
            width=260,
        )

        # grid the content frame elements
        self.info_type_label.grid(
            row=0, column=0, sticky="w", padx=(15, 0), pady=(5, 0)
        )
        self.info_content_label.grid(row=0, column=1, sticky="w", pady=(5, 0))

        self.info_list_frame.grid(
            row=1, column=0, columnspan=2, sticky="news", padx=(2), pady=(0, 10)
        )
        self.add_info_btn.grid(
            row=2, column=0, columnspan=2, sticky="we", padx=(50), pady=(10, 10)
        )

        # make the info list frame inside the content frame resizable
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

    def add_info(self, removeable=True):
        """
        Add a new information frame to the information list

        Args:
            removeable (bool): the state of the delete button of the information frame
        """
        list_frame = self.info_list_frame

        list_frame.add_element_frame(row=len(list_frame.content_children), column=0)
        info_content = InformationFrame(
            app=self.app, root=list_frame.element_frame, removeable=removeable
        )
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

    def get_infos(self) -> list:
        """
        Return all information contained in the information list frame

        Returns:
            list: the list of information as Tuple [(info_type, info_content)]
        """

        additional_infos = []

        for info_frame in self.info_list_frame.content_children:
            additional_infos.append(info_frame.get_information())

        return additional_infos


class InformationFrame(cW.BasisFrame):
    """
    Class to display a single information frame in the additional information list frame
    """

    def __init__(self, app, root, removeable=True):
        """
        Initialization of the information frame with a name label, a content entry and a delete button

        Args:
            app (customtkinter.CTK): the parent window of the information frame
            root (AdditionalInfoListFrame): the root frame of the information frame
            removeable (bool): the state of the delete button of the information frame
        """
        self.main_frame = root.root.root.root

        super().__init__(app=app, root=root, layer=2)

        self.info_type_entry = CTkEntry(self, height=40)
        self.info_content_entry = CTkEntry(self, height=40)

        self.delete_btn = cW.DeleteButton(
            self, height=40, width=10, corner_radius=12, command=self.delete_info
        )

        if removeable is False:
            self.delete_btn.configure(state="disabled")

        # grid the elements
        self.info_type_entry.grid(row=0, column=0, sticky="we", padx=(0, 10))
        self.info_content_entry.grid(row=0, column=1, sticky="we", padx=(0, 5))
        self.delete_btn.grid(row=0, column=2, sticky="e")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def delete_info(self):
        """
        Function for the DeleteBtn to remove the information frame from the information list
        """
        self.main_frame.delete_info(self)

    def get_information(self):
        """
        Returns the information contained in the information frame

        Returns:
            dict: the information as dictionary {"info_type": str, "info_content": str}
        """
        return {
            "info_type": self.info_type_entry.get(),
            "info_content": self.info_content_entry.get(),
        }


def clear_automation_insertion_frames(stack: list):
    """
    Clear the remaining automation insertion frames from the stack if the insertion process is canceled or finished.

    Args:
        stack (list): the stack containing the frames
    """
    stack.pop()
    stack.pop()
