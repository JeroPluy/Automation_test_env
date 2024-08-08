"""
This package is responsible for the database handling of the automation test environment.
"""

from backend.utils.env_const import DATABASE, INIT_FILE, INTEG_DATA

from os import path
import sqlite3 as sqlite


def _load_data_foundation():
    """load the standard integration names and their possible values into the database

    needed sql-Files:
        -   schema/standard_integration.sql
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


def init_db():
    """
    Initialize the database model in sqlite and load the base data

    needed sql-Files:
        -   ../schema/database_creation.spl
        -   ../schema/standard_integration.sql
    """
    # if data base already exists
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

# Trigger the function when the module is imported
init_db()