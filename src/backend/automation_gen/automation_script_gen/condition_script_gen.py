"""
This module generates the condition part of the automation script.
"""

from os import path

from .utils import TEMPLATE_PATH, append_script_context_to_script
from backend.utils.env_helper import Entity, is_jinja_template
from backend.ha_automation_utils.home_assistant_config_validation import valid_entity_id
from backend.ha_automation_utils.home_assistant_const import CONF_ABOVE, CONF_AND, CONF_BELOW, CONF_DEVICE, CONF_ID, CONF_NOT, CONF_NUMERIC_STATE, CONF_OR, CONF_STATE, CONF_TRIGGER, CONF_TYPE, CONF_ZONE

IF_TEMPLATE = "if ("
END_IF_TEMPLATE = "):\n"


def init_condition_part(filepath: str) -> None:
    """
    Initialize the condition part in the automation script.

    Args:
        filepath (str): The path to the automation script file.
    """

    condition_template = path.join(TEMPLATE_PATH, "condition_template.py")
    try:
        with open(condition_template, "r") as file:
            script_content = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Template file {condition_template} not found")
    # ! tabs aren't taken into account and are converted to 4 spaces
    script_content = script_content.replace("    ", "\t")

    append_script_context_to_script(filepath, script_content)


def _get_condition_expression(
    condition_type: str,
    entity: Entity,
    condition_pos: int,
    source: str = "condition",
    above_position: int = None,
) -> list:
    """
    Create the conditional expression for the condition.

    Args:
        condition_type (str): Depending on the condition type, the conditional expression is created.
        entity (Entity): The entity is used to create the conditional expression based on the expected value.
        condition_pos (int): The real position of the condition in the automation script.
        source (str, optional): The source of the entity (condition or action_inputs). Defaults to "condition".
        above_position (int, optional): The position of the above entity in the automation script.

    Returns:
        str: The conditional expression for the condition.
    """

    array_part = "condition" if source == "condition" else "action_inputs"

    if condition_type == CONF_STATE:
        comparison_str = ""
        # In contrast to the trigger expression, the condition expression can't be None
        exp_value = entity.expected_value[CONF_STATE]

        if isinstance(exp_value, list):
            # start position for the condition entities
            current_comparing_entity_pos = condition_pos
            if above_position is None:
                for value in exp_value:
                    if valid_entity_id(str(value)):
                        above_position = condition_pos
                        condition_pos += 1
            start_val = True
            for value in exp_value:
                # set an or before the next comparison
                if start_val:
                    start_val = False
                else:
                    comparison_str += " or "

                if valid_entity_id(str(value)):
                    comparison_str += f"{array_part}[{condition_pos}] == {array_part}[{current_comparing_entity_pos}]"
                    current_comparing_entity_pos += 1
                else:
                    if isinstance(value, str):
                        # replace double quotes with single quotes using str.replace()
                        value = value.replace('"', "'")
                        comparison_str += f'{array_part}[{condition_pos}] == "{value}"'
                    else:
                        comparison_str += f"{array_part}[{condition_pos}] == {value}"

        else:
            if above_position is None:
                if valid_entity_id(str(exp_value)):
                    above_position = condition_pos
                    condition_pos += 1

            if valid_entity_id(str(exp_value)):
                comparison_str += (
                    f"{array_part}[{condition_pos}] == {array_part}[{above_position}]"
                )
            else:
                if isinstance(exp_value, str):
                    # replace double quotes with single quotes using str.replace()
                    exp_value = exp_value.replace('"', "'")
                    comparison_str += f'{array_part}[{condition_pos}] == "{exp_value}"'
                else:
                    comparison_str += f"{array_part}[{condition_pos}] == {exp_value}"

        return [comparison_str, condition_pos]

    elif condition_type == CONF_NUMERIC_STATE:
        comparison_str = None
        above_condition_str = None
        below_condition_str = None
        middle_condition_str = None

        if CONF_ABOVE in entity.expected_value:
            value = entity.expected_value[CONF_ABOVE]
            if isinstance(value, (int, float)):
                comparison_str = f"{value} < "
            elif not is_jinja_template(str(value)) and valid_entity_id(str(value)):
                if above_position is not None:
                    comparison_str = f"{array_part}[{above_position}] < "
                else:
                    above_position = condition_pos
                    comparison_str = f"{array_part}[{condition_pos}] < "

                # cache the above condition
                above_condition_str = comparison_str

        # move the condition_pos after the above condition
        if above_condition_str is not None:
            if above_position == condition_pos:
                condition_pos += 1
            middle_condition_str = f"{array_part}[{condition_pos}]"
            comparison_str += middle_condition_str
            # complete the above condition
            above_condition_str += middle_condition_str
        else:
            middle_condition_str = f"{array_part}[{condition_pos}]"
            # checks if a above value is in the complete condition
            if comparison_str is None:
                comparison_str = middle_condition_str
            else:
                comparison_str += middle_condition_str

        if CONF_BELOW in entity.expected_value:
            value = entity.expected_value[CONF_BELOW]
            if isinstance(value, (int, float)):
                comparison_str += f" < {value}"
            elif not is_jinja_template(str(value)) and valid_entity_id(str(value)):
                comparison_str += f" < {array_part}[XXXX]"
                # cache the below condition
                below_condition_str = f"{middle_condition_str} < {array_part}[XXXX]"

        # add the none exception for the entity values to the condition
        if above_condition_str is None and below_condition_str is None:
            return [
                f"{comparison_str}",
                condition_pos,
                above_position,
            ]
        else:
            # create the if statement for the condition entities and handle the None exception
            if_statement = f"{comparison_str}"

            return [if_statement, condition_pos, above_position]

    elif condition_type == CONF_DEVICE:
        value = entity.expected_value[CONF_TYPE]

        # replace double quotes with single quotes using str.replace()
        value = value.replace('"', "'")
        return [f'{array_part}[{condition_pos}] == "{value}"']

    elif condition_type == CONF_TRIGGER:
        value = entity.expected_value[CONF_ID]
        return [f'trigger_id == "{value}"']

    elif condition_type == CONF_ZONE:
        values = entity
        if isinstance(values, list) and len(values) > 1:
            comparison_str = ""
            for person in range(0, len(values)):
                if person == 0:
                    comparison_str += f'{array_part}[{condition_pos}] == "{values[person].entity_name}"'
                else:
                    condition_pos += 1
                    comparison_str += f' and {array_part}[{condition_pos}] == "{values[person].entity_name}"'

            return [comparison_str, condition_pos]
        else:
            # single element list
            if isinstance(values, list):
                person = value[0]
            else:
                person = values
            return [
                f'{array_part}[{condition_pos}] == "{person.entity_name}"',
                condition_pos,
            ]

    # template, sun, time
    else:
        return [f"{array_part}[{condition_pos}]"]


