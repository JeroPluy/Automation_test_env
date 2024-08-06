# __init__.py

# This is the initialization file for the environment_package package.
# The environment_package contains the automation_script_gen, db, ha_automation, and utils subpackages.


from os import path, makedirs

from .utils.env_const import AUTOMATION_SCRIPT

if not path.exists(AUTOMATION_SCRIPT):
    makedirs(path.join(AUTOMATION_SCRIPT), exist_ok=True)