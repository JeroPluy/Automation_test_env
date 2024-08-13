# automation_gen/__init__.py

# Path: src/backend/automation_gen/__init__.py

# The `automation_gen` package is responsible for generating automation scripts and  the list of contained entities. 
# It consists of multiple scripts, each contributing to a specific part of the automation process.

# The `config_dissection.py` script is the bundling of all sections and enables the holistic creation of an automation
# with its entities as well as an executable automation script.


# The import of the automation_gen package gives access to the `create_automation` main function, which is the entry point
# for the automation generation process.
from .automation_creation import add_new_automation, load_new_automation_data, validate_automation_config

__all__ = ["add_new_automation", "load_new_automation_data", "validate_automation_config"]