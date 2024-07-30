"""
This module is responsible for generating the automation script which simulates the automation.

"""

from os import path
from environment_package.env_const import AUTOMATION_SCRIPT
from environment_package.env_helper import Entity, is_jinja_template
from environment_package.ha_automation.home_assistant_config_validation import (
    valid_entity_id,
)
from environment_package.ha_automation.home_assistant_const import (
    CONF_ABOVE,
    CONF_AND,
    CONF_BELOW,
    CONF_DEVICE,
    CONF_NOT,
    CONF_NOT_TO,
    CONF_NUMERIC_STATE,
    CONF_OR,
    CONF_PERS_NOTIFICATION,
    CONF_STATE,
    CONF_TO,
    CONF_TYPE,
    CONF_UPDATE_TYPE,
)


TEMPLATE_PATH = path.join("src", "environment_package", "automation_script_templates")

IF_TEMPLATE = "if ("
END_IF_TEMPLATE = "):\n"


def init_automation_script(automation_name: str, dir_path: str = None) -> str:
    """
    This function creates the automation script file in the automation_script directory

    Args:
        automation_name (str): The name of the automation script.
        dir_path (str, optional): The path to the directory where the automation script should be created. Defaults to None.

    Raises:
        FileNotFoundError: If the template file is not found.

    Returns:
        str: The path to the created automation script file.
    """
    file_name = automation_name + ".py"
    if dir_path is None:
        filepath = path.join(AUTOMATION_SCRIPT, file_name)
    else:
        filepath = path.join(dir_path, file_name)

    init_template = path.join(TEMPLATE_PATH, "init_template.py")
    try:
        with open(init_template, "r") as file:
            script_content = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Template file {init_template} not found")

    with open(filepath, "w") as script:
        script.write(script_content)
    return filepath


def _append_script_context_to_script(filepath: str, script_context: str) -> None:
    """
    Append the script context to the automation script file.

    Args:
        filepath (str): The path to the automation script file.
        script_context (str): The script context to be appended to the automation script file.

    Raises:
        FileNotFoundError: If the automation script file is not found.
    """
    try:
        with open(filepath, "a") as script:
            script.write(script_context)
    except FileNotFoundError:
        raise FileNotFoundError(f"File {filepath} not found")


