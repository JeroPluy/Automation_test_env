from backend.database import db_utils
from frontend.customWidgets import customWidgets as cW

from customtkinter import CTkCheckBox, CTkEntry, CTkLabel

from itertools import product

from datetime import datetime, timedelta


class RangeValueFrame(cW.BasisFrame):
    """
    Frame to display the range value creation
    """

    def __init__(self, app, entity_id, entity_name, nav_path, possible_values):
        """
        Initialize the frame

        Args:
            app (test_environment_app.AppWindow): the main application
            root (cW.BasisFrame): the parent frame
            entity_id (int): the
        """
        super().__init__(app=app)

        self.app = app

        self.entity_id = entity_id

        self.nav_bar = cW.NavigationBar(self, nav_path=nav_path + "/" + entity_name)

        self.value_entries_frame = PosValListFrame(
            app=app, root=self, possible_values=possible_values
        )

        self.nav_btns = NavBtns(app=self.app, root=self)

        # --- grid the elements ---

        self.nav_bar.grid(row=0, column=0, sticky="we")

        self.value_entries_frame.grid(row=1, column=0, sticky="news", padx=15, pady=10)

        self.nav_btns.grid(row=2, column=0, sticky="we")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)


class PosValListFrame(cW.BasisScrollFrame):
    """
    Subframe to display each possible value
    """

    def __init__(self, app, root, possible_values):
        """
        Initialize the frame

        Args:
            app (test_environment_app.AppWindow): the main application
            root (cW.BasisFrame): the parent frame
            possible_values (list): the possible values for the range
        """
        super().__init__(app=app, root=root, layer=1, scroll_direction="y")

        self.app = app

        self.pos_val_frame_list = []

        self.row_counter = 0

        for value in possible_values + [self.app.lang["ALL_POS"]]:
            self.add_element_frame(row=self.row_counter, layer=2)

            pos_val_frame = PossibleValueFrame(
                app=app, root=self.element_frame, value=value
            )
            self.pos_val_frame_list.append(pos_val_frame)

            # grid the frame with the possible value

            pos_val_frame.grid(
                row=len(self.pos_val_frame_list),
                column=0,
                sticky="we",
                pady=(2, 0),
                padx=5,
            )

            self.element_frame.columnconfigure(0, weight=1)
            self.element_frame.rowconfigure(0, weight=1)

            self.row_counter += 1

    def get_all_values(self) -> list | None:
        """
        Function to get all the values from the entry fields

        Returns:
            list: the list of all the values
        """
        return_list = []

        for frame in self.pos_val_frame_list:
            try:
                val = frame.get()
            except ValueError as e:
                print(e)
                return None
            if val is not None:
                if not isinstance(val, list):
                    return_list.append(val)
                else:
                    return_list.extend(val)

        return return_list

    def select_all(self):
        """
        Function to select all possible values
        """
        for frame in self.pos_val_frame_list:
            if hasattr(frame, "checkbox"):
                frame.checkbox.select()

    def deselect_all(self):
        """
        Function to deselect all possible values
        """
        for frame in self.pos_val_frame_list:
            if hasattr(frame, "checkbox"):
                frame.checkbox.deselect()


