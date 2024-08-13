"""
This module is responsible for the automation creation and the database insertion of the automation data.
"""

from backend import ha_automation_utils as ha_utils
from backend.automation_gen.config_dissection import create_automation
from backend.database import src as db


import asyncio


def validate_automation_config(
    automation_yaml: dict,
) -> ha_utils.AutomationConfig:
    """
    Validate the automation configuration

    Args:
        automation_yaml (dict): the automation configuration

    Returns:
        [ha_automation_config.AutomationConfig]: the automation configuration if the validation was successful
    """
    automation_config = asyncio.run(ha_utils.async_validate_config_item(automation_yaml))
    if not (automation_config.validation_status == "ok") and not (
        automation_config.validation_status == "unknown_template"
    ):
        print(
            automation_config.automation_name
            + " : \t "
            + automation_config.validation_status
            + " : \t"
            + str(automation_config.validation_error)
            + "\n"
        )
        return None
    else:
        return automation_config


def load_new_automation_data(test_file_path: str) -> dict:
    """
    Create the information for a automation from a test file

    Args:
        test_file_path (str): the path to the test file

    Returns:
        dict: the information of the test automation
    """

    # load the test file
    automation_yaml = ha_utils.load_yaml_dict(test_file_path)
    # validate the configuration
    automation_config = validate_automation_config(automation_yaml)
    if automation_config is not None:
        # create the automation and return it
        return create_automation(automation_config)


def add_new_automation(test_file_path: str):
    """
    load the automation data from the test file and add it to the database

    Args:
        test_file_path (str): the path to the test file
    """
    automation_data = load_new_automation_data(test_file_path)
    db.add_automation(automation_data)
