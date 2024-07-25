import os.path
import sqlite3 as sqlite

from environment_package.automation_dissection import Entity
from environment_package.env_const import standard_integrations

DATABASE = os.path.join("data", "automation_test_env.sqlite")
INIT_FILE = os.path.join("schema", "database_creation.sql")
INTEG_DATA = os.path.join("schema", "insert_integrations.sql")


def init_db():
    """Initialize the database model in sqlite and load the base data

    needed sql-Files:
        -   ../schema/database_creation.spl
        -   ../schema/standard_integration.sql
    """
    # if data base already exists
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


def _create_automation_in_db(info: dict):
    """create the automation in the database

    Args:
        info: dict - the information about the automation to be added to the database
    """

    a_name = info["a_name"]
    autom_mode = info["autom_mode"]
    max_instances = info["max_instances"]
    script_path = info["script"]
    version = 1
    project = info["project"]

    def _check_for_automation_with_same_name(name: str) -> int:
        SELECT_AUTOMATION = "SELECT a_id FROM automation WHERE a_name = ?"
        with sqlite.connect(DATABASE) as con:
            cur = con.cursor()
            cur.execute(SELECT_AUTOMATION, (name,))
            if cur.fetchone() is not None:
                return None
            else:
                return cur.fetchone()[0]

    same_automation = _check_for_automation_with_same_name(a_name)

    INSERT_AUTOMATION = "INSERT INTO automation (a_name, autom_mode, max_instances, script, error) VALUES (?, ?, ?, ?)"

    with sqlite.connect(DATABASE) as con:
        cur = con.cursor()
        if same_automation is not None:
            SELECT_VERSION = "SELECT info FROM additional_information WHERE a_id = ?"
            version = cur.execute(SELECT_VERSION, (same_automation))
        cur.execute(INSERT_AUTOMATION, (a_name, autom_mode, max_instances, script_path))
        a_id = cur.lastrowid
        con.commit()

        # Prepare the data for insertion
        infos = [
            (a_id, "project", project),
            (a_id, "version", version),
        ]

        # Define the SQL statement for inserting data
        ADD_INFOS = "INSERT INTO additional_information (a_id, info_type, info) VALUES (?, ?, ?)"

        # Execute the insert statement with multiple values
        cur.executemany(ADD_INFOS, infos)
        con.commit()

        return a_id


def _create_entities_in_db(a_id, entities: list):
    """create the entities in the database

    Args:
        entities: list - the entities to be added to the database
    """

    def _check_if_in_db(entity: Entity):
        SELECT_ENTITY = "SELECT e_id FROM entity WHERE name = ?"
        with sqlite.connect(DATABASE) as con:
            cur = con.cursor()
            cur.execute(SELECT_ENTITY, (entity.name,))
            if cur.fetchone() is not None:
                return None
            else:
                return cur.fetchone()[0]

    automation_entities = []

    # go through all entities and add them to the database
    for entity in entities:
        if not isinstance(entity, Entity):
            raise ValueError("entities must be a list of Entity objects")

        same_entity = _check_if_in_db(entity)
        if same_entity is not None:
            automation_entities.append((
                a_id,
                same_entity,
                entity.parameter_role,
                entity.position,
                entity.expected_value,
            ))
        else:
            with sqlite.connect(DATABASE) as con:
                cur = con.cursor()
                # get the id of the integration of the entity
                integration_id = standard_integrations.get(entity.integration)
                if integration_id is None:
                    SEARCH_INTEGRATION = "SELECT i_id FROM integration WHERE i_name = ?"
                    cur.execute(SEARCH_INTEGRATION, (entity.integration))
                    if cur.fetchone() is None:
                        integration_id = cur.fetchone()[0]
                    else:
                        # 0 is the id for the "None" integration
                        integration_id = 0

                # insert the new entity into the database
                INSERT_ENTITY = "INSERT INTO entity (e_name, i_id) VALUES (?, ?)"
                cur.execute(INSERT_ENTITY, (entity.name, integration_id))
                e_id = cur.lastrowid
                con.commit()

                automation_entities.append((
                    a_id,
                    e_id,
                    entity.parameter_role,
                    entity.position,
                    entity.expected_value,
                ))

    CREATE_AUTOMATION_ENTITY = "INSERT INTO automation_entity (a_id, e_id, p_role, position, exp_val) VALUES (?, ?, ?, ?, ?)"
    cur.executemany(CREATE_AUTOMATION_ENTITY, automation_entities)
    con.commit()


def add_automation(automation_data: dict):
    """add the whole automation config to the database

    Args:
        automation: dict - the automation config to be added to the database
    """
    a_id = _create_automation_in_db(automation_data["infos"])
    _create_entities_in_db(a_id, automation_data["entities"])


# just a test function
# TODO: remove this function
def get_db_path():
    print(os.path.isfile(INIT_FILE))
    print(os.path.isfile(INTEG_DATA))
