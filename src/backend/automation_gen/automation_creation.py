"""
This module is responsible for the automation creation and the database insertion of the automation data.
"""

from asyncio import run as async_run

from backend import ha_automation_utils as ha_utils
from backend.automation_gen.config_dissection import create_automation


def validate_automation_config(
    automation_yaml: dict,
    automation_name: str = None,
) -> ha_utils.AutomationConfig:
    """
    Validate the automation configuration

    Args:
        automation_yaml (dict): the automation configuration

    Returns:
        [ha_automation_config.AutomationConfig]: the automation configuration if the validation was successful
    """    
    
    # set the automation name if it was given and validate the configuration
    name_given = automation_name is not None
    automation_config = async_run(ha_utils.async_validate_config_item(automation_yaml, name_given))
    if name_given:
        automation_config.automation_name = automation_name
    
    # error handling if the validation was not successful
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


def load_new_automation_data(automation_file_path: str, automation_name: str=None) -> dict:
    """
    Create the information for a automation from a automation yaml file

    Args:
        automation_file_path (str): the path to the automation yaml file

    Returns:
        dict: the information of the test automation as a dictionary split into entities and infos
    """

    # load the automation file
    automation_yaml = ha_utils.load_yaml_dict(automation_file_path)
    if automation_yaml == {}:
        # validation failed
        return None
    
    # validate the configuration
    automation_config = validate_automation_config(automation_yaml, automation_name=automation_name)
    if automation_config is not None:
        # create the automation and return it
        return create_automation(automation_config)

