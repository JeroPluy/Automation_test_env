"""
This module contains the functions to add automations, entities and integrations to the database.
"""

from backend.utils.env_const import DATABASE

from backend.utils.env_helper_classes import Automation

from .db_utils import (
    get_automations_with_same_name,
    get_integration_id,
    validate_database_entity,
    update_additional_infos,
)

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
    version: int = 0

    same_automation_ids = get_automations_with_same_name(a_name)

    INSERT_AUTOMATION = "INSERT INTO automation (a_name, autom_mode, max_instances, script) VALUES (?, ?, ?, ?)"

    with sqlite.connect(DATABASE) as con:
        cur = con.cursor()

        # get the versions of the automations with the same name
        GET_VERSION = "SELECT add_info.info FROM additional_information AS add_info JOIN automation AS autom ON add_info.a_id == autom.a_id WHERE autom.a_id = ? AND info_type = 'version'"
        autom_id: int = None
        for autom_id in same_automation_ids:
            cur.execute(GET_VERSION, (str(autom_id),))
            answer = cur.fetchone()
            if answer is not None:
                if isinstance(answer[0], str):
                    continue 
                curr_version = int(answer[0])
                if curr_version >= version:
                    version = curr_version

        version += 1
        
        # insert the new automation
        cur.execute(INSERT_AUTOMATION, (a_name, autom_mode, max_instances, script_path))
        a_id = cur.lastrowid
        con.commit()

        return a_id, version


def _create_automation_entities_in_db(a_id, entities: list):
    """
    create the entities in the database

    Args:
        a_id: int - the id of the automation the entities belong to
        entities: list - the entities to be added to the database
    """

    automation_entities = []

    # go through all entities and add them to the database
    for entity in entities:
        # validate the entity and its integration
        validated_entity = validate_database_entity(entity)

        # if the entity already exists in the database
        if validated_entity["entity_id"] is not None:
            automation_entities.append((
                a_id,
                validated_entity["entity_id"],
                entity.parameter_role,
                entity.position,
                str(entity.expected_value),
                entity.parent,
            ))
        # if check for the integration
        else:
            # if integration is part of the database
            if validated_entity["integration_id"] is not None:
                integration_id = validated_entity["integration_id"]

                # create the new entity in the database
                with sqlite.connect(DATABASE) as con:
                    cur = con.cursor()

                    # insert the new entity into the database
                    INSERT_NEW_ENTITY = (
                        "INSERT INTO entity (e_name, i_id) VALUES (?, ?)"
                    )

                    cur.execute(INSERT_NEW_ENTITY, (entity.entity_name, integration_id))
                    e_id = cur.lastrowid
                    con.commit()
                    # add the new entity to the list to connect it to the automation in automation_entity
                    automation_entities.append((
                        a_id,
                        e_id,
                        entity.parameter_role,
                        entity.position,
                        str(entity.expected_value),
                        entity.parent,
                    ))
            else:
                raise ValueError(
                    f"Integration: '{entity.integration}' not found in the database. Please add the integration first."
                )

    # insert the entities as automation entities into the database
    CREATE_AUTOMATION_ENTITY = "INSERT INTO automation_entity (a_id, e_id, p_role, position, exp_val, parent) VALUES (?, ?, ?, ?, ?, ?)"
    with sqlite.connect(DATABASE) as con:
        cur = con.cursor()
        cur.executemany(CREATE_AUTOMATION_ENTITY, automation_entities)
        con.commit()


def add_automation(automation_data: dict) -> int:
    """
    add the whole automation config to the database

    Args:
        automation: dict - the automation config to be added to the database

    Returns:
        int - the id of the new automation in the database
    """
    a_id, version = _create_automation_in_db(automation_data["infos"])
    try:
        _create_automation_entities_in_db(a_id, automation_data["entities"])
    except ValueError as e:
        raise e
    return a_id, version


def add_additional_info(a_id: int, infos: list = []):
    """
    add additional information to the automation

    Args:
        a_id: int - the id of the automation
        infos: list - the additional information to be added to the database as a list of tuples (info_type, info)
    """

    # add the additional information to the database if it is not already there or update it if it is
    if infos != []:
        update_additional_infos(automation_id=a_id, add_infos=infos)
    
    # ensure that the project and version info is added to the database regardless of the user input
    with sqlite.connect(DATABASE) as con:
        cur = con.cursor()
        
        CHECK_INFOS = "SELECT info_type FROM additional_information WHERE a_id = ?"
        
        cur.execute(CHECK_INFOS, (a_id,))
        result = cur.fetchall()
        
        # inserting statement for missing data
        ADD_INFOS = "INSERT INTO additional_information (a_id, info_type, info) VALUES (?, ?, ?)"
        
        if ("project",) not in result:
            cur.execute(ADD_INFOS, (a_id, "project", "uncategorized"))
            con.commit()
            
        if ("version",) not in result:
            cur.execute(ADD_INFOS, (a_id, "version", "unknown"))
            con.commit()


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
