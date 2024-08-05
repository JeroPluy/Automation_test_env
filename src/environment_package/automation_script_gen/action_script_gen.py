"""
This module is used to generate the action part for the automation script.
"""

from os import path

from environment_package.automation_script_gen.automation_script_gen import TEMPLATE_PATH, _append_script_context_to_script, close_script
from environment_package.env_helper import Entity
from environment_package.ha_automation.home_assistant_const import CONF_DEVICE, CONF_EVENT, CONF_FOR, CONF_FOR_EACH, CONF_SERVICE, CONF_UNTIL, CONF_WHILE

END_IF_TEMPLATE = "):\n"

def init_action_part(filepath: str) -> None:
    """
    Initialize the action part in the automation script.

    Args:
        filepath (str): The path to the automation script file.
    """
    action_template = path.join(TEMPLATE_PATH, "action_template.py")
    try:
        with open(action_template, "r") as file:
            script_content = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Template file {action_template} not found")
    # ! tabs aren't taken into account and are converted to 4 spaces
    script_content = script_content.replace("    ", "\t")

    _append_script_context_to_script(filepath, script_content)


def start_action_condition_block(
    filepath: str, indentation_lvl: int = 1, first_element=True, not_condition=False
) -> None:
    """
    Start the condition block in the action part of the automation script.

    Args:
        filepath (str): The path to the automation script file.
        indentation_lvl (int, optional): The indentation level of the condition block. Defaults to 1.

    Returns:
        int: The new indentation level for the conditions in the condition block and the actions afterwards.
    """
    indentation = "\t" * indentation_lvl
    
    if first_element:
        if_level = "if"
    else:
        if_level = "elif"

    if not_condition:
        script_context = f"{indentation}{if_level} not (\n"
    else:
        script_context = f"{indentation}{if_level} (\n"
    _append_script_context_to_script(filepath, script_context)

    return indentation_lvl + 1


def close_action_condition_block(
    filepath: str,
    indentation_lvl: int = 1,
    no_condition: bool = False,
    timeout: bool = None,
) -> None:
    """
    Closing of the condition block in the action part of the automation script
    based on additional inputs like if the condition has a timeout or no conditional expressions.

    Args:
        filepath (str): The path to the automation script file.
        indentation_lvl (int, optional): The indentation level of the condition block. Defaults to 1.
        no_condition (bool, optional): If no entity is given to the condition.
        timeout (bool): Is a timeout for the wait for trigger section in the automation.
    """
    indentation = "\t" * (indentation_lvl)
    script_context = ""

    if no_condition:
        script_context += f"{indentation}\t False\n"

    if timeout:
        script_context += f" or True{END_IF_TEMPLATE}"
    else:
        script_context += f"{indentation}{END_IF_TEMPLATE}"

    _append_script_context_to_script(filepath, script_context)

    if timeout is not None:
        create_stopping_action(filepath, indentation_lvl, timeout)


def create_stopping_action(
    filepath: str, indentation_lvl: int, timeout: bool
) -> None:  #
    """
    Creates a interrupt in the automation script.

    Args:
        filepath (str): The path to the automation script file.
        indentation_lvl (int): The indentation level of the wait for trigger section in the automation script.
    """
    indentation = "\t" * indentation_lvl

    script_context = (
        f"{indentation}\tprint(json.dumps(action_results))\n{indentation}\treturn\n\n"
    )

    _append_script_context_to_script(filepath, script_context)


def create_empty_action_section(filepath: str, indentation_lvl: int) -> None:
    """
    Create an empty action section in the automation script.

    Args:
        filepath (str): The path to the automation script file.
        indentation_lvl (int): The indentation level of the action section in the automation script.
    """
    indentation = "\t" * indentation_lvl

    script_context = f"{indentation}pass\n"
    _append_script_context_to_script(filepath, script_context)


def create_else_action_section(filepath: str, indentation_lvl: int) -> None:
    """
    Create the else section in a branching part of the automation script.

    Args:
        filepath (str): The path to the automation script file.
        indentation_lvl (int): The indentation level of the else section in the automation script.
    """
    indentation = "\t" * (indentation_lvl - 1)

    script_context = f"{indentation}else:\n"
    _append_script_context_to_script(filepath, script_context)


def start_action_loop_block(
    loop_type: str, filepath: str, indentation_lvl: int, loop_settings: list
) -> int:
    """
    Start the loop block in the action part of the automation script.

    Args:
        loop_type (str): The type of the loop (CONF_FOR_EACH, CONF_WHILE, CONF_UNTIL, CONF_FOR).
        filepath (str): The path to the automation script file.
        indentation_lvl (int): The indentation level of the loop block.
        loop_settings (list): The settings for the loop. (the entity list for the loop or the range for the loop)

    Returns:
        int: The new indentation level for the actions in the loop block.
    """

    indentation = "\t" * indentation_lvl

    # loop initialization with the setting variables
    script_context = f"{indentation}first_loop = True\n{indentation}infinite_loop = False \n{indentation}output_counter = []\n\n"

    # creating the loop header with a counting variable for every output in the loop
    if loop_type == CONF_FOR_EACH:
        script_context += (
            f"{indentation}for action in {loop_settings}:\n{indentation}\toutput = 0\n"
        )

    # both loops get interupted by a if satetment with the condition of the loop
    elif loop_type == CONF_WHILE or loop_type == CONF_UNTIL:
        script_context += f"{indentation}loop_is_running = True\n{indentation}while (loop_is_running):\n{indentation}\toutput = 0\n"
    elif loop_type == CONF_FOR:
        script_context += f"{indentation}for x in range({loop_settings[0]},{loop_settings[1]}):\n{indentation}\toutput = 0\n"

    _append_script_context_to_script(filepath, script_context)

    return indentation_lvl + 1


