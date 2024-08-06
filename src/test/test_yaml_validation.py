"""
This module is used to test the YAML files for preconfigured automations and parameter behavior.

The python_path needs to be set to the src directory: (for venv) $env:PYTHONPATH = "D:\\Workspace\\Python\\custom_Tkinker_tryout\\src"
"""

import asyncio
import copy
import os

from backend.ha_automation_utils import (
    home_assistant_automation_validation as ha_automation_config,
)
from backend.ha_automation_utils.home_assistant_const import (
    CONF_ACTION,
    CONF_ALIAS,
    CONF_CONDITION,
    CONF_DESCRIPTION,
    CONF_ID,
    CONF_INITIAL_STATE,
    CONF_MAX,
    CONF_MAX_EXCEEDED,
    CONF_MODE,
    CONF_STORED_TRACES,
    CONF_TRACE,
    CONF_TRIGGER,
    CONF_VARIABLES,
    LOGSEVERITY_STRING,
    SCRIPT_MODE_CHOICES,
)
from backend.ha_automation_utils.home_assistant_yaml_loader import load_yaml_dict


def change_param(
    yaml_dict, param, value="invalid_value", nested=False, nested_param=None
) -> dict:
    """Change parameter in yaml dictionary to a value and validate the new yaml dictionary

    Args:
        yaml_dict: yaml dictionary
        param: parameter to change
        value: value to change to
        nested: if parameter is nested
        nested_param: nested parameter to change

    Returns:
        dict: [param, validation_result.automation_name, validation_result.validation_status, validation_result.validation_error]

    """

    if nested:
        # print("--- " + str(nested_param) + " changed to " + str(value) + " ---")
        yaml_dict[param][nested_param] = value  # Change to value
    else:
        # print("--- " + str(param) + " changed to " + str(value) + " ---")
        yaml_dict[param] = value  # Change to value
    validation_result = asyncio.run(
        ha_automation_config.async_validate_config_item(yaml_dict)
    )
    return [
        param,
        validation_result.automation_name,
        str(validation_result.validation_status),
        str(validation_result.validation_error),
    ]


def remove_param(yaml_dict, param, nested=False, nested_param=None):
    """Remove parameter from yaml dictionary and validate the new yaml dictionary

    Args:
        yaml_dict: yaml dictionary
        param: parameter to remove
        nested: if parameter is nested
        nested_param: nested parameter to remove

    Returns:
        dict: [param, validation_result.automation_name, validation_result.validation_status, validation_result.validation_error]

    """

    if nested:
        # print("--- " + str(nested_param) + " removed ---")
        yaml_dict[param].pop(nested_param)  # Remove parameter
    else:
        # print("--- " + str(param) + " removed ---")
        yaml_dict.pop(param)  # Remove parameter
    validation_result = asyncio.run(
        ha_automation_config.async_validate_config_item(yaml_dict)
    )
    return [
        param,
        validation_result.automation_name,
        str(validation_result.validation_status),
        str(validation_result.validation_error),
    ]


