# Backend Documentation

The `backend` package contains different subpackages for different tasks.

## Automation Generation

The package contains the modules to generate automations from configuration dictionaries. That includes a list of all used Entities and an executable automation script for testing the automation. In addition, all functions for a complete creation of an automation in the test environment are bundled in the main module. This includes **import**, **validation**, **data extraction** and **script creation** as well as **insertion into the database**. Only the integration creation for non-stored integrations is not yet included, which means that automations with such entities cannot be fully inserted into the database.

> The main module is: `automation_creation.py `
>
> The bundeling function is: `add_new_automation(test_file_path)`

## Database

The database consists of different modules that control access in different situations and make changes and readouts of data. The database itself will be initialized when the database package is imported if it does not already exist. During initialization, the standard integrations are also initialized. The `db_create_autom.py` module can be used to create automations in the database using automation data from the `create_automation()` function from [`automation_gen/config_dissection.py`](https://github.com/JeroPluy/Automation_test_env/blob/main/src/backend/automation_gen/config_dissection.py).

> The bundeling function for the automation creation is: db_create_autom -> add_automation(automation_data: dict)

## Utils

The backend contains two different utility packages. One contains [Home Assistant utilities](https://github.com/JeroPluy/Automation_test_env/tree/main/src/backend/ha_automation_utils) for loading YAML files and validating the automation configuration dictionaries. The [other](https://github.com/JeroPluy/Automation_test_env/tree/main/src/backend/utils) contains environment-specific support such as constants or helper classes.

## Automation Testing Functions

This package directory is currently empty, but contains the modules related to testing and creating test cases. To be continued...