class PossibleValueFrame(cW.BasisFrame):
    """
    Subframe to display the entry or checkbox field for one possible value
    """

    def __init__(self, app, root, value):
        """
        Initialize the frame for the possible value

        Args:
            app (test_environment_app.AppWindow): the main application
            root (cW.BasisFrame): the parent frame
            value (str): the value to be displayed which can be selected
        """

        super().__init__(app=app, root=root, layer=2)

        self.value = value

        # --- first column of the frame ---
        self.value_label = CTkLabel(self, text=value, width=150, anchor="w")

        # grid the label because it is always needed

        self.value_label.grid(row=0, column=0, sticky="w", pady=2, padx=5)

        # -- second column of the frame ---
        # differentiating between the value type and the value frames
        self.value_type_frame = False
        self.range_frame_needed = False

        # build the entry field/s or checkbox depending on the value type
        if value != "bool" and value in db_utils.specification_p_values:
            self.value_type_frame = True

            if value in ["int", "float", "datetime"] or value.startswith("tuple"):
                # create three entry fields for the start, end and step value

                self.range_frame_needed = True

                if value.startswith("tuple"):
                    # handle the tuple values
                    tuple_vals: list = (
                        value.replace("tuple[", "").replace("]", "").split(",")
                    )

                else:
                    tuple_vals = None

                self.range_frame = RangeFrame(app, self, tuple_vals=tuple_vals)

                # grid the range frame

                self.range_frame.grid(
                    row=0, column=1, sticky="news", pady=(5, 5), padx=(5, 3)
                )

            else:
                # create one entry field for the value type
                self.entry = CTkEntry(self)

                # grid the entry field

                self.entry.grid(row=0, column=1, sticky="news", pady=5, padx=(5, 3))

            self.columnconfigure(1, weight=1)
            self.rowconfigure(0, weight=1)

            # create a button to add more possible values frames with the same value type
            self.add_more_btn = cW.AcceptButton(
                root=self,
                width=40,
                height=40,
                kind=2,
                command=self.add_more,
                corner_radius=8,
            )

            # grid the button to add more possible values frames
            self.add_more_btn.grid(row=0, column=2, pady=4, padx=4)

        elif value == self.app.lang["ALL_POS"]:
            # create a checkbox to select / deselect all possible value checkboxes
            list_frame = self.root.root.root

            self.check_all = CTkCheckBox(
                self,
                text="",
                command=lambda: list_frame.select_all()
                if self.check_all.get() == 1
                else list_frame.deselect_all(),
            )
            self.check_all.grid(row=0, column=1, sticky="news", pady=2, padx=5)

            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)

        else:
            # create a checkbox for the possible value beeing included in the list or not
            self.checkbox = CTkCheckBox(self, text="")

            # grid the checkbox
            self.checkbox.grid(row=0, column=1, sticky="news", pady=2, padx=5)

            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)

    def get(self):
        """
        Function to get the value from the frame depending on the value type and if something is entered

        Returns:
            list | string | bool : the value from the entry field
        """
        if self.range_frame_needed:
            try:
                if "float" in self.value:
                    return self.range_frame.get_float_range()
                elif self.value == "datetime":
                    return self.range_frame.get_datetime_range()
                else:
                    return self.range_frame.get_int_range()
            except ValueError as e:
                raise ValueError("Invalid range format. " + str(e))
        elif self.value_type_frame:
            if self.value == "list[string]":
                str_list = self.entry.get().split(",")
                return (
                    [[val.strip() for val in str_list]]
                    if self.entry.get() != ""
                    else None
                )
            else:
                return self.entry.get() if self.entry.get() != "" else None
        else:
            if self.value == "bool":
                # TODO check if the checkbox is checked or unchecked or not interacted with (change to OptionMenu mybe)
                return True if self.checkbox.get() == 1 else False
            elif self.value == self.app.lang["ALL_POS"]:
                return None
            else:
                return (
                    self.value_label.cget("text") if self.checkbox.get() == 1 else None
                )

    def add_more(self):
        """
        Function to one more PossibleValueFrame to the PosValListFrame with the same value type
        """

        list_frame = self.root.root.root

        list_frame.add_element_frame(row=list_frame.row_counter, layer=2)

        poss_val_frame = PossibleValueFrame(
            self.app, list_frame.element_frame, self.value
        )
        list_frame.pos_val_frame_list.append(poss_val_frame)

        # grid the new created frame with the possible value

        poss_val_frame.grid(
            row=list_frame.row_counter, column=0, sticky="we", pady=(2, 0), padx=5
        )

        list_frame.element_frame.columnconfigure(0, weight=1)
        list_frame.element_frame.rowconfigure(0, weight=1)

        list_frame.row_counter += 1


