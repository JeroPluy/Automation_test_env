"""
This package is responsible for the database handling of the automation test environment.
"""

import sqlite3 as sqlite
from os import path

from backend.utils.env_const import (
    AUTOMATION_SCRIPT,
    DATABASE,
    EXAMPLE_DATA,
    EXAMPLE_SCRIPT,
    INIT_FILE,
    INTEG_DATA,
)

from .db_create_autom import add_automation, add_additional_info, add_integration

__all__ = ["add_automation", "add_additional_info", "add_integration"]


def _load_data_foundation():
    """
    load the standard integration names and their possible values into the database
    and add an example automation to the database

    needed sql-Files:
        -   schema/standard_integration.sql
        -   schema/example_automation.sql
    needed python-File:
        -   schema/example_automation.py
    """
    with open(INTEG_DATA) as integration_data:
        standard_integration_data = integration_data.read()

    try:
        # con = connection to the db
        with sqlite.connect(DATABASE) as con:
            # create cursor to execute commands on db
            cur = con.cursor()
            cur.executescript(standard_integration_data)
            # commit db actions, thus actually execute on the db
            con.commit()
    except sqlite.IntegrityError as e:
        print(str(e) + " - data already loaded")

    # add an example automation to the database not possible because of circular import
    with open(EXAMPLE_DATA) as automation_example:
        example_data = automation_example.read()

    try:
        # con = connection to the db
        with sqlite.connect(DATABASE) as con:
            # create cursor to execute commands on db
            cur = con.cursor()
            cur.executescript(example_data)
            # commit db actions, thus actually execute on the db
            con.commit()
    except sqlite.IntegrityError as e:
        print(str(e) + " - data already loaded")

    # copy the example automation script to the automation script folder
    with open(EXAMPLE_SCRIPT, "r") as example_script:
        script = example_script.read()
        with open(
            path.join(AUTOMATION_SCRIPT, "example_automation.py"), "w"
        ) as script_file:
            script_file.write(script)


def init_db():
    """
    Initialize the database model in sqlite and load the base data

    needed sql-Files:
        -   ../schema/database_creation.spl
        -   ../schema/standard_integration.sql
    """
    # init data base only if it does not exist
    if path.isfile(DATABASE):
        return
    else:
        with open(INIT_FILE) as model_creator:
            automation_test_env_model = model_creator.read()

            # con = connection to the db
            with sqlite.connect(DATABASE) as con:
                # create cursor to execute commands on db
                cur = con.cursor()
                cur.executescript(automation_test_env_model)
                # commit db actions, thus actually execute on the db
                con.commit()

            # load base data for the data base
            _load_data_foundation()

            # print success message
            print("Database initialized successfully")


# Trigger the function when the module is imported
init_db()
