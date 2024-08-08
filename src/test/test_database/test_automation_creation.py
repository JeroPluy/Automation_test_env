"""
Test the creation of automations in the database
"""

from backend.database.src import db_create_autom
from backend.database.src.db_utils import delete_automation

from backend.utils.env_const import DATABASE

from backend import ha_automation_utils as ha_utils
from backend import automation_gen as ag

import asyncio
from os import path
import sqlite3 as sqlite


def _create_test_automation_information(test_file_path: str) -> dict:
    """
    Create the information for a test automation from a test file

    Args:
        test_file_path (str): the path to the test file

    Returns:
        dict: the information of the test automation
    """
    # load the test file
    automation_yaml = ha_utils.load_yaml_dict(test_file_path)
    # validate the configuration
    automation_config = asyncio.run(
        ha_utils.async_validate_config_item(automation_yaml)
    )
    # create the automation and return it
    return ag.create_automation(automation_config)


def test_create_automation():
    """
    Test the creation of an automation in the database
    """
    
    test_file_path = path.join(
        "test_data",
        "yaml_files",
        "example_automations",
        "turn_off_living_room_main_light.yaml",
    )

    # create the automation information
    automation_info = _create_test_automation_information(test_file_path)

    # create the automation in the database
    db_create_autom.add_automation(automation_info)
    
    # get the automation from the database
    automation_id = db_create_autom.get_automation(automation_info["a_name"])

    # check if the automation was created
    assert automation_id is not None
    with sqlite.connect(DATABASE) as con:
        cur = con.cursor()
        SELECT_AUTOMATION = "SELECT * FROM automation WHERE a_id = ?"
        cur.execute(SELECT_AUTOMATION, (automation_id,))
        result = cur.fetchone()
        assert result is not None
        print(result)
        

if __name__ == "__main__":
    delete_automation()
    test_create_automation()
    