class RangeFrame(cW.BasisFrame):
    """
    Subframe to set range values for int, float, tuple and datetime values
    """

    def __init__(self, app, root, tuple_vals):
        """
        Initialize the frame for the range of the specification values

        Args:
            app (test_environment_app.AppWindow): the main application
            root (cW.BasisFrame): the parent frame
            tuple_vals (list): list of value types in the tuple
        """
        super().__init__(app=app, root=root, layer=2)

        self.list_frame = self.root.root.root.root

        self.start_label = CTkLabel(self, text=app.lang["START_VAL"] + ":")
        self.end_label = CTkLabel(self, text=app.lang["END_VAL"] + ":")
        self.step_label = CTkLabel(self, text=app.lang["STEP_SIZE"] + ":")

        # add the entry fields for the start, end and step value depending on the kind
        if tuple_vals is None:
            self.start_val = CTkEntry(self)
            self.end_val = CTkEntry(self)
            self.step_val = CTkEntry(self)
        else:
            self.entry_range_list = []

            row_pos = 1

            for type in tuple_vals:
                start_entry = CTkEntry(self)
                end_entry = CTkEntry(self)
                step_entry = CTkEntry(self)
                self.entry_range_list.append([start_entry, end_entry, step_entry])

                # grid the entry fields below the labels
                start_entry.grid(
                    row=row_pos, column=0, pady=(2, 0), padx=(0, 5), sticky="we"
                )
                end_entry.grid(
                    row=row_pos, column=1, pady=(2, 0), padx=(0, 5), sticky="we"
                )
                step_entry.grid(row=row_pos, column=2, pady=(2, 0), sticky="we")

                row_pos += 1

        # --- grid the elements ---

        # grid the declaration labels
        self.start_label.grid(row=0, column=0)
        self.end_label.grid(row=0, column=1)
        self.step_label.grid(row=0, column=2)

        if tuple_vals is None:
            # grid the entry fields below the labels
            self.start_val.grid(row=1, column=0, pady=(2, 0), padx=(0, 5), sticky="we")
            self.end_val.grid(row=1, column=1, pady=(2, 0), padx=(0, 5), sticky="we")
            self.step_val.grid(row=1, column=2, pady=(2, 0), sticky="we")

        self.columnconfigure((0, 1, 2), weight=1)
        self.rowconfigure(0, weight=1)

    def get_int_range(self) -> list:
        """
        Function to get the range values from the entry fields if the value type is int

        Returns:
            list: all values in the range from the start entry to the end entry with the step size
        """

        def _parse_str_to_int(value: str) -> int:
            """
            Function to parse the input string to an integer value

            Args:
                value (str): the string to be parsed

            Returns:
                int: the integer value
            """

            if value == "":
                return None
            else:
                try:
                    return int(value)
                except ValueError:
                    self.list_frame.warning_popup = cW.PopupWarning(
                        app=self.app,
                        title=self.app.lang["WARNING"],
                        message=value + ": " + self.app.lang["INVALID_INT_FORMAT"],
                    )
                    raise ValueError(self.app.lang["INVALID_INT_FORMAT"])

        range_vals = []

        if not hasattr(self, "entry_range_list"):
            # handle the case that some entry fields are empty or wrong input
            try:
                start_val = _parse_str_to_int(self.start_val.get())
                end_val = _parse_str_to_int(self.end_val.get())
                step_val = _parse_str_to_int(self.step_val.get())
            except ValueError:
                raise ValueError(self.app.lang["INVALID_INT_FORMAT"])

            if start_val is None:
                return None
            elif end_val is None or end_val <= start_val:
                return [start_val]
            elif step_val is None:
                self.step_val.delete(0, "end")
                self.step_val.insert(0, 1)
                step_val = 1
            elif step_val <= 0:
                self.list_frame.warning_popup = cW.PopupWarning(
                    app=self.app,
                    title=self.app.lang["WARNING"],
                    message=self.app.lang["INVALID_STEP_SIZE"],
                )
                raise ValueError(self.app.lang["INVALID_STEP_SIZE"])

            # create a list of all values in the range
            for i in range(start_val, end_val, step_val):
                range_vals.append(i)
        else:
            # create a list of all values in the range for each row of entry fields
            range_lists = []

            for entry_range in self.entry_range_list:
                every_possible_value = []

                # handle the case that some entry fields are empty or wrong input
                try:
                    start_val = _parse_str_to_int(entry_range[0].get())
                    end_val = _parse_str_to_int(entry_range[1].get())
                    step_val = _parse_str_to_int(entry_range[2].get())
                except ValueError:
                    return None

                if start_val is None:
                    return None
                elif end_val is None or end_val <= start_val:
                    range_lists.append(start_val)
                    continue
                elif step_val is None:
                    entry_range[2].delete(0, "end")
                    entry_range[2].insert(0, 1)
                    step_val = 1
                elif step_val <= 0:
                    self.list_frame.warning_popup = cW.PopupWarning(
                        app=self.app,
                        title=self.app.lang["WARNING"],
                        message=self.app.lang["INVALID_STEP_SIZE"],
                    )
                    raise ValueError(self.app.lang["INVALID_STEP_SIZE"])

                for i in range(start_val, end_val, step_val):
                    every_possible_value.append(i)

                range_lists.append(every_possible_value)

            range_vals = list(product(*range_lists))

        return range_vals

    def get_float_range(self) -> list:
        """
        Function to get the range values from the entry fields if the value type is float

        Returns:
            list: all values in the range from the start entry to the end entry with the step size
        """

        def _parse_str_to_float(value: str) -> float:
            """
            Function to parse the input string to a float value

            Args:
                value (str): the string to be parsed

            Returns:
                float: the float value
            """

            if value == "":
                return None
            else:
                try:
                    return float(value)
                except ValueError:
                    self.list_frame.warning_popup = cW.PopupWarning(
                        app=self.app,
                        title=self.app.lang["WARNING"],
                        message=value + ": " + self.app.lang["INVALID_FLOAT_FORMAT"],
                    )
                    raise ValueError(self.app.lang["INVALID_FLOAT_FORMAT"])

        def _frange(start, stop, step):
            """
            Generate a range of floating-point values between start and stop with a given step size.
            The addition of the step value is rounded to two decimal places to avoid floating-point errors.

            Args:
                start (float): The starting value of the range.
                stop (float): The end value of the range (not included).
                step (float): The step value between each range value.

            Yields:
                float: The next value in the range.
            """
            while start < stop:
                yield start
                start = round(start + step, 2)

        range_vals = []

        if not hasattr(self, "entry_range_list"):
            # handle the case that some entry fields are empty or wrong input
            try:
                start_val = _parse_str_to_float(self.start_val.get())
                end_val = _parse_str_to_float(self.end_val.get())
                step_val = _parse_str_to_float(self.step_val.get())
            except ValueError:
                raise ValueError(self.app.lang["INVALID_INT_FORMAT"])

            if start_val is None:
                return None
            elif end_val is None or end_val <= start_val:
                return [start_val]
            elif step_val is None:
                self.step_val.delete(0, "end")
                self.step_val.insert(0, 1.0)
                step_val = 1.0
            elif step_val <= 0:
                self.list_frame.warning_popup = cW.PopupWarning(
                    app=self.app,
                    title=self.app.lang["WARNING"],
                    message=self.app.lang["INVALID_STEP_SIZE"],
                )
                raise ValueError(self.app.lang["INVALID_STEP_SIZE"])

            for i in _frange(start_val, end_val, step_val):
                range_vals.append(round(i, 2))
        else:
            # create a list of all values in the range for each row of entry fields
            range_lists = []

            for entry_range in self.entry_range_list:
                every_possible_value = []

                # handle the case that some entry fields are empty or wrong input
                try:
                    start_val = _parse_str_to_float(entry_range[0].get())
                    end_val = _parse_str_to_float(entry_range[1].get())
                    step_val = _parse_str_to_float(entry_range[2].get())
                except ValueError:
                    return None

                if start_val is None:
                    return None
                elif end_val is None or end_val <= start_val:
                    range_lists.append([start_val])
                    continue
                elif step_val is None:
                    entry_range[2].delete(0, "end")
                    entry_range[2].insert(0, 1.0)
                    step_val = 1.0
                elif step_val <= 0:
                    self.list_frame.warning_popup = cW.PopupWarning(
                        app=self.app,
                        title=self.app.lang["WARNING"],
                        message=self.app.lang["INVALID_STEP_SIZE"],
                    )
                    raise ValueError(self.app.lang["INVALID_STEP_SIZE"])

                for i in _frange(start_val, end_val, step_val):
                    every_possible_value.append(round(i, 2))

                range_lists.append(every_possible_value)

            range_vals = list(product(*range_lists))

        return range_vals

    def get_datetime_range(self) -> list:
        """
        Function to get the range values from the entry fields if the value type is datetime

        Returns:
            list: all values in the range from the start entry to the end entry with the step size
        """

        # Define the allowed datetime formats
        DATE_FORMAT = "%d.%m.%Y"
        TIME_FORMAT = "%H:%M:%S"
        DATE_TIME_FORMAT = f"{DATE_FORMAT} {TIME_FORMAT}"

        def _parse_datetime_input(value: str) -> tuple:
            """
            Function to parse the input string to a datetime value

            Args:
                value (str): the string to be parsed

            Returns:
                datetime: the datetime value
            """
            for format in [DATE_TIME_FORMAT, DATE_FORMAT, TIME_FORMAT]:
                try:
                    return (datetime.strptime(value, format), format)
                except ValueError:
                    continue

            if value == "":
                return None, None
            else:
                self.list_frame.warning_popup = cW.PopupWarning(
                    app=self.app,
                    title=self.app.lang["WARNING"],
                    message=value + ": " + self.app.lang["INVALID_DATETIME_FORMAT"],
                )
                raise ValueError(self.app.lang["INVALID_DATETIME_FORMAT"])

        # handle the case that some entry fields are empty or wrong input
        start_dt, start_dt_format = _parse_datetime_input(self.start_val.get())
        end_dt, end_dt_format = _parse_datetime_input(self.end_val.get())

        if start_dt is None:
            return None
        elif end_dt is None or end_dt <= start_dt:
            # TODO DEBUG remove the visualization of the datetime format because it is not needed
            return [start_dt.strftime(start_dt_format)]

        step = self.step_val.get()

        if step == "":
            self.step_val.delete(0, "end")
            self.step_val.insert(0, "1 hour")
            step_size = timedelta(hours=1)
        else:
            step_size_val = step.split()[0]
            try:
                step_size_val = int(step_size_val)
            except ValueError:
                try:
                    step_size_val = float(step_size_val)
                except ValueError:
                    self.list_frame.warning_popup = cW.PopupWarning(
                        app=self.app,
                        title=self.app.lang["WARNING"],
                        message=step + ": " + self.app.lang["INVALID_DT_STEP_SIZE"],
                    )
                    raise ValueError(self.app.lang["INVALID_DT_STEP_SIZE"])

            if step_size_val <= 0:
                self.list_frame.warning_popup = cW.PopupWarning(
                    app=self.app,
                    title=self.app.lang["WARNING"],
                    message=step + ": " + self.app.lang["INVALID_DT_STEP_SIZE"],
                )
                raise ValueError(self.app.lang["INVALID_DT_STEP_SIZE"])

            # Determine the step size unit
            if self.app.lang["DAY"] in step:
                step_size = timedelta(days=step_size_val)
            elif self.app.lang["HOUR"] in step:
                step_size = timedelta(hours=step_size_val)
            elif self.app.lang["MINUTE"] in step:
                step_size = timedelta(minutes=step_size_val)
            elif self.app.lang["SECOND"] in step:
                step_size = timedelta(seconds=step_size_val)
            else:
                self.list_frame.warning_popup = cW.PopupWarning(
                    app=self.app,
                    title=self.app.lang["WARNING"],
                    message=step + ": " + self.app.lang["INVALID_DT_STEP_SIZE"],
                )
                raise ValueError(self.app.lang["INVALID_DT_STEP_SIZE"])

        # Generate the range of datetime values
        range_vals = []

        current = start_dt
        while current < end_dt:
            # TODO DEBUG remove the visualization of the datetime format because it is not needed
            range_vals.append(current.strftime(start_dt_format))
            current += step_size

        return range_vals


