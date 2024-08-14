"""
This test script is used to test the functionality of the backend functions.

If the dont work properly, because some modules are not found, please run the following commands in the terminal:

$env:PYTHONPATH = "..\\src"

In some environments, the PYTHONPATH needs to be set to the src directory.
"""

from asyncio import (
    create_subprocess_exec as create_aync_subprocess_exec,
    subprocess as async_subprocess,
    run as async_run,
)
import json
from os import path
import subprocess

from backend.utils.env_helper_classes import Automation, Entity

from backend.automation_gen import add_new_automation
from backend.database import src as db

DATABASE = path.join("data", "automation_test_env.sqlite")
TEST_SCRIPT_DIR = path.join("src", "test", "test_automation_gen", "test_scripts")

def print_entity_data(entity):
    """
    This function prints the entity data

    Args:
        entity (): the entity to print out
    """
    # make the parameter role readable (0=start, 1=condition, 2=action-condition, 3=action)
    role = (
        "start"
        if entity[0] == 0
        else "con"
        if entity[0] == 1
        else "action-con"
        if entity[0] == 2
        else "out"
        if entity[0] == 3
        else "unknown"
    )

    indentation = ": \t" if entity[0] == 2 else ": \t\t"

    print(
        role
        + indentation
        + str(entity[1])
        + ": \t"
        + str(entity[2])
        + ": \t"
        + entity[3]
        + " : \t"
        + str(entity[4])
    )


def run_sync_automation(
    script_path,
    inputs: list,
    automation: Automation = None,
):
    """
    run the automation synchronously and return the result

    Args:
        script_path (str): the path to the automation script
        inputs (list): the inputs for the automation inputs.
        automation (Automation): the automation to run

    Returns:
        str: the result of the automation
    """

    serialized_inputs = json.dumps(inputs)

    if automation is None:
        automation = Automation("test_automation", script_path)
    result = subprocess.run(
        ["python", automation.script, serialized_inputs], capture_output=True
    )
    return result.stdout.decode("utf-8")


async def run_async_automation(script_path, inputs: list):
    """
    The function calls the automation script and returns the result

    Args:
        srcript_path (str): the path to the automation script
        inputs (list): the inputs for the automation inputs
        containing the trigger, condition and action inputs as lists

    Returns:
        str: the result of the automation
    """

    serialized_inputs = json.dumps(inputs)

    command = ["python", script_path, serialized_inputs]

    # async implementation
    # starts the async process
    proc = await create_aync_subprocess_exec(
        *command,
        stdout=async_subprocess.PIPE,  # get the standard output
        stderr=async_subprocess.PIPE,  # Optional: get error messages
    )

    # wait for the process to finish and decode the output
    stdout, stderr = await proc.communicate()

    output = json.loads(stdout.decode("utf-8"))

    return output


if __name__ == "__main__":
    
    # path to the automation script file which is to be tested
    automation_name = "Turn_off_living_room_main_light"
    
    # please add the automation.yaml file to the test_data/yaml_files/example_automations folder
    yaml_file = "turn_off_living_room_main_light.yaml"
    
    autoamtion_file = path.join(
        "data", "automation_scripts", automation_name + "_V_1.py"
    )

    # check if the file exists and look for the yaml file if it does not
    if not path.isfile(autoamtion_file):
        print(f"File {autoamtion_file} does not exist")
        
        yaml_path = path.join("test_data", "yaml_files", "example_automations", yaml_file)
        
        # please add the automation.yaml file to the test_data/yaml_files/example_automations folder
        add_new_automation(yaml_path)
        
    entity_list = db.get_entities(automation_name=automation_name)
    for entity in entity_list:
        print_entity_data(entity)

    # the inputs for the automation script turn_off_living_room_main_light
    # start:          None:   0:      binary_sensor.moving_living_room :      {'to': 'off', 'from': 'on', 'for': {'hours': 0, 'minutes': 7, 'seconds': 0}}
    # start:          None:   1:      binary_sensor.person_living_room :      {'to': 'off', 'from': 'on', 'for': {'hours': 0, 'minutes': 7, 'seconds': 0}}
    # con:            None:   0:      light.main_light_living_room :  {'state': 'on'}
    # action-con:     None:   1:      media_player.living_room :      {'state': 'playing'}

    trigger_input_vals = [None, "off"]
    condition_input_vals = ["on"]
    action_input_vals = ["paused"]
    

    input_vals = [trigger_input_vals, condition_input_vals, action_input_vals]

    sync_result = run_sync_automation(autoamtion_file, input_vals)

    async_result = async_run(run_async_automation(autoamtion_file, input_vals))

    print(sync_result)
    print(async_result)
