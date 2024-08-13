"""
This module is responsible for initializing the automation script which simulates the automation and 
provides basic functions for the other specialized parts.

"""

from os import listdir, path
from ...utils.env_const import AUTOMATION_SCRIPT, TEMPLATE_PATH


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
    file_name = automation_name + "_V_1.py"
        
    if dir_path is None:
        dir_path = AUTOMATION_SCRIPT
        filepath = path.join(dir_path, file_name)
    else:
        # for testing purposes
        filepath = path.join(dir_path, file_name)
    
    # check if the file already exists
    if path.exists(filepath):
        latest_version = 0
        
        # itterate over all files in the directory look for the latest version of the automation
        for file in listdir(dir_path):
            if file.startswith(f"{automation_name}_"):
                # get the version number 
                file_version = int(file.split("_V_")[-1].split(".")[0])
                # update the latest version
                if file_version > latest_version:
                    latest_version = file_version
        
        # increment the version number
        file_name = f"{automation_name}_V_{latest_version + 1}.py"
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


def append_script_context_to_script(filepath: str, script_context: str) -> None:
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

    append_script_context_to_script(filepath, script_content)


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
