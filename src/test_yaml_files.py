import asyncio
import copy
import os

import home_assistant_automations.home_assistant_automation_config as config_validation
from home_assistant_automations.home_assistant_const import (
    CONF_ACTION, CONF_ALIAS, CONF_CONDITION, CONF_DESCRIPTION, CONF_ID,
    CONF_INITIAL_STATE, CONF_MAX, CONF_MAX_EXCEEDED, CONF_MODE,
    CONF_STORED_TRACES, CONF_TRACE, CONF_TRIGGER, CONF_VARIABLES,
    LOGSEVERITY_STRING, SCRIPT_MODE_CHOICES)
from home_assistant_automations.home_assistant_yaml_loader import \
    load_yaml_dict


def change_param(yaml_dict, param, value="invalid_value", nested = False, nested_param = None):
    """Change parameter in yaml dictionary to a value and validate the new yaml dictionary"""
    
    if nested:
        print("--- " + str(nested_param) + " changed to " + str(value) + " ---")
        yaml_dict[param][nested_param] = value # Change to value
    else:
        print("--- " + str(param) + " changed to " + str(value) + " ---")
        yaml_dict[param] = value # Change to value
    validation_result = asyncio.run(config_validation.async_validate_config_item(yaml_dict))
    print(param + " : " + validation_result.automation_name + " : " + validation_result.validation_status + " : " + str(validation_result.validation_error))

def remove_param(yaml_dict, param, nested = False, nested_param = None):
    """Remove parameter from yaml dictionary and validate the new yaml dictionary"""

    if nested:
        print("--- " + str(nested_param) + " removed ---")
        yaml_dict[param].pop(nested_param)  # Remove parameter
    else:
        print("--- " + str(param) + " removed ---")
        yaml_dict.pop(param) # Remove parameter
    validation_result = asyncio.run(config_validation.async_validate_config_item(yaml_dict))
    print(param + " : " + str(validation_result.automation_name) + " : " + validation_result.validation_status + " : " + str(validation_result.validation_error))


def test_main_automation_params()-> None:
    """Test all main automation parameters.

    This function tests the main automation parameters by performing various changes to the YAML dictionary
    and validating the changes. It also tests the handling of changes to nested parameters.

    Args:
        None

    Returns:
        None
    """

    BASIS_PARAMS = [
        CONF_ALIAS,
        CONF_ID,
        CONF_DESCRIPTION,
        CONF_INITIAL_STATE,
        [CONF_TRACE, CONF_STORED_TRACES],
        CONF_VARIABLES,
        [CONF_MODE,SCRIPT_MODE_CHOICES],
        CONF_MAX,
        [CONF_MAX_EXCEEDED, LOGSEVERITY_STRING],
        CONF_TRIGGER,
        CONF_CONDITION,
        CONF_ACTION
    ]

    # Automation to test basis parameters
    basis_file = os.path.join('test_data','yaml_files', "test_yaml", 'basis_automation.yaml')

    # Load basis automation yaml file
    yaml_dict = load_yaml_dict(basis_file)

    # Make a copy of the original yaml dictionary and all of its nested dictionaries or lists
    reset_dict = copy.deepcopy(yaml_dict) 

    # Validate basis automation
    print("--- Test basis automation ---")
    validation_result = asyncio.run(config_validation.async_validate_config_item(yaml_dict)) 
    print(basis_file + " : " + validation_result.automation_name + " : " + validation_result.validation_status + " : " + str(validation_result.validation_error))
    print("\n--- Test handling of changes to single basis parameters ---")

    # Test changes to single basis parameters
    for param in BASIS_PARAMS:
        if isinstance(param, list):
            if param[0] == CONF_TRACE:
                # Test changes to stored trace parameters only
                change_param(yaml_dict, param[0], -1, True, param[1]) # invalid value
                change_param(yaml_dict, param[0], 8, True, param[1]) # valid value
                remove_param(yaml_dict, param[0], True, param[1])
                yaml_dict = copy.deepcopy(reset_dict)

                # Test changes to trace parameters only
                change_param(yaml_dict, param[0], "invalid_value")
                remove_param(yaml_dict, param[0])
                yaml_dict = copy.deepcopy(reset_dict)

            # Test changes to mode parameters only
            elif param[0] == CONF_MODE or param[0] == CONF_MAX_EXCEEDED:
                # Test all modes
                for mode in param[1]:
                    change_param(yaml_dict, param[0], mode)

                # Test with invalid mode
                change_param(yaml_dict, param[0])
                remove_param(yaml_dict, param[0])
        else:
            # Test changes to initial state parameter
            if CONF_ID == param:                
                change_param(yaml_dict, param, 11054710) # invalid value for str
            elif CONF_ALIAS == param or CONF_DESCRIPTION == param:
                change_param(yaml_dict, param, None) # invalid value for string
            else:
                change_param(yaml_dict, param) # invalid value for int, bool
            remove_param(yaml_dict, param)

        yaml_dict = copy.deepcopy(reset_dict)


def test_preconfigured_yaml_files()-> None:
    """Test all preconfigured automations.

    This function iterates through all the YAML files in the 'test_data/yaml_files' directory,
    loads each YAML file as a dictionary using the 'yaml_loader.load_yaml_dict' function,
    and performs validation on the loaded YAML dictionary using the 'config_validation.async_validate_config_item' function.
    The validation result is then printed to the console.

    Args:
        None

    Returns:
        None
    """

    dir_path = os.path.join('test_data','yaml_files')
    for file in os.listdir(dir_path):
        if file.endswith(".yaml"):
            yaml_dict = load_yaml_dict(os.path.join(dir_path, file))
            print("Test " + file)
            validation_result = asyncio.run(config_validation.async_validate_config_item(yaml_dict))
            print(validation_result.automation_name + " : " + validation_result.validation_status + " : " + str(validation_result.validation_error))


def test_yaml_files():
    """
    This function is used to test the YAML files for preconfigured automations and parameter behavior.
    It prints the start and completion messages for each test.
    """
    print("--- Preconfigured automations test started ---")
    test_preconfigured_yaml_files()
    print("--- Preconfigured automations test completed --- \n")
    print("--- Parameter behavior test  started ---")
    test_main_automation_params()
    print("--- Parameter behavior test completed ---")


if __name__ == "__main__":
    test_yaml_files()