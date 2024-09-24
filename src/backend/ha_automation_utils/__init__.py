# Home Assistant Utilities

# The functions of the programs in this package enable loading YAML configuration files for automations and validating their structure and layout.
# In addition, constants used in Home Assistant are initialized to enable the functions and the dissection of the configuration files.

from .home_assistant_automation_validation import (
    AutomationConfig,
    async_validate_config_item,
)
from .home_assistant_yaml_loader import load_yaml_dict
