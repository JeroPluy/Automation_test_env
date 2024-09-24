"""
This module is used to generate the trigger section of the automation script.
"""

from ...ha_automation_utils.home_assistant_config_validation import valid_entity_id
from ...ha_automation_utils.home_assistant_const import (
    CONF_ABOVE,
    CONF_BELOW,
    CONF_DEVICE,
    CONF_NOT_TO,
    CONF_NUMERIC_STATE,
    CONF_OR,
    CONF_PERS_NOTIFICATION,
    CONF_STATE,
    CONF_TO,
    CONF_TYPE,
    CONF_UPDATE_TYPE,
)
from ...utils.env_helper import is_jinja_template
from ...utils.env_helper_classes import Entity
from .utils import append_script_context_to_script

IF_TEMPLATE = "if ("
END_IF_TEMPLATE = "):\n"

def _get_trigger_conditional_expression(
    trigger_type: str,
    entity: Entity,
    trigger_pos: int,
    above_position: int = None,
    source: str = "trigger",
) -> list:
    """
    Create the conditional expression for the trigger.

    Args:
        trigger_type (str): Depending on the trigger type, the conditional expression is created.
        entity (Entity): The entity is used to create the conditional expression based on the expected value.
        trigger_pos (int): The real position of the trigger in automation script.
        above_position (int, optional): The position of the above entity in the automation script.
        source (str, optional): The source of the entity in the automation script. Defaults to "trigger".

    Returns:
        str: The conditional expression for the trigger.
    """
    array_part = "trigger" if source == "trigger" else "action_inputs"

    not_none_condition = f"{array_part}[{trigger_pos}] is not None and"

    if trigger_type == CONF_STATE:
        if entity.expected_value is not None:
            comparison_str = ""
            operator = None

            if CONF_TO in entity.expected_value:
                exp_value = entity.expected_value[CONF_TO]
                operator = "=="
            elif CONF_NOT_TO in entity.expected_value:
                exp_value = entity.expected_value[CONF_NOT_TO]
                operator = "!="

            if isinstance(exp_value, list):
                if above_position is None:
                    above_position = trigger_pos
                    for value in exp_value:
                        if valid_entity_id(str(value)):
                            trigger_pos += 1
                # create the condition expression that the main entity could not be None
                comparison_str = f"{array_part}[{trigger_pos}] is not None and ("

                current_com_entity_pos = above_position
                start_val = True
                for value in exp_value:
                    # set an or before the next comparison
                    if start_val:
                        start_val = False
                    else:
                        comparison_str += " or "

                    if valid_entity_id(str(value)):
                        comparison_str += f"{array_part}[{trigger_pos}] {operator} {array_part}[{current_com_entity_pos}]"
                        current_com_entity_pos += 1
                    else:
                        if isinstance(value, str):
                            # replace double quotes with single quotes using str.replace()
                            value = value.replace('"', "'")
                            comparison_str += (
                                f'{array_part}[{trigger_pos}] {operator} "{value}"'
                            )
                        else:
                            comparison_str += (
                                f"{array_part}[{trigger_pos}] {operator} {value}"
                            )

                comparison_str += ")"

            else:
                if above_position is None:
                    if valid_entity_id(str(exp_value)):
                        above_position = trigger_pos
                        trigger_pos += 1
                # create the condition expression that the main entity could not be None
                comparison_str = f"{array_part}[{trigger_pos}] is not None and ("

                if valid_entity_id(str(exp_value)):
                    comparison_str += f"{array_part}[{trigger_pos}] {operator} {array_part}[{above_position}])"
                else:
                    if isinstance(exp_value, str):
                        # replace double quotes with single quotes using str.replace()
                        exp_value = exp_value.replace('"', "'")
                        comparison_str += (
                            f'{array_part}[{trigger_pos}] {operator} "{exp_value}")'
                        )
                    # float or int value
                    else:
                        comparison_str += (
                            f"{array_part}[{trigger_pos}] {operator} {exp_value})"
                        )

            return [comparison_str, trigger_pos, above_position]
        # if no expected state value is given, just return the trigger entity as a condition
        else:
            return [f"{array_part}[{trigger_pos}]", trigger_pos]

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
                    complete_condition_str = f"{array_part}[{above_position}] < "
                else:
                    above_position = trigger_pos
                    complete_condition_str = f"{array_part}[{trigger_pos}] < "

                # cache the above condition
                above_condition_str = complete_condition_str

        # move the trigger_pos after the above condition
        if above_condition_str is not None:
            if above_position == trigger_pos:
                trigger_pos += 1
            middle_condition_str = f"{array_part}[{trigger_pos}]"
            complete_condition_str += middle_condition_str
            # complete the above condition
            above_condition_str += middle_condition_str
        else:
            middle_condition_str = f"{array_part}[{trigger_pos}]"
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
                complete_condition_str += f" < {array_part}[XXXX]"
                # cache the below condition
                below_condition_str = f"{middle_condition_str} < {array_part}[XXXX]"

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
                if_statement = f"((({array_part}[{above_position}] is not None and {array_part}[{trigger_pos}] is not None and {array_part}[XXXX] is not None) and ({complete_condition_str})) or ({array_part}[{trigger_pos}] is not None and {array_part}[XXXX] is None and {array_part}[{above_position}] is None) or ({array_part}[{trigger_pos}] is not None and ({array_part}[{above_position}] is None and ({below_condition_str}))) or ({array_part}[{trigger_pos}] is not None and ({array_part}[XXXX] is None and ({above_condition_str}))))"
            elif below_condition_str is None:
                if_statement = f"((({array_part}[{above_position}] is not None and {array_part}[{trigger_pos}] is not None) and ({complete_condition_str})) or ({array_part}[{trigger_pos}] is not None and {array_part}[{above_position}] is None))"
            elif above_condition_str is None:
                if_statement = f"((({array_part}[{trigger_pos}] is not None and {array_part}[XXXX] is not None) and ({complete_condition_str})) or ({array_part}[{trigger_pos}] is not None and {array_part}[XXXX] is None))"

            return [if_statement, trigger_pos, above_position]

    elif trigger_type == CONF_PERS_NOTIFICATION:
        value = entity.expected_value[CONF_UPDATE_TYPE]
        if isinstance(value, str):
            # replace double quotes with single quotes using str.replace()
            value = value.replace('"', "'")
            return [f'{array_part}[{trigger_pos}] == "{value}"']
        elif isinstance(value, list):
            return [f"{array_part}[{trigger_pos}] == {value}"]

    elif trigger_type == CONF_DEVICE:
        value = entity.expected_value[CONF_TYPE]
        if isinstance(value, str):
            # replace double quotes with single quotes using str.replace()
            value = value.replace('"', "'")
            return [f'{array_part}[{trigger_pos}] == "{value}"']
        elif isinstance(value, list):
            return [f"{array_part}[{trigger_pos}] == {value}"]

    # event, homeassistant, mqtt, sun, tag, template, time, time_pattern, webhook, zone,
    # geo_location, calendar, conversation
    else:
        return [f"{array_part}[{trigger_pos}]"]


