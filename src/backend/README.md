# Backend Documentation

The `backend` package contains different subpackages for different tasks.

## Automation Generation

The package contains the modules to generate automations from configuration dictionaries. That includes a list of all used Entities and an executable automation script for testing the automation.

> The main module is: `config_dissection.py `
> 
> The bundeling function is: `create_automation(automation_config: AutomationConfig) -> dict`

## Database


## Utils

The backend contains two different utility packages. One contains [Home Assistant utilities](https://github.com/JeroPluy/Automation_test_env/tree/main/src/backend/ha_automation_utils) for loading YAML files and validating the automation configuration dictionaries. The [other](https://github.com/JeroPluy/Automation_test_env/tree/main/src/backend/utils) contains environment-specific support such as constants or helper classes.

## Automation Testing Functions