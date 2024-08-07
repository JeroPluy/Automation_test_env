# Testing

> **Usage Information:**
>To run the test scripts in the [`./src/test`](https://github.com/JeroPluy/Automation_test_env/tree/main/src/test) directory, you may need to change the Python virtual environment path for the terminal where the script is called.
>The following command can be used for this.
>
> ```shell
> $env:PYTHONPATH = "..\\src"
> ```

## YAML Import Testing

The `test_yaml_import.py` script can be used to test the import of test automations from `./test_data/yaml_files/test_yaml/` as well as all the automations from the `./test_data/yaml_files/` directory with a `.yaml` ending.

The configuration files in `test_yaml` are compared with dicts created by a separate conversion from yaml to json to confirm functionality. If additional fixed test automations are added, these must be included as with the other tests and in `the test_files` list, otherwise an error message will be raised due to an unknown configuration file.

To evaluate the import process of automations from the directory above, the imported and converted automations are output to the console.

## YAML Validation Testing

The `test_yaml_validation.py` script can be used to test the `ha_automation_config.async_validate_config_item(yaml_dict)` function which is used to validate the structure of configuration files.

In the first part, the `basis_automation.yaml` with the configuration variables it contains is checked by the validation function and must recognize this configuration as valid. Then, all parameters are assigned new invalid values, which the validation must recognize accordingly. Finally, the parameters are all removed individually and it is checked whether the validation classifies this correctly depending on the variable.

The second part of the validation check checks the validation of the test automations from the `./test_data/yaml_files/test_yaml/` directory. The anticipated outputs for the automation name, the validation status and the error message are compared with the validation results. If additional fixed test automations are added, these must be included as with the other tests, otherwise an error message will be raised due to an unknown configuration file.

In the last part of the validation check, all automation configurations the `./test_data/yaml_files/` directory are examined and the results are printed to the console for checking.

## Test Configuration Dissection

The `test_config_dissection.py` is a combined testing script in which the extraction of entities and the generation of the appropriate automation script aus  are tested.


