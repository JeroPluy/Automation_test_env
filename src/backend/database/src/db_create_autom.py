"""
This module contains the functions to add automations, entities and integrations to the database.
"""

from backend.utils.env_const import DATABASE

from backend.utils.env_helper_classes import Automation, Entity

from .db_utils import get_automations_with_same_name, get_integration_id

import sqlite3 as sqlite


def _create_automation_in_db(automation_info: Automation):
    """
    create the automation in the database

    Args:
        info: dict - the information about the automation to be added to the database
    """

    a_id: int = None
    a_name: str = automation_info.a_name
    autom_mode: int = automation_info.autom_mode
    max_instances: int = automation_info.max_instances
    script_path: str = automation_info.script
    version: int = 1
    project: str = automation_info.project if automation_info.project else "uncategorized"

    same_automation_ids = get_automations_with_same_name(a_name)

    INSERT_AUTOMATION = "INSERT INTO automation (a_name, autom_mode, max_instances, script) VALUES (?, ?, ?, ?)"

    with sqlite.connect(DATABASE) as con:
        cur = con.cursor()
        SELECT_VERSION = "SELECT info FROM additional_information AS add_info JOIN automation AS autom ON add_info.a_id == autom.a_id WHERE autom.a_name = ? and info_type = 'version'"
        for same_automation_id in same_automation_ids:
            cur.execute(SELECT_VERSION, (same_automation_id))
            version = cur.fetchone()[0]
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


def _create_automation_entities_in_db(a_id, entities: list):
    """
    create the entities in the database

    Args:
        a_id: int - the id of the automation the entities belong to
        entities: list - the entities to be added to the database
    """

    automation_entities = []

    def _check_for_same_entity(entity: Entity) -> int:
        """
        check if an entity with the same name already exists in the database

        Args:
            entity (Entity): the entity to be checked

        Returns:
            int: the id of the entity if it already exists, None otherwise
        """

        SELECT_ENTITY = "SELECT e_id FROM entity WHERE e_name = ?"
        with sqlite.connect(DATABASE) as con:
            cur = con.cursor()
            cur.execute(SELECT_ENTITY, (entity.entity_name,))
            if cur.fetchone() is None:
                return None
            else:
                return cur.fetchone()

    # go through all entities and add them to the database
    for entity in entities:
        if not isinstance(entity, Entity):
            raise Exception("Entities must be a list of Entity objects")

        same_entity = _check_for_same_entity(entity)
        if same_entity is not None:
            automation_entities.append((
                a_id,
                same_entity,
                entity.parameter_role,
                entity.position,
                entity.expected_value,
                entity.parent,
            ))
        else:
            # create the new entity in the database
            with sqlite.connect(DATABASE) as con:
                cur = con.cursor()

                # get the integration id of the entity
                integration_id = get_integration_id(entity.integration)
                if integration_id is None:
                    raise Exception(
                        f"Integration {entity.integration} not found in the database"
                    )

                # insert the new entity into the database
                INSERT_NEW_ENTITY = "INSERT INTO entity (e_name, i_id) VALUES (?, ?)"
                cur.execute(INSERT_NEW_ENTITY, (entity.entity_name, integration_id))
                e_id = cur.lastrowid
                con.commit()

                # add the new entity to the list to connect it to the automation in automation_entity
                automation_entities.append((
                    a_id,
                    e_id,
                    entity.parameter_role,
                    entity.position,
                    entity.expected_value,
                    entity.parent,
                ))

    # insert the entities as automation entities into the database
    CREATE_AUTOMATION_ENTITY = "INSERT INTO automation_entity (a_id, e_id, p_role, position, exp_val, parent) VALUES (?, ?, ?, ?, ?, ?)"
    with sqlite.connect(DATABASE) as con:
        cur = con.cursor()
        cur.executemany(CREATE_AUTOMATION_ENTITY, automation_entities)
        con.commit()


def add_automation(automation_data: dict):
    """
    add the whole automation config to the database

    Args:
        automation: dict - the automation config to be added to the database
    """
    a_id = _create_automation_in_db(automation_data["infos"])
    _create_automation_entities_in_db(a_id, automation_data["entities"])


def add_integration(
    integration_name: str, possible_values: list, force_overwrite: bool = False
):
    """
    add the integration with its possible values to the database

    Args:
        integration_name (str): the name of the new integration
        possible_values (list): the possible values of the new integration contained in a list with tuples (property_name, poss_val)
        force_overwrite (bool, optional): whether to overwrite the integration if it already exists. Defaults to False.
    """

    possible_value_ids: int = []

    def _check_for_same_pos_vals(property: str, pos_val: str) -> int:
        """check if a possible value type with the same property already exists in the databases"""

        SELECT_POS_VAL = (
            "SELECT pv_id FROM automation WHERE property = ? AND p_value = ?"
        )
        with sqlite.connect(DATABASE) as con:
            cur = con.cursor()
            cur.execute(SELECT_POS_VAL, (property, pos_val))
            if cur.fetchone() is None:
                return None
            else:
                return cur.fetchone()[0]

    # check if the integration already exists in the database
    if get_integration_id(integration_name) is not None and not force_overwrite:
        raise Exception(
            f"Integration: '{integration_name}' already exists in the database"
        )

    # go through all possible value tupel and get their ids for the connection to the new integration
    for value in possible_values:
        id = _check_for_same_pos_vals(value[0], value[1])

        # if the possible value already exists in the database
        if id is not None:
            # add the possible value to the list to connect it to the new integration in integration_values
            possible_value_ids.append(id)
        else:
            # add the new possible value to the database
            INSERT_POS_VAL = (
                "INSERT INTO possible_values (property, p_value) VALUES (?, ?)"
            )
            with sqlite.connect(DATABASE) as con:
                cur = con.cursor()
                cur.execute(INSERT_POS_VAL, (value[0], value[1]))
                pv_id = cur.lastrowid
                con.commit()

            # add the new possible value id to the list to connect it to the new integration in integration_values
            possible_value_ids.append(pv_id)

    # add the new integration to the database
    INSERT_NEW_INTEGRATION = "INSERT INTO integration (i_name) VALUES (?)"
    with sqlite.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute(INSERT_NEW_INTEGRATION, (integration_name))
        i_id = cur.lastrowid
        con.commit()

    # connect the new integration with its possible values
    INSERT_INTEGRATION_VALUES = (
        "INSERT INTO integration_values (i_id, pv_id) VALUES (?, ?)"
    )
    integration_values = [(i_id, pv_id) for pv_id in possible_value_ids]
    with sqlite.connect(DATABASE) as con:
        cur = con.cursor()
        cur.executemany(INSERT_INTEGRATION_VALUES, integration_values)
        con.commit()