def test_main_automation_params() -> None:
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
        [CONF_MODE, SCRIPT_MODE_CHOICES],
        CONF_MAX,
        [CONF_MAX_EXCEEDED, LOGSEVERITY_STRING],
        CONF_TRIGGER,
        CONF_CONDITION,
        CONF_ACTION,
    ]

    # Automation to test basis parameters
    basis_file = os.path.join(
        "test_data", "yaml_files", "test_yaml", "basis_automation.yaml"
    )
    automation_name = 'id_1600000000000'

    # Load basis automation yaml file
    yaml_dict = load_yaml_dict(basis_file)

    # Make a copy of the original yaml dictionary and all of its nested dictionaries or lists
    reset_dict = copy.deepcopy(yaml_dict)

    # Validate basis automation
    validation_result = asyncio.run(
        ha_automation_config.async_validate_config_item(yaml_dict)
    )
    print("\t" + basis_file + " : \t" + validation_result.automation_name + " : \t" + validation_result.validation_status + " : \t" + str(validation_result.validation_error))
    assert validation_result.automation_name == automation_name
    assert validation_result.validation_status == "ok"
    assert validation_result.validation_error is None
    print("--- Test basis automation passed ---")

    # Test changes to single basis parameters
    print("--- Test handling of changes to single basis parameters ---")
    for param in BASIS_PARAMS:
        print(f"\t Testing {param} parameter")
        if isinstance(param, list):
            if param[0] == CONF_TRACE:
                # Test changes to stored trace parameters only
                # invalid value for int
                assert change_param(yaml_dict, param[0], -1, True, param[1]) == [
                    param[0],
                    automation_name,
                    "failed_schema",
                    "value must be at least 0 for dictionary value @ data['trace']['stored_traces']. Got -1",
                ]
                # valid value for int
                assert change_param(yaml_dict, param[0], 8, True, param[1]) == [
                    param[0],
                    automation_name,
                    "ok",
                    "None",
                ]
                # test removing stored traces
                assert remove_param(yaml_dict, param[0], True, param[1]) == [
                    param[0],
                    automation_name,
                    "ok",
                    "None",
                ]
                yaml_dict = copy.deepcopy(reset_dict)

                # Test changes to trace parameters only
                assert change_param(yaml_dict, param[0], "invalid_value") == [
                    param[0],
                    automation_name,
                    "failed_schema",
                    "expected a dictionary for dictionary value @ data['trace']. Got 'invalid_value'",
                ]
                # test removing trace
                assert remove_param(yaml_dict, param[0]) == [
                    param[0],
                    automation_name,
                    "ok",
                    "None",
                ]
                yaml_dict = copy.deepcopy(reset_dict)

            # Test changes to mode parameters only
            elif param[0] == CONF_MODE or param[0] == CONF_MAX_EXCEEDED:
                # Test all modes
                for mode in param[1]:
                    assert change_param(yaml_dict, param[0], mode) == [
                        param[0],
                        automation_name,
                        "ok",
                        "None",
                    ]

                # Test with invalid mode
                if param[0] == CONF_MODE:
                    assert change_param(yaml_dict, param[0]) == [
                        param[0],
                        automation_name,
                        "failed_schema",
                        "value must be one of ['parallel', 'queued', 'restart', 'single'] for dictionary value @ data['mode']. Got 'invalid_value'",
                    ]
                else:
                    assert change_param(yaml_dict, param[0]) == [
                        param[0],
                        automation_name,
                        "failed_schema",
                        "value must be one of ['CRITICAL', 'DEBUG', 'ERROR', 'FATAL', 'INFO', 'NOTSET', 'SILENT', 'WARN', 'WARNING'] for dictionary value @ data['max_exceeded']. Got 'invalid_value'",
                    ]
                assert remove_param(yaml_dict, param[0]) == [
                    param[0],
                    automation_name,
                    "ok",
                    "None",
                ]
        else:
            # Test changes to initial state parameter
            if CONF_ID == param:
                # invalid value for str
                assert change_param(yaml_dict, param, 11054710) == [
                    param,
                    "!invalid_automation",
                    "failed_schema",
                    "expected str for dictionary value @ data['id']. Got 11054710",
                ]
            elif CONF_ALIAS == param or CONF_DESCRIPTION == param:
                # invalid value for string
                if CONF_ALIAS == param:
                    assert change_param(yaml_dict, param, None) == [
                        param,
                        '!invalid_automation',
                        'failed_schema',
                        "string value is None for dictionary value @ data['alias']. Got None",
                    ]
                else:
                    assert change_param(yaml_dict, param, None) == [
                        param,
                        "!invalid_automation",
                        "failed_schema",
                        "string value is None for dictionary value @ data['description']. Got None",
                    ]
            else:
                # invalid value for int, bool
                result = change_param(yaml_dict, param)
                print(
                    result[0]
                    + " : "
                    + result[1]
                    + " : "
                    + result[2]
                    + " : "
                    + result[3]
                )
            if CONF_ID == param:
                assert remove_param(yaml_dict, param) == [
                    param,
                    'Wohnzimmerlampe_einschalten',
                    "ok",
                    "None",
                ]
            else:
                if CONF_TRIGGER == param or CONF_ACTION == param:
                    result = remove_param(yaml_dict, param)
                    print(
                        result[0]
                        + " : "
                        + result[1]
                        + " : "
                        + result[2]
                        + " : "
                        + result[3]
                    )
                else:
                    assert remove_param(yaml_dict, param) == [
                        param,
                        automation_name,
                        "ok",
                        "None",
                    ]

        yaml_dict = copy.deepcopy(reset_dict)


def test_preconfigured_yaml_files() -> None:
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

    dir_path = os.path.join("test_data", "yaml_files")
    for file in os.listdir(dir_path):
        if file.endswith(".yaml"):
            yaml_dict = load_yaml_dict(os.path.join(dir_path, file))
            print("Test " + file)
            validation_result = asyncio.run(
                ha_automation_config.async_validate_config_item(yaml_dict)
            )
            print(
                validation_result.automation_name
                + " : \t "
                + validation_result.validation_status
                + " : \t"
                + str(validation_result.validation_error)
                + "\n"
            )


def test_yaml_configs():
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
    test_yaml_configs()
