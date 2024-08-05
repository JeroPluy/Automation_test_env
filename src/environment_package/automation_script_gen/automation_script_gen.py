"""
This module is responsible for initializing the automation script which simulates the automation and 
provides basic functions for the other specialized parts.

"""

from os import path
from environment_package.env_const import AUTOMATION_SCRIPT

TEMPLATE_PATH = path.join("src", "environment_package", "automation_script_gen", "automation_script_templates")


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