def create_combination_condition_script(
    condition_type: str,
    entity_list: list,
    condition_pos: int,
    filepath: str,
    indentation_lvl: int = 1,
    first_element: bool = True,
    source: str = "condition",
    combinator: str = CONF_AND,
) -> int:
    """
    Create the condition for combined condition entities in the automation script.

    Args:
        condition_type (str): The type of the condition.
        entity_list (list): The list of entities of the condition.
        condition_pos (int): The real position of the condition in the automation script.
        filepath (str): The path to the automation script file.
        indentation_lvl (int, optional): The indentation level of the condition block. Defaults to 1.
        first_element (bool, optional): Determine if the condition is the first element in the condition block.
                                        Defaults to True.
        source (str, optional): The source of the entity (condition or action_inputs). Defaults to "condition".
        combinator (str, optional): The combinator for the condition block. Defaults to CONF_AND.

    Returns:
        int: The new condition_pos for the next condition entity (is the next condition_pos in the automation script).
    """
    script_context = ""
    indentation = "\t" * indentation_lvl
    if combinator == CONF_NOT:
        combinator = "and not"

    # create the if statement for the condition list
    if len(entity_list) > 1:
        # normal condition indentation
        if first_element:
            script_context += indentation + "(\n"
        else:
            script_context += indentation + combinator + "(\n"

        indentation += "\t"
        # cache for the condition_pos of the above condition
        above_position = None

        for x in range(0, len(entity_list)):
            # create the condition expression for the entities
            condition_expression = _get_condition_expression(
                condition_type=condition_type,
                entity=entity_list[x],
                condition_pos=condition_pos,
                above_position=above_position,
                source=source,
            )

            if x == 0:
                script_context += indentation + "(" + condition_expression[0] + ")\n"
            else:
                if condition_type == CONF_TRIGGER:
                    combinator = CONF_OR
                # add the trigger expression to the script with the combinator
                script_context += (
                    f"{indentation}{combinator} (" + condition_expression[0] + ")\n"
                )

            # set the condition_pos for the next trigger expression
            if condition_type == CONF_NUMERIC_STATE:
                condition_pos = condition_expression[1]
                above_position = condition_expression[2]
            if condition_type != CONF_TRIGGER:
                condition_pos += 1

    elif len(entity_list) == 1:
        # create the trigger expression for the entities
        condition_expression = _get_condition_expression(
            condition_type=condition_type,
            entity=entity_list[0],
            condition_pos=condition_pos,
            source=source,
        )

        script_context = indentation + "(" + condition_expression[0] + ")"

        # set the condition_pos for the next trigger expression
        if condition_type == CONF_NUMERIC_STATE or condition_type == CONF_STATE:
            condition_pos = condition_expression[1]
        if condition_type != CONF_TRIGGER:
            condition_pos += 1

    indentation = indentation_lvl * "\t"
    script_context += indentation + ")\n"

    if condition_type == CONF_NUMERIC_STATE:
        if "XXXX" in script_context:
            script_context = script_context.replace("XXXX", str((condition_pos)))
            condition_pos += 1

    append_script_context_to_script(filepath, script_context)

    return condition_pos