class NavBtns(cW.NavigationButtons):
    """
    Navigation buttons for the range value frame
    """

    def __init__(self, app, root):
        """
        Initialize the navigation buttons

        Args:
            app (test_environment_app.AppWindow): the main application
            root (cW.BasisFrame): the parent frame
        """
        super().__init__(
            root=root,
            values=(app.lang["DISCARD"], app.lang["SAVE"]),
            options={"btn_1_type": "delete", "btn_2_type": "accept"},
        )

        self.root = root

    def btn_1_func(self):
        """
        Function to discard the changes and go back to the previous frame
        """
        self.root.app.go_back(self.root)

    def btn_2_func(self):
        """
        Function to save the values and go back to the previous frame
        """

        value: list = self.root.value_entries_frame.get_all_values()

        if value is not None:
            if len(value) < 5:
                self.root.app.entity_value_frame_dict[
                    self.root.entity_id
                ].visible_value = (str(value))
            else:
                showed_values: str = (
                    [str(val) for val in value[:3]]
                    + ["..."]
                    + [str(val) for val in value[-2:]]
                )
                self.root.app.entity_value_frame_dict[
                    self.root.entity_id
                ].visible_value = str(showed_values)

            self.root.app.entity_value_frame_dict[
                self.root.entity_id
            ].test_value = value

        else:
            self.root.app.entity_value_frame_dict[
                self.root.entity_id
            ].entity_value_selection.set("-")

        self.btn_1_func()