def create_combination_trigger_script(
    trigger_type: str,
    entity_list: list,
    trigger_pos: int,
    trigger_id: str | None,
    filepath: str,
    indentation_lvl: int = 1,
    source: str = "trigger",
) -> int:
    """
    Create the trigger condition for combined trigger entities in the automation script.

    Args:
        trigger_type (str): the type / platform of the trigger
        entity_list (list): the list of entities of the trigger
        trigger_pos (int): the position of the trigger in the automation script based on former triggers
        trigger_id (str | None):  the id of the trigger is used to identify the trigger for later call backs of which trigger was triggered
        filepath (str): the path to the automation script file
        indentation_lvl (int, optional): the indentation level of the trigger in the automation script. Defaults to 1.
        source (str, optional): the source of the entity in the automation script. Defaults to "trigger".

    Returns:
        int: the new trigger_pos for the next trigger entity (is the next trigger_pos in the automation script)
    """
    # set the combinator for the if statement
    combinator = CONF_OR
    script_context = ""
    indentation = "\t" * indentation_lvl

    # create the if statement for the trigger list
    if len(entity_list) > 1:
        if source != "action":
            script_context = indentation + IF_TEMPLATE

        # cache for the trigger_pos of the above condition
        above_position = None

        for x in range(0, len(entity_list)):
            # create the trigger expression for the entities
            trigger_expression = _get_trigger_conditional_expression(
                trigger_type, entity_list[x], trigger_pos, above_position, source
            )

            if x == 0:
                # add the trigger expression to the script without the combinator
                script_context += "(" + trigger_expression[0] + ")\n"
            else:
                # add the trigger expression to the script with the combinator
                script_context += (
                    f"{indentation}\t{combinator} (" + trigger_expression[0] + ")\n"
                )

            # set the trigger_pos for the next trigger expression
            if trigger_type == CONF_NUMERIC_STATE or trigger_type == CONF_STATE:
                trigger_pos = trigger_expression[1]
                above_position = trigger_expression[2]
            trigger_pos += 1

    elif len(entity_list) == 1:
        # create the trigger expression for the entities
        trigger_expression = _get_trigger_conditional_expression(
            trigger_type, entity_list[0], trigger_pos, source=source
        )
        # add the first trigger expression to the script
        script_context = indentation + IF_TEMPLATE + trigger_expression[0]

        # set the trigger_pos for the next trigger expression
        if trigger_type == CONF_NUMERIC_STATE or trigger_type == CONF_STATE:
            trigger_pos = trigger_expression[1]
        trigger_pos += 1

    # close the if statement

    script_context += indentation + END_IF_TEMPLATE

    if trigger_type == CONF_NUMERIC_STATE:
        if "XXXX" in script_context:
            script_context = script_context.replace("XXXX", str((trigger_pos)))
            trigger_pos += 1

    if source != "action":
        # add the trigger_id to the script and the triggered flag
        if trigger_id is None:
            script_context += (
                f"{indentation}\ttrigger_id = None\n{indentation}\ttriggered = True\n\n"
            )
        else:
            script_context += f"{indentation}\ttrigger_id = '{trigger_id}' \n{indentation}\ttriggered = True\n\n"

    append_script_context_to_script(filepath, script_context)

    return trigger_pos


