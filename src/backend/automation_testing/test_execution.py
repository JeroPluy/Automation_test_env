"""
This module contains the functions for running the automation tests.
"""

import json
import subprocess
from backend.utils.env_helper_classes import Automation
from asyncio import (
    subprocess as async_subprocess,
    create_subprocess_exec as create_aync_subprocess_exec,
)


def run_sync_automation(
    script_path,
    inputs: list,
    automation: Automation = None,
):
    """
    run the automation synchronously and return the result

    Args:
        script_path (str): the path to the automation script
        inputs (list): the inputs for the automation inputs.
        automation (Automation): the automation to run

    Returns:
        str: the result of the automation
    """

    serialized_inputs = json.dumps(inputs)

    if automation is None:
        automation = Automation("test_automation", script_path)
    result = subprocess.run(
        ["python", automation.script, serialized_inputs], capture_output=True
    )
    return result.stdout.decode("utf-8")


async def run_async_automation(script_path, inputs: list):
    """
    The function calls the automation script and returns the result

    Args:
        srcript_path (str): the path to the automation script
        inputs (list): the inputs for the automation inputs
        containing the trigger, condition and action inputs as lists

    Returns:
        str: the result of the automation
    """

    serialized_inputs = json.dumps(inputs)

    command = ["python", script_path, serialized_inputs]

    # async implementation
    # starts the async process
    proc = await create_aync_subprocess_exec(
        *command,
        stdout=async_subprocess.PIPE,  # get the standard output
        stderr=async_subprocess.PIPE,  # Optional: get error messages
    )

    # wait for the process to finish and decode the output
    stdout, stderr = await proc.communicate()

    output = json.loads(stdout.decode("utf-8"))

    return output
