from backend.utils.env_const import DATABASE, standard_integrations

import sqlite3 as sqlite

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