def create_condition_script(
    condition_type: str,
    entity: Entity,
    condition_pos: int,
    filepath: str,
    indentation_lvl: int = 1,
    first_element: bool = True,
    source: str = "condition",
    combinator: str = CONF_AND,
) -> int:
    """
    Create the condition for single condition entities in the automation script.

    Args:
        condition_type (str): The type of the condition.
        entity (Entity): The entity of the condition.
        condition_pos (int): The position of the condition in the automation script based on former conditions.
        filepath (str): The path to the automation script file.
        indentation_lvl (int, optional): The indentation level of the condition block. Defaults to 1.
        first_element (bool, optional): Determine if the condition is the first element in the condition block.
                                        Defaults to True.
        source (str, optional): The source of the entity (condition or action_inputs). Defaults to "condition".
        combinator (str, optional): The combinator for the condition block. Defaults to CONF_AND.

    Returns:
        int: The new condition_pos for the next condition entity (is the next condition_pos in the automation script).
    """
    indentation = "\t" * indentation_lvl
    script_context = ""
    if combinator == CONF_NOT:
        combinator = "and not"

    # create the trigger expression for the entity
    condition_expression = _get_condition_expression(
        condition_type=condition_type,
        entity=entity,
        condition_pos=condition_pos,
        source=source,
    )

    # normal condition indentation
    if first_element:
        script_context = indentation + "(" + condition_expression[0] + ")\n"
    else:
        script_context = (
            indentation + combinator + " (" + condition_expression[0] + ")\n"
        )
        

    # set the condition_pos for the next condition expression
    if (
        condition_type == CONF_NUMERIC_STATE
        or condition_type == CONF_STATE
        or condition_type == CONF_ZONE
    ):
        condition_pos = condition_expression[1]

        if condition_type == CONF_NUMERIC_STATE and "XXXX" in script_context:
            condition_pos += 1
            script_context = script_context.replace("XXXX", str((condition_pos)))

    append_script_context_to_script(filepath, script_context)

    if condition_type == CONF_TRIGGER:
        return condition_pos
    else:
        return condition_pos + 1


def start_logic_function_block(
    condition_type: str,
    filepath: str,
    indentation_lvl: int = 1,
    first_element: bool = False,
) -> int:
    """
    Start the function block for the logic connection of condition in the automation script.

    Args:
        condition_type (str): The type of the condition (CONF_OR, CONF_AND, CONF_NOT).
        condition_pos (int): The position of the condition in the automation script based on former conditions.
        filepath (str): The path to the automation script file.
        indentation_lvl (int, optional): The indentation level of the function block. Defaults to 1.
    """
    indentation = "\t" * indentation_lvl

    if first_element:
        script_context = f"{indentation}(\n"
    else:
        script_context = f"{indentation}and ("

    if condition_type == CONF_NOT:
        script_context += f"{indentation}\tnot\n"

    append_script_context_to_script(filepath, script_context)
    return indentation_lvl + 1


def create_next_logic_condition_part(
    condition_type: str,
    filepath: str,
    indentation_lvl: int = 2,
) -> None:
    """
    Create an or condition block for the next condition in the automation script,
    if the condition is not the first one and inside an or-condition-block.
    
    Args:
        condition_type (str): The type of the condition (CONF_OR, CONF_AND, CONF_NOT).
        filepath (str): The path to the automation script file.
        indentation_lvl (int, optional): The indentation level of the condition block. Defaults to 2.
    """
    
    indentation = "\t" * (indentation_lvl)
    
    if condition_type == CONF_OR:
        script_context = indentation + "or "
        
    append_script_context_to_script(filepath, script_context)


def close_logic_function_block(
    filepath, indentation_lvl: int = 2
) -> None:
    """
    Close the function block for the logic connection of condition in the automation script.
    
    Args:
        filepath (str): The path to the automation script file.
        indentation_lvl (int, optional): The indentation level of the function block. Defaults to 2.
    """
    indentation = "\t" * (indentation_lvl)
    script_context = ""

    script_context += f"{indentation})\n"
    append_script_context_to_script(filepath, script_context)


def close_condition_section(filepath: str) -> None:
    """
    Close the complete condition section in the automation script.

    Args:
        filepath (str): The path to the automation script file.
    """
    script_context = f"\t{END_IF_TEMPLATE}\t\tcondition_passed = True\n\t# The end of the condition section\n\treturn condition_passed\n\n"
    
    append_script_context_to_script(filepath, script_context)
