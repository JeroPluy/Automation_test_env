import asyncio
import yaml_loader
import os

import home_assistant_automation_config as config_validation
from home_assistant_const import SCRIPT_MODE_CHOICES

def test_preconfigured_yaml_files():
    dir_path = os.path.join('test_data','yaml_files', "test_yaml")
    for file in os.listdir(dir_path):
        yaml_dict = yaml_loader.load_yaml_dict(os.path.join(dir_path, file))
        validation_result = asyncio.run(config_validation.async_validate_config_item(yaml_dict))
        print(file + " : " + validation_result.validation_status + " : " + str(validation_result.validation_error))


def test_modes():
    basis_file = os.path.join('test_data','yaml_files', "test_yaml", 'basis_automation.yaml')
    yaml_dict = yaml_loader.load_yaml_dict(basis_file)
    SCRIPT_MODE_CHOICES.append("invalid_mode") # Add invalid mode to test validation
    for mode in SCRIPT_MODE_CHOICES:
        yaml_dict['mode'] = mode
        validation_result = asyncio.run(config_validation.async_validate_config_item(yaml_dict))
        print(mode + " : " + validation_result.validation_status + " : " + str(validation_result.validation_error))


def test_yaml_files():
    print("--- Test preconfigured automations started ---")
    test_preconfigured_yaml_files()
    print("--- Test preconfigured automations completed ")
    print("--- Test modes started ---")
    test_modes()
    print("--- Test modes completed ---")


test_yaml_files()