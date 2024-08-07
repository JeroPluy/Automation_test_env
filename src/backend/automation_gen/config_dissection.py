"""
This module brings together all extraction modules and enables the extraction of all automation entities 
as well as the creation of the complete automation script.
"""

from . import automation_script_gen as asg

from .trigger_dissection import extract_all_trigger
from .condtion_dissection import extract_all_conditions
from .action_dissection import extract_all_actions

from ..utils.env_const import SINGLE

from ..utils.env_helper import Automation

from ..ha_automation_utils.home_assistant_automation_validation import AutomationConfig
from ..ha_automation_utils.home_assistant_const import (
    CONF_MAX,
    CONF_MODE,
)


def create_procedure_list(
    automation_config: AutomationConfig, script_path: str
) -> list:
    """
    Create a list of entities from the automation configuration and adds them to the automation script.
    
    Args:
        automation_config (AutomationConfig): The automation configuration.
        script_path (str): The path to the automation script.
    
    Returns:
        list: A list of entities.
    """
    
    entity_list = []
    entity_list += extract_all_trigger(automation_config, script_path)
    entity_list += extract_all_conditions(automation_config, script_path)
    entity_list += extract_all_actions(automation_config, script_path)
    return entity_list


def create_automation(automation_config: AutomationConfig) -> dict:
    """
    Create an automation with all its information from the automation configuration.
    
    Args:
        automation_config (AutomationConfig): The automation configuration.
        
    Returns:
        dict: The automation data with all its information for inserting into the database.
    """
    automation_data = {}

    automation_name = automation_config.automation_name
    automation_script = asg.init_automation_script(automation_name)

    if CONF_MODE in automation_config:
        mode = automation_config[CONF_MODE]
    else:
        mode = SINGLE

    if CONF_MAX in automation_config:
        max_instances = automation_config[CONF_MAX]
    else:
        max_instances = 10

    automation = Automation(
        automation_name=automation_name,
        automation_script=automation_script,
        automation_mode=mode,
        max_instances=max_instances,
    )

    automation_data["entities"] = create_procedure_list(
        automation_config, automation_script
    )
    automation_data["infos"] = automation

    return automation_data
