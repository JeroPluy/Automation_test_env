"""
This test script is used to test the functionality of the backend functions.

The python_path needs to be set to the src directory: (for venv)
$env:PYTHONPATH = "..\\src"
"""

from os import listdir, path
import asyncio
import json

from backend.automation_gen.condtion_dissection import extract_all_conditions
from backend.automation_gen.trigger_dissection import extract_all_trigger

from backend.automation_gen.config_dissection import (
    Automation,
    create_automation,
    create_procedure_list,
)


from backend.automation_gen.automation_script_gen import create_locked_message, init_automation_script
import backend.database
from backend.ha_automation_utils import home_assistant_yaml_loader as yaml_loader
from backend.ha_automation_utils import (
    home_assistant_automation_validation as ha_automation_config,
)

import sqlite3 as sqlite
import subprocess

from backend.utils.env_helper import Entity


DATABASE = path.join("data", "automation_test_env.sqlite")


def test_all_yaml_files() -> list:
    """
    Test all yaml files in the test_data/yaml_files directory

    Returns:
        list: list of automations with their extracted entities and information
    """
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
            if not (automation_config.validation_status == "ok") and not (automation_config.validation_status == "unknown_template"):
                print(
                automation_config.automation_name
                + " : \t "
                + automation_config.validation_status
                + " : \t"
                + str(automation_config.validation_error)
                + "\n"
                )                
            else:
                if automation_config.validation_status == "unknown_template":
                    print(
                        automation_config.automation_name
                        + " : \t "
                        + automation_config.validation_status
                        + " : \t"
                        + str(automation_config.validation_error)
                        + "\n"
                    )

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


def test_script_init(basis_file: str) -> str:
    """
    Test the script initialization and return the path of the generated script

    Args:
        basis_file (str): the path to the yaml file

    Returns:
        str: the path of the generated script
    """
    automation_yaml = yaml_loader.load_yaml_dict(basis_file)
    automation_config = asyncio.run(
        ha_automation_config.async_validate_config_item(automation_yaml)
    )
    if not (automation_config.validation_status == "ok") and not (automation_config.validation_status == "unknown_template"):
        print(
            automation_config.automation_name
            + " : \t "
            + automation_config.validation_status
            + " : \t"
            + str(automation_config.validation_error)
            + "\n"
        )
        return None
    else:
        script_path = init_automation_script(automation_config.automation_name)
        print("Script created at: " + script_path)
        return script_path


def run_automation(script_path, trigger_inputs: list, condition_inputs: list, combined_inputs: list = None, automation: Automation = None):    
    """
    run the automation script and return the result

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
    """
    Test the extraction of all trigger entities in entity_extraction_test.yaml
    """
    
    basis_file = path.join(
        "test_data", "yaml_files", "test_yaml", "entity_extraction_test.yaml"
    )
    script_file = test_script_init(basis_file)
    automation_yaml = yaml_loader.load_yaml_dict(basis_file)
    automation_config = asyncio.run(
        ha_automation_config.async_validate_config_item(automation_yaml)
    )
    print(" --- " + automation_config.automation_name + " --- ")
    extracted_entities = extract_all_trigger(automation_config, script_file)
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
    """
    Test the extraction of all condition entities in entity_extraction_test.yaml
    """
    
    basis_file = path.join(
        "test_data", "yaml_files", "test_yaml", "entity_extraction_test.yaml"
    )
    script_file = test_script_init(basis_file)
    automation_yaml = yaml_loader.load_yaml_dict(basis_file)
    automation_config = asyncio.run(
        ha_automation_config.async_validate_config_item(automation_yaml)
    )
    print(" --- " + automation_config.automation_name + " --- ")
    extracted_entities = extract_all_conditions(automation_config, script_file)
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
    """
    Test the ectraction of all action entities in basis_file
    """
    
    basis_file = path.join("test_data", "yaml_files", "watering_the_garden.yaml")
    script_file = test_script_init(basis_file)
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


def test_entity_list(basis_file: str = None):
    """
    Test the extraction of all entities in basis_file

    Args:
        basis_file (str, optional): the path to the yaml file. 
        Defaults to None and then entity_extraction_test.yaml is used.
    """
    
    if basis_file is None:
        basis_file = path.join("test_data", "yaml_files", "test_yaml", "entity_extraction_test.yaml")
        
    script_file = script_file = test_script_init(basis_file)
    automation_yaml = yaml_loader.load_yaml_dict(basis_file)
    automation_config = asyncio.run(
        ha_automation_config.async_validate_config_item(automation_yaml)
    )
    if not (automation_config.validation_status == "ok"):
        print(
            automation_config.automation_name
            + " : \t "
            + automation_config.validation_status
            + " : \t"
            + str(automation_config.validation_error)
            + "\n"
        )
    else: 
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
    basis_file = path.join('test_data','yaml_files', 'test_yaml', 'bare_min.yaml')

    # test_trigger_entities()
    # test_condition_entities()
    # test_action_entities()
    
    test_entity_list(basis_file=basis_file)

    # file_path = test_script_generation(basis_file)
    
    # test_all_yaml_files()

    # automation: Automation = extract_information["infos"]
    # script_path = path.join("data", "automation_scripts", "entity_extraction_test.py")
    # 
    # print( "result of the automation: " + run_automation(script_path=script_path, trigger_inputs=[True, False, False], condition_inputs=[]))
