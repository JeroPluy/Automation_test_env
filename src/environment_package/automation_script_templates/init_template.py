"""
WARNING: This file was generated by the automation_script_gen module.
         Changes to this file may alter the automation flow or prevent the repeatability of a test run.

Please only change this file if you know what you are doing.
"""

import sys
import json

# read the arguments
serialized_inputs = sys.argv[1]

input_vals = json.loads(serialized_inputs)

trigger_id: str = None


def trigger_check(input_vals) -> bool:
    triggered = False
    trigger = input_vals[0]
    global trigger_id
