# automation_script_gen/__init__.py
# Path: src/backend/automation_gen/automation_script_gen/__init__.py


# The `automation_script_gen` package is responsible for managing the generating automation script parts.
# It consists of multiple scripts, each contributing to a specific part of the automation process. 

# The `util.py` script is used to initialize the main script and provides a general function for writing to the created script.
# This function can be used by other scripts in the package to write their respective automation code to the automation script.

# This module is used to generate the action part for the automation script.
from .action_script_gen import (
    close_action_condition_block,
    close_action_loop_block,
    close_action_section,
    create_action_loop_stop,
    create_action_script,
    create_else_action_section,
    create_empty_action_section,
    create_stopping_action,
    init_action_part,
    start_action_condition_block,
    start_action_loop_block,
)

# This module generates the condition part of the automation script.
from .condition_script_gen import (
    close_condition_section,
    close_logic_function_block,
    create_combination_condition_script,
    create_condition_script,
    create_next_logic_condition_part,
    init_condition_part,
    start_logic_function_block,
)

# This module is used to generate the trigger section of the automation script.
from .trigger_script_gen import (
    close_trigger_section,
    create_combination_trigger_script,
    create_trigger_script,
)
from .utils import (
    create_locked_message,
    init_automation_script,
)

# The __all__ variable is used to define the public available functions of the package 
# when imported with `from package import *`.
__all__ = [
    "init_automation_script",
    "create_locked_message",
    "close_trigger_section",
    "create_combination_trigger_script",
    "create_trigger_script",
    "close_condition_section",
    "close_logic_function_block",
    "create_combination_condition_script",
    "create_condition_script",
    "create_next_logic_condition_part",
    "init_condition_part",
    "start_logic_function_block",
    "close_action_condition_block",
    "close_action_loop_block",
    "close_action_section",
    "create_action_loop_stop",
    "create_action_script",
    "create_else_action_section",
    "create_empty_action_section",
    "create_stopping_action",
    "init_action_part",
    "start_action_condition_block",
    "start_action_loop_block",
]
