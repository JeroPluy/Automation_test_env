"""
This test script is used to test the functionality of the backend functions.

If the dont work properly, because some modules are not found, please run the following commands in the terminal:

$env:PYTHONPATH = "..\\src"

In some environments, the PYTHONPATH needs to be set to the src directory.
"""

from asyncio import run as async_run
from os import path

from backend.automation_testing.test_execution import run_async_automation, run_sync_automation
from backend.utils.env_const import LATEST

from backend import automation_gen as ag 
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
        
        
        yaml_path = path.join("test_data", "yaml_files", "example_automations", LATEST , yaml_file)
        
        automation_data = ag.load_new_automation_data(yaml_path)
        db.add_automation(automation_data)
        
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
