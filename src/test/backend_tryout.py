"""
This test script is used to test the functionality of the backend functions.

The python_path needs to be set to the src directory: (for venv)
$env:PYTHONPATH = "..\\src"
"""

import json
from os import path
import subprocess

from backend.utils.env_helper_classes import Automation



DATABASE = path.join("data", "automation_test_env.sqlite")

def run_sync_automation(
    script_path,
    trigger_inputs: list,
    condition_inputs: list,
    combined_inputs: list = None,
    automation: Automation = None,
):
    """
    run the automation synchronously and return the result

    Args:
        automation (Automation): the automation to run

    Returns:
        str: the result of the automation
    """
    if combined_inputs is None:
        input_vals = [trigger_inputs, condition_inputs]
    else:
        input_vals = combined_inputs

    serialized_inputs = json.dumps(input_vals)

    if automation is None:
        automation = Automation("test_automation", script_path)
    result = subprocess.run(
        ["python", automation.script, serialized_inputs], capture_output=True
    )
    return result.stdout.decode("utf-8")

if __name__ == "__main__":
    print("Hello Test!")
