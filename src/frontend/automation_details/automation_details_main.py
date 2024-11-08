from ..customWidgets import customWidgets as cW

from tkinter import StringVar
from customtkinter import CTkLabel, CTkCheckBox, CTkEntry

from backend.database import db_utils


class AutomationDetailsFrame(cW.BasisFrame):
    def __init__(self, app, a_id, automation_name):
        super().__init__(app=app, layer=0)

        self.automation = db_utils.get_automation_data(a_id)

        self.nav_bar = cW.NavigationBar(
            self, mode=app.settings["MODE"], nav_path=automation_name
        )

        self.main_frame = cW.BasisScrollFrame(app, self, scroll_direction="y", layer=0)

        self.nav_btns = NavBtns(self, values=(app.lang["DISCARD"], app.lang["SAVE"]))

        # add the menu btns to the main frame
        self.main_frame.add_element_frame(row=0, column=0, layer=0)
        self.main_frame.element_frame.columnconfigure(0, weight=1)

        self.menu_btns_frame = MenuBtns(app, self.main_frame.element_frame)

        # add the main content frame to the main frame
        self.main_frame.add_element_frame(row=1, column=0, layer=1)
        self.main_frame.element_frame.columnconfigure(0, weight=1)

        self.main_content_frame = cW.BasisFrame(
            app, self.main_frame.element_frame, layer=1
        )

        self.info_labels = InfoLabels(
            app=app, root=self.main_content_frame, automation=self.automation
        )

        # grid the main elements
        self.nav_bar.grid(row=0, column=0, sticky="ew")
        self.main_frame.grid(row=1, column=0, sticky="news", pady=(0, 10), padx=(0))
        self.nav_btns.grid(row=2, column=0, sticky="ew")

        self.columnconfigure(0, weight=1)
        # make the content frame resizable depending on the window size
        self.rowconfigure(1, weight=1)

        # grid the main frame elements
        self.menu_btns_frame.grid(row=0, column=0, sticky="news")
        self.main_content_frame.grid(
            row=1, column=0, sticky="news", padx=(0), pady=(15, 0)
        )

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)

        # grid the main content frame elements
        self.info_labels.grid(row=0, column=0, sticky="news", padx=(15), pady=(0, 15))

        self.main_content_frame.columnconfigure(0, weight=1)


class MenuBtns(cW.BasisFrame):
    def __init__(self, app, root):
        super().__init__(app, root, layer=0)

        self.test_case_coll_btn = cW.NeutralButton(
            self,
            text=app.lang["TEST_CASE_COLLECTION"],
            width=350,
            height=40,
            command=self.open_test_case_coll,
        )

        self.test_results_btn = cW.NeutralButton(
            self,
            text=app.lang["TEST_RESULTS"],
            width=350,
            height=40,
            command=self.open_test_results,
        )

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.test_case_coll_btn.grid(row=0, column=0, sticky="w", padx=(15, 5))
        self.test_results_btn.grid(row=0, column=1, sticky="e", padx=(5, 15))

    def open_test_case_coll(self):
        # TODO open the test case collection
        print("Open test case collection")

    def open_test_results(self):
        # TODO open the test results
        print("Open test results")