def _get_trigger_conditional_expression(
    trigger_type: str, entity: Entity, trigger_pos: int, above_position: int = None
) -> list:
    """
    Create the conditional expression for the trigger.

    Args:
        trigger_type (str): Depending on the trigger type, the conditional expression is created.
        entity (Entity): The entity is used to create the conditional expression based on the expected value.
        trigger_pos (int): The real position of the trigger in automation script.

    Returns:
        str: The conditional expression for the trigger.
    """
    not_none_condition = f"trigger[{trigger_pos}] is not None and"

    if trigger_type == CONF_STATE:
        if entity.expected_value is not None:
            if CONF_TO in entity.expected_value:
                value = entity.expected_value[CONF_TO]
                if not is_jinja_template(str(value)):
                    if isinstance(value, str):
                        return [f"{not_none_condition} trigger[{trigger_pos}] == '{value}'"]
                    else:
                        return [f"{not_none_condition} trigger[{trigger_pos}] == {value}"]
            elif CONF_NOT_TO in entity.expected_value:
                value = entity.expected_value[CONF_NOT_TO]
                if not is_jinja_template(str(value)):
                    if isinstance(value, str):
                        return [f"{not_none_condition} trigger[{trigger_pos}] != '{value}'"]
                    else:
                        return [f"{not_none_condition} trigger[{trigger_pos}] != {value}"]
        return [f"{not_none_condition} trigger[{trigger_pos}]"]

    elif trigger_type == CONF_NUMERIC_STATE:
        complete_condition_str = None
        above_condition_str = None
        below_condition_str = None
        middle_condition_str = None

        if CONF_ABOVE in entity.expected_value:
            value = entity.expected_value[CONF_ABOVE]
            if isinstance(value, (int, float)):
                complete_condition_str = f"{value} < "
            elif not is_jinja_template(str(value)) and valid_entity_id(str(value)):
                if above_position is not None:
                    complete_condition_str = f"trigger[{above_position}] < "
                else:
                    above_position = trigger_pos
                    complete_condition_str = f"trigger[{trigger_pos}] < "

                # cache the above condition
                above_condition_str = complete_condition_str

        # move the trigger_pos after the above condition
        if above_condition_str is not None:
            if above_position == trigger_pos:
                trigger_pos += 1
            middle_condition_str = f"trigger[{trigger_pos}]"
            complete_condition_str += middle_condition_str
            # complete the above condition
            above_condition_str += middle_condition_str
        else:
            middle_condition_str = f"trigger[{trigger_pos}]"
            # checks if a above value is in the complete condition
            if complete_condition_str is None:
                complete_condition_str = middle_condition_str
            else:
                complete_condition_str += middle_condition_str

        if CONF_BELOW in entity.expected_value:
            value = entity.expected_value[CONF_BELOW]
            if isinstance(value, (int, float)):
                complete_condition_str += f" < {value}"
            elif not is_jinja_template(str(value)) and valid_entity_id(str(value)):
                complete_condition_str += " < trigger[XXXX]"
                # cache the below condition
                below_condition_str = f"{middle_condition_str} < trigger[XXXX]"

        # add the none exception for the entity values to the condition
        if above_condition_str is None and below_condition_str is None:
            return [
                f"{not_none_condition} ({complete_condition_str})",
                trigger_pos,
                above_position,
            ]
        else:
            # create the if statement for the trigger entities and handle the None exception
            if_statement = None

            if above_condition_str is not None and below_condition_str is not None:
                if_statement = f"((trigger[{above_position}] is not None and trigger[{trigger_pos}] is not None and trigger[XXXX] is not None) and ({complete_condition_str})) or (trigger[{trigger_pos}] is not None and trigger[XXXX] is None and trigger[{above_position}] is None) or (trigger[{trigger_pos}] is not None and (trigger[{above_position}] is None and ({below_condition_str}))) or (trigger[{trigger_pos}] is not None and (trigger[XXXX] is None and ({above_condition_str})))"
            elif below_condition_str is None:
                if_statement = f"((trigger[{above_position}] is not None and trigger[{trigger_pos}] is not None) and ({complete_condition_str})) or (trigger[{trigger_pos}] is not None and trigger[{above_position}] is None)"
            elif above_condition_str is None:
                if_statement = f"((trigger[{trigger_pos}] is not None and trigger[XXXX] is not None) and ({complete_condition_str})) or (trigger[{trigger_pos}] is not None and trigger[XXXX] is None)"

            return [if_statement, trigger_pos, above_position]

    elif trigger_type == CONF_PERS_NOTIFICATION:
        value = entity.expected_value[CONF_UPDATE_TYPE]
        if isinstance(value, str):
            return [f"trigger[{trigger_pos}] == '{value}'"]
        elif isinstance(value, list):
            return [f"trigger[{trigger_pos}] == {value}"]

    elif trigger_type == CONF_DEVICE:
        value = entity.expected_value[CONF_TYPE]
        if isinstance(value, str):
            return [f"trigger[{trigger_pos}] == '{value}'"]
        elif isinstance(value, list):
            return [f"trigger[{trigger_pos}] == {value}"]

    # event, homeassistant, mqtt, sun, tag, template, time, time_pattern, webhook, zone,
    # geo_location, calendar, conversation
    else:
        return [f"trigger[{trigger_pos}]"]