def create_trigger_script(
    trigger_type: str,
    entity: Entity,
    trigger_pos: int,
    trigger_id: str | None,
    filepath: str,
    indentation_lvl: int = 1,
    source: str = "trigger",
) -> int:
    """
    Create the trigger condition for single trigger entities in the automation script.

    Args:
        trigger_type (str): the type / platform of the trigger
        entity (Entity): the main entity of the trigger
        trigger_pos (int): the position of the trigger in the automation script based on former triggers
        trigger_id (str | None):  the id of the trigger is used to identify the trigger for later call backs of which trigger was triggered
        filepath (str): the path to the automation script file
        indentation_lvl (int, optional): the indentation level of the trigger in the automation script. Defaults to 1.
        source (str, optional): the source of the entity in the automation script. Defaults to "trigger".

    Returns:
        int: the new trigger_pos for the next trigger entity (is the next trigger_pos in the automation script)
    """
    indentation = "\t" * indentation_lvl

    # create the trigger expression for the entity
    trigger_expression = _get_trigger_conditional_expression(
        trigger_type, entity, trigger_pos, source=source
    )
    # complete the trigger expression for the entity
    if source != "action":
        script_context = (
            indentation + IF_TEMPLATE + trigger_expression[0] + END_IF_TEMPLATE
        )
    else:
        script_context = indentation + "(" + trigger_expression[0] + ")\n"

    # set the trigger_pos for the next trigger expression and replace the XXXX with the trigger_pos of the below condition
    if trigger_type == CONF_NUMERIC_STATE or trigger_type == CONF_STATE:
        trigger_pos = trigger_expression[1]

        if trigger_type == CONF_NUMERIC_STATE and "XXXX" in script_context:
            trigger_pos += 1
            script_context = script_context.replace("XXXX", str((trigger_pos)))

    if source != "action":
        # add the trigger_id to the script and the triggered flag
        if trigger_id is None:
            script_context += (
                f"{indentation}\ttrigger_id = None\n{indentation}\ttriggered = True\n\n"
            )
        else:
            script_context += f"{indentation}\ttrigger_id = '{trigger_id}' \n{indentation}\ttriggered = True\n\n"

    append_script_context_to_script(filepath, script_context)

    return trigger_pos + 1


def close_trigger_section(filepath: str) -> None:
    """
    Close the trigger section in the automation script.

    Args:
        filepath (str): The path to the automation script file.
    """
    script_context = "\t# The end of the trigger section\n\treturn triggered\n\n"
    
    append_script_context_to_script(filepath, script_context)
