from os import listdir, path
import asyncio
import json
from environment_package.config_dissection import (
    Automation,
    Entity,
    create_automation,
    _extract_all_conditions,
    _extract_all_trigger,
    create_procedure_list,
)
from environment_package.automation_script_gen import create_locked_message, init_automation_script
import environment_package.db as db
from environment_package.ha_automation import home_assistant_yaml_loader as yaml_loader
from environment_package.ha_automation import (
    home_assistant_automation_validation as ha_automation_config,
)

import sqlite3 as sqlite
import subprocess

DATABASE = path.join("data", "automation_test_env.sqlite")


def test_all_yaml_files():
    automations = []
    yaml_dir = path.join("test_data", "yaml_files")
    for file in listdir(yaml_dir):
        if file.endswith(".yaml"):
            basis_file = path.join(yaml_dir, file)
            automation_yaml = yaml_loader.load_yaml_dict(basis_file)
            automation_config = asyncio.run(
                ha_automation_config.async_validate_config_item(automation_yaml)
            )
            print(" --- " + automation_config.automation_name + " --- ")
            extract_information = create_automation(automation_config)
            entity: Entity = None
            for entity in extract_information["entities"]:
                role = (
                    "in"
                    if entity.parameter_role == 1
                    else "out"
                    if entity.parameter_role == 2
                    else "start"
                )
                print(
                    role
                    + ": \t \t"
                    + str(entity.parent)
                    + ": \t"
                    + str(entity.position)
                    + ": \t"
                    + entity.entity_name
                    + " : \t"
                    + str(entity.expected_value)
                )
            automations.append(extract_information)
    return automations


def test_script_init(basis_file: str):
    automation_yaml = yaml_loader.load_yaml_dict(basis_file)
    automation_config = asyncio.run(
        ha_automation_config.async_validate_config_item(automation_yaml)
    )
    file_path = init_automation_script(automation_config.automation_name)
    print("Script created at: " + file_path)
    return file_path


def run_automation(script_path, trigger_inputs: list, condition_inputs: list, combined_inputs: list = None, automation: Automation = None):    
    """run the automation script and return the result

    Args:
        automation (Automation): the automation to run

    Returns:
        str: the result of the automation
    """
    if combined_inputs is None:
        input_vals = [trigger_inputs, condition_inputs]
    else:
        input_vals = combined_inputs
    
    serialized_inputs = json.dumps(input_vals)
        
    if automation is None:
        automation = Automation("test_automation", script_path)
    result = subprocess.run(
        ["python", automation.script, serialized_inputs], capture_output=True
    )
    return result.stdout.decode("utf-8")


def test_trigger_entities():
    basis_file = path.join(
        "test_data", "yaml_files", "test_yaml", "entity_extraction_test.yaml"
    )
    script_file = test_script_init(basis_file)
    automation_yaml = yaml_loader.load_yaml_dict(basis_file)
    automation_config = asyncio.run(
        ha_automation_config.async_validate_config_item(automation_yaml)
    )
    print(" --- " + automation_config.automation_name + " --- ")
    extracted_entities = _extract_all_trigger(automation_config, script_file)
    entity: Entity = None
    for entity in extracted_entities:
        role = (
            "in"
            if entity.parameter_role == 1
            else "out"
            if entity.parameter_role == 2
            else "start"
        )
        print(
            role
            + ": \t \t"
            + str(entity.parent)
            + ": \t"
            + str(entity.position)
            + ": \t"
            + entity.entity_name
            + " : \t"
            + str(entity.expected_value)
        )


def test_condition_entities():
    basis_file = path.join(
        "test_data", "yaml_files", "test_yaml", "entity_extraction_test.yaml"
    )
    script_file = script_file = test_script_init(basis_file)
    automation_yaml = yaml_loader.load_yaml_dict(basis_file)
    automation_config = asyncio.run(
        ha_automation_config.async_validate_config_item(automation_yaml)
    )
    print(" --- " + automation_config.automation_name + " --- ")
    extracted_entities = _extract_all_conditions(automation_config, script_file)
    entity: Entity = None
    for entity in extracted_entities:
        role = (
            "in"
            if entity.parameter_role == 1
            else "out"
            if entity.parameter_role == 2
            else "start"
        )
        print(
            role
            + ": \t \t"
            + str(entity.parent)
            + ": \t"
            + str(entity.position)
            + ": \t"
            + entity.entity_name
            + " : \t"
            + str(entity.expected_value)
        )


def test_action_entities():
    basis_file = path.join("test_data", "yaml_files", "watering_the_garden.yaml")
    script_file = script_file = test_script_init(basis_file)
    automation_yaml = yaml_loader.load_yaml_dict(basis_file)
    automation_config = asyncio.run(
        ha_automation_config.async_validate_config_item(automation_yaml, script_file)
    )
    print(" --- " + automation_config.automation_name + " --- ")
    extracted_entities = create_procedure_list(automation_config)
    entity: Entity = None
    for entity in extracted_entities:
        role = (
            "in"
            if entity.parameter_role == 1
            else "out"
            if entity.parameter_role == 2
            else "start"
        )
        print(
            role
            + ": \t \t"
            + str(entity.parent)
            + ": \t"
            + str(entity.position)
            + ": \t"
            + entity.entity_name
            + " : \t"
            + str(entity.expected_value)
        )

def test_entity_list():
    basis_file = path.join("test_data", "yaml_files", "test_yaml", "entity_extraction_test.yaml")
    script_file = script_file = test_script_init(basis_file)
    automation_yaml = yaml_loader.load_yaml_dict(basis_file)
    automation_config = asyncio.run(
        ha_automation_config.async_validate_config_item(automation_yaml)
    )
    print(" --- " + automation_config.automation_name + " --- ")
    extracted_entities = create_procedure_list(automation_config, script_file)
    entity: Entity = None
    for entity in extracted_entities:
        role = (
            "in"
            if entity.parameter_role == 1
            else "out"
            if entity.parameter_role == 2
            else "start"
        )
        print(
            role
            + ": \t \t"
            + str(entity.parent)
            + ": \t"
            + str(entity.position)
            + ": \t"
            + entity.entity_name
            + " : \t"
            + str(entity.expected_value)
        )

if __name__ == "__main__":
    # Automation to test basis parameters
    basis_file = path.join(
        "test_data", "yaml_files", "turn_off_living_room_main_light_event.yaml"
    )
    # basis_file = os.path.join('test_data','yaml_files', 'test_yaml', 'basis_automation.yaml')

    # test_trigger_entities()
    # test_condition_entities()
    # test_action_entities()
    
    test_entity_list()

    # file_path = test_script_generation(basis_file)
    

    # test_all_yaml_files()

    # automation: Automation = extract_information["infos"]
    # script_path = path.join("data", "automation_scripts", "entity_extraction_test.py")
    # 
    # print( "result of the automation: " + run_automation(script_path=script_path, trigger_inputs=[True, False, False], condition_inputs=[]))