def create_action_loop_stop(
    filepath: str, indentation_lvl: int, loop_type: str
) -> None:
    """
    Create the interrupt for the loop block.

    Args:
        filepath (str): The path to the automation script file.
        indentation_lvl (int): The indentation level of the loop block.
        loop_type (str): The type of the loop (CONF_FOR_EACH, CONF_WHILE, CONF_UNTIL, CONF_FOR).
    """
    indentation = "\t" * indentation_lvl

    script_context = f"{indentation}\tloop_is_running = False\n"

    if loop_type == CONF_WHILE:
        script_context += f"{indentation}\tbreak\n"
    # make space to the starting loop block
    script_context += "\n"

    _append_script_context_to_script(filepath, script_context)


def close_action_loop_block(
    filepath: str, indentation_lvl: int, is_infinite: bool, loop_tpye: str
) -> None:
    """
    Creates a counting, combining and possible aborting of the loop block.

    Args:
        loop_type (str): The type of the loop (CONF_FOR_EACH, CONF_WHILE, CONF_UNTIL, CONF_FOR).
        filepath (str): The path to the automation script file.
        indentation_lvl (int): The indentation level of the loop block
        is_infinite (bool): Is the loop an infinite loop by the condition of the loop.
    """
    indentation = "\t" * (indentation_lvl - 1)
    script_context = ""

    # set the first_loop variable to False
    script_context += f"{indentation}\tif first_loop:\n"
    script_context += f"{indentation}\t\tfirst_loop = False\n\n"

    # if the loop is infinite, the loop is running to be stopped by the condition
    if is_infinite or loop_tpye == CONF_UNTIL or loop_tpye == CONF_WHILE:
        script_context += f"{indentation}\t# The loop would continue infinitly. Thats why its stopped after one iteration\n"
        script_context += f"{indentation}\tif loop_is_running:\n"
        script_context += (
            f"{indentation}\t\tinfinite_loop = True\n{indentation}\t\tbreak\n\n"
        )

    script_context += (
        f"{indentation}# map the call counters to the outputs of the loop\n"
    )
    script_context += f"{indentation}for x in range(0, len(action_results)):\n"
    script_context += f"{indentation}\tif infinite_loop:\n"
    script_context += f"{indentation}\t\taction_results[x]['count'] = 'infinite'\n"
    script_context += f"{indentation}\telse:\n"
    script_context += (
        f"{indentation}\t\taction_results[x]['count'] = output_counter[x]\n\n"
    )

    _append_script_context_to_script(filepath, script_context)

    return indentation_lvl - 1


def create_action_script(
    action_type: str,
    entity: Entity,
    filepath: str,
    indentation_lvl: int = 1,
    loop_action: bool = False,
) -> None:
    """
    Create the outputs for the action part of the automation script.

    Args:
        action_type (str): The type of the action which is an output (CONF_EVENT, CONF_DEVICE, CONF_SERVICE).
        entity (Entity): The entity which is the output of the action.
        filepath (str): The path to the automation script file.
        indentation_lvl (int, optional): The indentation level of the action part. Defaults to 1.
        loop_action (bool, optional): If the action is part of a loop it need special implementation for counting its calls.
                                      Defaults to False.
    """
    
    indentation = "\t" * indentation_lvl
    script_context = ""
    result = ""

    if action_type == CONF_EVENT:
        result = "{" + f"'{entity.integration}': {entity.expected_value}" + "}"
    elif action_type == CONF_DEVICE:
        result = (
            "{"
            + f"'{entity.entity_name}':'{entity.expected_value[CONF_SERVICE]}'"
            + "}"
        )
    elif action_type == CONF_SERVICE:
        result = (
            "{"
            + f"'{entity.entity_name}':'{entity.expected_value[CONF_SERVICE]}'"
            + "}"
        )

    if loop_action:
        # make a loop action with a call counter for every output
        script_context = f"{indentation}if first_loop:\n"
        script_context += f"{indentation}\taction_results.append({result})\n"
        script_context += f"{indentation}\toutput_counter.append(1)\n"
        script_context += f"{indentation}else:\n"
        script_context += f"{indentation}\toutput_counter[output] += 1\n"
        script_context += f"{indentation}\toutput += 1\n\n"
    else:
        script_context = f"{indentation}action_results.append({result})\n\n"

    _append_script_context_to_script(filepath, script_context)


def close_action_section(filepath: str) -> None:
    """
    Close the action section in the automation script and add the final print statement.
    It is also calling the function to close the script.

    Args:
        filepath (str): The path to the automation script file.
    """
    script_context = (
        "\n\t# The end of the action section\n\tprint(json.dumps(action_results))\n\n"
    )
    _append_script_context_to_script(filepath, script_context)

    close_script(filepath)