class InfoLabels(cW.BasisFrame):
    def __init__(self, app, root, automation):
        super().__init__(app, root, layer=1)

        locked_state = "disabled" if automation.error is not None else "normal"

        # created frame
        self.created_frame = cW.BasisFrame(app, self, layer=2)

        self.created_label = CTkLabel(
            master=self.created_frame,
            text=app.lang["CREATED"] + ":",
            width=100,
            anchor="w",
        )

        self.created_date = CTkLabel(
            master=self.created_frame,
            text=automation.created,
        )

        # automation mode frame
        self.a_mode_frame = cW.BasisFrame(app, self, layer=2)

        self.a_mode_label = CTkLabel(
            master=self.a_mode_frame,
            text=app.lang["AUTOMATION_MODE"] + ":",
            width=100,
            anchor="w",
        )

        autom_mode = automation.autom_mode

        if autom_mode == 0:
            autom_mode_str = app.lang["SINGLE"]
        elif autom_mode == 1:
            autom_mode_str = app.lang["RESTART"]
        elif autom_mode == 2:
            autom_mode_str = app.lang["QUEUED"]
        elif autom_mode == 3:
            autom_mode_str = app.lang["PARALLEL"]

        self.a_mode_dropdown = cW.FramedOptionMenu(
            root=self.a_mode_frame,
            values=[
                app.lang["SINGLE"],
                app.lang["RESTART"],
                app.lang["QUEUED"],
                app.lang["PARALLEL"],
            ],
            default_value=autom_mode_str,
            state=locked_state,
        )

        # error frame
        # TODO better coloring and theme mode handling
        if automation.error == 1:
            error_color = "red"
        elif automation.error == 0:
            error_color = "green"
        else:
            error_color = "#FCFCFC"

        self.error_frame = cW.BasisFrame(app, self, layer=-1, fg_color=error_color)
        self.error_frame.configure("rounded_corners=6")

        self.error_label = CTkLabel(
            master=self.error_frame,
            text=app.lang["ERROR_DETECT"] + ":",
            width=100,
        )

        # TODO change Checkbox to a framed icon with ❌, ✔️ and ❓
        self.error_checkbox = CTkCheckBox(
            master=self.error_frame,
            text="",
            variable=automation.error,
            state="disabled",  # should not be changed
        )

        self.max_inst_frame = cW.BasisFrame(app, self, layer=2)

        self.max_instances_label = CTkLabel(
            master=self.max_inst_frame,
            text=app.lang["MAX_INSTANCES"] + ":",
            width=100,
        )

        max_inst_value_str = StringVar(value=automation.max_instances)

        # TODO gray out the entry field if the state is locked
        self.max_instances_value = CTkEntry(
            master=self.max_inst_frame,
            textvariable=max_inst_value_str,
            state=locked_state,
            width=50,
            justify="right",
        )

        # grid the label frames
        self.created_frame.grid(row=0, column=0, sticky="we", padx=(0, 5), pady=(0, 5))
        self.a_mode_frame.grid(row=0, column=1, sticky="we", padx=(5, 0), pady=(0, 5))
        self.error_frame.grid(row=1, column=0, sticky="we", padx=(0, 5), pady=(5))
        self.max_inst_frame.grid(row=1, column=1, sticky="we", padx=(5, 0), pady=(5))

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # grid the created elements
        self.created_label.grid(row=0, column=0, sticky="w", pady=(2, 2), padx=(10, 0))
        self.created_date.grid(row=0, column=1, sticky="e", pady=(2, 2), padx=(0, 5))
        self.created_frame.columnconfigure(1, weight=1)

        # grid the error elements
        self.error_label.grid(row=0, column=0, sticky="w", pady=(2, 2), padx=(10, 0))
        self.error_checkbox.grid(row=0, column=1, sticky="e", pady=(2, 2), padx=(0, 5))
        self.error_frame.columnconfigure(1, weight=1)

        # grid the automation mode elements
        self.a_mode_label.grid(row=0, column=0, sticky="w", pady=(2, 2), padx=(10, 0))
        self.a_mode_dropdown.grid(row=0, column=1, sticky="e", pady=(2, 2), padx=(0, 5))
        self.a_mode_frame.columnconfigure(1, weight=1)

        # grid the max instances elements
        self.max_instances_label.grid(
            row=0, column=0, sticky="w", pady=(2, 2), padx=(10, 0)
        )
        self.max_instances_value.grid(
            row=0, column=1, sticky="e", pady=(2, 2), padx=(0, 5)
        )
        self.max_inst_frame.columnconfigure(1, weight=1)


class NavBtns(cW.NavigationButtons):
    def __init__(
        self, root, values, options={"btn_1_type": "delete", "btn_2_type": "accept"}
    ):
        self.root = root
        super().__init__(root=root, values=values, options=options)

    def btn_1_func(self):
        self.root.app.go_back(self.root)

    def btn_2_func(self):
        # TODO save the automation changes
        self.btn_1_func()
