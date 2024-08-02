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
        # for testing purposes
        filepath = path.join(dir_path, file_name)

    init_template = path.join(TEMPLATE_PATH, "init_template.py")
    try:
        with open(init_template, "r") as file:
            script_content = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Template file {init_template} not found")

    # ! tabs aren't taken into account and are converted to 4 spaces
    script_content = script_content.replace("    ", "\t")

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
    # TODO use the function for the condition as well

    Args:
        trigger_type (str): Depending on the trigger type, the conditional expression is created.
        entity (Entity): The entity is used to create the conditional expression based on the expected value.
        trigger_pos (int): The real position of the trigger in automation script.
        above_position (int, optional): The position of the above entity in the automation script.

    Returns:
        str: The conditional expression for the trigger.
    """
    not_none_condition = f"trigger[{trigger_pos}] is not None and"

    if trigger_type == CONF_STATE:
        if entity.expected_value is not None:
            comparison_str = ""
            operator = None

            if CONF_TO in entity.expected_value:
                value = entity.expected_value[CONF_TO]
                operator = "=="
            elif CONF_NOT_TO in entity.expected_value:
                value = entity.expected_value[CONF_NOT_TO]
                operator = "!="

            if isinstance(value, list):
                if above_position is None:
                    for value in entity.expected_value[CONF_TO]:
                        if valid_entity_id(str(value)):
                            above_position = trigger_pos
                            trigger_pos += 1
                # create the condition expression that the main entity could not be None            
                comparison_str =  f"trigger[{trigger_pos}] is not None and ("

                current_com_entity_pos = 0
                start_val = True
                for value in entity.expected_value[CONF_TO]:
                    # set an or before the next comparison
                    if start_val:
                        start_val = False
                    else:
                        comparison_str += " or "

                    if valid_entity_id(str(value)):
                        comparison_str += f"trigger[{trigger_pos}] {operator} trigger[{current_com_entity_pos}]"
                        current_com_entity_pos += 1
                    else:
                        if isinstance(value, str):
                            # replace double quotes with single quotes using str.replace()
                            value = value.replace('"', "'")
                            comparison_str += (
                                f'trigger[{trigger_pos}] {operator} "{value}"'
                            )
                        else:
                            comparison_str += (
                                f"trigger[{trigger_pos}] {operator} {value}"
                            )

                comparison_str += ")"

            else:
                if above_position is None:
                    if valid_entity_id(str(value)):
                        above_position = trigger_pos
                        trigger_pos += 1
                # create the condition expression that the main entity could not be None        
                comparison_str = f"trigger[{trigger_pos}] is not None and ("
                
                if valid_entity_id(str(value)):
                    comparison_str += (
                        f"trigger[{trigger_pos}] {operator} trigger[{above_position}])"
                    )
                else:
                    if isinstance(value, str):
                        # replace double quotes with single quotes using str.replace()
                        value = value.replace('"', "'")
                        comparison_str += (
                            f'trigger[{trigger_pos}] {operator} "{value}")'
                        )
                    # float or int value
                    else:
                        comparison_str += f"trigger[{trigger_pos}] {operator} {value})"

            return [comparison_str, trigger_pos, above_position]
        # if no expected state value is given, just return the trigger entity as a condition
        else:
            return [f"trigger[{trigger_pos}]", trigger_pos]

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
                if_statement = f"(((trigger[{above_position}] is not None and trigger[{trigger_pos}] is not None and trigger[XXXX] is not None) and ({complete_condition_str})) or (trigger[{trigger_pos}] is not None and trigger[XXXX] is None and trigger[{above_position}] is None) or (trigger[{trigger_pos}] is not None and (trigger[{above_position}] is None and ({below_condition_str}))) or (trigger[{trigger_pos}] is not None and (trigger[XXXX] is None and ({above_condition_str}))))"
            elif below_condition_str is None:
                if_statement = f"(((trigger[{above_position}] is not None and trigger[{trigger_pos}] is not None) and ({complete_condition_str})) or (trigger[{trigger_pos}] is not None and trigger[{above_position}] is None))"
            elif above_condition_str is None:
                if_statement = f"(((trigger[{trigger_pos}] is not None and trigger[XXXX] is not None) and ({complete_condition_str})) or (trigger[{trigger_pos}] is not None and trigger[XXXX] is None))"

            return [if_statement, trigger_pos, above_position]

    elif trigger_type == CONF_PERS_NOTIFICATION:
        value = entity.expected_value[CONF_UPDATE_TYPE]
        if isinstance(value, str):
            # replace double quotes with single quotes using str.replace()
            value = value.replace('"', "'")
            return [f'trigger[{trigger_pos}] == "{value}"']
        elif isinstance(value, list):
            return [f"trigger[{trigger_pos}] == {value}"]

    elif trigger_type == CONF_DEVICE:
        value = entity.expected_value[CONF_TYPE]
        if isinstance(value, str):
            # replace double quotes with single quotes using str.replace()
            value = value.replace('"', "'")
            return [f'trigger[{trigger_pos}] == "{value}"']
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
    identation_lvl: int = 1,
) -> int:
    """
    Create the trigger condition one trigger entity in the automation script.

    Args:
        trigger_type (str): the type / platform of the trigger
        entity (Entity): the main entity of the trigger
        trigger_pos (int): the position of the trigger in the automation script based on former triggers
        trigger_id (str | None):  the id of the trigger is used to identify the trigger for later call backs of which trigger was triggered
        filepath (str): the path to the automation script file

    Returns:
        int: the new trigger_pos for the next trigger entity (is the next trigger_pos in the automation script)
    """
    # set the combinator for the if statement
    combinator = CONF_OR
    script_context = ""
    identation = "\t" * identation_lvl

    # create the if statement for the trigger list
    if len(entity_list) > 1:
        script_context = identation + IF_TEMPLATE
        # cache for the trigger_pos of the above condition
        above_position = None

        for x in range(0, len(entity_list)):
            # create the trigger expression for the entities
            trigger_expression = _get_trigger_conditional_expression(
                trigger_type, entity_list[x], trigger_pos, above_position
            )

            if x == 0:
                # add the trigger expression to the script without the combinator
                script_context += "(" + trigger_expression[0] + ")\n"
            else:
                # add the trigger expression to the script with the combinator
                script_context += f"{identation}\t{combinator} (" + trigger_expression[0] + ")\n"

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
        script_context = identation + IF_TEMPLATE + trigger_expression[0]

        # set the trigger_pos for the next trigger expression
        if trigger_type == CONF_NUMERIC_STATE or trigger_type == CONF_STATE:
            trigger_pos = trigger_expression[1]
        trigger_pos += 1

    # close the if statement
    script_context += identation + END_IF_TEMPLATE

    if trigger_type == CONF_NUMERIC_STATE:
        if "XXXX" in script_context:
            script_context = script_context.replace("XXXX", str((trigger_pos)))
            trigger_pos += 1

    # add the trigger_id to the script and the triggered flag
    if trigger_id is None:
        script_context += f"{identation}\ttrigger_id = None\n\t\ttriggered = True\n\n"
    else:
        script_context += f"{identation}\ttrigger_id = '{trigger_id}' \n{identation}\ttriggered = True\n\n"
    _append_script_context_to_script(filepath, script_context)

    return trigger_pos


def create_trigger_script(
    trigger_type: str,
    entity: Entity,
    trigger_pos: int,
    trigger_id: str | None,
    filepath: str,
    identation_lvl: int = 1,
) -> int:
    """
    Create the trigger condition one trigger entity in the automation script.

    Args:
        trigger_type (str): the type / platform of the trigger
        entity (Entity): the main entity of the trigger
        trigger_pos (int): the position of the trigger in the automation script based on former triggers
        trigger_id (str | None):  the id of the trigger is used to identify the trigger for later call backs of which trigger was triggered
        filepath (str): the path to the automation script file

    Returns:
        int: the new trigger_pos for the next trigger entity (is the next trigger_pos in the automation script)
    """
    identation = "\t" * identation_lvl

    # create the trigger expression for the entity
    trigger_expression = _get_trigger_conditional_expression(
        trigger_type, entity, trigger_pos
    )
    # complete the trigger expression for the entity
    script_context = identation + IF_TEMPLATE + trigger_expression[0] + "):\n"

    # set the trigger_pos for the next trigger expression and replace the XXXX with the trigger_pos of the below condition
    if trigger_type == CONF_NUMERIC_STATE or trigger_type == CONF_STATE:
        trigger_pos = trigger_expression[1]

        if trigger_type == CONF_NUMERIC_STATE and "XXXX" in script_context:
            trigger_pos += 1
            script_context = script_context.replace("XXXX", str((trigger_pos)))

    # add the trigger_id to the script and the triggered flag
    if trigger_id is None:
        script_context += f"{identation}\ttrigger_id = None\n{identation}\ttriggered = True\n\n"
    else:
        script_context += f"{identation}\ttrigger_id = '{trigger_id}' \n{identation}\ttriggered = True\n\n"
    _append_script_context_to_script(filepath, script_context)

    return trigger_pos + 1


def close_trigger_section(filepath: str) -> None:
    """
    Close the trigger section in the automation script.

    Args:
        filepath (str): The path to the automation script file.
    """
    script_context = "\t# The end of the trigger section\n\treturn {'triggered': triggered, 'trigger_id' : trigger_id}\n\n"
    _append_script_context_to_script(filepath, script_context)


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

    _append_script_context_to_script(filepath, script_content)


def _get_condition_expression(
    condition_type: str, entity: Entity, condition_pos: int, above_position: int = None
) -> list:
    """
    Create the conditional expression for the condition.

    Args:
        condition_type (str): Depending on the condition type, the conditional expression is created.
        entity (Entity): The entity is used to create the conditional expression based on the expected value.
        condition_pos (int): The real position of the condition in the automation script.
        above_position (int, optional): The position of the above entity in the automation script.

    Returns:
        str: The conditional expression for the condition.
    """
    
    if condition_type == CONF_STATE:
        comparison_str = "("
        # In contrast to the trigger expression, the condition expression can't be None
        value = entity.expected_value[CONF_STATE]
        
        if isinstance(value, list):
            # start position for the condition entities
            current_comparing_entity_pos = condition_pos
            if above_position is None:
                    for value in entity.expected_value[CONF_STATE]:
                        if valid_entity_id(str(value)):
                            above_position = condition_pos
                            condition_pos += 1
            start_val = True
            for value in entity.expected_value[CONF_STATE]:
                # set an or before the next comparison
                if start_val:
                    start_val = False
                else:
                    comparison_str += " or "

                if valid_entity_id(str(value)):
                    comparison_str += f"condition[{condition_pos}] == condition[{current_comparing_entity_pos}]"
                    current_comparing_entity_pos += 1
                else:
                    if isinstance(value, str):
                        # replace double quotes with single quotes using str.replace()
                        value = value.replace('"', "'")
                        comparison_str += f'condition[{condition_pos}] == "{value}"'
                    else:
                        comparison_str += f"condition[{condition_pos}] == {value}"
                    
            comparison_str += ")"
        
        else:
            if above_position is None:
                if valid_entity_id(str(value)):
                    above_position = condition_pos
                    condition_pos += 1
            
            if valid_entity_id(str(value)):
                comparison_str += f"condition[{condition_pos}] == condition[{above_position}])"
            else:
                if isinstance(value, str):
                    # replace double quotes with single quotes using str.replace()
                    value = value.replace('"', "'")
                    comparison_str += f'condition[{condition_pos}] == "{value}")'
                else:
                    comparison_str += f"condition[{condition_pos}] == {value})"
    
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
                    comparison_str = f"condition[{above_position}] < "
                else:
                    above_position = condition_pos
                    comparison_str = f"condition[{condition_pos}] < "

                # cache the above condition
                above_condition_str = comparison_str

        # move the condition_pos after the above condition
        if above_condition_str is not None:
            if above_position == condition_pos:
                condition_pos += 1
            middle_condition_str = f"condition[{condition_pos}]"
            comparison_str += middle_condition_str
            # complete the above condition
            above_condition_str += middle_condition_str
        else:
            middle_condition_str = f"condition[{condition_pos}]"
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
                comparison_str += " < condition[XXXX]"
                # cache the below condition
                below_condition_str = f"{middle_condition_str} < condition[XXXX]"

        # add the none exception for the entity values to the condition
        if above_condition_str is None and below_condition_str is None:
            return [
                f"({comparison_str})",
                condition_pos,
                above_position,
            ]
        else:
            # create the if statement for the condition entities and handle the None exception
            if_statement = f"({comparison_str})"
            
            return [if_statement, condition_pos, above_position]

    # template, sun
    else:
        return [f"condition[{condition_pos}]"]

def create_combination_condition_script(
    condition_type: str,
    entity_list: list,
    condition_pos: int,
    filepath: str,
    identation_lvl: int = 1,
) -> int:
    """
    Create the condition of multiple condition entities in the automation script.

    Args:
        condition_type (str): The type of the condition.
        entity_list (list): The list of entities of the condition.
        condition_pos (int): The real position of the condition in the automation script.
        filepath (str): The path to the automation script file.

    Returns:
        int: The new condition_pos for the next condition entity (is the next condition_pos in the automation script).
    """
    # set the combinator for the if statement
    combinator = CONF_AND
    script_context = ""
    identation = "\t" * identation_lvl

    # create the if statement for the condition list
    if len(entity_list) > 1:
        
        # if its not part of an logic block
        if identation_lvl == 1:
            script_context += identation + IF_TEMPLATE
        else:
            script_context += "(\n"
            # identation = "\t" * (identation_lvl + 1)
        # cache for the condition_pos of the above condition
        above_position = None

        for x in range(0, len(entity_list)):
            # create the condition expression for the entities
            condition_expression = _get_condition_expression(
                condition_type, entity_list[x], condition_pos, above_position
            )

            if x == 0:
                # if its not part of an logic block
                if identation_lvl == 1:
                    # add the trigger expression to the script without the combinator
                    script_context +=  condition_expression[0] + "\n"
                else:
                    script_context += identation + condition_expression[0] + "\n"
            else:
                # add the trigger expression to the script with the combinator
                script_context += f"{identation}{combinator} (" + condition_expression[0] + ")\n"

            # set the condition_pos for the next trigger expression
            if condition_type == CONF_NUMERIC_STATE:
                condition_pos = condition_expression[1]
                above_position = condition_expression[2]
            condition_pos += 1
    
    elif len(entity_list) == 1:
        # create the trigger expression for the entities
        condition_expression = _get_condition_expression(
            condition_type, entity_list[0], condition_pos
        )
        
        # if its not part of an logic block
        if identation_lvl == 1:
            # add the first trigger expression to the script
            script_context = identation + IF_TEMPLATE + condition_expression[0]
        else:
            script_context = identation + condition_expression[0]

        # set the condition_pos for the next trigger expression
        if condition_type == CONF_NUMERIC_STATE or condition_type == CONF_STATE:
            condition_pos = condition_expression[1]
        condition_pos += 1

    # if its not part of an logic block
    if identation_lvl == 1:
        # close the if statement
        script_context += identation + END_IF_TEMPLATE
    else:
        script_context += identation + ")\n"

    if condition_type == CONF_NUMERIC_STATE:
        if "XXXX" in script_context:
            script_context = script_context.replace("XXXX", str((condition_pos)))
            condition_pos += 1
    
    # if its not part of an logic block
    if identation_lvl == 1:
        # add the trigger_id to the script and the triggered flag
        script_context += f"{identation}\tcondition_passed = True\n\n"
    _append_script_context_to_script(filepath, script_context)

    return condition_pos


def create_condition_script(
    condition_type: str,
    entity: Entity,
    condition_pos: int,
    filepath: str,
    identation_lvl: int = 1,
) -> int:
    """
    Create the condition of one ondition entity in the automation script.

    Args:
        condition_type (str): The type of the condition.
        entity (Entity): The entity of the condition.
        condition_pos (int): The position of the condition in the automation script based on former conditions.
        filepath (str): The path to the automation script file.

    Returns:
        int: The new condition_pos for the next condition entity (is the next condition_pos in the automation script).
    """
    identation = "\t" * identation_lvl
    
    # create the trigger expression for the entity
    condition_expression = _get_condition_expression(
        condition_type, entity, condition_pos
    )
    
    # if its not part of an logic block
    if identation_lvl == 1:
        # complete the condition expression for the entity
        script_context = identation + IF_TEMPLATE + condition_expression[0] + "):\n"
    else:
        script_context = condition_expression[0] + "\n"

    # set the condition_pos for the next condition expression
    if condition_type == CONF_NUMERIC_STATE or condition_type == CONF_STATE:
        condition_pos = condition_expression[1]

        if condition_type == CONF_NUMERIC_STATE and "XXXX" in script_context:
            condition_pos += 1
            script_context = script_context.replace("XXXX", str((condition_pos)))

    
    # if its not part of an logic block
    if identation_lvl == 1:
        # add the condition_id to the script and the condition_passed flag
        script_context += f"{identation}\tcondition_passed = True\n\n"
    _append_script_context_to_script(filepath, script_context)

    return condition_pos + 1


def start_logic_function_block(
    condition_type: str,
    filepath: str,
    identation_lvl: int = 1) -> None:
    """
    start the function block for the logic connection of condition in the automation script.
    
    Args:
        condition_type (str): The type of the condition (CONF_OR, CONF_AND, CONF_NOT).
        condition_pos (int): The position of the condition in the automation script based on former conditions.
        filepath (str): The path to the automation script file.
        identation_lvl (int, optional): The identation level of the function block. Defaults to 1.
    """
    identation = "\t" * identation_lvl
    
    script_context = f"{identation}if (\n\t{identation}"
    if condition_type == CONF_NOT:
        script_context += "not "
    _append_script_context_to_script(filepath, script_context)

def create_next_logic_condition_part(condition_type: str, filepath: str, identation_lvl: int = 2) -> None:
    """
    Create the next logic condition part in the automation script.
    """
    identation = "\t" * (identation_lvl + 1) 

    # TODO make it look better with the identation 
    if condition_type == CONF_OR:
        script_context = f"{identation}or "
    elif condition_type == CONF_AND:
        script_context = f"{identation}and "
    elif condition_type == CONF_NOT:
        script_context = f"{identation}and not "
    _append_script_context_to_script(filepath, script_context)

def close_logic_function_block(filepath, identation_lvl: int = 2)-> None:
    """
    close the function block for the logic connection of condition in the automation script.
    """
    identation = "\t" * identation_lvl
    
    script_context = f"{identation}):\n{identation}\tcondition_passed = True\n\n"
    _append_script_context_to_script(filepath, script_context)



def close_condition_section(filepath: str) -> None:
    """
    Close the condition section in the automation script.

    Args:
        filepath (str): The path to the automation script file.
    """
    script_context = "\t# The end of the condition section\n\treturn {'condition_passed': condition_passed}\n\n"
    _append_script_context_to_script(filepath, script_context)


def close_script(filepath: str) -> None:
    """
    Close the automation script.

    Args:
        filepath (str): The path to the automation script file.
    """

    main_function_template = path.join(TEMPLATE_PATH, "run_main_template.py")
    try:
        with open(main_function_template, "r") as file:
            script_content = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Template file {main_function_template} not found")
    # ! tabs aren't taken into account and are converted to 4 spaces
    script_content = script_content.replace("    ", "\t")

    _append_script_context_to_script(filepath, script_content)


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
