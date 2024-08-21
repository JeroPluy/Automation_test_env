# automation_gen/__init__.py

# Path: src/backend/automation_gen/__init__.py

# The `automation_gen` package is responsible for generating automation scripts and  the list of contained entities.
# It consists of multiple scripts, each contributing to a specific part of the automation process.

# The `config_dissection.py` script is the bundling of all sections and enables the holistic creation of an automation
# with its entities as well as an executable automation script.


# The import of the automation_gen package gives access to the `automation_creation` functions, which are the combination of all
# extraction modules and enable the extraction of all automation entities as well as the creation of the complete automation script.

from .automation_creation import (
    load_new_automation_data,
    change_integration,
)

__all__ = [
    "load_new_automation_data",
    "change_integration",
]
