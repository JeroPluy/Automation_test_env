"""
This module contains the functions for running the automation tests.
"""

import json
import subprocess
from asyncio import run as async_run
from backend.utils.env_helper_classes import Automation
from asyncio import (
    subprocess as async_subprocess,
    create_subprocess_exec as create_aync_subprocess_exec,
)

from backend.utils.env_const import SINGLE, RESTART, QUEUED, PARALLEL


def _run_sync_automation(
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


async def _run_async_automation(script_path, inputs: list):
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


def _run_test_case(testcase: dict, automation_mode: int):
    """
    Run a single automation test case

    Args:
        testcase (list): the test case input values for the test run
        automation_mode (int): the mode of the automation
    """
    script_path = testcase["script_path"]
    inputs = testcase["input_values"]

    # run the test case
    # TODO: figure out when it has to be run async or sync
    if automation_mode == SINGLE:
        result = async_run(_run_async_automation(script_path, inputs))
    elif automation_mode == RESTART:
        result = _run_sync_automation(script_path, inputs)
    elif automation_mode == QUEUED:
        result = _run_sync_automation(script_path, inputs)
    elif automation_mode == PARALLEL:
        result = async_run(_run_async_automation(script_path, inputs))

    return {"testcase": testcase["id"], "result": result}


def run_distinct_automations(testcases: list, automation_mode: int):
    """
    Run the automation test cases in the list in single mode

    Args:
        testcases (list): the list of test cases to run
        automation_mode (int): the mode of the automation
    """

    results = []

    for testcase in testcases:
        results.append(_run_test_case(testcase, automation_mode))

    return results


def run_simultaneous_automations(
    testcases: list, automation_mode: int, max_instances: int
):
    """
    Run the automation test cases in the list in parallel mode

    Args:
        testcases (list): the list of test cases to run
        automation_mode (int): the mode of the automation
        max_instances (int): the maximum number of instances to run
    """

    results = []

    for i in range(max_instances):
        results.append(_run_test_case(testcases[i], automation_mode))

    if automation_mode == RESTART:
        pass
        # TODO: implement the restart logic here (50% of the time the test case should be stopped)

    return results