def create_combination_trigger_script(
    trigger_type: str,
    entity_list: list,
    trigger_pos: int,
    trigger_id: str | None,
    filepath: str,
    combination: str = CONF_OR,
) -> int:
    # set the combinator for the if statement
    combinator = combination

    # create the if statement for the trigger list
    if len(entity_list) > 1:
        script_context = IF_TEMPLATE 
        # cache for the trigger_pos of the above condition
        above_position = None

        for x in range(0, len(entity_list)):
            # create the trigger expression for the entities
            trigger_expression = _get_trigger_conditional_expression(
                trigger_type, entity_list[x], trigger_pos, above_position
            )

            if x == 0:
                # add the trigger expression to the script without the combinator
                script_context += trigger_expression[0] + "\n"
            else:
                # add the trigger expression to the script with the combinator
                script_context += f"\t{combinator} " + trigger_expression[0] + "\n"
            
            # set the trigger_pos for the next trigger expression
            if trigger_type == CONF_NUMERIC_STATE:
                trigger_pos = trigger_expression[1]
                above_position = trigger_expression[2]
            trigger_pos += 1

    elif len(entity_list) == 1:
        # create the trigger expression for the entities
        trigger_expression = _get_trigger_conditional_expression(
            trigger_type, entity_list[0], trigger_pos
        )
        # add the first trigger expression to the script
        script_context = IF_TEMPLATE + trigger_expression[0]

        # set the trigger_pos for the next trigger expression
        if trigger_type == CONF_NUMERIC_STATE:
            trigger_pos = trigger_expression[1]
        trigger_pos += 1

    # close the if statement
    script_context += END_IF_TEMPLATE

    if trigger_type == CONF_NUMERIC_STATE:
        if "XXXX" in script_context:
            script_context = script_context.replace("XXXX", str((trigger_pos)))
            trigger_pos += 1

    # add the trigger_id to the script and the triggered flag
    if trigger_id is None:
        script_context += "\ttrigger_id = None\n\ttriggered = True\n\n"
    else:
        script_context += f"\ttrigger_id = '{trigger_id}' \n\ttriggered = True\n\n"
    _append_script_context_to_script(filepath, script_context)

    return trigger_pos


def create_trigger_script(
    trigger_type: str,
    entity: Entity,
    trigger_pos: int,
    trigger_id: str | None,
    filepath: str,
) -> int:
    # create the trigger expression for the entity
    trigger_expression = _get_trigger_conditional_expression(
        trigger_type, entity, trigger_pos
    )
    # complete the trigger expression for the entity
    script_context = IF_TEMPLATE + trigger_expression[0] + END_IF_TEMPLATE

    # set the trigger_pos for the next trigger expression and replace the XXXX with the trigger_pos of the below condition
    if trigger_type == CONF_NUMERIC_STATE:
        trigger_pos = trigger_expression[1]
        if "XXXX" in script_context:
            trigger_pos += 1
            script_context = script_context.replace("XXXX", str((trigger_pos)))

    # add the trigger_id to the script and the triggered flag
    if trigger_id is None:
        script_context += "\ttrigger_id = None\n\ttriggered = True\n\n"
    else:
        script_context += f"\ttrigger_id = '{trigger_id}' \n\ttriggered = True\n\n"
    _append_script_context_to_script(filepath, script_context)

    return trigger_pos + 1


def close_trigger_section(filepath: str) -> None:
    """
    Close the trigger section in the automation script.

    Args:
        filepath (str): The path to the automation script file.
    """
    # TODO remove print statement
    script_context = "# The end of the trigger section \nif triggered: \n\tprint('Triggered')\n"
    _append_script_context_to_script(filepath, script_context)

def create_condition_script(
    condition_type: str,
    entity: Entity,
    condition_pos: int,
    trigger_id: str | None,
    filepath: str,
) -> int:
    pass
    

def create_locked_message(filepath: str) -> None:
    """
    Create the locked message for the automation script.

    Args:
        filepath (str): The path to the automation script file.
    """
    locked_message = """
!!!! ATTENTION: THIS FILE RAN ONCE. EVERY CHANGE TO THIS FILE WILL ALTER THE AUTOMATION FLOW OR PREVENT THE REPEATABILITY OF A TEST RUN.

If you still want to make changes to the automation script, please:
    1. create a new automation,
    2. copy this content to the new script
    3. and make the changes in a new automation to ensure the repeatability of the test run.
    """

    with open(filepath, "r") as script:
        script_content = script.readlines()

    script_content.insert(5, locked_message + "\n")

    with open(filepath, "w") as script:
        script.writelines(script_content)
    return filepath
