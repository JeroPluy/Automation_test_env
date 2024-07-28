"""
This module is responsible for generating the automation script which simulates the automation.

"""

from os import path
from environment_package.env_const import AUTOMATION_SCRIPT



TEMPLATE_PATH = path.join('src','environment_package','automation_script_templates')

def init_automation_script(automation_name) -> str:
    file_name = automation_name + ".py"
    filepath = path.join(AUTOMATION_SCRIPT, file_name)

    init_template = path.join(TEMPLATE_PATH, "init_template.py")
    try:
        with open(init_template, 'r') as file:
            script_content = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Template file {init_template} not found")

    with open(filepath, "w") as script:
        script.write(script_content)
    return filepath
    

def create_trigger_script(trigger_info: list) -> str:
     pass
            
            

# def _append_template_to_script(filepath: str, template_name: str) -> None:
#     template_path = path.join(TEMPLATE_PATH, template_name +".py")
#     try:
#         with open(template_path, 'r') as file:
#             template_content = file.read()
#     except FileNotFoundError:
#         raise FileNotFoundError(f"Template file {template_path} not found")
    
#     with open(filepath, "a") as script:
#         script.write( '\n' + template_content)
#     return filepath


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
        
    script_content.insert(5, locked_message + '\n')
    
    with open(filepath, "w") as script:
        script.writelines(script_content)
    return filepath

