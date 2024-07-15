import sqlite3 as sqlite
import os.path

DATABASE = os.path.join("data", "automation_test_env.sqlite")
INIT_FILE = os.path.join("schema", "database_creation.sql")
INTEG_DATA = os.path.join("schema", "insert_standard_integration.sql")

def init_db():
    """Initialize the database model in sqlite and load the base data
    
    needed sql-Files: 
        -   ../schema/database_creation.spl
        -   ../schema/standard_integration.sql
    """
    #if data base already exists
    if os.path.isfile(DATABASE):
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
            load_data_foundation()


def load_data_foundation():
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

# just a test function
# TODO: remove 
def get_db_path():
    print(os.path.isfile(INIT_FILE))
    print(os.path.isfile(INTEG_DATA))