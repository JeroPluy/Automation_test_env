from backend.utils.env_const import DATABASE, standard_integrations

import sqlite3 as sqlite

from backend.utils.env_helper_classes import Entity


def get_automations_with_same_name(name: str) -> list:
    """
    Get the ids of the automations with the same name

    Args:
        name: str - the name of the automation

    Returns:
        list - the ids of the automations with the same name
    """

    same_name_ids = []

    SELECT_AUTOMATION = "SELECT a_id FROM automation WHERE a_name = ?"
    with sqlite.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute(SELECT_AUTOMATION, (name,))
        result = cur.fetchall()
        if result:
            same_name_ids = [row[0] for row in result]

    return same_name_ids


def get_integration_id(integration_name: str) -> int:
    """
    Get the id of the integration by its name

    Args:
        integration_name: str - the name of the integration

    Returns:
        int | None - the id of the integration
    """
    # get the id of the integration of the entity
    integration_id = standard_integrations.get(integration_name)

    # if the integration is not in the standard integrations, search for it in the database
    if integration_id is None:
        SEARCH_INTEGRATION = "SELECT i_id FROM integration WHERE i_name = (?)"
        with sqlite.connect(DATABASE) as con:
            cur = con.cursor()
            cur.execute(SEARCH_INTEGRATION, (integration_name,))
            if cur.fetchone() is not None:
                integration_id = cur.fetchone()[0]

    return integration_id


def validate_database_entity(entity: Entity) -> dict:
    """
    Validate the integrations of an automation

    Args:
        entities: list - the entities of the automation

    Returns:
        bool: True if all integrations are valid, False otherwise
    """

    SELECT_ENTITY = "SELECT e_id FROM entity WHERE e_name = ?"

    with sqlite.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute(SELECT_ENTITY, (entity.entity_name,))
        result = cur.fetchone()
        if result is None:
            same_entity = None
        else:
            same_entity = result[0]

    if same_entity is not None:
        return {"entity_id": same_entity}
    else:
        return_dict = {"entity_id": None}

        # create the new entity in the database
        with sqlite.connect(DATABASE) as con:
            cur = con.cursor()

            # get the integration id of the entity
            integration_id = get_integration_id(entity.integration)
            return_dict["integration_id"] = integration_id
            return return_dict


def delete_automation(automation_id: int = None):
    """
    Delete an automation and its automation entities from the database

    Args:
        automation_id: int | None - the id of the automation to be deleted
    """
    if automation_id is None:
        DELETE_AUTOMATION = "DELETE FROM automation;"
        DELETE_AUTOMATION_ENTITIES = "DELETE FROM automation_entity;"
    else:
        DELETE_AUTOMATION = "DELETE FROM automation WHERE a_id = ?;"
        DELETE_AUTOMATION_ENTITIES = "DELETE FROM automation_entity WHERE a_id = ?;"

    with sqlite.connect(DATABASE) as con:
        cur = con.cursor()
        if automation_id is None:
            cur.execute(DELETE_AUTOMATION)
            cur.execute(DELETE_AUTOMATION_ENTITIES)
        else:
            cur.execute(DELETE_AUTOMATION, (automation_id,))
            cur.execute(DELETE_AUTOMATION_ENTITIES, (automation_id,))
        con.commit()

    # remove the autoamtion script from the file system
    # if path.exists(file):
    #     remove(file)


def get_entities(automation_id: int = None, automation_name: str = None) -> list:
    """
    Get the entities of an automation

    Args:
        automation_id: int - the id of the automation

    Returns:
        list - the entities of the automation
    """
    if automation_id is not None:
        SELECT_ENTITIES = "SELECT ae.p_role, ae.parent, ae.position, entity.e_name, ae.exp_val FROM automation_entity AS ae JOIN entity ON entity.e_id == ae.e_id WHERE a_id = ?"
        search_param = (automation_id,)
    else:
        SELECT_ENTITIES = "SELECT ae.p_role, ae.parent, ae.position, entity.e_name, ae.exp_val FROM automation_entity AS ae JOIN automation ON automation.a_id = ae.a_id JOIN entity ON entity.e_id = ae.e_id WHERE automation.a_name = ?"
        search_param = (automation_name,)

    with sqlite.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute(SELECT_ENTITIES, search_param)
        result = cur.fetchall()

    return result


def load_projects() -> list:
    """
    Load the projects from the database

    Returns:
        list - the projects
    """
    SELECT_PROJECTS = (
        "SELECT DISTINCT info FROM additional_information WHERE info_type = 'project'"
    )

    with sqlite.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute(SELECT_PROJECTS)
        result = cur.fetchall()

    return [row[0] for row in result]


def load_automations(project: str = None) -> list:
    """
    Load the automation ids and their names from the database
    """

    SELECT_AUTOMATIONS = """
        SELECT automation.a_id, automation.a_name, aI2.info 
        FROM automation 
        JOIN additional_information AS aI ON automation.a_id = aI.a_id 
        JOIN additional_information AS aI2 ON automation.a_id = aI2.a_id
        WHERE aI.info = ? 
        AND aI.info_type = 'project'
        AND aI2.info_type = 'version'
    """

    with sqlite.connect(DATABASE) as con:
        cur = con.cursor()
        if project is not None:
            cur.execute(SELECT_AUTOMATIONS, (project,))
        else:
            cur.execute(SELECT_AUTOMATIONS, ("uncategorized",))
        result = cur.fetchall()

    return [(row[0], row[1], row[2]) for row in result]
