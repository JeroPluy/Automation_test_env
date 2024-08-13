"""
Test cases for every config module in the config_dissection.py

The tests validate the correct extraction of the entities from the configuration
and the correct implementation of the entities in the automation script

"""

from asyncio import create_subprocess_exec, subprocess, run as async_run
import json
from os import path, mkdir
import voluptuous as vol

from backend.automation_gen.trigger_dissection import _trigger_entities
from backend.automation_gen.condtion_dissection import _condition_entities
from backend.automation_gen.action_dissection import _action_entities

from backend.automation_gen.automation_script_gen.action_script_gen import (
    close_action_section,
    init_action_part,
)
from backend.automation_gen.automation_script_gen.utils import (
    append_script_context_to_script,
    init_automation_script,
)
from backend.automation_gen.automation_script_gen.condition_script_gen import (
    init_condition_part,
)

from backend.automation_gen.config_dissection import (
    create_procedure_list,
)

from backend.ha_automation_utils import home_assistant_yaml_loader as yaml_loader

from backend.utils.env_const import INPUT, OUTPUT, START, ACTION_INPUT
from backend.ha_automation_utils.home_assistant_const import (
    ATTR_AREA_ID,
    CONF_ABOVE,
    CONF_AFTER,
    CONF_AFTER_OFFSET,
    CONF_ALLOWED_METHODS,
    CONF_AND,
    CONF_AT,
    CONF_ATTRIBUTE,
    CONF_BEFORE,
    CONF_BEFORE_OFFSET,
    CONF_BELOW,
    CONF_CHOOSE,
    CONF_COMMAND,
    CONF_CONDITION,
    CONF_CONDITIONS,
    CONF_CONTINUE_ON_TIMEOUT,
    CONF_COUNT,
    CONF_DEFAULT,
    CONF_DEVICE_ID,
    CONF_DOMAIN,
    CONF_ELSE,
    CONF_ENABLED,
    CONF_ENTITY_ID,
    CONF_EVENT,
    CONF_EVENT_CONTEXT,
    CONF_EVENT_DATA,
    CONF_EVENT_TYPE,
    CONF_FOR,
    CONF_FROM,
    CONF_ID,
    CONF_LOCAL,
    CONF_NOFITY_ID,
    CONF_NOT,
    CONF_NOT_FROM,
    CONF_NOT_TO,
    CONF_NUMERIC_STATE,
    CONF_OFFSET,
    CONF_OR,
    CONF_PARALLEL,
    CONF_PAYLOAD,
    CONF_PLATFORM,
    CONF_QOS,
    CONF_REPEAT,
    CONF_SEQUENCE,
    CONF_SERVICE,
    CONF_SERVICE_DATA,
    CONF_SOURCE,
    CONF_STATE,
    CONF_TARGET,
    CONF_TEMPLATE,
    CONF_THEN,
    CONF_TIMEOUT,
    CONF_TO,
    CONF_TRIGGER,
    CONF_TYPE,
    CONF_UNTIL,
    CONF_UPDATE_TYPE,
    CONF_VALUE_TEMPLATE,
    CONF_WEBHOOK_ID,
    CONF_WEEKDAY,
    CONF_WHILE,
    CONF_ZONE,
    HOURS,
    MINUTES,
    SCRIPT_ACTION_IF,
    SCRIPT_ACTION_WAIT_FOR_TRIGGER,
    SECONDS,
    TAG_ID,
)


TEST_DIR = path.join("src", "test", "test_automation_gen", "test_scripts")

# additional functions for testing


async def run_automation(
    script_path,
    trigger_inputs: list,
    condition_inputs: list,
    action_inputs: list = [],
    combined_inputs: list = None,
):
    """
    The function calls the automation script and returns the result

    Args:
        srcript_path (str): the path to the automation script
        trigger_inputs (list): the inputs for the trigger
        condition_inputs (list): the inputs for the condition
        action_inputs (list): the inputs for the action. Default is an empty list
        combined_inputs (list, optional): the inputs for the automation inputs 
        containing the trigger, condition and action inputs as lists
        
    Returns:
        str: the result of the automation
    """
    
    if combined_inputs is None:
        input_vals = [trigger_inputs, condition_inputs, action_inputs]
    else:
        input_vals = combined_inputs

    serialized_inputs = json.dumps(input_vals)

    command = ["python", script_path, serialized_inputs]

    # async implementation
    # starts the process and waits for it to finish
    proc = await create_subprocess_exec(
        *command,
        stdout=subprocess.PIPE,  # get the standard output
        stderr=subprocess.PIPE,  # Optional: get error messages
    )

    # wait for the process to finish and decode the output
    stdout, stderr = await proc.communicate()

    output = json.loads(stdout.decode("utf-8"))

    return output

    # synchron subprocess implementation
    # result = subprocess.run(
    # ["python", script_path, serialized_inputs], capture_output=True
    # )
    # return result.stdout.decode("utf-8")


def test_trigger_return(filepath: str) -> None:
    """
    This function adds a print statement to the script to test the trigger return value

    Args:
        filepath (str): the path to the script file
    """
    script_context = "\n\toutput = triggered\n\treturn output\n\nprint(json.dumps(trigger_check(input_vals)))"
    append_script_context_to_script(filepath, script_context)


def test_trigger_fill(filepath: str, trigger_id: str = None) -> None:
    """
    This function adds a return statement to skip the trigger check part

    Args:
        filepath (str): the path to the script file
        trigger_id (str): the trigger id to be used in the test
    """
    # insert trigger return list
    script_context = (
        f"\n# just test inputs\n\ttrigger_id = '{trigger_id}'\n\treturn True\n\n"
    )
    append_script_context_to_script(filepath, script_context)

    # insert condition definition
    init_condition_part(filepath)


def test_condition_return(filepath: str) -> None:
    """
    This function adds a print statement to the script to test the condition return value

    Args:
        filepath (str): the path to the script file
    """
    script_context = "\t):\n\t\tcondition_passed = True\n\toutput = {'condition_passed': condition_passed}\n\n\treturn output"
    script_context += "\n\nif trigger_check(input_vals):"
    script_context += "\n\tif isinstance(condition_evaluation(input_vals), dict):"
    script_context += "\n\t\tprint(json.dumps(condition_evaluation(input_vals)))"
    append_script_context_to_script(filepath, script_context)


def test_condition_fill(filepath: str) -> None:
    """
    This function adds a return statements to skip the trigger check and the condition evaluation part

    Args:
        filepath (str): the path to the script file
    """
    # insert the trigger check filler
    test_trigger_fill(filepath)

    # create a condition evaluation filler
    script_context = "\t\tTrue\n\t):\n\t\tcondition_passed = True\n\n\treturn True\n\n"
    append_script_context_to_script(filepath, script_context)

    init_action_part(filepath)


def create_dummy_action_return(filepath: str) -> None:
    """
    This function adds a dummy action result to the script

    Args:
        filepath (str): the path to the script file
    """

    script_context = "\taction_results.append({'dummy.target':'doSomething'})\n"
    append_script_context_to_script(filepath, script_context)


# test funcitons


async def test_trigger_entities():
    TRIGGER_DIR = path.join(TEST_DIR, "trigger")
    if not path.exists(TRIGGER_DIR):
        mkdir(TRIGGER_DIR)

    async def test_trigger_event():
        # Test case 1: Event trigger with single event type
        trigger_part_event_1 = {
            CONF_PLATFORM: CONF_EVENT,
            CONF_EVENT_TYPE: "event_type_1",
        }
        file_path = init_automation_script("trigger_part_event_1", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_event_1, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_event_1, end_position, real_pos = results
        assert len(entities_event_1) == 1
        assert entities_event_1[0].parent is None
        assert entities_event_1[0].position == 1
        assert entities_event_1[0].parameter_role == START
        assert entities_event_1[0].integration == CONF_EVENT
        assert entities_event_1[0].entity_name is not None
        assert entities_event_1[0].expected_value == {CONF_EVENT_TYPE: "event_type_1"}
        assert end_position == 1

        # test run the automation script
        trigger_part_event_1_input = [True]
        assert (await run_automation(file_path, trigger_part_event_1_input, [])) is True

        trigger_part_event_1_input = [False]
        assert (
            await run_automation(file_path, trigger_part_event_1_input, [])
        ) is False

        trigger_part_event_1_input = [None]
        assert (
            await run_automation(file_path, trigger_part_event_1_input, [])
        ) is False

        assert real_pos == 1

        # Test case 2: Event trigger with multiple event types
        trigger_part_event_2 = {
            CONF_PLATFORM: CONF_EVENT,
            CONF_EVENT_TYPE: ["event_type_2", "event_type_3"],
        }
        file_path = init_automation_script("trigger_part_event_2", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_event_2, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_event_2, end_position, real_pos = results
        assert len(entities_event_2) == 2
        assert entities_event_2[0].parent == 1
        assert entities_event_2[0].position == 2
        assert entities_event_2[0].parameter_role == START
        assert entities_event_2[0].integration == CONF_EVENT
        assert entities_event_2[0].entity_name is not None
        assert entities_event_2[0].expected_value == {CONF_EVENT_TYPE: "event_type_2"}
        assert entities_event_2[1].parent == 1
        assert entities_event_2[1].position == 3
        assert entities_event_2[1].integration == CONF_EVENT
        assert entities_event_2[1].entity_name is not None
        assert entities_event_2[1].expected_value == {CONF_EVENT_TYPE: "event_type_3"}
        assert end_position == 3
        # test run the automation script
        trigger_part_event_2_input = [False, True]
        assert (await run_automation(file_path, trigger_part_event_2_input, [])) is True

        trigger_part_event_2_input = [False, False]
        assert (
            await run_automation(file_path, trigger_part_event_2_input, [])
        ) is False

        trigger_part_event_2_input = [True, False]
        assert (await run_automation(file_path, trigger_part_event_2_input, [])) is True

        trigger_part_event_2_input = [True, True]
        assert (await run_automation(file_path, trigger_part_event_2_input, [])) is True

        trigger_part_event_2_input = [None, None]
        assert (
            await run_automation(file_path, trigger_part_event_2_input, [])
        ) is False

        trigger_part_event_2_input = [True, None]
        assert (await run_automation(file_path, trigger_part_event_2_input, [])) is True

        trigger_part_event_2_input = [False, None]
        assert (
            await run_automation(file_path, trigger_part_event_2_input, [])
        ) is False

        assert real_pos == 2

        # Test case 3: Event trigger with event data and context
        trigger_part_event_3 = {
            CONF_PLATFORM: CONF_EVENT,
            CONF_EVENT_TYPE: "event_type_3",
            CONF_EVENT_DATA: {"key_1": "value_1", "key_2": "value_2"},
            CONF_EVENT_CONTEXT: {"key_3-2": ["value_3-2-1", "value_3-2-2"]},
        }
        file_path = init_automation_script("trigger_part_event_3", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_event_3, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_event_3, end_position, real_pos = results
        assert len(entities_event_3) == 1
        assert entities_event_3[0].parent is None
        assert entities_event_3[0].position == 1
        assert entities_event_3[0].parameter_role == START
        assert entities_event_3[0].integration == CONF_EVENT
        assert entities_event_3[0].entity_name is not None
        assert entities_event_3[0].expected_value == {
            CONF_EVENT_TYPE: "event_type_3",
            CONF_EVENT_DATA: {"key_1": "value_1", "key_2": "value_2"},
            CONF_EVENT_CONTEXT: {"key_3-2": ["value_3-2-1", "value_3-2-2"]},
        }
        assert end_position == 1

        # test run the automation script
        trigger_part_event_3_input = [True]
        assert (await run_automation(file_path, trigger_part_event_3_input, [])) is True

        trigger_part_event_3_input = [False]
        assert (
            await run_automation(file_path, trigger_part_event_3_input, [])
        ) is False

        trigger_part_event_3_input = [None]
        assert (
            await run_automation(file_path, trigger_part_event_3_input, [])
        ) is False

        assert real_pos == 1

    async def test_trigger_ha():
        # Test case 1: Home Assistant trigger with single event
        trigger_part_ha_1 = {CONF_PLATFORM: "homeassistant", CONF_EVENT: "start"}
        file_path = init_automation_script("trigger_part_ha_1", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_ha_1, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_ha_1, end_position, real_pos = results
        assert len(entities_ha_1) == 1
        assert entities_ha_1[0].parent is None
        assert entities_ha_1[0].position == 1
        assert entities_ha_1[0].parameter_role == START
        assert entities_ha_1[0].integration == "homeassistant"
        assert entities_ha_1[0].entity_name == "homeassistant._"
        assert entities_ha_1[0].expected_value == {CONF_EVENT: "start"}
        assert end_position == 1

        # test run the automation script
        trigger_part_ha_1_input = [True]
        assert (await run_automation(file_path, trigger_part_ha_1_input, [])) is True

        trigger_part_ha_1_input = [False]
        assert (await run_automation(file_path, trigger_part_ha_1_input, [])) is False

        trigger_part_ha_1_input = [None]
        assert (await run_automation(file_path, trigger_part_ha_1_input, [])) is False

        assert real_pos == 1

        # Test case 2: Home Assistant trigger with single event
        trigger_part_ha_2 = {CONF_PLATFORM: "homeassistant", CONF_EVENT: "shutdown"}
        file_path = init_automation_script("trigger_part_ha_2", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_ha_2, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_ha_2, end_position, real_pos = results
        assert len(entities_ha_2) == 1
        assert entities_ha_2[0].parent is None
        assert entities_ha_2[0].position == 1
        assert entities_ha_2[0].parameter_role == START
        assert entities_ha_2[0].integration == "homeassistant"
        assert entities_ha_2[0].entity_name == "homeassistant._"
        assert entities_ha_2[0].expected_value == {CONF_EVENT: "shutdown"}
        assert end_position == 1

        # test run the automation script
        trigger_part_ha_2_input = [True]
        assert (await run_automation(file_path, trigger_part_ha_2_input, [])) is True

        trigger_part_ha_2_input = [False]
        assert (await run_automation(file_path, trigger_part_ha_2_input, [])) is False

        trigger_part_ha_2_input = [None]
        assert (await run_automation(file_path, trigger_part_ha_2_input, [])) is False

        assert real_pos == 1

    async def test_trigger_mqtt():
        # Test case 1: MQTT trigger with qos
        trigger_part_mqtt_1 = {
            CONF_PLATFORM: "mqtt",
            "topic": "mqtt_topic",
            CONF_QOS: 0,
        }
        file_path = init_automation_script("trigger_part_mqtt_1", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_mqtt_1, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_mqtt_1, end_position, real_pos = results
        assert len(entities_mqtt_1) == 1
        assert entities_mqtt_1[0].parent is None
        assert entities_mqtt_1[0].position == 1
        assert entities_mqtt_1[0].parameter_role == START
        assert entities_mqtt_1[0].integration == "mqtt"
        assert entities_mqtt_1[0].entity_name == "mqtt.mqtt_topic"
        assert entities_mqtt_1[0].expected_value == {CONF_QOS: 0}
        assert end_position == 1

        # test run the automation script
        trigger_part_mqtt_1_input = [True]
        assert (await run_automation(file_path, trigger_part_mqtt_1_input, [])) is True

        trigger_part_mqtt_1_input = [False]
        assert (await run_automation(file_path, trigger_part_mqtt_1_input, [])) is False

        trigger_part_mqtt_1_input = [None]
        assert (await run_automation(file_path, trigger_part_mqtt_1_input, [])) is False

        assert real_pos == 1

        # Test case 2: MQTT trigger with payload
        trigger_part_mqtt_2 = {
            CONF_PLATFORM: "mqtt",
            "topic": "mqtt_topic",
            CONF_PAYLOAD: "mqtt_payload",
        }
        file_path = init_automation_script("trigger_part_mqtt_2", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_mqtt_2, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_mqtt_2, end_position, real_pos = results
        assert len(entities_mqtt_2) == 1
        assert entities_mqtt_2[0].parent is None
        assert entities_mqtt_2[0].position == 1
        assert entities_mqtt_2[0].parameter_role == START
        assert entities_mqtt_2[0].integration == "mqtt"
        assert entities_mqtt_2[0].entity_name == "mqtt.mqtt_topic"
        assert entities_mqtt_2[0].expected_value == {CONF_PAYLOAD: "mqtt_payload"}
        assert end_position == 1

        trigger_part_mqtt_2_input = [True]
        assert (await run_automation(file_path, trigger_part_mqtt_2_input, [])) is True

        trigger_part_mqtt_2_input = [False]
        assert (await run_automation(file_path, trigger_part_mqtt_2_input, [])) is False

        trigger_part_mqtt_2_input = [None]
        assert (await run_automation(file_path, trigger_part_mqtt_2_input, [])) is False

        assert real_pos == 1

        # Test case 3: MQTT trigger with qos and payload
        trigger_part_mqtt_3 = {
            CONF_PLATFORM: "mqtt",
            "topic": "mqtt_topic",
            CONF_PAYLOAD: "mqtt_payload",
            CONF_QOS: 0,
        }
        file_path = init_automation_script("trigger_part_mqtt_3", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_mqtt_3, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_mqtt_3, end_position, real_pos = results
        assert len(entities_mqtt_3) == 1
        assert entities_mqtt_3[0].parent is None
        assert entities_mqtt_3[0].position == 1
        assert entities_mqtt_3[0].parameter_role == START
        assert entities_mqtt_3[0].integration == "mqtt"
        assert entities_mqtt_3[0].entity_name == "mqtt.mqtt_topic"
        assert entities_mqtt_3[0].expected_value == {
            CONF_PAYLOAD: "mqtt_payload",
            CONF_QOS: 0,
        }
        assert end_position == 1

        trigger_part_mqtt_3_input = [True]
        assert (await run_automation(file_path, trigger_part_mqtt_3_input, [])) is True

        trigger_part_mqtt_3_input = [False]
        assert (await run_automation(file_path, trigger_part_mqtt_3_input, [])) is False

        trigger_part_mqtt_3_input = [None]
        assert (await run_automation(file_path, trigger_part_mqtt_3_input, [])) is False

        assert real_pos == 1

    async def test_trigger_num_state():
        # Test case 1: Numerical state trigger with below values
        trigger_part_num_state_1 = {
            CONF_PLATFORM: CONF_NUMERIC_STATE,
            CONF_ENTITY_ID: ["sensor.temperature"],
            CONF_BELOW: 30,
        }
        file_path = init_automation_script("trigger_part_num_state_1", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_num_state_1, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_num_state_1, end_position, real_pos = results
        assert len(entities_num_state_1) == 1
        assert entities_num_state_1[0].parent is None
        assert entities_num_state_1[0].position == 1
        assert entities_num_state_1[0].parameter_role == START
        assert entities_num_state_1[0].integration == "sensor"
        assert entities_num_state_1[0].entity_name == "sensor.temperature"
        assert entities_num_state_1[0].expected_value == {"below": 30}
        assert end_position == 1

        # border test cases
        trigger_part_num_state_1_input = [16]
        assert (
            await run_automation(file_path, trigger_part_num_state_1_input, [])
        ) is True

        trigger_part_num_state_1_input = [30]
        assert (
            await run_automation(file_path, trigger_part_num_state_1_input, [])
        ) is False

        trigger_part_num_state_1_input = [31]
        assert (
            await run_automation(file_path, trigger_part_num_state_1_input, [])
        ) is False

        trigger_part_num_state_1_input = [None]
        assert (
            await run_automation(file_path, trigger_part_num_state_1_input, [])
        ) is False

        assert real_pos == 1

        # Test case 2: Numerical state trigger with above value
        trigger_part_num_state_2 = {
            CONF_PLATFORM: CONF_NUMERIC_STATE,
            CONF_ENTITY_ID: ["sensor.temperature"],
            CONF_ABOVE: 20,
        }
        file_path = init_automation_script("trigger_part_num_state_2", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_num_state_2, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_num_state_2, end_position, real_pos = results
        assert len(entities_num_state_2) == 1
        assert entities_num_state_2[0].parent is None
        assert entities_num_state_2[0].position == 1
        assert entities_num_state_2[0].parameter_role == START
        assert entities_num_state_2[0].integration == "sensor"
        assert entities_num_state_2[0].entity_name == "sensor.temperature"
        assert entities_num_state_2[0].expected_value == {"above": 20}
        assert end_position == 1

        # border test cases
        trigger_part_num_state_2_input = [25]
        assert (
            await run_automation(file_path, trigger_part_num_state_2_input, [])
        ) is True

        trigger_part_num_state_2_input = [20]
        assert (
            await run_automation(file_path, trigger_part_num_state_2_input, [])
        ) is False

        trigger_part_num_state_2_input = [19]
        assert (
            await run_automation(file_path, trigger_part_num_state_2_input, [])
        ) is False

        trigger_part_num_state_2_input = [None]
        assert (
            await run_automation(file_path, trigger_part_num_state_2_input, [])
        ) is False

        assert real_pos == 1

        # Test case 3: Numerical state trigger with above and below values
        trigger_part_num_state_3 = {
            CONF_PLATFORM: CONF_NUMERIC_STATE,
            CONF_ENTITY_ID: ["sensor.temperature"],
            CONF_ABOVE: 20,
            CONF_BELOW: 30,
        }
        file_path = init_automation_script("trigger_part_num_state_3", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_num_state_3, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_num_state_3, end_position, real_pos = results
        assert len(entities_num_state_3) == 1
        assert entities_num_state_3[0].parent is None
        assert entities_num_state_3[0].position == 1
        assert entities_num_state_3[0].parameter_role == START
        assert entities_num_state_3[0].integration == "sensor"
        assert entities_num_state_3[0].entity_name == "sensor.temperature"
        assert entities_num_state_3[0].expected_value == {
            CONF_ABOVE: 20,
            CONF_BELOW: 30,
        }
        assert end_position == 1

        # border test cases
        trigger_part_num_state_3_input = [25]
        assert (
            await run_automation(file_path, trigger_part_num_state_3_input, [])
        ) is True

        trigger_part_num_state_3_input = [30]
        assert (
            await run_automation(file_path, trigger_part_num_state_3_input, [])
        ) is False

        trigger_part_num_state_3_input = [31]
        assert (
            await run_automation(file_path, trigger_part_num_state_3_input, [])
        ) is False

        trigger_part_num_state_3_input = [20]
        assert (
            await run_automation(file_path, trigger_part_num_state_3_input, [])
        ) is False

        trigger_part_num_state_3_input = [19]
        assert (
            await run_automation(file_path, trigger_part_num_state_3_input, [])
        ) is False

        trigger_part_num_state_3_input = [None]
        assert (
            await run_automation(file_path, trigger_part_num_state_3_input, [])
        ) is False

        assert real_pos == 1

        # Test case 4: Numerical state trigger with above, below, and for values
        trigger_part_num_state_4 = {
            CONF_PLATFORM: CONF_NUMERIC_STATE,
            CONF_ENTITY_ID: ["sensor.temperature"],
            CONF_ABOVE: 20,
            CONF_BELOW: 30,
            CONF_FOR: "00:01:00",
        }
        file_path = init_automation_script("trigger_part_num_state_4", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_num_state_4, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_num_state_4, end_position, real_pos = results
        assert len(entities_num_state_4) == 1
        assert entities_num_state_4[0].parent is None
        assert entities_num_state_4[0].position == 1
        assert entities_num_state_4[0].parameter_role == START
        assert entities_num_state_4[0].integration == "sensor"
        assert entities_num_state_4[0].entity_name == "sensor.temperature"
        assert entities_num_state_4[0].expected_value == {
            CONF_ABOVE: 20,
            CONF_BELOW: 30,
            CONF_FOR: "00:01:00",
        }
        assert end_position == 1

        # border test cases
        trigger_part_num_state_4_input = [25]
        assert (
            await run_automation(file_path, trigger_part_num_state_4_input, [])
        ) is True

        trigger_part_num_state_4_input = [30]
        assert (
            await run_automation(file_path, trigger_part_num_state_4_input, [])
        ) is False

        trigger_part_num_state_4_input = [31]
        assert (
            await run_automation(file_path, trigger_part_num_state_4_input, [])
        ) is False

        trigger_part_num_state_4_input = [20]
        assert (
            await run_automation(file_path, trigger_part_num_state_4_input, [])
        ) is False

        trigger_part_num_state_4_input = [19]
        assert (
            await run_automation(file_path, trigger_part_num_state_4_input, [])
        ) is False

        trigger_part_num_state_4_input = [None]
        assert (
            await run_automation(file_path, trigger_part_num_state_4_input, [])
        ) is False

        assert real_pos == 1

        # Test case 5: Numerical state trigger with above value for an attribute
        trigger_part_num_state_5 = {
            CONF_PLATFORM: CONF_NUMERIC_STATE,
            CONF_ENTITY_ID: ["sensor.temperature"],
            CONF_ATTRIBUTE: "attribute_1",
            CONF_ABOVE: 20,
        }
        file_path = init_automation_script("trigger_part_num_state_5", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_num_state_5, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_num_state_5, end_position, real_pos = results
        assert len(entities_num_state_5) == 1
        assert entities_num_state_5[0].parent is None
        assert entities_num_state_5[0].position == 1
        assert entities_num_state_5[0].parameter_role == START
        assert entities_num_state_5[0].integration == "sensor"
        assert entities_num_state_5[0].entity_name == "sensor.temperature.attribute_1"
        assert entities_num_state_5[0].expected_value == {CONF_ABOVE: 20}
        assert end_position == 1

        # border test cases
        trigger_part_num_state_5_input = [25]
        assert (
            await run_automation(file_path, trigger_part_num_state_5_input, [])
        ) is True

        trigger_part_num_state_5_input = [20]
        assert (
            await run_automation(file_path, trigger_part_num_state_5_input, [])
        ) is False

        trigger_part_num_state_5_input = [19]
        assert (
            await run_automation(file_path, trigger_part_num_state_5_input, [])
        ) is False

        trigger_part_num_state_5_input = [None]
        assert real_pos == 1

        # Test case 6: Numerical state trigger with below entity state
        trigger_part_num_state_6 = {
            CONF_PLATFORM: CONF_NUMERIC_STATE,
            CONF_ENTITY_ID: ["sensor.temperature"],
            CONF_BELOW: "sensor.temperature3",
        }
        file_path = init_automation_script("trigger_part_num_state_6", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_num_state_6, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_num_state_6, end_position, real_pos = results
        assert len(entities_num_state_6) == 2
        assert entities_num_state_6[0].parent == 1
        assert entities_num_state_6[0].position == 2
        assert entities_num_state_6[0].parameter_role == START
        assert entities_num_state_6[0].integration == "sensor"
        assert entities_num_state_6[0].entity_name == "sensor.temperature"
        assert entities_num_state_6[0].expected_value == {
            CONF_BELOW: "sensor.temperature3",
        }
        assert entities_num_state_6[1].parent == 1
        assert entities_num_state_6[1].position == 3
        assert entities_num_state_6[1].parameter_role == START
        assert entities_num_state_6[1].integration == "sensor"
        assert entities_num_state_6[1].entity_name == "sensor.temperature3"
        assert entities_num_state_6[1].expected_value == {
            CONF_ABOVE: "sensor.temperature"
        }
        assert end_position == 3
        # border test cases - the list build like this [CONF_ABOVE, CONF_ENTITY_ID/s, CONF_BELOW]
        trigger_part_num_state_6_input = [20, 25]
        assert (
            await run_automation(file_path, trigger_part_num_state_6_input, [])
        ) is True

        trigger_part_num_state_6_input = [20, 20]
        assert (
            await run_automation(file_path, trigger_part_num_state_6_input, [])
        ) is False

        trigger_part_num_state_6_input = [20, 19]
        assert (
            await run_automation(file_path, trigger_part_num_state_6_input, [])
        ) is False

        trigger_part_num_state_6_input = [20, None]
        assert (
            await run_automation(file_path, trigger_part_num_state_6_input, [])
        ) is True

        trigger_part_num_state_6_input = [None, 20]
        assert (
            await run_automation(file_path, trigger_part_num_state_6_input, [])
        ) is False

        trigger_part_num_state_6_input = [None, None]
        assert (
            await run_automation(file_path, trigger_part_num_state_6_input, [])
        ) is False

        assert real_pos == 2

        # Test case 7: Numerical state trigger with above entity state
        trigger_part_num_state_7 = {
            CONF_PLATFORM: CONF_NUMERIC_STATE,
            CONF_ENTITY_ID: ["sensor.temperature"],
            CONF_ABOVE: "sensor.temperature2",
        }
        file_path = init_automation_script("trigger_part_num_state_7", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_num_state_7, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_num_state_7, end_position, real_pos = results
        assert len(entities_num_state_7) == 2
        assert entities_num_state_7[0].parent == 1
        assert entities_num_state_7[0].position == 2
        assert entities_num_state_7[0].parameter_role == START
        assert entities_num_state_7[0].integration == "sensor"
        assert entities_num_state_7[0].entity_name == "sensor.temperature"
        assert entities_num_state_7[0].expected_value == {
            CONF_ABOVE: "sensor.temperature2",
        }
        assert entities_num_state_7[1].parent == 1
        assert entities_num_state_7[1].position == 3
        assert entities_num_state_7[1].parameter_role == START
        assert entities_num_state_7[1].integration == "sensor"
        assert entities_num_state_7[1].entity_name == "sensor.temperature2"
        assert entities_num_state_7[1].expected_value == {
            CONF_BELOW: "sensor.temperature"
        }
        assert end_position == 3
        # border test cases - the list build like this [CONF_ABOVE, CONF_ENTITY_ID/s, CONF_BELOW]
        trigger_part_num_state_7_input = [20, 25]
        assert (
            await run_automation(file_path, trigger_part_num_state_7_input, [])
        ) is True

        trigger_part_num_state_7_input = [20, 20]
        assert (
            await run_automation(file_path, trigger_part_num_state_7_input, [])
        ) is False

        trigger_part_num_state_7_input = [35, 30]
        assert (
            await run_automation(file_path, trigger_part_num_state_7_input, [])
        ) is False

        trigger_part_num_state_7_input = [20, None]
        assert (
            await run_automation(file_path, trigger_part_num_state_7_input, [])
        ) is False

        trigger_part_num_state_7_input = [None, 20]
        assert (
            await run_automation(file_path, trigger_part_num_state_7_input, [])
        ) is True

        trigger_part_num_state_7_input = [None, None]
        assert (
            await run_automation(file_path, trigger_part_num_state_7_input, [])
        ) is False

        assert real_pos == 2

        # Test case 8: Numerical state trigger with multiple entities, above, and below entity states and
        # at a specific position
        trigger_part_num_state_8 = {
            CONF_PLATFORM: CONF_NUMERIC_STATE,
            CONF_ENTITY_ID: ["sensor.temperature", "sensor.temperature4"],
            CONF_ABOVE: "sensor.temperature3",
            CONF_BELOW: "sensor.temperature2",
        }
        file_path = init_automation_script("trigger_part_num_state_8", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_num_state_8, position=2, real_position=2, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_num_state_8, end_position, real_pos = results
        assert len(entities_num_state_8) == 4
        assert entities_num_state_8[0].parent == 3
        assert entities_num_state_8[0].position == 4
        assert entities_num_state_8[0].parameter_role == START
        assert entities_num_state_8[0].integration == "sensor"
        assert entities_num_state_8[0].entity_name == "sensor.temperature"
        assert entities_num_state_8[0].expected_value == {
            CONF_BELOW: "sensor.temperature2",
            CONF_ABOVE: "sensor.temperature3",
        }
        assert entities_num_state_8[1].parent == 3
        assert entities_num_state_8[1].position == 5
        assert entities_num_state_8[1].parameter_role == START
        assert entities_num_state_8[1].integration == "sensor"
        assert entities_num_state_8[1].entity_name == "sensor.temperature4"
        assert entities_num_state_8[1].expected_value == {
            CONF_BELOW: "sensor.temperature2",
            CONF_ABOVE: "sensor.temperature3",
        }
        assert entities_num_state_8[2].parent == 2
        assert entities_num_state_8[2].position == 6
        assert entities_num_state_8[2].parameter_role == START
        assert entities_num_state_8[2].integration == "sensor"
        assert entities_num_state_8[2].entity_name == "sensor.temperature3"
        assert entities_num_state_8[2].expected_value == {
            CONF_BELOW: ["sensor.temperature", "sensor.temperature4"]
        }
        assert entities_num_state_8[3].parent == 2
        assert entities_num_state_8[3].position == 7
        assert entities_num_state_8[3].parameter_role == START
        assert entities_num_state_8[3].integration == "sensor"
        assert entities_num_state_8[3].entity_name == "sensor.temperature2"
        assert entities_num_state_8[3].expected_value == {
            CONF_ABOVE: ["sensor.temperature", "sensor.temperature4"]
        }
        assert end_position == 7
        # border test cases -  - the list build like this [CONF_ABOVE, CONF_ENTITY_ID/s, CONF_BELOW]
        # position 0 and 1 are not used by the script
        trigger_part_num_state_8_input = ["filler", "filler", 10, 20, 20, 30]
        assert (
            await run_automation(file_path, trigger_part_num_state_8_input, [])
        ) is True

        trigger_part_num_state_8_input = ["filler", "filler", 23, 20, 20, 30]
        assert (
            await run_automation(file_path, trigger_part_num_state_8_input, [])
        ) is False

        trigger_part_num_state_8_input = ["filler", "filler", 10, 20, 20, 19]
        assert (
            await run_automation(file_path, trigger_part_num_state_8_input, [])
        ) is False

        trigger_part_num_state_8_input = ["filler", "filler", 10, 20, 18, 19]
        assert (
            await run_automation(file_path, trigger_part_num_state_8_input, [])
        ) is True

        trigger_part_num_state_8_input = ["filler", "filler", None, None, 20, None]
        assert (
            await run_automation(file_path, trigger_part_num_state_8_input, [])
        ) is True

        trigger_part_num_state_8_input = ["filler", "filler", None, 20, None, 544]
        assert (
            await run_automation(file_path, trigger_part_num_state_8_input, [])
        ) is True

        trigger_part_num_state_8_input = ["filler", "filler", 2, 20, None, None]
        assert (
            await run_automation(file_path, trigger_part_num_state_8_input, [])
        ) is True

        trigger_part_num_state_8_input = ["filler", "filler", 2, None, None, None]
        assert (
            await run_automation(file_path, trigger_part_num_state_8_input, [])
        ) is False

        trigger_part_num_state_8_input = ["filler", "filler", 2, None, None, 50]
        assert (
            await run_automation(file_path, trigger_part_num_state_8_input, [])
        ) is False

        trigger_part_num_state_8_input = ["filler", "filler", None, None, None, None]
        assert (
            await run_automation(file_path, trigger_part_num_state_8_input, [])
        ) is False

        assert real_pos == 6

    async def test_trigger_state():
        # # Test case 1: State trigger with on values
        trigger_part_state_1 = {
            CONF_PLATFORM: CONF_STATE,
            CONF_ENTITY_ID: ["binary_sensor.motion"],
        }
        file_path = init_automation_script("trigger_part_state_1", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_state_1, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_state_1, end_position, real_pos = results
        assert len(entities_state_1) == 1
        assert entities_state_1[0].parent is None
        assert entities_state_1[0].position == 1
        assert entities_state_1[0].parameter_role == START
        assert entities_state_1[0].integration == "binary_sensor"
        assert entities_state_1[0].entity_name == "binary_sensor.motion"
        assert entities_state_1[0].expected_value is None
        assert end_position == 1

        trigger_part_state_1_input = ["on"]
        assert (await run_automation(file_path, trigger_part_state_1_input, [])) is True

        trigger_part_state_1_input = ["off"]
        assert (await run_automation(file_path, trigger_part_state_1_input, [])) is True

        trigger_part_state_1_input = ["unknown"]
        assert (await run_automation(file_path, trigger_part_state_1_input, [])) is True

        trigger_part_state_1_input = ["unavailable"]
        assert (await run_automation(file_path, trigger_part_state_1_input, [])) is True

        trigger_part_state_1_input = [None]
        assert (
            await run_automation(file_path, trigger_part_state_1_input, [])
        ) is False

        assert real_pos == 1

        # Test case 2: State trigger with on values
        trigger_part_state_2 = {
            CONF_PLATFORM: CONF_STATE,
            CONF_ENTITY_ID: ["binary_sensor.motion"],
            CONF_TO: "on",
        }
        file_path = init_automation_script("trigger_part_state_2", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_state_2, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_state_2, end_position, real_pos = results
        assert len(entities_state_2) == 1
        assert entities_state_2[0].parent is None
        assert entities_state_2[0].position == 1
        assert entities_state_2[0].parameter_role == START
        assert entities_state_2[0].integration == "binary_sensor"
        assert entities_state_2[0].entity_name == "binary_sensor.motion"
        assert entities_state_2[0].expected_value == {CONF_TO: "on"}
        assert end_position == 1

        trigger_part_state_2_input = ["on"]
        assert (await run_automation(file_path, trigger_part_state_2_input, [])) is True

        for state_val in ["off", "unknown", "unavailable", None]:
            trigger_part_state_2_input = [state_val]
            assert (
                await run_automation(file_path, trigger_part_state_2_input, [])
            ) is False

        assert real_pos == 1

        # Test case 3: State trigger with from and to values
        trigger_part_state_3 = {
            CONF_PLATFORM: CONF_STATE,
            CONF_ENTITY_ID: ["binary_sensor.motion"],
            CONF_FROM: "off",
            CONF_TO: "on",
        }
        file_path = init_automation_script("trigger_part_state_3", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_state_3, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_state_3, end_position, real_pos = results
        assert len(entities_state_3) == 1
        assert entities_state_3[0].parent is None
        assert entities_state_3[0].position == 1
        assert entities_state_3[0].parameter_role == START
        assert entities_state_3[0].integration == "binary_sensor"
        assert entities_state_3[0].entity_name == "binary_sensor.motion"
        assert entities_state_3[0].expected_value == {CONF_TO: "on", CONF_FROM: "off"}
        assert end_position == 1

        trigger_part_state_3_input = ["on"]
        assert (await run_automation(file_path, trigger_part_state_3_input, [])) is True

        for state_val in ["off", "unknown", "unavailable", None]:
            trigger_part_state_3_input = [state_val]
            assert (
                await run_automation(file_path, trigger_part_state_3_input, [])
            ) is False

        assert real_pos == 1

        # Test case 4: State trigger with from, to, and for values
        trigger_part_state_4 = {
            CONF_PLATFORM: CONF_STATE,
            CONF_ENTITY_ID: ["binary_sensor.motion"],
            CONF_FROM: "off",
            CONF_TO: "on",
            CONF_FOR: "00:01:00",
        }
        file_path = init_automation_script("trigger_part_state_4", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_state_4, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_state_4, end_position, real_pos = results
        assert len(entities_state_4) == 1
        assert entities_state_4[0].parent is None
        assert entities_state_4[0].position == 1
        assert entities_state_4[0].parameter_role == START
        assert entities_state_4[0].integration == "binary_sensor"
        assert entities_state_4[0].entity_name == "binary_sensor.motion"
        assert entities_state_4[0].expected_value == {
            CONF_TO: "on",
            CONF_FROM: "off",
            CONF_FOR: "00:01:00",
        }
        assert end_position == 1

        trigger_part_state_4_input = ["on"]
        assert (await run_automation(file_path, trigger_part_state_4_input, [])) is True

        for state_val in ["off", "unknown", "unavailable", None]:
            trigger_part_state_4_input = [state_val]
            assert (
                await run_automation(file_path, trigger_part_state_4_input, [])
            ) is False

        assert real_pos == 1

        # Test case 5: State trigger with not from and not to values
        trigger_part_state_5 = {
            CONF_PLATFORM: CONF_STATE,
            CONF_ENTITY_ID: ["binary_sensor.motion"],
            CONF_NOT_TO: "on",
            CONF_NOT_FROM: "off",
        }
        file_path = init_automation_script("trigger_part_state_5", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_state_5, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_state_5, end_position, real_pos = results
        assert len(entities_state_5) == 1
        assert entities_state_5[0].parent is None
        assert entities_state_5[0].position == 1
        assert entities_state_5[0].parameter_role == START
        assert entities_state_5[0].integration == "binary_sensor"
        assert entities_state_5[0].entity_name == "binary_sensor.motion"
        assert entities_state_5[0].expected_value == {
            CONF_NOT_TO: "on",
            CONF_NOT_FROM: "off",
        }
        assert end_position == 1

        trigger_part_state_5_input = ["on"]
        assert (
            await run_automation(file_path, trigger_part_state_5_input, [])
        ) is False

        trigger_part_state_5_input = [None]
        assert (
            await run_automation(file_path, trigger_part_state_5_input, [])
        ) is False

        for state_val in ["off", "unknown", "unavailable"]:
            trigger_part_state_5_input = [state_val]
            assert (
                await run_automation(file_path, trigger_part_state_5_input, [])
            ) is True

        assert real_pos == 1

        # Test case 6: State trigger with attribute value
        trigger_part_state_6 = {
            CONF_PLATFORM: CONF_STATE,
            CONF_ENTITY_ID: ["binary_sensor.motion"],
            CONF_ATTRIBUTE: "attribute_1",
            CONF_TO: "temp2",
            CONF_FROM: "temp1",
        }
        file_path = init_automation_script("trigger_part_state_6", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_state_6, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_state_6, end_position, real_pos = results
        assert len(entities_state_6) == 1
        assert entities_state_6[0].parent is None
        assert entities_state_6[0].position == 1
        assert entities_state_6[0].parameter_role == START
        assert entities_state_6[0].integration == "binary_sensor"
        assert entities_state_6[0].entity_name == "binary_sensor.motion.attribute_1"
        assert entities_state_6[0].expected_value == {
            CONF_TO: "temp2",
            CONF_FROM: "temp1",
        }
        assert end_position == 1

        trigger_part_state_6_input = ["temp2"]
        assert (await run_automation(file_path, trigger_part_state_6_input, [])) is True

        for state_val in ["temp1", "temp3", "temp4", None]:
            trigger_part_state_6_input = [state_val]
            assert (
                await run_automation(file_path, trigger_part_state_6_input, [])
            ) is False

        assert real_pos == 1

        # Test case 7: State trigger with multiple entity ids
        trigger_part_state_7 = {
            CONF_PLATFORM: CONF_STATE,
            CONF_ENTITY_ID: ["binary_sensor.motion", "binary_sensor.motion_2"],
            CONF_TO: "on",
        }
        file_path = init_automation_script("trigger_part_state_7", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_state_7, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_state_7, end_position, real_pos = results
        assert len(entities_state_7) == 2
        assert entities_state_7[0].parent == 1
        assert entities_state_7[0].position == 2
        assert entities_state_7[0].parameter_role == START
        assert entities_state_7[0].integration == "binary_sensor"
        assert entities_state_7[0].entity_name == "binary_sensor.motion"
        assert entities_state_7[0].expected_value == {CONF_TO: "on"}
        assert entities_state_7[1].parent == 1
        assert entities_state_7[1].position == 3
        assert entities_state_7[1].parameter_role == START
        assert entities_state_7[1].integration == "binary_sensor"
        assert entities_state_7[1].entity_name == "binary_sensor.motion_2"
        assert entities_state_7[1].expected_value == {CONF_TO: "on"}
        assert end_position == 3

        # border test cases
        # the list build like this [CONF_ENTITY_ID/s]

        # the first entity is on
        trigger_part_state_7_input = ["on", "off"]
        assert (await run_automation(file_path, trigger_part_state_7_input, [])) is True

        # the first entity is off
        trigger_part_state_7_input = ["off", "on"]
        assert (await run_automation(file_path, trigger_part_state_7_input, [])) is True

        # both entities are off
        trigger_part_state_7_input = ["off", "off"]
        assert (
            await run_automation(file_path, trigger_part_state_7_input, [])
        ) is False

        # the first entity is on and the second is None
        trigger_part_state_7_input = ["on", None]
        assert (await run_automation(file_path, trigger_part_state_7_input, [])) is True

        # the first entity is None and the second is on
        trigger_part_state_7_input = [None, "on"]
        assert (await run_automation(file_path, trigger_part_state_7_input, [])) is True

        # both entities are None
        trigger_part_state_7_input = [None, None]
        assert (
            await run_automation(file_path, trigger_part_state_7_input, [])
        ) is False

        assert real_pos == 2

        # Test case 8: State trigger with conditional entity state
        trigger_part_state_8 = {
            CONF_PLATFORM: CONF_STATE,
            CONF_ENTITY_ID: ["binary_sensor.motion"],
            CONF_TO: "binary_sensor.motion_2",
        }
        file_path = init_automation_script("trigger_part_state_8", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_state_8, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_state_8, end_position, real_pos = results
        assert len(entities_state_8) == 2
        assert entities_state_8[0].parent == 1
        assert entities_state_8[0].position == 2
        assert entities_state_8[0].parameter_role == START
        assert entities_state_8[0].integration == "binary_sensor"
        assert entities_state_8[0].entity_name == "binary_sensor.motion"
        assert entities_state_8[0].expected_value == {CONF_TO: "binary_sensor.motion_2"}
        assert entities_state_8[1].parent == 1
        assert entities_state_8[1].position == 3
        assert entities_state_8[1].parameter_role == START
        assert entities_state_8[1].integration == "binary_sensor"
        assert entities_state_8[1].entity_name == "binary_sensor.motion_2"
        assert end_position == 3

        # border test cases - the list build like this [CONF_TO, CONF_ENTITY_ID/s]
        # the enitity is off but the expected value is on
        trigger_part_state_8_input = ["on", "off"]
        assert (
            await run_automation(file_path, trigger_part_state_8_input, [])
        ) is False

        # the enitity is off as expected
        trigger_part_state_8_input = ["off", "off"]
        assert (await run_automation(file_path, trigger_part_state_8_input, [])) is True

        # the enitity is on as expected
        trigger_part_state_8_input = ["on", "on"]
        assert (await run_automation(file_path, trigger_part_state_8_input, [])) is True

        # the enitity is None
        trigger_part_state_8_input = [None, "on"]
        assert (
            await run_automation(file_path, trigger_part_state_8_input, [])
        ) is False

        # the enitity is None
        trigger_part_state_8_input = [None, None]
        assert (
            await run_automation(file_path, trigger_part_state_8_input, [])
        ) is False

        # the enitity is on but the expected value is None
        trigger_part_state_8_input = ["on", None]
        assert (
            await run_automation(file_path, trigger_part_state_8_input, [])
        ) is False

        assert real_pos == 2

        # Test case 9: State trigger with multiple entity ids and conditional entity state
        trigger_part_state_9 = {
            CONF_PLATFORM: CONF_STATE,
            CONF_ENTITY_ID: ["binary_sensor.motion", "binary_sensor.motion_2"],
            CONF_TO: [
                "binary_sensor.motion_3",
                "unknown",
                "binary_sensor.motion_4",
                "on",
            ],
        }
        file_path = init_automation_script("trigger_part_state_9", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_state_9, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_state_9, end_position, real_pos = results
        assert len(entities_state_9) == 4
        assert entities_state_9[0].parent == 2
        assert entities_state_9[0].position == 3
        assert entities_state_9[0].parameter_role == START
        assert entities_state_9[0].integration == "binary_sensor"
        assert entities_state_9[0].entity_name == "binary_sensor.motion"
        assert entities_state_9[0].expected_value == {
            CONF_TO: [
                "binary_sensor.motion_3",
                "unknown",
                "binary_sensor.motion_4",
                "on",
            ]
        }
        assert entities_state_9[1].parent == 2
        assert entities_state_9[1].position == 4
        assert entities_state_9[1].parameter_role == START
        assert entities_state_9[1].integration == "binary_sensor"
        assert entities_state_9[1].entity_name == "binary_sensor.motion_2"
        assert entities_state_9[1].expected_value == {
            CONF_TO: [
                "binary_sensor.motion_3",
                "unknown",
                "binary_sensor.motion_4",
                "on",
            ]
        }
        assert entities_state_9[2].parent == 1
        assert entities_state_9[2].position == 5
        assert entities_state_9[2].parameter_role == START
        assert entities_state_9[2].integration == "binary_sensor"
        assert entities_state_9[2].entity_name == "binary_sensor.motion_3"
        assert entities_state_9[3].parent == 1
        assert entities_state_9[3].position == 6
        assert entities_state_9[3].parameter_role == START
        assert entities_state_9[3].integration == "binary_sensor"
        assert entities_state_9[3].entity_name == "binary_sensor.motion_4"
        assert end_position == 6

        # border test cases - the list build like this [CONF_TO, CONF_ENTITY_ID/s]
        trigger_part_state_9_input = ["test1", "test", "test1", "off"]
        assert (await run_automation(file_path, trigger_part_state_9_input, [])) is True

        trigger_part_state_9_input = ["test1", "test1", "test", "off"]
        assert (
            await run_automation(file_path, trigger_part_state_9_input, [])
        ) is False

        trigger_part_state_9_input = ["on", "off", "off", "on"]
        assert (await run_automation(file_path, trigger_part_state_9_input, [])) is True

        trigger_part_state_9_input = [None, None, "off", "off"]
        assert (
            await run_automation(file_path, trigger_part_state_9_input, [])
        ) is False

        trigger_part_state_9_input = [None, None, "unknown", None]
        assert (await run_automation(file_path, trigger_part_state_9_input, [])) is True

        trigger_part_state_9_input = [None, None, None, "on"]
        assert (await run_automation(file_path, trigger_part_state_9_input, [])) is True

        trigger_part_state_9_input = [None, None, None, None]
        assert (
            await run_automation(file_path, trigger_part_state_9_input, [])
        ) is False

        real_pos == 4

        # Test case 10: State trigger on a attribute with multiple conditions and conditional entity state
        trigger_part_state_10 = {
            "platform": "state",
            "entity_id": ["humidifier.hygrostat"],
            "attribute": "humidity",
            "to": [1, "20", "sensor.outside_humidity"],
        }
        file_path = init_automation_script("trigger_part_state_10", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_state_10, position=23, real_position=19, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_state_10, end_position, real_pos = results
        assert len(entities_state_10) == 2
        assert entities_state_10[0].parent == 23
        assert entities_state_10[0].position == 24
        assert entities_state_10[0].parameter_role == START
        assert entities_state_10[0].integration == "humidifier"
        assert entities_state_10[0].entity_name == "humidifier.hygrostat.humidity"
        assert entities_state_10[0].expected_value == {
            "to": [1, "20", "sensor.outside_humidity"]
        }
        assert entities_state_10[1].parent == 23
        assert entities_state_10[1].position == 25
        assert entities_state_10[1].parameter_role == START
        assert entities_state_10[1].integration == "sensor"
        assert entities_state_10[1].entity_name == "sensor.outside_humidity"
        assert end_position == 25

        # border test cases - the list build like this [CONF_TO, CONF_ENTITY_ID/s]
        trigger_part_state_10_input = [
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "test",
            "20",
        ]
        assert (
            await run_automation(file_path, trigger_part_state_10_input, [])
        ) is True

        trigger_part_state_10_input = [
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "test",
            21,
        ]
        assert (
            await run_automation(file_path, trigger_part_state_10_input, [])
        ) is False

        trigger_part_state_10_input = [
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            1,
            None,
        ]
        assert (
            await run_automation(file_path, trigger_part_state_10_input, [])
        ) is False

        trigger_part_state_10_input = [
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "79",
            "79",
        ]
        assert (
            await run_automation(file_path, trigger_part_state_10_input, [])
        ) is True

        trigger_part_state_10_input = [
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "test",
            1,
        ]
        assert (
            await run_automation(file_path, trigger_part_state_10_input, [])
        ) is True

    async def test_trigger_sun():
        # Test case 1: Sun trigger
        trigger_part_sun_1 = {CONF_PLATFORM: "sun", CONF_EVENT: "sunset"}
        file_path = init_automation_script("trigger_part_sun_1", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_sun_1, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_sun_1, end_position, real_pos = results
        assert len(entities_sun_1) == 1
        assert entities_sun_1[0].parent is None
        assert entities_sun_1[0].position == 1
        assert entities_sun_1[0].parameter_role == START
        assert entities_sun_1[0].integration == "sun"
        assert entities_sun_1[0].entity_name == "sun.sun"
        assert entities_sun_1[0].expected_value == {CONF_EVENT: "sunset"}
        assert end_position == 1

        trigger_part_sun_1_input = [True]
        assert (await run_automation(file_path, trigger_part_sun_1_input, [])) is True

        trigger_part_sun_1_input = [False]
        assert (await run_automation(file_path, trigger_part_sun_1_input, [])) is False

        trigger_part_sun_1_input = [None]
        assert (await run_automation(file_path, trigger_part_sun_1_input, [])) is False

        assert real_pos == 1

        # Test case 2: Sun trigger with offset
        trigger_part_sun_2 = {
            CONF_PLATFORM: "sun",
            CONF_EVENT: "sunset",
            CONF_OFFSET: "-01:00:00",
        }
        file_path = init_automation_script("trigger_part_sun_2", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_sun_2, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_sun_2, end_position, real_pos = results
        assert len(entities_sun_2) == 1
        assert entities_sun_2[0].parent is None
        assert entities_sun_2[0].position == 1
        assert entities_sun_2[0].parameter_role == START
        assert entities_sun_2[0].integration == "sun"
        assert entities_sun_2[0].entity_name == "sun.sun"
        assert entities_sun_2[0].expected_value == {
            CONF_EVENT: "sunset",
            CONF_OFFSET: "-01:00:00",
        }
        assert end_position == 1

        trigger_part_sun_2_input = [True]
        assert (await run_automation(file_path, trigger_part_sun_2_input, [])) is True

        trigger_part_sun_2_input = [False]
        assert (await run_automation(file_path, trigger_part_sun_2_input, [])) is False

        trigger_part_sun_2_input = [None]
        assert (await run_automation(file_path, trigger_part_sun_2_input, [])) is False

        assert real_pos == 1

    async def test_trigger_tag():
        # Test case 1: Tag trigger with single device
        trigger_part_tag_1 = {
            CONF_PLATFORM: "tag",
            TAG_ID: "tag_id_1",
            CONF_DEVICE_ID: "device_id_1",
        }
        file_path = init_automation_script("trigger_part_tag_1", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_tag_1, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_tag_1, end_position, real_pos = results
        assert len(entities_tag_1) == 1
        assert entities_tag_1[0].parent is None
        assert entities_tag_1[0].position == 1
        assert entities_tag_1[0].parameter_role == START
        assert entities_tag_1[0].integration == "tag"
        assert entities_tag_1[0].entity_name == "tag.tag_id_1"
        assert entities_tag_1[0].expected_value == {CONF_DEVICE_ID: "device_id_1"}
        assert end_position == 1

        trigger_part_tag_1_input = [True]
        assert (await run_automation(file_path, trigger_part_tag_1_input, [])) is True

        trigger_part_tag_1_input = [False]
        assert (await run_automation(file_path, trigger_part_tag_1_input, [])) is False

        trigger_part_tag_1_input = [None]
        assert (await run_automation(file_path, trigger_part_tag_1_input, [])) is False

        assert real_pos == 1

        # Test case 2: Tag trigger with multiple devices
        trigger_part_tag_2 = {
            CONF_PLATFORM: "tag",
            TAG_ID: "tag_id_2",
            CONF_DEVICE_ID: ["device_id_2", "device_id_3"],
        }
        file_path = init_automation_script("trigger_part_tag_2", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_tag_2, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_tag_2, end_position, real_pos = results
        assert len(entities_tag_2) == 1
        assert entities_tag_2[0].parent is None
        assert entities_tag_2[0].position == 1
        assert entities_tag_2[0].parameter_role == START
        assert entities_tag_2[0].integration == "tag"
        assert entities_tag_2[0].entity_name == "tag.tag_id_2"
        assert entities_tag_2[0].expected_value == {
            CONF_DEVICE_ID: ["device_id_2", "device_id_3"]
        }
        assert end_position == 1

        trigger_part_tag_2_input = [True]
        assert (await run_automation(file_path, trigger_part_tag_2_input, [])) is True

        trigger_part_tag_2_input = [False]
        assert (await run_automation(file_path, trigger_part_tag_2_input, [])) is False

        trigger_part_tag_2_input = [None]
        assert (await run_automation(file_path, trigger_part_tag_2_input, [])) is False

        assert real_pos == 1

        # Test case 3: Tag trigger with multiple tags and devices
        trigger_part_tag_3 = {
            CONF_PLATFORM: "tag",
            TAG_ID: ["tag_id_2", "tag_id_3"],
            CONF_DEVICE_ID: ["device_id_2", "device_id_3"],
        }
        file_path = init_automation_script("trigger_part_tag_3", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_tag_3, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_tag_3, end_position, real_pos = results
        assert len(entities_tag_3) == 2
        assert entities_tag_3[0].parent == 1
        assert entities_tag_3[0].position == 2
        assert entities_tag_3[0].parameter_role == START
        assert entities_tag_3[0].integration == "tag"
        assert entities_tag_3[0].entity_name == "tag.tag_id_2"
        assert entities_tag_3[0].expected_value == {
            CONF_DEVICE_ID: ["device_id_2", "device_id_3"]
        }
        assert entities_tag_3[1].position == 3
        assert entities_tag_3[1].parameter_role == START
        assert entities_tag_3[1].integration == "tag"
        assert entities_tag_3[1].entity_name == "tag.tag_id_3"
        assert entities_tag_3[1].expected_value == {
            CONF_DEVICE_ID: ["device_id_2", "device_id_3"]
        }
        assert end_position == 3
        trigger_part_tag_3_input = [True, False]
        assert (await run_automation(file_path, trigger_part_tag_3_input, [])) is True

        trigger_part_tag_3_input = [False, True]
        assert (await run_automation(file_path, trigger_part_tag_3_input, [])) is True

        trigger_part_tag_3_input = [None, None]
        assert (await run_automation(file_path, trigger_part_tag_3_input, [])) is False

        trigger_part_tag_3_input = [None, True]
        assert (await run_automation(file_path, trigger_part_tag_3_input, [])) is True

        trigger_part_tag_3_input = [False, None]
        assert (await run_automation(file_path, trigger_part_tag_3_input, [])) is False

        assert real_pos == 2

    async def test_trigger_template():
        # Test case 1: Template trigger with a value
        trigger_part_template_1 = {
            CONF_PLATFORM: "template",
            CONF_VALUE_TEMPLATE: "{% if is_state('device_tracker.paulus', 'home') %}true{% endif %}",
        }
        file_path = init_automation_script("trigger_part_template_1", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_template_1, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_template_1, end_position, real_pos = results
        assert len(entities_template_1) == 1
        assert entities_template_1[0].parent == 1
        assert entities_template_1[0].position == 2
        assert entities_template_1[0].parameter_role == START
        assert entities_template_1[0].integration == "device_tracker"
        assert entities_template_1[0].entity_name == "device_tracker.paulus"
        assert entities_template_1[0].expected_value == {
            CONF_VALUE_TEMPLATE: "{% if is_state('device_tracker.paulus', 'home') %}true{% endif %}"
        }
        assert end_position == 2
        trigger_part_template_1_input = [True]
        assert (
            await run_automation(file_path, trigger_part_template_1_input, [])
        ) is True
        trigger_part_template_1_input = [False]
        assert (
            await run_automation(file_path, trigger_part_template_1_input, [])
        ) is False
        trigger_part_template_1_input = [None]
        assert (
            await run_automation(file_path, trigger_part_template_1_input, [])
        ) is False
        assert real_pos == 1

        # Test case 2: Template trigger with two values
        trigger_part_template_2 = {
            CONF_PLATFORM: "template",
            CONF_VALUE_TEMPLATE: "{{ is_state('device_tracker.paulus', 'home') and is_state('device_tracker.anne_therese', 'home') }}",
        }
        file_path = init_automation_script("trigger_part_template_2", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_template_2, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_template_2, end_position, real_pos = results
        assert len(entities_template_2) == 2
        assert entities_template_2[0].parent == 1
        assert entities_template_2[0].position == 2
        assert entities_template_2[0].parameter_role == START
        assert entities_template_2[0].integration == "device_tracker"
        assert entities_template_2[0].entity_name == "device_tracker.paulus"
        assert entities_template_2[0].expected_value == {
            CONF_VALUE_TEMPLATE: "{{ is_state('device_tracker.paulus', 'home') and is_state('device_tracker.anne_therese', 'home') }}"
        }
        assert entities_template_2[1].position == 3
        assert entities_template_2[1].parameter_role == START
        assert entities_template_2[1].integration == "device_tracker"
        assert entities_template_2[1].entity_name == "device_tracker.anne_therese"
        assert entities_template_2[1].expected_value == {
            CONF_VALUE_TEMPLATE: "{{ is_state('device_tracker.paulus', 'home') and is_state('device_tracker.anne_therese', 'home') }}"
        }
        assert end_position == 3
        trigger_part_template_2_input = [True, True]
        assert (
            await run_automation(file_path, trigger_part_template_2_input, [])
        ) is True
        trigger_part_template_2_input = [True, False]
        assert (
            await run_automation(file_path, trigger_part_template_2_input, [])
        ) is True
        trigger_part_template_2_input = [None, True]
        assert (
            await run_automation(file_path, trigger_part_template_2_input, [])
        ) is True
        trigger_part_template_2_input = [False, False]
        assert (
            await run_automation(file_path, trigger_part_template_2_input, [])
        ) is False
        trigger_part_template_2_input = [None, None]
        assert (
            await run_automation(file_path, trigger_part_template_2_input, [])
        ) is False
        trigger_part_template_2_input = [None, False]
        assert (
            await run_automation(file_path, trigger_part_template_2_input, [])
        ) is False
        assert real_pos == 2

        # Test case 3: Template trigger with value and for
        trigger_part_template_3 = {
            CONF_PLATFORM: "template",
            CONF_VALUE_TEMPLATE: "{{ is_state('device_tracker.paulus', 'home') }}",
            CONF_FOR: "00:01:00",
        }
        file_path = init_automation_script("trigger_part_template_3", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_template_3, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_template_3, end_position, real_pos = results
        assert len(entities_template_3) == 1
        assert entities_template_3[0].parent == 1
        assert entities_template_3[0].position == 2
        assert entities_template_3[0].parameter_role == START
        assert entities_template_3[0].integration == "device_tracker"
        assert entities_template_3[0].entity_name == "device_tracker.paulus"
        assert entities_template_3[0].expected_value == {
            CONF_VALUE_TEMPLATE: "{{ is_state('device_tracker.paulus', 'home') }}",
            CONF_FOR: "00:01:00",
        }
        assert end_position == 2
        trigger_part_template_3_input = [True]
        assert (
            await run_automation(file_path, trigger_part_template_3_input, [])
        ) is True
        trigger_part_template_3_input = [False]
        assert (
            await run_automation(file_path, trigger_part_template_3_input, [])
        ) is False
        trigger_part_template_3_input = [None]
        assert (
            await run_automation(file_path, trigger_part_template_3_input, [])
        ) is False
        assert real_pos == 1

    async def test_trigger_time():
        # Test case 1: Time trigger at 06:05:02
        trigger_part_time_1 = {CONF_PLATFORM: "time", CONF_AT: "06:05:02"}
        file_path = init_automation_script("trigger_part_time_1", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_time_1, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_time_1, end_position, real_pos = results
        assert len(entities_time_1) == 1
        assert entities_time_1[0].parent is None
        assert entities_time_1[0].position == 1
        assert entities_time_1[0].parameter_role == START
        assert entities_time_1[0].integration == "time"
        assert entities_time_1[0].entity_name == "time.time"
        assert entities_time_1[0].expected_value == {CONF_AT: "06:05:02"}
        assert end_position == 1

        trigger_part_time_1_input = [True]
        assert (await run_automation(file_path, trigger_part_time_1_input, [])) is True

        trigger_part_time_1_input = [False]
        assert (await run_automation(file_path, trigger_part_time_1_input, [])) is False

        trigger_part_time_1_input = [None]
        assert (await run_automation(file_path, trigger_part_time_1_input, [])) is False

        assert real_pos == 1

        # Test case 2: Time trigger at 06:05 and 06:10
        trigger_part_time_2 = {CONF_PLATFORM: "time", CONF_AT: ["06:05", "06:10"]}
        file_path = init_automation_script("trigger_part_time_2", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_time_2, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_time_2, end_position, real_pos = results
        assert len(entities_time_2) == 2
        assert entities_time_2[0].parent == 1
        assert entities_time_2[0].position == 2
        assert entities_time_2[0].parameter_role == START
        assert entities_time_2[0].integration == "time"
        assert entities_time_2[0].entity_name == "time.time"
        assert entities_time_2[0].expected_value == {CONF_AT: "06:05"}
        assert entities_time_2[1].position == 3
        assert entities_time_2[1].parameter_role == START
        assert entities_time_2[1].integration == "time"
        assert entities_time_2[1].entity_name == "time.time"
        assert entities_time_2[1].expected_value == {CONF_AT: "06:10"}
        assert end_position == 3

        trigger_part_time_2_input = [True, False]
        assert (await run_automation(file_path, trigger_part_time_2_input, [])) is True

        trigger_part_time_2_input = [False, True]
        assert (await run_automation(file_path, trigger_part_time_2_input, [])) is True

        trigger_part_time_2_input = [None, None]
        assert (await run_automation(file_path, trigger_part_time_2_input, [])) is False

        trigger_part_time_2_input = [None, True]
        assert (await run_automation(file_path, trigger_part_time_2_input, [])) is True

        trigger_part_time_2_input = [False, None]
        assert (await run_automation(file_path, trigger_part_time_2_input, [])) is False

        assert real_pos == 2

    async def test_trigger_time_pattern():
        # Test case 1: Time pattern trigger at **:**:02 seconds
        trigger_part_time_pattern_1 = {CONF_PLATFORM: "time_pattern", SECONDS: 2}
        file_path = init_automation_script("trigger_part_time_pattern_1", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_time_pattern_1,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        test_trigger_return(file_path)

        entities_time_pattern_1, end_position, real_pos = results
        assert len(entities_time_pattern_1) == 1
        assert entities_time_pattern_1[0].parent is None
        assert entities_time_pattern_1[0].position == 1
        assert entities_time_pattern_1[0].parameter_role == START
        assert entities_time_pattern_1[0].integration == "time_pattern"
        assert entities_time_pattern_1[0].entity_name is not None
        assert entities_time_pattern_1[0].expected_value == {SECONDS: 2}
        assert end_position == 1

        trigger_part_time_pattern_1_input = [True]
        assert (
            await run_automation(file_path, trigger_part_time_pattern_1_input, [])
        ) is True

        trigger_part_time_pattern_1_input = [False]
        assert (
            await run_automation(file_path, trigger_part_time_pattern_1_input, [])
        ) is False

        trigger_part_time_pattern_1_input = [None]
        assert (
            await run_automation(file_path, trigger_part_time_pattern_1_input, [])
        ) is False

        assert real_pos == 1

        # Test case 2: Time pattern trigger at **:02:00
        trigger_part_time_pattern_2 = {CONF_PLATFORM: "time_pattern", MINUTES: 2}
        file_path = init_automation_script("trigger_part_time_pattern_2", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_time_pattern_2,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        test_trigger_return(file_path)

        entities_time_pattern_2, end_position, real_pos = results
        assert len(entities_time_pattern_2) == 1
        assert entities_time_pattern_2[0].parent is None
        assert entities_time_pattern_2[0].position == 1
        assert entities_time_pattern_2[0].parameter_role == START
        assert entities_time_pattern_2[0].integration == "time_pattern"
        assert entities_time_pattern_2[0].entity_name is not None
        assert entities_time_pattern_2[0].expected_value == {MINUTES: 2}
        assert end_position == 1

        trigger_part_time_pattern_2_input = [True]
        assert (
            await run_automation(file_path, trigger_part_time_pattern_2_input, [])
        ) is True

        trigger_part_time_pattern_2_input = [False]
        assert (
            await run_automation(file_path, trigger_part_time_pattern_2_input, [])
        ) is False

        trigger_part_time_pattern_2_input = [None]
        assert (
            await run_automation(file_path, trigger_part_time_pattern_2_input, [])
        ) is False

        assert real_pos == 1

        # Test case 3: Time pattern trigger at 02:00:00
        trigger_part_time_pattern_3 = {CONF_PLATFORM: "time_pattern", HOURS: 2}
        file_path = init_automation_script("trigger_part_time_pattern_3", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_time_pattern_3,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        test_trigger_return(file_path)

        entities_time_pattern_3, end_position, real_pos = results
        assert len(entities_time_pattern_3) == 1
        assert entities_time_pattern_3[0].parent is None
        assert entities_time_pattern_3[0].position == 1
        assert entities_time_pattern_3[0].parameter_role == START
        assert entities_time_pattern_3[0].integration == "time_pattern"
        assert entities_time_pattern_3[0].entity_name is not None
        assert entities_time_pattern_3[0].expected_value == {HOURS: 2}
        assert end_position == 1

        trigger_part_time_pattern_3_input = [True]
        assert (
            await run_automation(file_path, trigger_part_time_pattern_3_input, [])
        ) is True

        trigger_part_time_pattern_3_input = [False]
        assert (
            await run_automation(file_path, trigger_part_time_pattern_3_input, [])
        ) is False

        trigger_part_time_pattern_3_input = [None]
        assert (
            await run_automation(file_path, trigger_part_time_pattern_3_input, [])
        ) is False

        assert real_pos == 1

        # Test case 4: Time pattern trigger at 06:05:02 AM with leading zero in hours
        trigger_part_time_pattern_4 = {
            CONF_PLATFORM: "time_pattern",
            HOURS: "06",
            MINUTES: "5",
            SECONDS: "2",
        }
        file_path = init_automation_script("trigger_part_time_pattern_4", TRIGGER_DIR)
        try:
            _trigger_entities(
                trigger_part_time_pattern_4,
                position=1,
                real_position=0,
                script_path=file_path,
            )
            assert False  # The function should raise an exception
        except vol.Invalid as e:
            assert str(e) == "Leading zero in hours is not allowed"

        # Test case 5: Time pattern trigger at 6:05:02 AM with leading zero in minutes
        trigger_part_time_pattern_5 = {
            CONF_PLATFORM: "time_pattern",
            HOURS: 6,
            MINUTES: "05",
            SECONDS: 2,
        }
        file_path = init_automation_script("trigger_part_time_pattern_5", TRIGGER_DIR)
        try:
            _trigger_entities(
                trigger_part_time_pattern_5,
                position=1,
                real_position=0,
                script_path=file_path,
            )
            assert False  # The function should raise an exception
        except vol.Invalid as e:
            assert str(e) == "Leading zero in minutes is not allowed"

        # Test case 6: Time pattern trigger at 6:05:02 AM with leading zero in seconds
        trigger_part_time_pattern_6 = {
            CONF_PLATFORM: "time_pattern",
            HOURS: 6,
            MINUTES: 5,
            SECONDS: "02",
        }
        file_path = init_automation_script("trigger_part_time_pattern_6", TRIGGER_DIR)
        try:
            _trigger_entities(
                trigger_part_time_pattern_6,
                position=1,
                real_position=0,
                script_path=file_path,
            )
            assert False  # The function should raise an exception
        except vol.Invalid as e:
            assert str(e) == "Leading zero in seconds is not allowed"

        # Test case 7: Time pattern trigger at every 5 minutes
        trigger_part_time_pattern_7 = {CONF_PLATFORM: "time_pattern", MINUTES: "/5"}
        file_path = init_automation_script("trigger_part_time_pattern_7", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_time_pattern_7,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        test_trigger_return(file_path)

        entities_time_pattern_7, end_position, real_pos = results
        assert len(entities_time_pattern_7) == 1
        assert entities_time_pattern_7[0].parent is None
        assert entities_time_pattern_7[0].position == 1
        assert entities_time_pattern_7[0].parameter_role == START
        assert entities_time_pattern_7[0].integration == "time_pattern"
        assert entities_time_pattern_7[0].entity_name is not None
        assert entities_time_pattern_7[0].expected_value == {MINUTES: "/5"}
        assert end_position == 1

        trigger_part_time_pattern_7_input = [True]
        assert (
            await run_automation(file_path, trigger_part_time_pattern_7_input, [])
        ) is True

        trigger_part_time_pattern_7_input = [False]
        assert (
            await run_automation(file_path, trigger_part_time_pattern_7_input, [])
        ) is False

        trigger_part_time_pattern_7_input = [None]
        assert (
            await run_automation(file_path, trigger_part_time_pattern_7_input, [])
        ) is False

        assert real_pos == 1

    async def test_trigger_pers_notify():
        # Test case 1: Trigger at the creation of a persistent notification
        trigger_part_pers_notify_1 = {
            CONF_PLATFORM: "persistent_notification",
            CONF_UPDATE_TYPE: "added",
        }
        file_path = init_automation_script("trigger_part_pers_notify_1", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_pers_notify_1,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        test_trigger_return(file_path)

        entities_pers_notify_1, end_position, real_pos = results
        assert len(entities_pers_notify_1) == 1
        assert entities_pers_notify_1[0].parent is None
        assert entities_pers_notify_1[0].position == 1
        assert entities_pers_notify_1[0].parameter_role == START
        assert entities_pers_notify_1[0].integration == "persistent_notification"
        assert entities_pers_notify_1[0].entity_name is not None
        assert entities_pers_notify_1[0].expected_value == {CONF_UPDATE_TYPE: "added"}
        assert end_position == 1

        trigger_part_pers_notify_1_input = ["added"]
        assert (
            await run_automation(file_path, trigger_part_pers_notify_1_input, [])
        ) is True

        for update_type in ["updated", "removed", "current", None]:
            trigger_part_pers_notify_1_input = [update_type]
            assert (
                await run_automation(file_path, trigger_part_pers_notify_1_input, [])
            ) is False

        assert real_pos == 1

        # Test case 2: Trigger at the creation of a persistent notification with the id "notify_id_1"
        trigger_part_pers_notify_2 = {
            CONF_PLATFORM: "persistent_notification",
            CONF_UPDATE_TYPE: "added",
            CONF_NOFITY_ID: "notify_id_1",
        }
        file_path = init_automation_script("trigger_part_pers_notify_2", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_pers_notify_2,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        test_trigger_return(file_path)

        entities_pers_notify_2, end_position, real_pos = results
        assert len(entities_pers_notify_2) == 1
        assert entities_pers_notify_2[0].parent is None
        assert entities_pers_notify_2[0].position == 1
        assert entities_pers_notify_2[0].parameter_role == START
        assert entities_pers_notify_2[0].integration == "persistent_notification"
        assert (
            entities_pers_notify_2[0].entity_name
            == "persistent_notification.notify_id_1"
        )
        assert entities_pers_notify_2[0].expected_value == {CONF_UPDATE_TYPE: "added"}
        assert end_position == 1

        trigger_part_pers_notify_2_input = ["added"]
        assert (
            await run_automation(file_path, trigger_part_pers_notify_2_input, [])
        ) is True

        for update_type in ["updated", "removed", "current", None]:
            trigger_part_pers_notify_2_input = [update_type]
            assert (
                await run_automation(file_path, trigger_part_pers_notify_2_input, [])
            ) is False

        assert real_pos == 1

    async def test_trigger_webhook():
        # Test case 1: Trigger at the post or get of a webhook with id "webhook_id_1"
        trigger_part_webhook_1 = {
            CONF_PLATFORM: "webhook",
            CONF_WEBHOOK_ID: "webhook_id_1",
            CONF_ALLOWED_METHODS: ["POST", "GET"],
        }
        file_path = init_automation_script("trigger_part_webhook_1", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_webhook_1, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_webhook_1, end_position, real_pos = results
        assert len(entities_webhook_1) == 1
        assert entities_webhook_1[0].parent is None
        assert entities_webhook_1[0].position == 1
        assert entities_webhook_1[0].parameter_role == START
        assert entities_webhook_1[0].integration == "webhook"
        assert entities_webhook_1[0].entity_name == "webhook.webhook_id_1"
        assert entities_webhook_1[0].expected_value == {
            CONF_ALLOWED_METHODS: ["POST", "GET"]
        }
        assert end_position == 1

        trigger_part_webhook_1_input = [True]
        assert (
            await run_automation(file_path, trigger_part_webhook_1_input, [])
        ) is True
        trigger_part_webhook_1_input = [False]
        assert (
            await run_automation(file_path, trigger_part_webhook_1_input, [])
        ) is False
        trigger_part_webhook_1_input = [None]
        assert (
            await run_automation(file_path, trigger_part_webhook_1_input, [])
        ) is False
        assert real_pos == 1

        # Test case 2: Trigger at the post of a webhook with id "webhook_id_2" only locally
        trigger_part_webhook_2 = {
            CONF_PLATFORM: "webhook",
            CONF_WEBHOOK_ID: "webhook_id_2",
            CONF_ALLOWED_METHODS: ["POST"],
            CONF_LOCAL: True,
        }
        file_path = init_automation_script("trigger_part_webhook_2", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_webhook_2, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_webhook_2, end_position, real_pos = results
        assert len(entities_webhook_2) == 1
        assert entities_webhook_2[0].parent is None
        assert entities_webhook_2[0].position == 1
        assert entities_webhook_2[0].parameter_role == START
        assert entities_webhook_2[0].integration == "webhook"
        assert entities_webhook_2[0].entity_name == "webhook.webhook_id_2"
        assert entities_webhook_2[0].expected_value == {
            CONF_ALLOWED_METHODS: ["POST"],
            CONF_LOCAL: True,
        }
        trigger_part_webhook_2_input = [True]
        assert (
            await run_automation(file_path, trigger_part_webhook_2_input, [])
        ) is True
        trigger_part_webhook_2_input = [False]
        assert (
            await run_automation(file_path, trigger_part_webhook_2_input, [])
        ) is False
        trigger_part_webhook_2_input = [None]
        assert (
            await run_automation(file_path, trigger_part_webhook_2_input, [])
        ) is False
        assert real_pos == 1

    async def test_trigger_zone():
        # Test case 1: Trigger when paulus enters the home zone
        trigger_part_zone_1 = {
            CONF_PLATFORM: "zone",
            CONF_ZONE: "zone.home",
            CONF_EVENT: "enter",
            CONF_ENTITY_ID: "device_tracker.paulus",
        }
        file_path = init_automation_script("trigger_part_zone_1", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_zone_1, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_zone_1, end_position, real_pos = results
        assert len(entities_zone_1) == 1
        assert entities_zone_1[0].parent is None
        assert entities_zone_1[0].position == 1
        assert entities_zone_1[0].parameter_role == START
        assert entities_zone_1[0].integration == "zone"
        assert entities_zone_1[0].entity_name == "zone.home"
        assert entities_zone_1[0].expected_value == {
            CONF_EVENT: "enter",
            CONF_ENTITY_ID: "device_tracker.paulus",
        }
        assert end_position == 1

        trigger_part_zone_1_input = [True]
        assert (await run_automation(file_path, trigger_part_zone_1_input, [])) is True

        trigger_part_zone_1_input = [False]
        assert (await run_automation(file_path, trigger_part_zone_1_input, [])) is False

        trigger_part_zone_1_input = [None]
        assert (await run_automation(file_path, trigger_part_zone_1_input, [])) is False

        assert real_pos == 1

    async def test_trigger_geo_local():
        # Test case 1: Trigger when paulus enters the home zone with a local device
        trigger_part_geo_local_1 = {
            CONF_PLATFORM: "geo_location",
            CONF_ZONE: "zone.home",
            CONF_EVENT: "enter",
            CONF_SOURCE: "geo_location-source",
        }
        file_path = init_automation_script("trigger_part_geo_local_1", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_geo_local_1, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_geo_local_1, end_position, real_pos = results
        assert len(entities_geo_local_1) == 1
        assert entities_geo_local_1[0].parent is None
        assert entities_geo_local_1[0].position == 1
        assert entities_geo_local_1[0].parameter_role == START
        assert entities_geo_local_1[0].integration == "zone"
        assert entities_geo_local_1[0].entity_name == "zone.home"
        assert entities_geo_local_1[0].expected_value == {
            CONF_EVENT: "enter",
            CONF_SOURCE: "geo_location-source",
        }
        assert end_position == 1

        trigger_part_geo_local_1_input = [True]
        assert (
            await run_automation(file_path, trigger_part_geo_local_1_input, [])
        ) is True

        trigger_part_geo_local_1_input = [False]
        assert (
            await run_automation(file_path, trigger_part_geo_local_1_input, [])
        ) is False

        trigger_part_geo_local_1_input = [None]
        assert (
            await run_automation(file_path, trigger_part_geo_local_1_input, [])
        ) is False

        assert real_pos == 1

    async def test_trigger_device():
        # Test case 1: Trigger when device_id_1 does something
        trigger_part_device_1 = {
            CONF_PLATFORM: "device",
            CONF_DEVICE_ID: "device_id_1",
            CONF_ENTITY_ID: "test_entity_id",
            CONF_TYPE: "do something",
            CONF_DOMAIN: "domain",
        }
        file_path = init_automation_script("trigger_part_device_1", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_device_1, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_device_1, end_position, real_pos = results
        assert len(entities_device_1) == 1
        assert entities_device_1[0].parent is None
        assert entities_device_1[0].position == 1
        assert entities_device_1[0].parameter_role == START
        assert entities_device_1[0].integration == "device"
        assert entities_device_1[0].entity_name == "device.device_id_1"
        assert entities_device_1[0].expected_value == {
            CONF_ENTITY_ID: "test_entity_id",
            CONF_TYPE: "do something",
            CONF_DOMAIN: "domain",
        }
        assert end_position == 1

        trigger_part_device_1_input = ["do something"]
        assert (
            await run_automation(file_path, trigger_part_device_1_input, [])
        ) is True

        trigger_part_device_1_input = ["do nothing"]
        assert (
            await run_automation(file_path, trigger_part_device_1_input, [])
        ) is False

        trigger_part_device_1_input = [None]
        assert (
            await run_automation(file_path, trigger_part_device_1_input, [])
        ) is False

        assert real_pos == 1

    async def test_trigger_calendar():
        # Test case 1: Trigger when calender_name has an event event_name
        trigger_part_calendar_1 = {
            CONF_PLATFORM: "calendar",
            CONF_ENTITY_ID: "calendar.calendar_name",
            CONF_EVENT: "event_name",
        }
        file_path = init_automation_script("trigger_part_calendar_1", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_calendar_1, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_calendar_1, end_position, real_pos = results
        assert len(entities_calendar_1) == 1
        assert entities_calendar_1[0].parent is None
        assert entities_calendar_1[0].position == 1
        assert entities_calendar_1[0].parameter_role == START
        assert entities_calendar_1[0].integration == "calendar"
        assert entities_calendar_1[0].entity_name == "calendar.calendar_name"
        assert entities_calendar_1[0].expected_value == {CONF_EVENT: "event_name"}
        assert end_position == 1

        trigger_part_calendar_1_input = [True]
        assert (
            await run_automation(file_path, trigger_part_calendar_1_input, [])
        ) is True
        trigger_part_calendar_1_input = [False]
        assert (
            await run_automation(file_path, trigger_part_calendar_1_input, [])
        ) is False
        trigger_part_calendar_1_input = [None]
        assert (
            await run_automation(file_path, trigger_part_calendar_1_input, [])
        ) is False
        assert real_pos == 1

        # Test case 2: Trigger when calender_name has an event event_name with an offset of -01:00:00
        trigger_part_calendar_2 = {
            CONF_PLATFORM: "calendar",
            CONF_ENTITY_ID: "calendar.calendar_name",
            CONF_EVENT: "event_name",
            CONF_OFFSET: "-01:00:00",
        }
        file_path = init_automation_script("trigger_part_calendar_2", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_calendar_2, position=1, real_position=0, script_path=file_path
        )
        entities_calendar_2, end_position, real_pos = results
        test_trigger_return(file_path)

        assert len(entities_calendar_2) == 1
        assert entities_calendar_2[0].parent is None
        assert entities_calendar_2[0].position == 1
        assert entities_calendar_2[0].parameter_role == START
        assert entities_calendar_2[0].integration == "calendar"
        assert entities_calendar_2[0].entity_name == "calendar.calendar_name"
        assert entities_calendar_2[0].expected_value == {
            CONF_EVENT: "event_name",
            CONF_OFFSET: "-01:00:00",
        }
        assert end_position == 1

        trigger_part_calendar_2_input = [True]
        assert (
            await run_automation(file_path, trigger_part_calendar_2_input, [])
        ) is True
        trigger_part_calendar_2_input = [False]
        assert (
            await run_automation(file_path, trigger_part_calendar_2_input, [])
        ) is False
        trigger_part_calendar_2_input = [None]
        assert (
            await run_automation(file_path, trigger_part_calendar_2_input, [])
        ) is False
        assert real_pos == 1

    async def test_trigger_conversation():
        # Test case 1: Trigger when conversation has an intentional_name command
        trigger_part_conversation_1 = {
            CONF_PLATFORM: "conversation",
            CONF_COMMAND: "intentional_name",
        }
        file_path = init_automation_script("trigger_part_conversation_1", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_conversation_1,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        entities_conversation_1, end_position, real_pos = results
        test_trigger_return(file_path)

        assert len(entities_conversation_1) == 1
        assert entities_conversation_1[0].parent is None
        assert entities_conversation_1[0].position == 1
        assert entities_conversation_1[0].parameter_role == START
        assert entities_conversation_1[0].integration == "conversation"
        assert entities_conversation_1[0].entity_name is not None
        assert entities_conversation_1[0].expected_value == {
            CONF_COMMAND: "intentional_name"
        }
        assert end_position == 1

        trigger_part_conversation_1_input = [True]
        assert (
            await run_automation(file_path, trigger_part_conversation_1_input, [])
        ) is True

        trigger_part_conversation_1_input = [False]
        assert (
            await run_automation(file_path, trigger_part_conversation_1_input, [])
        ) is False

        trigger_part_conversation_1_input = [None]
        assert (
            await run_automation(file_path, trigger_part_conversation_1_input, [])
        ) is False

        assert real_pos == 1

        # Test case 2: Trigger when conversation has a be my guest command or a intentional_name command
        trigger_part_conversation_2 = {
            CONF_PLATFORM: "conversation",
            CONF_COMMAND: ["intentional_name", "be my guest"],
        }
        file_path = init_automation_script("trigger_part_conversation_2", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_conversation_2,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        test_trigger_return(file_path)

        entities_conversation_2, end_position, real_pos = results
        assert len(entities_conversation_2) == 2
        assert entities_conversation_2[0].parent == 1
        assert entities_conversation_2[0].position == 2
        assert entities_conversation_2[0].parameter_role == START
        assert entities_conversation_2[0].integration == "conversation"
        assert entities_conversation_2[0].entity_name is not None
        assert entities_conversation_2[0].expected_value == {
            CONF_COMMAND: "intentional_name"
        }
        assert entities_conversation_2[1].position == 3
        assert entities_conversation_2[1].parameter_role == START
        assert entities_conversation_2[1].integration == "conversation"
        assert entities_conversation_2[1].entity_name is not None
        assert entities_conversation_2[1].expected_value == {
            CONF_COMMAND: "be my guest"
        }
        assert end_position == 3
        trigger_part_conversation_2_input = [True, True]
        assert (
            await run_automation(file_path, trigger_part_conversation_2_input, [])
        ) is True

        trigger_part_conversation_2_input = [True, False]
        assert (
            await run_automation(file_path, trigger_part_conversation_2_input, [])
        ) is True

        trigger_part_conversation_2_input = [None, True]
        assert (
            await run_automation(file_path, trigger_part_conversation_2_input, [])
        ) is True

        trigger_part_conversation_2_input = [False, False]
        assert (
            await run_automation(file_path, trigger_part_conversation_2_input, [])
        ) is False

        trigger_part_conversation_2_input = [None, None]
        assert (
            await run_automation(file_path, trigger_part_conversation_2_input, [])
        ) is False

        trigger_part_conversation_2_input = [False, None]
        assert (
            await run_automation(file_path, trigger_part_conversation_2_input, [])
        ) is False

        assert real_pos == 2

    async def test_trigger_unsupported():
        # Test case 1: Unsupported platform
        trigger_part_x = {CONF_PLATFORM: "unsupported"}
        file_path = init_automation_script("trigger_part_x", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_x, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_x, end_position, real_pos = results
        assert len(entities_x) == 0
        assert end_position == 1
        trigger_part_x_input = [True]
        assert (await run_automation(file_path, trigger_part_x_input, [])) is False

        trigger_part_x_input = [None]
        assert (await run_automation(file_path, trigger_part_x_input, [])) is False

        assert real_pos == 0

        # Test case 2: State trigger with disabled set to false
        trigger_part_x2 = {
            CONF_PLATFORM: "state",
            CONF_ENABLED: False,
            CONF_ENTITY_ID: "sensor.temperature",
        }
        file_path = init_automation_script("trigger_part_x2", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_x2, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_x2, end_position, real_pos = results
        assert len(entities_x2) == 0
        assert end_position == 1
        trigger_part_x2_input = [True]
        assert (await run_automation(file_path, trigger_part_x2_input, [])) is False

        trigger_part_x2_input = [None]
        assert (await run_automation(file_path, trigger_part_x2_input, [])) is False

        assert real_pos == 0

    async def test_trigger_disabled():
        # Test case 1: Trigger with disabled set to true
        trigger_part_disabled = {
            CONF_PLATFORM: "state",
            CONF_ENTITY_ID: "sensor.temperature",
            CONF_ENABLED: False,
        }
        file_path = init_automation_script("trigger_part_disabled", TRIGGER_DIR)
        results = _trigger_entities(
            trigger_part_disabled, position=1, real_position=0, script_path=file_path
        )
        test_trigger_return(file_path)

        entities_disabled, end_position, real_pos = results
        assert len(entities_disabled) == 0
        assert end_position == 1
        assert real_pos == 0

    async def test_trigger_all():
        await test_trigger_event()
        await test_trigger_ha()
        await test_trigger_mqtt()
        await test_trigger_num_state()
        await test_trigger_state()
        await test_trigger_sun()
        await test_trigger_tag()
        await test_trigger_template()
        await test_trigger_time()
        await test_trigger_time_pattern()
        await test_trigger_pers_notify()
        await test_trigger_webhook()
        await test_trigger_zone()
        await test_trigger_geo_local()
        await test_trigger_device()
        await test_trigger_calendar()
        await test_trigger_conversation()
        await test_trigger_unsupported()
        await test_trigger_disabled()

    await test_trigger_all()
    print("All trigger test cases passed!")


async def test_condition_entities():
    CONDITION_DIR = path.join(TEST_DIR, "conditions")
    if not path.exists(CONDITION_DIR):
        mkdir(CONDITION_DIR)

    async def test_condition_num_state():
        # Test case 1: Numeric state condition with below value and on entity
        condition_part_num_state_1 = {
            CONF_CONDITION: CONF_NUMERIC_STATE,
            CONF_ENTITY_ID: ["sensor.temperature"],
            CONF_BELOW: 30,
        }
        file_path = init_automation_script("condition_part_num_state_1", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_num_state_1,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        test_condition_return(file_path)

        entities_num_state_1, end_position, real_pos = results
        assert len(entities_num_state_1) == 1
        assert entities_num_state_1[0].parent is None
        assert entities_num_state_1[0].position == 1
        assert entities_num_state_1[0].parameter_role == INPUT
        assert entities_num_state_1[0].integration == "sensor"
        assert entities_num_state_1[0].entity_name == "sensor.temperature"
        assert entities_num_state_1[0].expected_value == {"below": 30}
        assert end_position == 1

        # border test cases
        condition_part_num_state_1_input = [10]
        assert (
            await run_automation(file_path, [], condition_part_num_state_1_input)
        ) == {
            "condition_passed": True,
        }

        condition_part_num_state_1_input = [30]
        assert (
            await run_automation(file_path, [], condition_part_num_state_1_input)
        ) == {
            "condition_passed": False,
        }

        condition_part_num_state_1_input = [29]
        assert (
            await run_automation(file_path, [], condition_part_num_state_1_input)
        ) == {
            "condition_passed": True,
        }

        condition_part_num_state_1_input = [None]
        assert (
            await run_automation(file_path, [], condition_part_num_state_1_input)
        ) == {"ValueError": "Condition values cannot be None"}

        assert real_pos == 1

        # Test case 2: Numeric state condition with above value and on entity
        condition_part_num_state_2 = {
            CONF_CONDITION: CONF_NUMERIC_STATE,
            CONF_ENTITY_ID: ["sensor.temperature"],
            CONF_ABOVE: 20,
        }
        file_path = init_automation_script("condition_part_num_state_2", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_num_state_2,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        test_condition_return(file_path)

        entities_num_state_2, end_position, real_pos = results
        assert len(entities_num_state_2) == 1
        assert entities_num_state_2[0].parent is None
        assert entities_num_state_2[0].position == 1
        assert entities_num_state_2[0].parameter_role == INPUT
        assert entities_num_state_2[0].integration == "sensor"
        assert entities_num_state_2[0].entity_name == "sensor.temperature"
        assert entities_num_state_2[0].expected_value == {"above": 20}
        assert end_position == 1

        # border test cases
        condition_part_num_state_2_input = [25]
        assert (
            await run_automation(file_path, [], condition_part_num_state_2_input)
        ) == {
            "condition_passed": True,
        }

        condition_part_num_state_2_input = [20]
        assert (
            await run_automation(file_path, [], condition_part_num_state_2_input)
        ) == {
            "condition_passed": False,
        }

        condition_part_num_state_2_input = [19]
        assert (
            await run_automation(file_path, [], condition_part_num_state_2_input)
        ) == {
            "condition_passed": False,
        }

        condition_part_num_state_2_input = [None]
        assert (
            await run_automation(file_path, [], condition_part_num_state_2_input)
        ) == {"ValueError": "Condition values cannot be None"}

        assert real_pos == 1

        # Test case 3: Numeric state condition with above and below values and on entity
        condition_part_num_state_3 = {
            CONF_CONDITION: CONF_NUMERIC_STATE,
            CONF_ENTITY_ID: ["sensor.temperature"],
            CONF_BELOW: 30,
            CONF_ABOVE: 20,
        }
        file_path = init_automation_script("condition_part_num_state_3", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_num_state_3,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        test_condition_return(file_path)

        entities_num_state_3, end_position, real_pos = results
        assert len(entities_num_state_3) == 1
        assert entities_num_state_3[0].parent is None
        assert entities_num_state_3[0].position == 1
        assert entities_num_state_3[0].parameter_role == INPUT
        assert entities_num_state_3[0].integration == "sensor"
        assert entities_num_state_3[0].entity_name == "sensor.temperature"
        assert entities_num_state_3[0].expected_value == {"above": 20, "below": 30}
        assert end_position == 1

        # border test cases
        condition_part_num_state_3_input = [25]
        assert (
            await run_automation(file_path, [], condition_part_num_state_3_input)
        ) == {
            "condition_passed": True,
        }

        condition_part_num_state_3_input = [30]
        assert (
            await run_automation(file_path, [], condition_part_num_state_3_input)
        ) == {
            "condition_passed": False,
        }

        condition_part_num_state_3_input = [31]
        assert (
            await run_automation(file_path, [], condition_part_num_state_3_input)
        ) == {
            "condition_passed": False,
        }

        condition_part_num_state_3_input = [20]
        assert (
            await run_automation(file_path, [], condition_part_num_state_3_input)
        ) == {
            "condition_passed": False,
        }

        condition_part_num_state_3_input = [19]
        assert (
            await run_automation(file_path, [], condition_part_num_state_3_input)
        ) == {
            "condition_passed": False,
        }

        condition_part_num_state_3_input = [None]
        assert (
            await run_automation(file_path, [], condition_part_num_state_3_input)
        ) == {"ValueError": "Condition values cannot be None"}

        assert real_pos == 1

        # Test case 4: Numerical state trigger with above, below, and for values
        condition_part_num_state_4 = {
            CONF_CONDITION: CONF_NUMERIC_STATE,
            CONF_ENTITY_ID: ["sensor.temperature"],
            CONF_ABOVE: 20,
            CONF_BELOW: 30,
            CONF_FOR: "00:01:00",
        }
        file_path = init_automation_script("condition_part_num_state_4", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_num_state_4,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        test_condition_return(file_path)

        entities_num_state_4, end_position, real_pos = results
        assert len(entities_num_state_4) == 1
        assert entities_num_state_4[0].parent is None
        assert entities_num_state_4[0].position == 1
        assert entities_num_state_4[0].parameter_role == INPUT
        assert entities_num_state_4[0].integration == "sensor"
        assert entities_num_state_4[0].entity_name == "sensor.temperature"
        assert entities_num_state_4[0].expected_value == {
            CONF_ABOVE: 20,
            CONF_BELOW: 30,
            CONF_FOR: "00:01:00",
        }
        assert end_position == 1

        # border test cases
        condition_part_num_state_4_input = [25]
        assert (
            await run_automation(file_path, [], condition_part_num_state_4_input)
        ) == {"condition_passed": True}

        condition_part_num_state_4_input = [30]
        assert (
            await run_automation(file_path, [], condition_part_num_state_4_input)
        ) == {"condition_passed": False}

        condition_part_num_state_4_input = [31]
        assert (
            await run_automation(file_path, [], condition_part_num_state_4_input)
        ) == {"condition_passed": False}

        condition_part_num_state_4_input = [20]
        assert (
            await run_automation(file_path, [], condition_part_num_state_4_input)
        ) == {"condition_passed": False}

        condition_part_num_state_4_input = [19]
        assert (
            await run_automation(file_path, [], condition_part_num_state_4_input)
        ) == {"condition_passed": False}

        condition_part_num_state_4_input = [None]
        assert (
            await run_automation(file_path, [], condition_part_num_state_4_input)
        ) == {"ValueError": "Condition values cannot be None"}

        assert real_pos == 1

        # Test case 5: Numerical state condition with above value for an attribute
        condition_part_num_state_5 = {
            CONF_CONDITION: CONF_NUMERIC_STATE,
            CONF_ENTITY_ID: ["sensor.temperature"],
            CONF_ATTRIBUTE: "attribute_1",
            CONF_ABOVE: 20,
        }
        file_path = init_automation_script("condition_part_num_state_5", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_num_state_5,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        test_condition_return(file_path)

        entities_num_state_5, end_position, real_pos = results
        assert len(entities_num_state_5) == 1
        assert entities_num_state_5[0].parent is None
        assert entities_num_state_5[0].position == 1
        assert entities_num_state_5[0].parameter_role == INPUT
        assert entities_num_state_5[0].integration == "sensor"
        assert entities_num_state_5[0].entity_name == "sensor.temperature.attribute_1"
        assert entities_num_state_5[0].expected_value == {CONF_ABOVE: 20}
        assert end_position == 1

        # border test cases
        condition_part_num_state_5_input = [25]
        assert (
            await run_automation(file_path, [], condition_part_num_state_5_input)
        ) == {"condition_passed": True}

        condition_part_num_state_5_input = [20]
        assert (
            await run_automation(file_path, [], condition_part_num_state_5_input)
        ) == {"condition_passed": False}

        condition_part_num_state_5_input = [19]
        assert (
            await run_automation(file_path, [], condition_part_num_state_5_input)
        ) == {"condition_passed": False}

        condition_part_num_state_5_input = [None]
        assert (
            await run_automation(file_path, [], condition_part_num_state_5_input)
        ) == {"ValueError": "Condition values cannot be None"}
        assert real_pos == 1

        # Test case 6: Numeric state condition with below value and two entities
        condition_part_num_state_6 = {
            CONF_CONDITION: CONF_NUMERIC_STATE,
            CONF_ENTITY_ID: ["sensor.temperature", "sensor.humidity"],
            CONF_BELOW: 50,
        }
        file_path = init_automation_script("condition_part_num_state_6", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_num_state_6,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        test_condition_return(file_path)

        entities_num_state_6, end_position, real_pos = results
        assert len(entities_num_state_6) == 2
        assert entities_num_state_6[0].parent == 1
        assert entities_num_state_6[0].position == 2
        assert entities_num_state_6[0].parameter_role == INPUT
        assert entities_num_state_6[0].integration == "sensor"
        assert entities_num_state_6[0].entity_name == "sensor.temperature"
        assert entities_num_state_6[0].expected_value == {"below": 50}
        assert entities_num_state_6[1].position == 3
        assert entities_num_state_6[1].parameter_role == INPUT
        assert entities_num_state_6[1].integration == "sensor"
        assert entities_num_state_6[1].entity_name == "sensor.humidity"
        assert entities_num_state_6[1].expected_value == {"below": 50}
        assert end_position == 3

        # border test cases
        condition_part_num_state_6_input = [40, 45]
        assert (
            await run_automation(file_path, [], condition_part_num_state_6_input)
        ) == {
            "condition_passed": True,
        }

        condition_part_num_state_6_input = [50, 45]
        assert (
            await run_automation(file_path, [], condition_part_num_state_6_input)
        ) == {
            "condition_passed": False,
        }

        condition_part_num_state_6_input = [40, 50]
        assert (
            await run_automation(file_path, [], condition_part_num_state_6_input)
        ) == {
            "condition_passed": False,
        }

        condition_part_num_state_6_input = [None, 45]
        assert (
            await run_automation(file_path, [], condition_part_num_state_6_input)
        ) == {"ValueError": "Condition values cannot be None"}

        condition_part_num_state_6_input = [40, None]
        assert (
            await run_automation(file_path, [], condition_part_num_state_6_input)
        ) == {"ValueError": "Condition values cannot be None"}

        condition_part_num_state_6_input = [None, None]
        assert (
            await run_automation(file_path, [], condition_part_num_state_6_input)
        ) == {"ValueError": "Condition values cannot be None"}

        assert real_pos == 2

        # Test case 7: Numeric state condition with above value and list free entity
        condition_part_num_state_7 = {
            CONF_CONDITION: CONF_NUMERIC_STATE,
            CONF_ENTITY_ID: "sensor.temperature",
            CONF_ABOVE: 20,
        }
        file_path = init_automation_script("condition_part_num_state_7", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_num_state_7,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        test_condition_return(file_path)

        entities_num_state_7, end_position, real_pos = results
        assert len(entities_num_state_7) == 1
        assert entities_num_state_7[0].parent is None
        assert entities_num_state_7[0].position == 1
        assert entities_num_state_7[0].parameter_role == INPUT
        assert entities_num_state_7[0].integration == "sensor"
        assert entities_num_state_7[0].entity_name == "sensor.temperature"
        assert entities_num_state_7[0].expected_value == {"above": 20}
        assert end_position == 1

        condition_part_num_state_7_input = [25]
        assert (
            await run_automation(file_path, [], condition_part_num_state_7_input)
        ) == {
            "condition_passed": True,
        }

        condition_part_num_state_7_input = [20]
        assert (
            await run_automation(file_path, [], condition_part_num_state_7_input)
        ) == {
            "condition_passed": False,
        }

        condition_part_num_state_7_input = [19]
        assert (
            await run_automation(file_path, [], condition_part_num_state_7_input)
        ) == {
            "condition_passed": False,
        }

        condition_part_num_state_7_input = [None]
        assert (
            await run_automation(file_path, [], condition_part_num_state_7_input)
        ) == {"ValueError": "Condition values cannot be None"}

        assert real_pos == 1

        # Test case 8: Numeric state condition with above value and at a specific position
        condition_part_num_state_8 = {
            CONF_CONDITION: CONF_NUMERIC_STATE,
            CONF_ENTITY_ID: ["sensor.temperature"],
            CONF_ABOVE: 20,
        }
        file_path = init_automation_script("condition_part_num_state_8", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_num_state_8,
            position=4,
            parent=2,
            real_position=0,
            script_path=file_path,
        )
        test_condition_return(file_path)

        entities_num_state_8, end_position, real_pos = results
        assert len(entities_num_state_8) == 1
        assert entities_num_state_8[0].parent == 2
        assert entities_num_state_8[0].position == 4
        assert entities_num_state_8[0].parameter_role == INPUT
        assert entities_num_state_8[0].integration == "sensor"
        assert entities_num_state_8[0].entity_name == "sensor.temperature"
        assert entities_num_state_8[0].expected_value == {"above": 20}
        assert end_position == 4

        condition_part_num_state_8_input = [25]
        assert (
            await run_automation(file_path, [], condition_part_num_state_8_input)
        ) == {
            "condition_passed": True,
        }

        condition_part_num_state_8_input = [20]
        assert (
            await run_automation(file_path, [], condition_part_num_state_8_input)
        ) == {
            "condition_passed": False,
        }

        condition_part_num_state_8_input = [None]
        assert (
            await run_automation(file_path, [], condition_part_num_state_8_input)
        ) == {"ValueError": "Condition values cannot be None"}

        real_pos == 1

        # Test case 9: Numeric state condition with above entity state
        condition_part_num_state_9 = {
            CONF_CONDITION: CONF_NUMERIC_STATE,
            CONF_ENTITY_ID: ["sensor.temperature"],
            CONF_ABOVE: "sensor.temperature2",
        }
        file_path = init_automation_script("condition_part_num_state_9", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_num_state_9,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        test_condition_return(file_path)

        entities_num_state_9, end_position, real_pos = results
        assert len(entities_num_state_9) == 2
        assert entities_num_state_9[0].parent == 1
        assert entities_num_state_9[0].position == 2
        assert entities_num_state_9[0].parameter_role == INPUT
        assert entities_num_state_9[0].integration == "sensor"
        assert entities_num_state_9[0].entity_name == "sensor.temperature"
        assert entities_num_state_9[0].expected_value == {
            CONF_ABOVE: "sensor.temperature2",
        }
        assert entities_num_state_9[1].parent == 1
        assert entities_num_state_9[1].position == 3
        assert entities_num_state_9[1].parameter_role == INPUT
        assert entities_num_state_9[1].integration == "sensor"
        assert entities_num_state_9[1].entity_name == "sensor.temperature2"
        assert entities_num_state_9[1].expected_value == {
            CONF_BELOW: "sensor.temperature"
        }
        assert end_position == 3
        # border test cases - the list build like this [CONF_ABOVE, CONF_ENTITY_ID/s, CONF_BELOW]
        condition_part_num_state_9_input = [25, 35]
        assert (
            await run_automation(file_path, [], condition_part_num_state_9_input)
        ) == {
            "condition_passed": True,
        }

        condition_part_num_state_9_input = [30, 25]
        assert (
            await run_automation(file_path, [], condition_part_num_state_9_input)
        ) == {
            "condition_passed": False,
        }

        condition_part_num_state_9_input = [25, 25]
        assert (
            await run_automation(file_path, [], condition_part_num_state_9_input)
        ) == {
            "condition_passed": False,
        }

        condition_part_num_state_9_input = [None, 25]
        assert (
            await run_automation(file_path, [], condition_part_num_state_9_input)
        ) == {"ValueError": "Condition values cannot be None"}

        condition_part_num_state_9_input = [25, None]
        assert (
            await run_automation(file_path, [], condition_part_num_state_9_input)
        ) == {"ValueError": "Condition values cannot be None"}

        condition_part_num_state_9_input = [None, None]
        assert (
            await run_automation(file_path, [], condition_part_num_state_9_input)
        ) == {"ValueError": "Condition values cannot be None"}

        assert real_pos == 2

        # Test case 10: Numerical state condition with multiple entities, above, and below entity states and
        # at a specific position
        condition_part_num_state_10 = {
            CONF_CONDITION: CONF_NUMERIC_STATE,
            CONF_ENTITY_ID: ["sensor.temperature", "sensor.temperature4"],
            CONF_ABOVE: "sensor.temperature3",
            CONF_BELOW: "sensor.temperature2",
        }
        file_path = init_automation_script("condition_part_num_state_10", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_num_state_10,
            position=2,
            real_position=2,
            script_path=file_path,
        )
        test_condition_return(file_path)

        entities_num_state_10, end_position, real_pos = results
        assert len(entities_num_state_10) == 4
        assert entities_num_state_10[0].parent == 3
        assert entities_num_state_10[0].position == 4
        assert entities_num_state_10[0].parameter_role == INPUT
        assert entities_num_state_10[0].integration == "sensor"
        assert entities_num_state_10[0].entity_name == "sensor.temperature"
        assert entities_num_state_10[0].expected_value == {
            CONF_BELOW: "sensor.temperature2",
            CONF_ABOVE: "sensor.temperature3",
        }
        assert entities_num_state_10[1].parent == 3
        assert entities_num_state_10[1].position == 5
        assert entities_num_state_10[1].parameter_role == INPUT
        assert entities_num_state_10[1].integration == "sensor"
        assert entities_num_state_10[1].entity_name == "sensor.temperature4"
        assert entities_num_state_10[1].expected_value == {
            CONF_BELOW: "sensor.temperature2",
            CONF_ABOVE: "sensor.temperature3",
        }
        assert entities_num_state_10[2].parent == 2
        assert entities_num_state_10[2].position == 6
        assert entities_num_state_10[2].parameter_role == INPUT
        assert entities_num_state_10[2].integration == "sensor"
        assert entities_num_state_10[2].entity_name == "sensor.temperature3"
        assert entities_num_state_10[2].expected_value == {
            CONF_BELOW: ["sensor.temperature", "sensor.temperature4"]
        }
        assert entities_num_state_10[3].parent == 2
        assert entities_num_state_10[3].position == 7
        assert entities_num_state_10[3].parameter_role == INPUT
        assert entities_num_state_10[3].integration == "sensor"
        assert entities_num_state_10[3].entity_name == "sensor.temperature2"
        assert entities_num_state_10[3].expected_value == {
            CONF_ABOVE: ["sensor.temperature", "sensor.temperature4"]
        }
        assert end_position == 7
        # border test cases -  - the list build like this [CONF_ABOVE, CONF_ENTITY_ID/s, CONF_BELOW]
        # position 0 and 1 are not used by the script
        condition_part_num_state_10_input = ["filler", "filler", 10, 20, 20, 30]
        assert (
            await run_automation(file_path, [], condition_part_num_state_10_input)
        ) == {
            "condition_passed": True,
        }

        condition_part_num_state_10_input = ["filler", "filler", 23, 20, 20, 30]
        assert (
            await run_automation(file_path, [], condition_part_num_state_10_input)
        ) == {
            "condition_passed": False,
        }

        condition_part_num_state_10_input = ["filler", "filler", 10, 20, 20, 19]
        assert (
            await run_automation(file_path, [], condition_part_num_state_10_input)
        ) == {
            "condition_passed": False,
        }

        condition_part_num_state_10_input = ["filler", "filler", 10, 20, 18, 19]
        assert (
            await run_automation(file_path, [], condition_part_num_state_10_input)
        ) == {
            "condition_passed": False,
        }

        condition_part_num_state_10_input = ["filler", "filler", None, None, 20, None]
        assert (
            await run_automation(file_path, [], condition_part_num_state_10_input)
        ) == {"ValueError": "Condition values cannot be None"}

        condition_part_num_state_10_input = ["filler", "filler", None, 20, None, 544]
        assert (
            await run_automation(file_path, [], condition_part_num_state_10_input)
        ) == {"ValueError": "Condition values cannot be None"}

        condition_part_num_state_10_input = ["filler", "filler", 2, 20, None, None]
        assert (
            await run_automation(file_path, [], condition_part_num_state_10_input)
        ) == {"ValueError": "Condition values cannot be None"}

        condition_part_num_state_10_input = ["filler", "filler", None, None, None, None]
        assert (
            await run_automation(file_path, [], condition_part_num_state_10_input)
        ) == {"ValueError": "Condition values cannot be None"}

        assert real_pos == 6

    async def test_condition_state():
        # Test case 1: State condition with one entity in that state
        condition_part_state_1 = {
            CONF_CONDITION: CONF_STATE,
            CONF_ENTITY_ID: ["binary_sensor.motion"],
            CONF_STATE: "on",
        }
        file_path = init_automation_script("condition_part_state_1", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_state_1, position=1, real_position=0, script_path=file_path
        )
        test_condition_return(file_path)

        entities_state_1, end_position, real_pos = results
        assert len(entities_state_1) == 1
        assert entities_state_1[0].parent is None
        assert entities_state_1[0].position == 1
        assert entities_state_1[0].parameter_role == INPUT
        assert entities_state_1[0].integration == "binary_sensor"
        assert entities_state_1[0].entity_name == "binary_sensor.motion"
        assert entities_state_1[0].expected_value == {"state": "on"}
        assert end_position == 1

        condition_part_state_1_input = ["on"]
        assert (await run_automation(file_path, [], condition_part_state_1_input)) == {
            "condition_passed": True,
        }

        for state_val in ["off", "unavailable", "unknown"]:
            condition_part_state_1_input = [state_val]
            assert (
                await run_automation(file_path, [], condition_part_state_1_input)
            ) == {"condition_passed": False}

        condition_part_state_1_input = [None]
        assert (await run_automation(file_path, [], condition_part_state_1_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        real_pos == 1

        # Test case 2: State condition with one entity in that state and for a specific time
        condition_part_state_2 = {
            CONF_CONDITION: CONF_STATE,
            CONF_ENTITY_ID: ["binary_sensor.motion"],
            CONF_STATE: "off",
            CONF_FOR: "00:05:00",
        }
        file_path = init_automation_script("condition_part_state_2", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_state_2, position=1, real_position=0, script_path=file_path
        )
        test_condition_return(file_path)

        entities_state_2, end_position, real_pos = results
        assert len(entities_state_2) == 1
        assert entities_state_2[0].parent is None
        assert entities_state_2[0].position == 1
        assert entities_state_2[0].parameter_role == INPUT
        assert entities_state_2[0].integration == "binary_sensor"
        assert entities_state_2[0].entity_name == "binary_sensor.motion"
        assert entities_state_2[0].expected_value == {"state": "off", "for": "00:05:00"}
        assert end_position == 1

        condition_part_state_2_input = ["off"]
        assert (await run_automation(file_path, [], condition_part_state_2_input)) == {
            "condition_passed": True,
        }

        for state_val in ["on", "unavailable", "unknown"]:
            condition_part_state_2_input = [state_val]
            assert (
                await run_automation(file_path, [], condition_part_state_2_input)
            ) == {
                "condition_passed": False,
            }

        condition_part_state_2_input = [None]
        assert (await run_automation(file_path, [], condition_part_state_2_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        real_pos == 1

        # Test case 3: State condition with two entities in that state
        condition_part_state_3 = {
            CONF_CONDITION: CONF_STATE,
            CONF_ENTITY_ID: ["binary_sensor.motion", "switch.light"],
            CONF_STATE: "off",
        }
        file_path = init_automation_script("condition_part_state_3", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_state_3, position=1, real_position=0, script_path=file_path
        )
        test_condition_return(file_path)

        entities_state_3, end_position, real_pos = results
        assert len(entities_state_3) == 2
        assert entities_state_3[0].parent == 1
        assert entities_state_3[0].position == 2
        assert entities_state_3[0].parameter_role == INPUT
        assert entities_state_3[0].integration == "binary_sensor"
        assert entities_state_3[0].entity_name == "binary_sensor.motion"
        assert entities_state_3[0].expected_value == {"state": "off"}
        assert entities_state_3[1].parent == 1
        assert entities_state_3[1].position == 3
        assert entities_state_3[1].parameter_role == INPUT
        assert entities_state_3[1].integration == "switch"
        assert entities_state_3[1].entity_name == "switch.light"
        assert entities_state_3[1].expected_value == {"state": "off"}
        assert end_position == 3

        condition_part_state_3_input = ["on", "off"]
        assert (await run_automation(file_path, [], condition_part_state_3_input)) == {
            "condition_passed": False,
        }

        condition_part_state_3_input = ["off", "on"]
        assert (await run_automation(file_path, [], condition_part_state_3_input)) == {
            "condition_passed": False,
        }

        condition_part_state_3_input = ["off", "off"]
        assert (await run_automation(file_path, [], condition_part_state_3_input)) == {
            "condition_passed": True,
        }

        condition_part_state_3_input = ["on", None]
        assert (await run_automation(file_path, [], condition_part_state_3_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        condition_part_state_3_input = [None, None]
        assert (await run_automation(file_path, [], condition_part_state_3_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        assert real_pos == 2

        # Test case 4: State condition with one entity in that state and at a specific position
        condition_part_state_4 = {
            CONF_CONDITION: CONF_STATE,
            CONF_ENTITY_ID: ["binary_sensor.motion"],
            CONF_STATE: "on",
        }
        file_path = init_automation_script("condition_part_state_4", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_state_4,
            position=4,
            parent=2,
            real_position=0,
            script_path=file_path,
        )
        test_condition_return(file_path)

        entities_state_4, end_position, real_pos = results
        assert len(entities_state_4) == 1
        assert entities_state_4[0].parent == 2
        assert entities_state_4[0].position == 4
        assert entities_state_4[0].parameter_role == INPUT
        assert entities_state_4[0].integration == "binary_sensor"
        assert entities_state_4[0].entity_name == "binary_sensor.motion"
        assert entities_state_4[0].expected_value == {"state": "on"}
        assert end_position == 4

        condition_part_state_4_input = ["on"]
        assert (await run_automation(file_path, [], condition_part_state_4_input)) == {
            "condition_passed": True,
        }

        for state_val in ["off", "unavailable", "unknown"]:
            condition_part_state_4_input = [state_val]
            assert (
                await run_automation(file_path, [], condition_part_state_4_input)
            ) == {
                "condition_passed": False,
            }

        condition_part_state_4_input = [None]
        assert (await run_automation(file_path, [], condition_part_state_4_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        real_pos == 1

        # Test case 5: State condition with two entities in that state and at a specific position
        condition_part_state_5 = {
            CONF_CONDITION: CONF_STATE,
            CONF_ENTITY_ID: ["binary_sensor.motion", "switch.light"],
            CONF_STATE: "off",
        }
        file_path = init_automation_script("condition_part_state_5", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_state_5,
            position=4,
            parent=2,
            real_position=0,
            script_path=file_path,
        )
        test_condition_return(file_path)

        entities_state_5, end_position, real_pos = results
        assert len(entities_state_5) == 2
        assert entities_state_5[0].parent == 4
        assert entities_state_5[0].position == 5
        assert entities_state_5[0].parameter_role == INPUT
        assert entities_state_5[0].integration == "binary_sensor"
        assert entities_state_5[0].entity_name == "binary_sensor.motion"
        assert entities_state_5[0].expected_value == {"state": "off"}
        assert entities_state_5[1].parent == 4
        assert entities_state_5[1].position == 6
        assert entities_state_5[1].parameter_role == INPUT
        assert entities_state_5[1].integration == "switch"
        assert entities_state_5[1].entity_name == "switch.light"
        assert entities_state_5[1].expected_value == {"state": "off"}
        assert end_position == 6

        condition_part_state_5_input = ["on", "off"]
        assert (await run_automation(file_path, [], condition_part_state_5_input)) == {
            "condition_passed": False,
        }

        condition_part_state_5_input = ["off", "on"]
        assert (await run_automation(file_path, [], condition_part_state_5_input)) == {
            "condition_passed": False,
        }

        condition_part_state_5_input = ["off", "off"]
        assert (await run_automation(file_path, [], condition_part_state_5_input)) == {
            "condition_passed": True,
        }

        condition_part_state_5_input = ["on", None]
        assert (await run_automation(file_path, [], condition_part_state_5_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        condition_part_state_5_input = [None, None]
        assert (await run_automation(file_path, [], condition_part_state_5_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        assert real_pos == 2

        # Test case 6: State condition with one entity in two possible states and at a specific position
        condition_part_state_6 = {
            CONF_CONDITION: CONF_STATE,
            CONF_ENTITY_ID: ["binary_sensor.motion"],
            CONF_STATE: ["on", "off"],
        }
        file_path = init_automation_script("condition_part_state_6", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_state_6,
            position=4,
            parent=2,
            real_position=0,
            script_path=file_path,
        )
        test_condition_return(file_path)

        entities_state_6, end_position, real_pos = results
        assert len(entities_state_6) == 1
        assert entities_state_6[0].parent == 2
        assert entities_state_6[0].position == 4
        assert entities_state_6[0].parameter_role == INPUT
        assert entities_state_6[0].integration == "binary_sensor"
        assert entities_state_6[0].entity_name == "binary_sensor.motion"
        assert entities_state_6[0].expected_value == {"state": ["on", "off"]}
        assert end_position == 4

        condition_part_state_6_input = ["off"]
        assert (await run_automation(file_path, [], condition_part_state_6_input)) == {
            "condition_passed": True,
        }

        condition_part_state_6_input = ["off"]
        assert (await run_automation(file_path, [], condition_part_state_6_input)) == {
            "condition_passed": True,
        }

        for state_val in ["unavailable", "unknown"]:
            condition_part_state_6_input = [state_val]
            assert (
                await run_automation(file_path, [], condition_part_state_6_input)
            ) == {
                "condition_passed": False,
            }

        condition_part_state_6_input = [None]
        assert (await run_automation(file_path, [], condition_part_state_6_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        real_pos == 1

        # Test case 7: State condition with two entity two possible states and at a specific position
        condition_part_state_7 = {
            CONF_CONDITION: CONF_STATE,
            CONF_ENTITY_ID: ["binary_sensor.motion", "switch.light"],
            CONF_STATE: ["on", "off"],
        }
        file_path = init_automation_script("condition_part_state_7", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_state_7,
            position=4,
            parent=2,
            real_position=0,
            script_path=file_path,
        )
        test_condition_return(file_path)

        entities_state_7, end_position, real_pos = results
        assert len(entities_state_7) == 2
        assert entities_state_7[0].parent == 4
        assert entities_state_7[0].position == 5
        assert entities_state_7[0].parameter_role == INPUT
        assert entities_state_7[0].integration == "binary_sensor"
        assert entities_state_7[0].entity_name == "binary_sensor.motion"
        assert entities_state_7[0].expected_value == {"state": ["on", "off"]}
        assert entities_state_7[1].parent == 4
        assert entities_state_7[1].position == 6
        assert entities_state_7[1].parameter_role == INPUT
        assert entities_state_7[1].integration == "switch"
        assert entities_state_7[1].entity_name == "switch.light"
        assert entities_state_7[1].expected_value == {"state": ["on", "off"]}
        assert end_position == 6

        # Test case 8: State condition with conditional entity state
        condition_part_state_8 = {
            CONF_CONDITION: CONF_STATE,
            CONF_ENTITY_ID: ["binary_sensor.motion"],
            CONF_STATE: "binary_sensor.motion_2",
        }
        file_path = init_automation_script("condition_part_state_8", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_state_8, position=1, real_position=0, script_path=file_path
        )
        test_condition_return(file_path)

        entities_state_8, end_position, real_pos = results
        assert len(entities_state_8) == 2
        assert entities_state_8[0].parent == 1
        assert entities_state_8[0].position == 2
        assert entities_state_8[0].parameter_role == INPUT
        assert entities_state_8[0].integration == "binary_sensor"
        assert entities_state_8[0].entity_name == "binary_sensor.motion"
        assert entities_state_8[0].expected_value == {
            CONF_STATE: "binary_sensor.motion_2"
        }
        assert entities_state_8[1].parent == 1
        assert entities_state_8[1].position == 3
        assert entities_state_8[1].parameter_role == INPUT
        assert entities_state_8[1].integration == "binary_sensor"
        assert entities_state_8[1].entity_name == "binary_sensor.motion_2"
        assert end_position == 3

        # border test cases - the list build like this [CONF_STATE/s, CONF_ENTITY_ID/s]
        condition_part_state_8_input = ["on", "off"]
        assert (await run_automation(file_path, [], condition_part_state_8_input)) == {
            "condition_passed": False,
        }

        condition_part_state_8_input = ["off", "off"]
        assert (await run_automation(file_path, [], condition_part_state_8_input)) == {
            "condition_passed": True,
        }

        condition_part_state_8_input = ["on", "on"]
        assert (await run_automation(file_path, [], condition_part_state_8_input)) == {
            "condition_passed": True,
        }

        condition_part_state_8_input = [None, "on"]
        assert (await run_automation(file_path, [], condition_part_state_8_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        condition_part_state_8_input = [None, None]
        assert (await run_automation(file_path, [], condition_part_state_8_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        assert real_pos == 2

        # Test case 9: State condition with multiple entity ids and conditional entity state
        condition_part_state_9 = {
            CONF_CONDITION: CONF_STATE,
            CONF_ENTITY_ID: ["binary_sensor.motion", "binary_sensor.motion_2"],
            CONF_STATE: [
                "binary_sensor.motion_3",
                "unknown",
                "binary_sensor.motion_4",
                "on",
            ],
        }
        file_path = init_automation_script("condition_part_state_9", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_state_9, position=1, real_position=0, script_path=file_path
        )
        test_condition_return(file_path)

        entities_state_9, end_position, real_pos = results
        assert len(entities_state_9) == 4
        assert entities_state_9[0].parent == 2
        assert entities_state_9[0].position == 3
        assert entities_state_9[0].parameter_role == INPUT
        assert entities_state_9[0].integration == "binary_sensor"
        assert entities_state_9[0].entity_name == "binary_sensor.motion"
        assert entities_state_9[0].expected_value == {
            CONF_STATE: [
                "binary_sensor.motion_3",
                "unknown",
                "binary_sensor.motion_4",
                "on",
            ]
        }
        assert entities_state_9[1].parent == 2
        assert entities_state_9[1].position == 4
        assert entities_state_9[1].parameter_role == INPUT
        assert entities_state_9[1].integration == "binary_sensor"
        assert entities_state_9[1].entity_name == "binary_sensor.motion_2"
        assert entities_state_9[1].expected_value == {
            CONF_STATE: [
                "binary_sensor.motion_3",
                "unknown",
                "binary_sensor.motion_4",
                "on",
            ]
        }
        assert entities_state_9[2].parent == 1
        assert entities_state_9[2].position == 5
        assert entities_state_9[2].parameter_role == INPUT
        assert entities_state_9[2].integration == "binary_sensor"
        assert entities_state_9[2].entity_name == "binary_sensor.motion_3"
        assert entities_state_9[3].parent == 1
        assert entities_state_9[3].position == 6
        assert entities_state_9[3].parameter_role == INPUT
        assert entities_state_9[3].integration == "binary_sensor"
        assert entities_state_9[3].entity_name == "binary_sensor.motion_4"
        assert end_position == 6

        # border test cases - the list build like this [CONF_STATE/s, CONF_ENTITY_ID/s]
        condition_part_state_9_input = ["test1", "test", "test1", "on"]
        assert (
            await run_automation(
                file_path,
                [],
                condition_part_state_9_input,
            )
        ) == {
            "condition_passed": True,
        }

        condition_part_state_9_input = ["test", "test1", "on", "test1"]
        assert (
            await run_automation(
                file_path,
                [],
                condition_part_state_9_input,
            )
        ) == {
            "condition_passed": True,
        }

        condition_part_state_9_input = ["on", "Test1", "Test1", "Test1"]
        assert (
            await run_automation(
                file_path,
                [],
                condition_part_state_9_input,
            )
        ) == {
            "condition_passed": True,
        }

        condition_part_state_9_input = ["Test1", "off", "Test1", "Test1"]
        assert (
            await run_automation(
                file_path,
                [],
                condition_part_state_9_input,
            )
        ) == {
            "condition_passed": True,
        }

        condition_part_state_9_input = [None, None, "off", "off"]
        assert (
            await run_automation(
                file_path,
                [],
                condition_part_state_9_input,
            )
        ) == {"ValueError": "Condition values cannot be None"}

        condition_part_state_9_input = [None, None, "unknown", None]
        assert (
            await run_automation(
                file_path,
                [],
                condition_part_state_9_input,
            )
        ) == {"ValueError": "Condition values cannot be None"}

        condition_part_state_9_input = [None, None, "on", None]
        assert (
            await run_automation(
                file_path,
                [],
                condition_part_state_9_input,
            )
        ) == {"ValueError": "Condition values cannot be None"}

        condition_part_state_9_input = [None, None, None, None]
        assert (
            await run_automation(
                file_path,
                [],
                condition_part_state_9_input,
            )
        ) == {"ValueError": "Condition values cannot be None"}

        real_pos == 4

        # Test case 10: State condition with multiple entity ids and conditional entity states and at a specific position
        condition_part_state_10 = {
            "condition": "state",
            "entity_id": ["humidifier.hygrostat"],
            "attribute": "humidity",
            "state": [1, "20", "sensor.outside_humidity"],
        }
        file_path = init_automation_script("condition_part_state_10", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_state_10,
            position=23,
            real_position=19,
            script_path=file_path,
        )
        test_condition_return(file_path)

        entities_state_10, end_position, real_pos = results
        assert len(entities_state_10) == 2
        assert entities_state_10[0].parent == 23
        assert entities_state_10[0].position == 24
        assert entities_state_10[0].parameter_role == INPUT
        assert entities_state_10[0].integration == "humidifier"
        assert entities_state_10[0].entity_name == "humidifier.hygrostat.humidity"
        assert entities_state_10[0].expected_value == {
            "state": [1, "20", "sensor.outside_humidity"]
        }
        assert entities_state_10[1].parent == 23
        assert entities_state_10[1].position == 25
        assert entities_state_10[1].parameter_role == INPUT
        assert entities_state_10[1].integration == "sensor"
        assert entities_state_10[1].entity_name == "sensor.outside_humidity"
        assert end_position == 25

        # border test cases - the list build like this [CONF_TO, CONF_ENTITY_ID/s]
        condition_part_state_10_input = [
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "test",
            "20",
        ]
        assert (await run_automation(file_path, [], condition_part_state_10_input)) == {
            "condition_passed": True,
        }

        condition_part_state_10_input = [
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "test",
            21,
        ]
        assert (await run_automation(file_path, [], condition_part_state_10_input)) == {
            "condition_passed": False,
        }

        condition_part_state_10_input = [
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            1,
            None,
        ]
        assert (await run_automation(file_path, [], condition_part_state_10_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        condition_part_state_10_input = [
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "79",
            "79",
        ]
        assert (await run_automation(file_path, [], condition_part_state_10_input)) == {
            "condition_passed": True,
        }

        condition_part_state_10_input = [
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            None,
            1,
        ]
        assert (await run_automation(file_path, [], condition_part_state_10_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        condition_part_state_10_input = [
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "test",
            1,
        ]
        assert (await run_automation(file_path, [], condition_part_state_10_input)) == {
            "condition_passed": True,
        }

    async def test_condition_or():
        # Test case 1: OR condition with one entity in that state
        condition_part_or_1 = {
            CONF_CONDITION: CONF_OR,
            CONF_CONDITIONS: [
                {
                    CONF_CONDITION: CONF_STATE,
                    CONF_ENTITY_ID: "binary_sensor.motion",
                    CONF_STATE: "on",
                },
            ],
        }
        file_path = init_automation_script("condition_part_or_1", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part=condition_part_or_1,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        test_condition_return(file_path)

        entities_or_1, end_position, real_pos = results
        assert len(entities_or_1) == 1
        assert entities_or_1[0].parent == 1
        assert entities_or_1[0].position == 2
        assert entities_or_1[0].parameter_role == INPUT
        assert entities_or_1[0].integration == "binary_sensor"
        assert entities_or_1[0].entity_name == "binary_sensor.motion"
        assert entities_or_1[0].expected_value == {CONF_STATE: "on"}
        assert end_position == 2

        condition_part_or_1_input = ["on"]
        assert (await run_automation(file_path, [], condition_part_or_1_input)) == {
            "condition_passed": True,
        }

        for state_val in ["off", "unavailable", "unknown"]:
            condition_part_or_1_input = [state_val]
            assert (await run_automation(file_path, [], condition_part_or_1_input)) == {
                "condition_passed": False,
            }

        condition_part_or_1_input = [None]
        assert (await run_automation(file_path, [], condition_part_or_1_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        real_pos == 1

        # Test case 2: OR condition with two entities in that state
        condition_part_or_2 = {
            CONF_CONDITION: CONF_OR,
            CONF_CONDITIONS: [
                {
                    CONF_CONDITION: CONF_NUMERIC_STATE,
                    CONF_ENTITY_ID: ["binary_sensor.motion"],
                    CONF_ABOVE: 10,
                },
                {
                    CONF_CONDITION: CONF_STATE,
                    CONF_ENTITY_ID: "binary_sensor.motion_2",
                    CONF_STATE: "off",
                },
            ],
        }
        file_path = init_automation_script("condition_part_or_2", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_or_2,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        test_condition_return(file_path)

        entities_or_2, end_position, real_pos = results
        assert len(entities_or_2) == 2
        assert entities_or_2[0].parent == 1
        assert entities_or_2[0].position == 2
        assert entities_or_2[0].parameter_role == INPUT
        assert entities_or_2[0].integration == "binary_sensor"
        assert entities_or_2[0].entity_name == "binary_sensor.motion"
        assert entities_or_2[0].expected_value == {CONF_ABOVE: 10}
        assert entities_or_2[1].parent == 1
        assert entities_or_2[1].position == 3
        assert entities_or_2[1].parameter_role == INPUT
        assert entities_or_2[1].integration == "binary_sensor"
        assert entities_or_2[1].entity_name == "binary_sensor.motion_2"
        assert entities_or_2[1].expected_value == {CONF_STATE: "off"}
        assert end_position == 3

        # border test cases - the list build like this [CONF_NUM_STATE, CONF_STATE]
        # both conditions are True so the result is True
        condition_part_or_2_input = [11, "off"]
        assert (await run_automation(file_path, [], condition_part_or_2_input)) == {
            "condition_passed": True,
        }

        # second condition is True so the result is True
        condition_part_or_2_input = [9, "off"]
        assert (await run_automation(file_path, [], condition_part_or_2_input)) == {
            "condition_passed": True,
        }

        # first condition is True so the result is True
        condition_part_or_2_input = [11, "on"]
        assert (await run_automation(file_path, [], condition_part_or_2_input)) == {
            "condition_passed": True,
        }

        # both conditions are False so the result is False
        condition_part_or_2_input = [9, "on"]
        assert (await run_automation(file_path, [], condition_part_or_2_input)) == {
            "condition_passed": False,
        }

        # first condition is True so the result is True
        condition_part_or_2_input = [11, None]
        assert (await run_automation(file_path, [], condition_part_or_2_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        # both conditions are None so the result is False
        condition_part_or_2_input = [None, None]
        assert (await run_automation(file_path, [], condition_part_or_2_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        real_pos == 2

        # Test case 3: OR condition with three entities in that state
        condition_part_or_3 = {
            CONF_CONDITION: CONF_OR,
            CONF_CONDITIONS: [
                {
                    CONF_CONDITION: CONF_STATE,
                    CONF_ENTITY_ID: ["binary_sensor.motion", "binary_sensor.motion_3"],
                    CONF_STATE: "on",
                },
                {
                    CONF_CONDITION: CONF_STATE,
                    CONF_ENTITY_ID: "binary_sensor.motion_2",
                    CONF_STATE: ["off", "unavailable", "sensor.temperature"],
                },
                {
                    CONF_CONDITION: CONF_NUMERIC_STATE,
                    CONF_ENTITY_ID: "sensor.temperature",
                    CONF_BELOW: "sensor.temperature2",
                    CONF_ABOVE: "sensor.temperature3",
                },
            ],
        }
        file_path = init_automation_script("condition_part_or_3", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_or_3,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        test_condition_return(file_path)

        entities_or_3, end_position, real_pos = results
        assert len(entities_or_3) == 7
        assert entities_or_3[0].parent == 2
        assert entities_or_3[0].position == 3
        assert entities_or_3[0].parameter_role == INPUT
        assert entities_or_3[0].integration == "binary_sensor"
        assert entities_or_3[0].entity_name == "binary_sensor.motion"
        assert entities_or_3[0].expected_value == {CONF_STATE: "on"}
        assert entities_or_3[1].parent == 2
        assert entities_or_3[1].position == 4
        assert entities_or_3[1].parameter_role == INPUT
        assert entities_or_3[1].integration == "binary_sensor"
        assert entities_or_3[1].entity_name == "binary_sensor.motion_3"
        assert entities_or_3[1].expected_value == {CONF_STATE: "on"}
        assert entities_or_3[2].parent == 5
        assert entities_or_3[2].position == 6
        assert entities_or_3[2].parameter_role == INPUT
        assert entities_or_3[2].integration == "binary_sensor"
        assert entities_or_3[2].entity_name == "binary_sensor.motion_2"
        assert entities_or_3[2].expected_value == {
            CONF_STATE: ["off", "unavailable", "sensor.temperature"]
        }
        assert entities_or_3[3].parent == 5
        assert entities_or_3[3].position == 7
        assert entities_or_3[3].parameter_role == INPUT
        assert entities_or_3[3].integration == "sensor"
        assert entities_or_3[3].entity_name == "sensor.temperature"
        assert entities_or_3[4].parent == 8
        assert entities_or_3[4].position == 9
        assert entities_or_3[4].parameter_role == INPUT
        assert entities_or_3[4].integration == "sensor"
        assert entities_or_3[4].entity_name == "sensor.temperature"
        assert entities_or_3[4].expected_value == {
            CONF_BELOW: "sensor.temperature2",
            CONF_ABOVE: "sensor.temperature3",
        }
        assert entities_or_3[5].parent == 8
        assert entities_or_3[5].position == 10
        assert entities_or_3[5].parameter_role == INPUT
        assert entities_or_3[5].integration == "sensor"
        assert entities_or_3[5].entity_name == "sensor.temperature3"
        assert entities_or_3[5].expected_value == {CONF_BELOW: "sensor.temperature"}
        assert entities_or_3[6].parent == 8
        assert entities_or_3[6].position == 11
        assert entities_or_3[6].parameter_role == INPUT
        assert entities_or_3[6].integration == "sensor"
        assert entities_or_3[6].entity_name == "sensor.temperature2"
        assert entities_or_3[6].expected_value == {CONF_ABOVE: "sensor.temperature"}
        assert end_position == 11

        # the structure of the input:
        # ([(ENTITY_ID_STATE, ENTITY_ID_STATE), (ENTITY_ID_STATE, CONF_STATE), (CONF_ABOVE, ENTITY_ID_STATE, CONF_BELOW)])

        # every condition is True so the result should be True
        condition_part_or_3_input = ["on", "on", "off", 10, 5, 10, 20]
        assert (await run_automation(file_path, [], condition_part_or_3_input)) == {
            "condition_passed": True,
        }

        # only last condition is False so the result should be True
        condition_part_or_3_input = ["on", "on", "off", 10, 5, 10, 5]
        assert (await run_automation(file_path, [], condition_part_or_3_input)) == {
            "condition_passed": True,
        }

        # only first two conditions are False so the result should be True
        condition_part_or_3_input = ["off", "off", "on", 10, 5, 10, 20]
        assert (await run_automation(file_path, [], condition_part_or_3_input)) == {
            "condition_passed": True,
        }

        # all conditions are False so the result should be False
        condition_part_or_3_input = ["off", "off", "on", 10, 5, 10, 5]
        assert (await run_automation(file_path, [], condition_part_or_3_input)) == {
            "condition_passed": False,
        }

        # all values are None so the result should be False
        condition_part_or_3_input = [None, None, None, None, None, None, None]
        assert (await run_automation(file_path, [], condition_part_or_3_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        assert real_pos == 7

    async def test_condition_and():
        # Test case 1: AND condition with one entity in that state
        condition_part_and_1 = {
            CONF_CONDITION: CONF_AND,
            CONF_CONDITIONS: [
                {
                    CONF_CONDITION: CONF_STATE,
                    CONF_ENTITY_ID: "binary_sensor.motion",
                    CONF_STATE: "on",
                },
            ],
        }
        file_path = init_automation_script("condition_part_and_1", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_and_1,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        test_condition_return(file_path)

        entities_and_1, end_position, real_pos = results
        assert len(entities_and_1) == 1
        assert entities_and_1[0].parent == 1
        assert entities_and_1[0].position == 2
        assert entities_and_1[0].parameter_role == INPUT
        assert entities_and_1[0].integration == "binary_sensor"
        assert entities_and_1[0].entity_name == "binary_sensor.motion"
        assert entities_and_1[0].expected_value == {CONF_STATE: "on"}
        assert end_position == 2

        condition_part_and_1_input = ["on"]
        assert (await run_automation(file_path, [], condition_part_and_1_input)) == {
            "condition_passed": True,
        }

        for state_val in ["off", "unavailable", "unknown"]:
            condition_part_and_1_input = [state_val]
            assert (
                await run_automation(file_path, [], condition_part_and_1_input)
            ) == {
                "condition_passed": False,
            }

        condition_part_and_1_input = [None]
        assert (await run_automation(file_path, [], condition_part_and_1_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        real_pos == 1

        # Test case 2: AND condition with two entities in that state
        condition_part_and_2 = {
            CONF_CONDITION: CONF_AND,
            CONF_CONDITIONS: [
                {
                    CONF_CONDITION: CONF_NUMERIC_STATE,
                    CONF_ENTITY_ID: ["binary_sensor.motion"],
                    CONF_ABOVE: 10,
                },
                {
                    CONF_CONDITION: CONF_STATE,
                    CONF_ENTITY_ID: "binary_sensor.motion_2",
                    CONF_STATE: "off",
                },
            ],
        }
        file_path = init_automation_script("condition_part_and_2", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_and_2,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        test_condition_return(file_path)

        entities_and_2, end_position, real_pos = results
        assert len(entities_and_2) == 2
        assert entities_and_2[0].parent == 1
        assert entities_and_2[0].position == 2
        assert entities_and_2[0].parameter_role == INPUT
        assert entities_and_2[0].integration == "binary_sensor"
        assert entities_and_2[0].entity_name == "binary_sensor.motion"
        assert entities_and_2[0].expected_value == {CONF_ABOVE: 10}
        assert entities_and_2[1].parent == 1
        assert entities_and_2[1].position == 3
        assert entities_and_2[1].parameter_role == INPUT
        assert entities_and_2[1].integration == "binary_sensor"
        assert entities_and_2[1].entity_name == "binary_sensor.motion_2"
        assert entities_and_2[1].expected_value == {CONF_STATE: "off"}
        assert end_position == 3

        # border test cases - the list build like this [CONF_NUM_STATE, CONF_STATE]
        # both conditions are True so the result should be True
        condition_part_and_2_input = [11, "off"]
        assert (await run_automation(file_path, [], condition_part_and_2_input)) == {
            "condition_passed": True,
        }

        # first condition is False so the result should be False
        condition_part_and_2_input = [9, "off"]
        assert (await run_automation(file_path, [], condition_part_and_2_input)) == {
            "condition_passed": False,
        }

        # second condition is False so the result should be False
        condition_part_and_2_input = [11, "on"]
        assert (await run_automation(file_path, [], condition_part_and_2_input)) == {
            "condition_passed": False,
        }

        # both conditions are False so the result should be False
        condition_part_and_2_input = [9, "on"]
        assert (await run_automation(file_path, [], condition_part_and_2_input)) == {
            "condition_passed": False,
        }

        # the first condition is None so the result should be False
        condition_part_and_2_input = [9, None]
        assert (await run_automation(file_path, [], condition_part_and_2_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        # both values are None so the result should be False
        condition_part_and_2_input = [None, None]
        assert (await run_automation(file_path, [], condition_part_and_2_input)) == {
            "ValueError": "Condition values cannot be None"
        }
        real_pos == 2

        # Test case 3: AND condition with three entities in that state
        condition_part_and_3 = {
            CONF_CONDITION: CONF_AND,
            CONF_CONDITIONS: [
                {
                    CONF_CONDITION: CONF_STATE,
                    CONF_ENTITY_ID: ["binary_sensor.motion", "binary_sensor.motion_3"],
                    CONF_STATE: "on",
                },
                {
                    CONF_CONDITION: CONF_STATE,
                    CONF_ENTITY_ID: "binary_sensor.motion_2",
                    CONF_STATE: ["off", "unavailable", "sensor.temperature"],
                },
                {
                    CONF_CONDITION: CONF_NUMERIC_STATE,
                    CONF_ENTITY_ID: "sensor.temperature",
                    CONF_BELOW: "sensor.temperature2",
                    CONF_ABOVE: "sensor.temperature3",
                },
            ],
        }
        file_path = init_automation_script("condition_part_and_3", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_and_3,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        test_condition_return(file_path)

        entities_and_3, end_position, real_pos = results
        assert len(entities_and_3) == 7
        assert entities_and_3[0].parent == 2
        assert entities_and_3[0].position == 3
        assert entities_and_3[0].parameter_role == INPUT
        assert entities_and_3[0].integration == "binary_sensor"
        assert entities_and_3[0].entity_name == "binary_sensor.motion"
        assert entities_and_3[0].expected_value == {CONF_STATE: "on"}
        assert entities_and_3[1].parent == 2
        assert entities_and_3[1].position == 4
        assert entities_and_3[1].parameter_role == INPUT
        assert entities_and_3[1].integration == "binary_sensor"
        assert entities_and_3[1].entity_name == "binary_sensor.motion_3"
        assert entities_and_3[1].expected_value == {CONF_STATE: "on"}
        assert entities_and_3[2].parent == 5
        assert entities_and_3[2].position == 6
        assert entities_and_3[2].parameter_role == INPUT
        assert entities_and_3[2].integration == "binary_sensor"
        assert entities_and_3[2].entity_name == "binary_sensor.motion_2"
        assert entities_and_3[2].expected_value == {
            CONF_STATE: ["off", "unavailable", "sensor.temperature"]
        }
        assert entities_and_3[3].parent == 5
        assert entities_and_3[3].position == 7
        assert entities_and_3[3].parameter_role == INPUT
        assert entities_and_3[3].integration == "sensor"
        assert entities_and_3[3].entity_name == "sensor.temperature"
        assert entities_and_3[4].parent == 8
        assert entities_and_3[4].position == 9
        assert entities_and_3[4].parameter_role == INPUT
        assert entities_and_3[4].integration == "sensor"
        assert entities_and_3[4].entity_name == "sensor.temperature"
        assert entities_and_3[4].expected_value == {
            CONF_BELOW: "sensor.temperature2",
            CONF_ABOVE: "sensor.temperature3",
        }
        assert entities_and_3[5].parent == 8
        assert entities_and_3[5].position == 10
        assert entities_and_3[5].parameter_role == INPUT
        assert entities_and_3[5].integration == "sensor"
        assert entities_and_3[5].entity_name == "sensor.temperature3"
        assert entities_and_3[5].expected_value == {CONF_BELOW: "sensor.temperature"}
        assert entities_and_3[6].parent == 8
        assert entities_and_3[6].position == 11
        assert entities_and_3[6].parameter_role == INPUT
        assert entities_and_3[6].integration == "sensor"
        assert entities_and_3[6].entity_name == "sensor.temperature2"
        assert entities_and_3[6].expected_value == {CONF_ABOVE: "sensor.temperature"}
        assert end_position == 11

        # the structure of the input: ([(ENTITY_ID, ENTITY_ID), (EXP_ENTITY_STATE, ENTITY_ID), (BELOW, STATE, ABOVE)])
        # every condition is True so the result should be True
        condition_part_and_3_input = ["on", "on", 10, "off", 5, 10, 20]
        assert (await run_automation(file_path, [], condition_part_and_3_input)) == {
            "condition_passed": True,
        }

        # last condition is False so the result should be False
        condition_part_and_3_input = ["on", "on", 10, "off", 5, 10, 5]
        assert (await run_automation(file_path, [], condition_part_and_3_input)) == {
            "condition_passed": False,
        }

        # first two conditions are False so the result should be False
        condition_part_and_3_input = ["off", "off", 10, "on", 5, 10, 20]
        assert (await run_automation(file_path, [], condition_part_and_3_input)) == {
            "condition_passed": False,
        }

        # all conditions are False so the result should be False
        condition_part_and_3_input = ["off", "off", 10, "on", 5, 10, 5]
        assert (await run_automation(file_path, [], condition_part_and_3_input)) == {
            "condition_passed": False,
        }

        # all conditions are True and the second condition is like the comparing entity so the result should be True
        condition_part_not_3_input = ["on", "on", "test1", "test1", 5, 10, 35]
        assert (await run_automation(file_path, [], condition_part_not_3_input)) == {
            "condition_passed": True,
        }

        # all values are None so the result should be False
        condition_part_and_3_input = [None, None, None, None, None, None, None]
        assert (await run_automation(file_path, [], condition_part_and_3_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        assert real_pos == 7

    async def test_condition_not():
        # Test case 1: NOT condition with one entity in that state
        condition_part_not_1 = {
            CONF_CONDITION: CONF_NOT,
            CONF_CONDITIONS: [
                {
                    CONF_CONDITION: CONF_STATE,
                    CONF_ENTITY_ID: "binary_sensor.motion",
                    CONF_STATE: "on",
                },
            ],
        }
        file_path = init_automation_script("condition_part_not_1", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_not_1,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        test_condition_return(file_path)

        entities_not_1, end_position, real_pos = results
        assert len(entities_not_1) == 1
        assert entities_not_1[0].parent == 1
        assert entities_not_1[0].position == 2
        assert entities_not_1[0].parameter_role == INPUT
        assert entities_not_1[0].integration == "binary_sensor"
        assert entities_not_1[0].entity_name == "binary_sensor.motion"
        assert entities_not_1[0].expected_value == {CONF_STATE: "on"}
        assert end_position == 2

        condition_part_not_1_input = ["on"]
        assert (await run_automation(file_path, [], condition_part_not_1_input)) == {
            "condition_passed": False,
        }

        for state_val in ["off", "unavailable", "unknown"]:
            condition_part_not_1_input = [state_val]
            assert (
                await run_automation(file_path, [], condition_part_not_1_input)
            ) == {
                "condition_passed": True,
            }

        condition_part_not_1_input = [None]
        assert (await run_automation(file_path, [], condition_part_not_1_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        real_pos == 1

        # Test case 2: NOT condition with two entities in that state
        condition_part_not_2 = {
            CONF_CONDITION: CONF_NOT,
            CONF_CONDITIONS: [
                {
                    CONF_CONDITION: CONF_NUMERIC_STATE,
                    CONF_ENTITY_ID: ["binary_sensor.motion"],
                    CONF_ABOVE: 10,
                },
                {
                    CONF_CONDITION: CONF_STATE,
                    CONF_ENTITY_ID: "binary_sensor.motion_2",
                    CONF_STATE: "off",
                },
            ],
        }
        file_path = init_automation_script("condition_part_not_2", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_not_2,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        test_condition_return(file_path)

        entities_not_2, end_position, real_pos = results
        assert len(entities_not_2) == 2
        assert entities_not_2[0].parent == 1
        assert entities_not_2[0].position == 2
        assert entities_not_2[0].parameter_role == INPUT
        assert entities_not_2[0].integration == "binary_sensor"
        assert entities_not_2[0].entity_name == "binary_sensor.motion"
        assert entities_not_2[0].expected_value == {CONF_ABOVE: 10}
        assert entities_not_2[1].parent == 1
        assert entities_not_2[1].position == 3
        assert entities_not_2[1].parameter_role == INPUT
        assert entities_not_2[1].integration == "binary_sensor"
        assert entities_not_2[1].entity_name == "binary_sensor.motion_2"
        assert entities_not_2[1].expected_value == {CONF_STATE: "off"}
        assert end_position == 3

        # border test cases - the list build like this [CONF_NUM_STATE, CONF_STATE]
        # both conditions are True so the result should be False
        condition_part_not_2_input = [11, "off"]
        assert (await run_automation(file_path, [], condition_part_not_2_input)) == {
            "condition_passed": False,
        }

        # the second condition is True so the result is False
        condition_part_not_2_input = [9, "off"]
        assert (await run_automation(file_path, [], condition_part_not_2_input)) == {
            "condition_passed": False,
        }

        # the first condition is True so the result should be False
        condition_part_not_2_input = [11, "on"]
        assert (await run_automation(file_path, [], condition_part_not_2_input)) == {
            "condition_passed": False,
        }

        # both conditions are False so the result is True
        condition_part_not_2_input = [9, "on"]
        assert (await run_automation(file_path, [], condition_part_not_2_input)) == {
            "condition_passed": True,
        }

        #  the first condition is True so the result should be False
        condition_part_not_2_input = [11, None]
        assert (await run_automation(file_path, [], condition_part_not_2_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        # the first condition is False and the second condition is None so the result should be True
        condition_part_not_2_input = [9, None]
        assert (await run_automation(file_path, [], condition_part_not_2_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        # both values are None so the result should be True
        condition_part_not_2_input = [None, None]
        assert (await run_automation(file_path, [], condition_part_not_2_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        real_pos == 2

        # Test case 3: NOT condition with three entities in that state
        condition_part_not_3 = {
            CONF_CONDITION: CONF_NOT,
            CONF_CONDITIONS: [
                {
                    CONF_CONDITION: CONF_STATE,
                    CONF_ENTITY_ID: ["binary_sensor.motion", "binary_sensor.motion_3"],
                    CONF_STATE: "on",
                },
                {
                    CONF_CONDITION: CONF_STATE,
                    CONF_ENTITY_ID: "binary_sensor.motion_2",
                    CONF_STATE: ["off", "unavailable", "sensor.temperature"],
                },
                {
                    CONF_CONDITION: CONF_NUMERIC_STATE,
                    CONF_ENTITY_ID: "sensor.temperature",
                    CONF_BELOW: "sensor.temperature2",
                    CONF_ABOVE: "sensor.temperature3",
                },
            ],
        }
        file_path = init_automation_script("condition_part_not_3", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_not_3,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        test_condition_return(file_path)

        entities_not_3, end_position, real_pos = results
        assert len(entities_not_3) == 7
        assert entities_not_3[0].parent == 2
        assert entities_not_3[0].position == 3
        assert entities_not_3[0].parameter_role == INPUT
        assert entities_not_3[0].integration == "binary_sensor"
        assert entities_not_3[0].entity_name == "binary_sensor.motion"
        assert entities_not_3[0].expected_value == {CONF_STATE: "on"}
        assert entities_not_3[1].parent == 2
        assert entities_not_3[1].position == 4
        assert entities_not_3[1].parameter_role == INPUT
        assert entities_not_3[1].integration == "binary_sensor"
        assert entities_not_3[1].entity_name == "binary_sensor.motion_3"
        assert entities_not_3[1].expected_value == {CONF_STATE: "on"}
        assert entities_not_3[2].parent == 5
        assert entities_not_3[2].position == 6
        assert entities_not_3[2].parameter_role == INPUT
        assert entities_not_3[2].integration == "binary_sensor"
        assert entities_not_3[2].entity_name == "binary_sensor.motion_2"
        assert entities_not_3[2].expected_value == {
            CONF_STATE: ["off", "unavailable", "sensor.temperature"]
        }
        assert entities_not_3[3].parent == 5
        assert entities_not_3[3].position == 7
        assert entities_not_3[3].parameter_role == INPUT
        assert entities_not_3[3].integration == "sensor"
        assert entities_not_3[3].entity_name == "sensor.temperature"
        assert entities_not_3[4].parent == 8
        assert entities_not_3[4].position == 9
        assert entities_not_3[4].parameter_role == INPUT
        assert entities_not_3[4].integration == "sensor"
        assert entities_not_3[4].entity_name == "sensor.temperature"
        assert entities_not_3[4].expected_value == {
            CONF_BELOW: "sensor.temperature2",
            CONF_ABOVE: "sensor.temperature3",
        }
        assert entities_not_3[5].parent == 8
        assert entities_not_3[5].position == 10
        assert entities_not_3[5].parameter_role == INPUT
        assert entities_not_3[5].integration == "sensor"
        assert entities_not_3[5].entity_name == "sensor.temperature3"
        assert entities_not_3[5].expected_value == {CONF_BELOW: "sensor.temperature"}
        assert entities_not_3[6].parent == 8
        assert entities_not_3[6].position == 11
        assert entities_not_3[6].parameter_role == INPUT
        assert entities_not_3[6].integration == "sensor"
        assert entities_not_3[6].entity_name == "sensor.temperature2"
        assert entities_not_3[6].expected_value == {CONF_ABOVE: "sensor.temperature"}
        assert end_position == 11

        # the structure of the input: ([(ENTITY_ID, ENTITY_ID), (EXP_ENTITY_STATE, ENTITY_ID), (BELOW, STATE, ABOVE)])
        # every condition is True so the result should be False
        condition_part_not_3_input = ["on", "on", 10, "off", 5, 10, 20]
        assert (await run_automation(file_path, [], condition_part_not_3_input)) == {
            "condition_passed": False,
        }

        # only the last condition is False so the result should be False
        condition_part_not_3_input = ["on", "on", 10, "off", 5, 10, 5]
        assert (await run_automation(file_path, [], condition_part_not_3_input)) == {
            "condition_passed": False,
        }

        # only the first two conditions are False so the result should be False
        condition_part_not_3_input = ["off", "off", 10, "on", 5, 10, 20]
        assert (await run_automation(file_path, [], condition_part_not_3_input)) == {
            "condition_passed": False,
        }

        # all conditions are False so the result should be True
        condition_part_not_3_input = ["off", "off", 10, "on", 5, 10, 5]
        assert (await run_automation(file_path, [], condition_part_not_3_input)) == {
            "condition_passed": True,
        }

        # all values are None so the result should be True
        condition_part_not_3_input = [None, None, None, None, None, None, None]
        assert (await run_automation(file_path, [], condition_part_not_3_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        assert real_pos == 7

    async def test_condition_template():
        # Test case 1: Template condition with one entity
        condition_part_template_1 = {
            CONF_CONDITION: CONF_TEMPLATE,
            CONF_VALUE_TEMPLATE: "{{ is_state('device_tracker.paulus', 'home') }}",
        }
        file_path = init_automation_script("condition_part_template_1", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_template_1,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        test_condition_return(file_path)

        entities_template_1, end_position, real_pos = results
        assert len(entities_template_1) == 1
        assert entities_template_1[0].parent is None
        assert entities_template_1[0].position == 1
        assert entities_template_1[0].parameter_role == INPUT
        assert entities_template_1[0].integration == "device_tracker"
        assert entities_template_1[0].entity_name == "device_tracker.paulus"
        assert entities_template_1[0].expected_value == {
            CONF_VALUE_TEMPLATE: "{{ is_state('device_tracker.paulus', 'home') }}"
        }
        assert end_position == 1

        condition_part_template_1_input = [True]
        assert (
            await run_automation(file_path, [], condition_part_template_1_input)
        ) == {
            "condition_passed": True,
        }

        condition_part_template_1_input = [False]
        assert (
            await run_automation(file_path, [], condition_part_template_1_input)
        ) == {
            "condition_passed": False,
        }

        condition_part_template_1_input = [None]
        assert (
            await run_automation(file_path, [], condition_part_template_1_input)
        ) == {"ValueError": "Condition values cannot be None"}

        assert real_pos == 1

        # Test case 2: Template condition with two entities
        condition_part_template_2 = {
            CONF_CONDITION: CONF_TEMPLATE,
            CONF_VALUE_TEMPLATE: "{{ is_state('device_tracker.paulus', 'home') and is_state('device_tracker.anne_therese', 'home') }}",
        }
        file_path = init_automation_script("condition_part_template_2", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_template_2,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        test_condition_return(file_path)

        entities_template_2, end_position, real_pos = results
        assert len(entities_template_2) == 2
        assert entities_template_2[0].parent == 1
        assert entities_template_2[0].position == 2
        assert entities_template_2[0].parameter_role == INPUT
        assert entities_template_2[0].integration == "device_tracker"
        assert entities_template_2[0].entity_name == "device_tracker.paulus"
        assert entities_template_2[0].expected_value == {
            CONF_VALUE_TEMPLATE: "{{ is_state('device_tracker.paulus', 'home') and is_state('device_tracker.anne_therese', 'home') }}"
        }
        assert entities_template_2[1].parent == 1
        assert entities_template_2[1].position == 3
        assert entities_template_2[1].parameter_role == INPUT
        assert entities_template_2[1].integration == "device_tracker"
        assert entities_template_2[1].entity_name == "device_tracker.anne_therese"
        assert entities_template_2[1].expected_value == {
            CONF_VALUE_TEMPLATE: "{{ is_state('device_tracker.paulus', 'home') and is_state('device_tracker.anne_therese', 'home') }}"
        }
        assert end_position == 3

        # both entity conditions are True so the result is True
        condition_part_template_2_input = [True, True]
        assert (
            await run_automation(file_path, [], condition_part_template_2_input)
        ) == {
            "condition_passed": True,
        }

        # one of the entity conditions is False so the result is False
        condition_part_template_2_input = [False, True]
        assert (
            await run_automation(file_path, [], condition_part_template_2_input)
        ) == {
            "condition_passed": False,
        }

        # if one of the values is None the result is an error
        condition_part_template_2_input = [None, None]
        assert (
            await run_automation(file_path, [], condition_part_template_2_input)
        ) == {"ValueError": "Condition values cannot be None"}

        assert real_pos == 2

        # Test case 3: Template condition with one entity and at a specific position
        condition_part_template_3 = {
            CONF_CONDITION: CONF_TEMPLATE,
            CONF_VALUE_TEMPLATE: "{{ is_state('device_tracker.paulus', 'home') }}",
        }
        file_path = init_automation_script("condition_part_template_3", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_template_3,
            position=4,
            parent=2,
            real_position=0,
            script_path=file_path,
        )
        test_condition_return(file_path)

        entities_template_3, end_position, real_pos = results
        assert len(entities_template_3) == 1
        assert entities_template_3[0].parent == 2
        assert entities_template_3[0].position == 4
        assert entities_template_3[0].parameter_role == INPUT
        assert entities_template_3[0].integration == "device_tracker"
        assert entities_template_3[0].entity_name == "device_tracker.paulus"
        assert entities_template_3[0].expected_value == {
            CONF_VALUE_TEMPLATE: "{{ is_state('device_tracker.paulus', 'home') }}"
        }
        assert end_position == 4

        condition_part_template_3_input = [True]
        assert (
            await run_automation(file_path, [], condition_part_template_3_input)
        ) == {
            "condition_passed": True,
        }

        condition_part_template_3_input = [False]
        assert (
            await run_automation(file_path, [], condition_part_template_3_input)
        ) == {
            "condition_passed": False,
        }

        condition_part_template_3_input = [None]
        assert (
            await run_automation(file_path, [], condition_part_template_3_input)
        ) == {"ValueError": "Condition values cannot be None"}

        assert real_pos == 1

        # Test case 4: Template condition with two entities and at a specific position
        condition_part_template_4 = {
            CONF_CONDITION: CONF_TEMPLATE,
            CONF_VALUE_TEMPLATE: "{{ is_state('device_tracker.paulus', 'home') and is_state('device_tracker.anne_therese', 'home') }}",
        }
        file_path = init_automation_script("condition_part_template_4", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_template_4,
            position=4,
            parent=2,
            real_position=0,
            script_path=file_path,
        )
        test_condition_return(file_path)

        entities_template_4, end_position, real_pos = results
        assert len(entities_template_4) == 2
        assert entities_template_4[0].parent == 4
        assert entities_template_4[0].position == 5
        assert entities_template_4[0].parameter_role == INPUT
        assert entities_template_4[0].integration == "device_tracker"
        assert entities_template_4[0].entity_name == "device_tracker.paulus"
        assert entities_template_4[0].expected_value == {
            CONF_VALUE_TEMPLATE: "{{ is_state('device_tracker.paulus', 'home') and is_state('device_tracker.anne_therese', 'home') }}"
        }
        assert entities_template_4[1].parent == 4
        assert entities_template_4[1].position == 6
        assert entities_template_4[1].parameter_role == INPUT
        assert entities_template_4[1].integration == "device_tracker"
        assert entities_template_4[1].entity_name == "device_tracker.anne_therese"
        assert entities_template_4[1].expected_value == {
            CONF_VALUE_TEMPLATE: "{{ is_state('device_tracker.paulus', 'home') and is_state('device_tracker.anne_therese', 'home') }}"
        }
        assert end_position == 6

        condition_part_template_4_input = [True, True]
        assert (
            await run_automation(file_path, [], condition_part_template_4_input)
        ) == {
            "condition_passed": True,
        }

        condition_part_template_4_input = [False, True]
        assert (
            await run_automation(file_path, [], condition_part_template_4_input)
        ) == {
            "condition_passed": False,
        }

        condition_part_template_4_input = [None, None]
        assert (
            await run_automation(file_path, [], condition_part_template_4_input)
        ) == {"ValueError": "Condition values cannot be None"}

        assert real_pos == 2

        # Test case 5: Template condition without a condition parameter
        condition_part_template_5 = ("{{ is_state('device_tracker.paulus', 'home') }}",)
        file_path = init_automation_script("condition_part_template_5", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_template_5,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        test_condition_return(file_path)

        entities_template_5, end_position, real_pos = results
        assert len(entities_template_5) == 1
        assert entities_template_5[0].parent is None
        assert entities_template_5[0].position == 1
        assert entities_template_5[0].parameter_role == INPUT
        assert entities_template_5[0].integration == "device_tracker"
        assert entities_template_5[0].entity_name == "device_tracker.paulus"
        assert entities_template_5[0].expected_value == {
            CONF_VALUE_TEMPLATE: "{{ is_state('device_tracker.paulus', 'home') }}"
        }
        assert end_position == 1

        condition_part_template_5_input = [True]
        assert (
            await run_automation(file_path, [], condition_part_template_5_input)
        ) == {
            "condition_passed": True,
        }

        condition_part_template_5_input = [False]
        assert (
            await run_automation(file_path, [], condition_part_template_5_input)
        ) == {
            "condition_passed": False,
        }

        condition_part_template_5_input = [None]
        assert (
            await run_automation(file_path, [], condition_part_template_5_input)
        ) == {"ValueError": "Condition values cannot be None"}

        assert real_pos == 1

    async def test_condition_sun():
        # Test case 1: Sun condition after the sunset
        condition_part_sun_1 = {
            CONF_CONDITION: "sun",
            CONF_AFTER: "sunset",
        }
        file_path = init_automation_script("condition_part_sun_1", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_sun_1, position=1, real_position=0, script_path=file_path
        )
        test_condition_return(file_path)

        entities_sun_1, end_position, real_pos = results
        assert len(entities_sun_1) == 1
        assert entities_sun_1[0].parent is None
        assert entities_sun_1[0].position == 1
        assert entities_sun_1[0].parameter_role == INPUT
        assert entities_sun_1[0].integration == "sun"
        assert entities_sun_1[0].entity_name == "sun.sun"
        assert entities_sun_1[0].expected_value == {"after": "sunset"}
        assert end_position == 1

        condition_part_sun_1_input = [True]
        assert (await run_automation(file_path, [], condition_part_sun_1_input)) == {
            "condition_passed": True,
        }

        condition_part_sun_1_input = [False]
        assert (await run_automation(file_path, [], condition_part_sun_1_input)) == {
            "condition_passed": False,
        }

        condition_part_sun_1_input = [None]
        assert (await run_automation(file_path, [], condition_part_sun_1_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        assert real_pos == 1

        # Test case 2: Sun condition before the sunset
        condition_part_sun_2 = {
            CONF_CONDITION: "sun",
            CONF_BEFORE: "sunset",
        }
        file_path = init_automation_script("condition_part_sun_2", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_sun_2, position=1, real_position=0, script_path=file_path
        )
        test_condition_return(file_path)

        entities_sun_2, end_position, real_pos = results
        assert len(entities_sun_2) == 1
        assert entities_sun_2[0].parent is None
        assert entities_sun_2[0].position == 1
        assert entities_sun_2[0].parameter_role == INPUT
        assert entities_sun_2[0].integration == "sun"
        assert entities_sun_2[0].entity_name == "sun.sun"
        assert entities_sun_2[0].expected_value == {"before": "sunset"}
        assert end_position == 1

        condition_part_sun_2_input = [True]
        assert (await run_automation(file_path, [], condition_part_sun_2_input)) == {
            "condition_passed": True,
        }

        condition_part_sun_2_input = [False]
        assert (await run_automation(file_path, [], condition_part_sun_2_input)) == {
            "condition_passed": False,
        }

        condition_part_sun_2_input = [None]
        assert (await run_automation(file_path, [], condition_part_sun_2_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        assert real_pos == 1

        # Test case 3: Sun condition 1 hour after the sunset and 1 hour after the sunrise
        condition_part_sun_3 = {
            CONF_CONDITION: "sun",
            CONF_AFTER: "sunset",
            CONF_BEFORE: "sunrise",
            CONF_BEFORE_OFFSET: "-01:00:00",
            CONF_AFTER_OFFSET: "01:00:00",
        }
        file_path = init_automation_script("condition_part_sun_3", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_sun_3, position=1, real_position=0, script_path=file_path
        )
        test_condition_return(file_path)

        entities_sun_3, end_position, real_pos = results
        assert len(entities_sun_3) == 1
        assert entities_sun_3[0].parent is None
        assert entities_sun_3[0].position == 1
        assert entities_sun_3[0].parameter_role == INPUT
        assert entities_sun_3[0].integration == "sun"
        assert entities_sun_3[0].entity_name == "sun.sun"
        assert entities_sun_3[0].expected_value == {
            "after": "sunset",
            "before": "sunrise",
            "before_offset": "-01:00:00",
            "after_offset": "01:00:00",
        }
        assert end_position == 1

        condition_part_sun_3_input = [True]
        assert (await run_automation(file_path, [], condition_part_sun_3_input)) == {
            "condition_passed": True,
        }

        condition_part_sun_3_input = [False]
        assert (await run_automation(file_path, [], condition_part_sun_3_input)) == {
            "condition_passed": False,
        }

        condition_part_sun_3_input = [None]
        assert (await run_automation(file_path, [], condition_part_sun_3_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        assert real_pos == 1

        # Test case 4: Sun condition after the sunset and before the sunrise at a specific position
        condition_part_sun_4 = {
            CONF_CONDITION: "sun",
            CONF_AFTER: "sunset",
            CONF_BEFORE: "sunrise",
        }
        file_path = init_automation_script("condition_part_sun_4", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_sun_4,
            position=3,
            parent=2,
            real_position=0,
            script_path=file_path,
        )
        test_condition_return(file_path)

        entities_sun_4, end_position, real_pos = results
        assert len(entities_sun_4) == 1
        assert entities_sun_4[0].parent == 2
        assert entities_sun_4[0].position == 3
        assert entities_sun_4[0].parameter_role == INPUT
        assert entities_sun_4[0].integration == "sun"
        assert entities_sun_4[0].entity_name == "sun.sun"
        assert entities_sun_4[0].expected_value == {
            "after": "sunset",
            "before": "sunrise",
        }
        assert end_position == 3

        condition_part_sun_4_input = [True]
        assert (await run_automation(file_path, [], condition_part_sun_4_input)) == {
            "condition_passed": True,
        }

        condition_part_sun_4_input = [False]
        assert (await run_automation(file_path, [], condition_part_sun_4_input)) == {
            "condition_passed": False,
        }

        condition_part_sun_4_input = [None]
        assert (await run_automation(file_path, [], condition_part_sun_4_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        assert real_pos == 1

    async def test_condition_device():
        # Test case 1: Device condition with a device that is [CONF_IS_ON, IS_OFF]
        condition_part_device_1 = {
            CONF_CONDITION: "device",
            CONF_DEVICE_ID: "device_id_1",
            CONF_DOMAIN: "domain",
            CONF_ENTITY_ID: "test_entity_id",
            CONF_TYPE: "is_on",
        }
        file_path = init_automation_script("condition_part_device_1", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_device_1, position=1, real_position=0, script_path=file_path
        )
        test_condition_return(file_path)

        entities_device_1, end_position, real_pos = results
        assert len(entities_device_1) == 1
        assert entities_device_1[0].parent is None
        assert entities_device_1[0].position == 1
        assert entities_device_1[0].parameter_role == INPUT
        assert entities_device_1[0].integration == "device"
        assert entities_device_1[0].entity_name == "device.device_id_1"
        assert entities_device_1[0].expected_value == {
            CONF_ENTITY_ID: "test_entity_id",
            CONF_TYPE: "is_on",
            CONF_DOMAIN: "domain",
        }
        assert end_position == 1

        condition_part_device_1_input = ["is_on"]
        assert (await run_automation(file_path, [], condition_part_device_1_input)) == {
            "condition_passed": True,
        }

        condition_part_device_1_input = ["is_off"]
        assert (await run_automation(file_path, [], condition_part_device_1_input)) == {
            "condition_passed": False,
        }

        condition_part_device_1_input = [None]
        assert (await run_automation(file_path, [], condition_part_device_1_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        # Test case 2: Device condition with a device that does something at a specific position
        condition_part_device_2 = {
            CONF_CONDITION: "device",
            CONF_DEVICE_ID: "device_id_1",
            CONF_DOMAIN: "domain",
            CONF_ENTITY_ID: "test_entity_id",
            CONF_TYPE: "is_on",
        }
        file_path = init_automation_script("condition_part_device_2", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_device_2,
            position=5,
            parent=2,
            real_position=0,
            script_path=file_path,
        )
        test_condition_return(file_path)

        entities_device_2, end_position, real_pos = results
        assert len(entities_device_2) == 1
        assert entities_device_2[0].parent == 2
        assert entities_device_2[0].position == 5
        assert entities_device_2[0].parameter_role == INPUT
        assert entities_device_2[0].integration == "device"
        assert entities_device_2[0].entity_name == "device.device_id_1"
        assert entities_device_2[0].expected_value == {
            CONF_ENTITY_ID: "test_entity_id",
            CONF_TYPE: "is_on",
            CONF_DOMAIN: "domain",
        }
        assert end_position == 5

        condition_part_device_2_input = ["is_on"]
        assert (await run_automation(file_path, [], condition_part_device_2_input)) == {
            "condition_passed": True,
        }

        condition_part_device_2_input = ["is_off"]
        assert (await run_automation(file_path, [], condition_part_device_2_input)) == {
            "condition_passed": False,
        }

        condition_part_device_2_input = [None]
        assert (await run_automation(file_path, [], condition_part_device_2_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        assert real_pos == 1

    async def test_condition_time():
        # Test case 1: Time condition before a specific time
        condition_part_time_1 = {
            CONF_CONDITION: "time",
            CONF_BEFORE: "12:00:00",
        }
        file_path = init_automation_script("condition_part_time_1", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_time_1, position=1, real_position=0, script_path=file_path
        )
        test_condition_return(file_path)

        entities_time_1, end_position, real_pos = results
        assert len(entities_time_1) == 1
        assert entities_time_1[0].parent is None
        assert entities_time_1[0].position == 1
        assert entities_time_1[0].parameter_role == INPUT
        assert entities_time_1[0].integration == "datetime"
        assert entities_time_1[0].entity_name is not None
        assert entities_time_1[0].expected_value == {"before": "12:00:00"}
        assert end_position == 1

        condtion_part_time_1_input = [True]
        assert (await run_automation(file_path, [], condtion_part_time_1_input)) == {
            "condition_passed": True,
        }

        condtion_part_time_1_input = [False]
        assert (await run_automation(file_path, [], condtion_part_time_1_input)) == {
            "condition_passed": False,
        }

        condtion_part_time_1_input = [None]
        assert (await run_automation(file_path, [], condtion_part_time_1_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        assert real_pos == 1

        # Test case 2: Time condition after a specific time
        condition_part_time_2 = {
            CONF_CONDITION: "time",
            CONF_AFTER: "12:00:00",
        }
        file_path = init_automation_script("condition_part_time_2", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_time_2, position=1, real_position=0, script_path=file_path
        )
        test_condition_return(file_path)

        entities_time_2, end_position, real_pos = results
        assert len(entities_time_2) == 1
        assert entities_time_2[0].parent is None
        assert entities_time_2[0].position == 1
        assert entities_time_2[0].parameter_role == INPUT
        assert entities_time_2[0].integration == "datetime"
        assert entities_time_2[0].entity_name is not None
        assert entities_time_2[0].expected_value == {"after": "12:00:00"}
        assert end_position == 1

        condtion_part_time_2_input = [True]
        assert (await run_automation(file_path, [], condtion_part_time_2_input)) == {
            "condition_passed": True,
        }

        condtion_part_time_2_input = [False]
        assert (await run_automation(file_path, [], condtion_part_time_2_input)) == {
            "condition_passed": False,
        }

        condtion_part_time_2_input = [None]
        assert (await run_automation(file_path, [], condtion_part_time_2_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        assert real_pos == 1

        # Test case 3: Time condition between two specific times on monday
        condition_part_time_3 = {
            CONF_CONDITION: "time",
            CONF_AFTER: "12:00:00",
            CONF_BEFORE: "14:00:00",
            CONF_WEEKDAY: "mon",
        }
        file_path = init_automation_script("condition_part_time_3", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_time_3, position=1, real_position=0, script_path=file_path
        )
        test_condition_return(file_path)

        entities_time_3, end_position, real_pos = results
        assert len(entities_time_3) == 1
        assert entities_time_3[0].parent is None
        assert entities_time_3[0].position == 1
        assert entities_time_3[0].parameter_role == INPUT
        assert entities_time_3[0].integration == "datetime"
        assert entities_time_3[0].entity_name is not None
        assert entities_time_3[0].expected_value == {
            "after": "12:00:00",
            "before": "14:00:00",
            "weekday": "mon",
        }
        assert end_position == 1

        condtion_part_time_3_input = [True]
        assert (await run_automation(file_path, [], condtion_part_time_3_input)) == {
            "condition_passed": True,
        }

        condtion_part_time_3_input = [False]
        assert (await run_automation(file_path, [], condtion_part_time_3_input)) == {
            "condition_passed": False,
        }

        condtion_part_time_3_input = [None]
        assert (await run_automation(file_path, [], condtion_part_time_3_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        assert real_pos == 1

        # Test case 4: Time condition between two specific times on friday at a specific position
        condition_part_time_4 = {
            CONF_CONDITION: "time",
            CONF_AFTER: "12:00:00",
            CONF_BEFORE: "14:00:00",
            CONF_WEEKDAY: "fri",
        }
        file_path = init_automation_script("condition_part_time_4", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_time_4,
            position=12,
            real_position=0,
            script_path=file_path,
            parent=10,
        )
        test_condition_return(file_path)

        entities_time_4, end_position, real_pos = results
        assert len(entities_time_4) == 1
        assert entities_time_4[0].parent == 10
        assert entities_time_4[0].position == 12
        assert entities_time_4[0].parameter_role == INPUT
        assert entities_time_4[0].integration == "datetime"
        assert entities_time_4[0].entity_name is not None
        assert entities_time_4[0].expected_value == {
            "after": "12:00:00",
            "before": "14:00:00",
            "weekday": "fri",
        }
        assert end_position == 12

        condtion_part_time_4_input = [True]
        assert (await run_automation(file_path, [], condtion_part_time_4_input)) == {
            "condition_passed": True,
        }

        condtion_part_time_4_input = [False]
        assert (await run_automation(file_path, [], condtion_part_time_4_input)) == {
            "condition_passed": False,
        }

        condtion_part_time_4_input = [None]
        assert (await run_automation(file_path, [], condtion_part_time_4_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        assert real_pos == 1

    async def test_condition_trigger():
        # Test case 1: Trigger condition with a trigger that has an string id
        condition_part_trigger_1 = {CONF_CONDITION: CONF_TRIGGER, CONF_ID: "trigger_1"}
        file_path = init_automation_script("condition_part_trigger_1", CONDITION_DIR)
        test_trigger_fill(file_path, "trigger_1")
        results = _condition_entities(
            condition_part_trigger_1, position=1, real_position=0, script_path=file_path
        )
        test_condition_return(file_path)

        entities_trigger_1, end_position, real_pos = results
        assert len(entities_trigger_1) == 1
        assert entities_trigger_1[0].parent is None
        assert entities_trigger_1[0].position == 1
        assert entities_trigger_1[0].parameter_role == INPUT
        assert entities_trigger_1[0].integration == "trigger"
        assert entities_trigger_1[0].entity_name is not None
        assert entities_trigger_1[0].expected_value == {CONF_ID: "trigger_1"}
        assert end_position == 1

        # # The automation was triggered by a trigger with id trigger_1 so the result is True
        assert (await run_automation(file_path, [], [])) == {
            "condition_passed": True,
        }

        assert real_pos == 0

        # Test case 2: Trigger condition with a trigger that has an integer id
        condition_part_trigger_2 = {CONF_CONDITION: CONF_TRIGGER, CONF_ID: 1}
        file_path = init_automation_script("condition_part_trigger_2", CONDITION_DIR)
        test_trigger_fill(file_path, "trigger_1")
        results = _condition_entities(
            condition_part_trigger_2, position=1, real_position=0, script_path=file_path
        )
        test_condition_return(file_path)

        entities_trigger_2, end_position, real_pos = results
        assert len(entities_trigger_2) == 1
        assert entities_trigger_2[0].parent is None
        assert entities_trigger_2[0].position == 1
        assert entities_trigger_2[0].parameter_role == INPUT
        assert entities_trigger_2[0].integration == "trigger"
        assert entities_trigger_2[0].entity_name is not None
        assert entities_trigger_2[0].expected_value == {CONF_ID: "1"}
        assert end_position == 1

        # The automation was triggered by a trigger with the id trigger_1 and not id = 1 so the result is False
        assert (await run_automation(file_path, [], [])) == {
            "condition_passed": False,
        }

        assert real_pos == 0

        # Test case 3: Trigger condition with a trigger that has an string id at a specific position
        condition_part_trigger_3 = {CONF_CONDITION: "trigger", CONF_ID: "trigger_1"}
        file_path = init_automation_script("condition_part_trigger_3", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_trigger_3,
            position=4,
            parent=2,
            real_position=0,
            script_path=file_path,
        )
        test_condition_return(file_path)

        entities_trigger_3, end_position, real_pos = results
        assert len(entities_trigger_3) == 1
        assert entities_trigger_3[0].parent == 2
        assert entities_trigger_3[0].position == 4
        assert entities_trigger_3[0].parameter_role == INPUT
        assert entities_trigger_3[0].integration == "trigger"
        assert entities_trigger_3[0].entity_name is not None
        assert entities_trigger_3[0].expected_value == {CONF_ID: "trigger_1"}
        assert end_position == 4

        # The automation was triggered by a trigger with no id and not trigger_1 so the result is False
        assert (await run_automation(file_path, [], [])) == {
            "condition_passed": False,
        }

        assert real_pos == 0

        # Test case 4: Trigger condition with a list of possible trigger ids at a specific position
        condition_part_trigger_4 = {
            CONF_CONDITION: "trigger",
            CONF_ID: ["trigger_1", "trigger_2"],
        }
        file_path = init_automation_script("condition_part_trigger_4", CONDITION_DIR)
        test_trigger_fill(file_path, "trigger_2")
        results = _condition_entities(
            condition_part_trigger_4,
            position=4,
            parent=2,
            real_position=0,
            script_path=file_path,
        )
        test_condition_return(file_path)

        entities_trigger_4, end_position, real_pos = results
        assert len(entities_trigger_4) == 2
        assert entities_trigger_4[0].parent == 4
        assert entities_trigger_4[0].position == 5
        assert entities_trigger_4[0].parameter_role == INPUT
        assert entities_trigger_4[0].integration == "trigger"
        assert entities_trigger_4[0].entity_name is not None
        assert entities_trigger_4[0].expected_value == {CONF_ID: "trigger_1"}
        assert entities_trigger_4[1].parent == 4
        assert entities_trigger_4[1].position == 6
        assert entities_trigger_4[1].parameter_role == INPUT
        assert entities_trigger_4[1].integration == "trigger"
        assert entities_trigger_4[1].entity_name is not None
        assert entities_trigger_4[1].expected_value == {CONF_ID: "trigger_2"}
        assert end_position == 6

        # The automation was triggered by a trigger with id trigger_2 so the result is True
        assert (await run_automation(file_path, [], [])) == {
            "condition_passed": True,
        }
        assert real_pos == 0

    async def test_condition_zone():
        # Test case 1: Zone condition with one entity
        condition_part_zone_1 = {
            CONF_CONDITION: "zone",
            CONF_ENTITY_ID: "device_tracker.paulus",
            CONF_ZONE: "zone.home",
        }
        file_path = init_automation_script("condition_part_zone_1", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_zone_1, position=1, real_position=0, script_path=file_path
        )
        test_condition_return(file_path)

        entities_zone_1, end_position, real_pos = results
        assert len(entities_zone_1) == 2
        assert entities_zone_1[0].parent == 1
        assert entities_zone_1[0].position == 2
        assert entities_zone_1[0].parameter_role == INPUT
        assert entities_zone_1[0].integration == "device_tracker"
        assert entities_zone_1[0].entity_name == "device_tracker.paulus"
        assert entities_zone_1[0].expected_value == {"zone": "zone.home"}
        assert entities_zone_1[1].parent == 1
        assert entities_zone_1[1].position == 3
        assert entities_zone_1[1].parameter_role == INPUT
        assert entities_zone_1[1].integration == "zone"
        assert entities_zone_1[1].entity_name == "zone.home"
        assert entities_zone_1[1].expected_value == {
            "entity_id": "device_tracker.paulus"
        }
        assert end_position == 3

        condition_part_zone_1_input = ["device_tracker.paulus"]
        assert (await run_automation(file_path, [], condition_part_zone_1_input)) == {
            "condition_passed": True,
        }

        condition_part_zone_1_input = ["device_tracker.anne_therese"]
        assert (await run_automation(file_path, [], condition_part_zone_1_input)) == {
            "condition_passed": False,
        }

        condition_part_zone_1_input = [None]
        assert (await run_automation(file_path, [], condition_part_zone_1_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        assert real_pos == 1

        # Test case 2: Zone condition with one entity in a list
        condition_part_zone_2 = {
            CONF_CONDITION: "zone",
            CONF_ENTITY_ID: ["device_tracker.paulus"],
            CONF_ZONE: "zone.home",
        }
        file_path = init_automation_script("condition_part_zone_2", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_zone_2, position=1, real_position=0, script_path=file_path
        )
        test_condition_return(file_path)

        entities_zone_2, end_position, real_pos = results
        assert len(entities_zone_2) == 2
        assert entities_zone_2[0].parent == 1
        assert entities_zone_2[0].position == 2
        assert entities_zone_2[0].parameter_role == INPUT
        assert entities_zone_2[0].integration == "device_tracker"
        assert entities_zone_2[0].entity_name == "device_tracker.paulus"
        assert entities_zone_2[0].expected_value == {"zone": "zone.home"}
        assert entities_zone_2[1].parent == 1
        assert entities_zone_2[1].position == 3
        assert entities_zone_2[1].parameter_role == INPUT
        assert entities_zone_2[1].integration == "zone"
        assert entities_zone_2[1].entity_name == "zone.home"
        assert entities_zone_2[1].expected_value == {
            "entity_id": "device_tracker.paulus"
        }
        assert end_position == 3

        condition_part_zone_2_input = ["device_tracker.paulus"]
        assert (await run_automation(file_path, [], condition_part_zone_2_input)) == {
            "condition_passed": True,
        }

        condition_part_zone_2_input = ["device_tracker.anne_therese"]
        assert (await run_automation(file_path, [], condition_part_zone_2_input)) == {
            "condition_passed": False,
        }

        condition_part_zone_2_input = [None]
        assert (await run_automation(file_path, [], condition_part_zone_2_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        assert real_pos == 1

        # Test case 3: Zone condition with two entities
        condition_part_zone_3 = {
            CONF_CONDITION: "zone",
            CONF_ENTITY_ID: ["device_tracker.paulus", "device_tracker.anne_therese"],
            CONF_ZONE: "zone.home",
        }
        file_path = init_automation_script("condition_part_zone_3", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_zone_3, position=1, real_position=0, script_path=file_path
        )
        test_condition_return(file_path)

        entities_zone_3, end_position, real_pos = results
        assert len(entities_zone_3) == 3
        assert entities_zone_3[0].parent == 2
        assert entities_zone_3[0].position == 3
        assert entities_zone_3[0].parameter_role == INPUT
        assert entities_zone_3[0].integration == "device_tracker"
        assert entities_zone_3[0].entity_name == "device_tracker.paulus"
        assert entities_zone_3[0].expected_value == {"zone": "zone.home"}
        assert entities_zone_3[1].parent == 2
        assert entities_zone_3[1].position == 4
        assert entities_zone_3[1].parameter_role == INPUT
        assert entities_zone_3[1].integration == "device_tracker"
        assert entities_zone_3[1].entity_name == "device_tracker.anne_therese"
        assert entities_zone_3[1].expected_value == {"zone": "zone.home"}
        assert entities_zone_3[2].parent == 1
        assert entities_zone_3[2].position == 5
        assert entities_zone_3[2].parameter_role == INPUT
        assert entities_zone_3[2].integration == "zone"
        assert entities_zone_3[2].entity_name == "zone.home"
        assert entities_zone_3[2].expected_value == {
            CONF_ENTITY_ID: ["device_tracker.paulus", "device_tracker.anne_therese"]
        }
        assert end_position == 5

        # not enough input
        condition_part_zone_3_input = ["device_tracker.paulus", "filler"]
        assert (await run_automation(file_path, [], condition_part_zone_3_input)) == {
            "condition_passed": False,
        }

        # not enough input
        condition_part_zone_3_input = ["filler", "device_tracker.anne_therese"]
        assert (await run_automation(file_path, [], condition_part_zone_3_input)) == {
            "condition_passed": False,
        }

        # right input order
        condition_part_zone_3_input = [
            "device_tracker.paulus",
            "device_tracker.anne_therese",
        ]
        assert (await run_automation(file_path, [], condition_part_zone_3_input)) == {
            "condition_passed": True,
        }

        # wrong input order
        condition_part_zone_3_input = [
            "device_tracker.anne_therese",
            "device_tracker.paulus",
        ]
        assert (await run_automation(file_path, [], condition_part_zone_3_input)) == {
            "condition_passed": False,
        }

        # wrong inputs
        condition_part_zone_3_input = [
            "device_tracker.perter_walt",
            "device_tracker.anne_therese",
        ]
        assert (await run_automation(file_path, [], condition_part_zone_3_input)) == {
            "condition_passed": False,
        }

        # None inputs arent allowed
        condition_part_zone_3_input = [None, None]
        assert (await run_automation(file_path, [], condition_part_zone_3_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        assert real_pos == 2

        # Test case 4: Zone condition with two entities and at a specific position
        condition_part_zone_4 = {
            CONF_CONDITION: "zone",
            CONF_ENTITY_ID: ["device_tracker.paulus", "device_tracker.anne_therese"],
            CONF_ZONE: "zone.kitchen",
        }
        file_path = init_automation_script("condition_part_zone_4", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_zone_4,
            position=4,
            parent=2,
            real_position=0,
            script_path=file_path,
        )
        test_condition_return(file_path)

        entities_zone_4, end_position, real_pos = results
        assert len(entities_zone_4) == 3
        assert entities_zone_4[0].parent == 5
        assert entities_zone_4[0].position == 6
        assert entities_zone_4[0].parameter_role == INPUT
        assert entities_zone_4[0].integration == "device_tracker"
        assert entities_zone_4[0].entity_name == "device_tracker.paulus"
        assert entities_zone_4[0].expected_value == {"zone": "zone.kitchen"}
        assert entities_zone_4[1].parent == 5
        assert entities_zone_4[1].position == 7
        assert entities_zone_4[1].parameter_role == INPUT
        assert entities_zone_4[1].integration == "device_tracker"
        assert entities_zone_4[1].entity_name == "device_tracker.anne_therese"
        assert entities_zone_4[1].expected_value == {"zone": "zone.kitchen"}
        assert entities_zone_4[2].parent == 4
        assert entities_zone_4[2].position == 8
        assert entities_zone_4[2].parameter_role == INPUT
        assert entities_zone_4[2].integration == "zone"
        assert entities_zone_4[2].entity_name == "zone.kitchen"
        assert entities_zone_4[2].expected_value == {
            "entity_id": ["device_tracker.paulus", "device_tracker.anne_therese"]
        }
        assert end_position == 8

        # not enough input
        condition_part_zone_4_input = ["device_tracker.paulus", "filler"]
        assert (await run_automation(file_path, [], condition_part_zone_4_input)) == {
            "condition_passed": False,
        }

        # not enough input
        condition_part_zone_4_input = ["filler", "device_tracker.anne_therese"]
        assert (await run_automation(file_path, [], condition_part_zone_4_input)) == {
            "condition_passed": False,
        }

        # right input order
        condition_part_zone_4_input = [
            "device_tracker.paulus",
            "device_tracker.anne_therese",
        ]
        assert (await run_automation(file_path, [], condition_part_zone_4_input)) == {
            "condition_passed": True,
        }

        # wrong input order
        condition_part_zone_4_input = [
            "device_tracker.anne_therese",
            "device_tracker.paulus",
        ]
        assert (await run_automation(file_path, [], condition_part_zone_4_input)) == {
            "condition_passed": False,
        }

        # wrong inputs
        condition_part_zone_4_input = [
            "device_tracker.perter_walt",
            "device_tracker.anne_therese",
        ]
        assert (await run_automation(file_path, [], condition_part_zone_4_input)) == {
            "condition_passed": False,
        }

        # None inputs arent allowed
        condition_part_zone_4_input = [None, None]
        assert (await run_automation(file_path, [], condition_part_zone_4_input)) == {
            "ValueError": "Condition values cannot be None"
        }

        assert real_pos == 2

    async def test_condition_unsupported():
        # Test case 1: unknown condition
        condition_part_x = {
            CONF_CONDITION: "x",
            CONF_SERVICE_DATA: {"entity_id": "light.kitchen"},
        }
        file_path = init_automation_script("condition_part_x", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_x, position=1, real_position=0, script_path=file_path
        )
        test_condition_return(file_path)

        entities_x, end_position, real_pos = results
        assert len(entities_x) == 0
        assert end_position == 1
        assert real_pos == 0

    async def test_condition_disabled():
        # Test case 1: disabled condition
        condition_part_x2 = {
            CONF_CONDITION: "state",
            CONF_ENTITY_ID: "sensor.temperature",
            CONF_STATE: "on",
            CONF_ENABLED: False,
        }
        file_path = init_automation_script("condition_part_x2", CONDITION_DIR)
        test_trigger_fill(file_path)
        results = _condition_entities(
            condition_part_x2, position=1, real_position=0, script_path=file_path
        )
        test_condition_return(file_path)

        entities_x2, end_position, real_pos = results
        assert len(entities_x2) == 0
        assert end_position == 1
        assert real_pos == 0

    async def test_condition_all():
        await test_condition_num_state()
        await test_condition_state()
        await test_condition_or()
        await test_condition_and()
        await test_condition_not()
        await test_condition_template()
        await test_condition_sun()
        await test_condition_device()
        await test_condition_time()
        await test_condition_trigger()
        await test_condition_zone()
        await test_condition_unsupported()
        await test_condition_disabled()

    await test_condition_all()
    print("All condition test cases passed!")


async def test_action_entities():
    ACTION_DIR = path.join(TEST_DIR, "action")
    if not path.exists(ACTION_DIR):
        mkdir(ACTION_DIR)

    async def test_action_call_service():
        # Test case 1: Call service action for one entity
        action_part_call_service_1 = {
            CONF_SERVICE: "light.doSomething",
            CONF_TARGET: {CONF_ENTITY_ID: "light.kitchen"},
        }
        file_path = init_automation_script("action_part_call_service_1", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_call_service_1,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        close_action_section(file_path)

        entities_call_service_1, end_position, real_pos = results
        assert len(entities_call_service_1) == 1
        assert entities_call_service_1[0].parent is None
        assert entities_call_service_1[0].position == 1
        assert entities_call_service_1[0].parameter_role == OUTPUT
        assert entities_call_service_1[0].integration == "light"
        assert entities_call_service_1[0].entity_name == "light.kitchen"
        assert entities_call_service_1[0].expected_value == {
            CONF_SERVICE: "doSomething"
        }
        assert end_position == 1

        assert (await run_automation(file_path, [], [])) == [
            {"light.kitchen": "doSomething"}
        ]

        assert real_pos == 0

        # Test case 2: Call service action for two entity
        action_part_call_service_2 = {
            CONF_SERVICE: "light.doSomething",
            CONF_TARGET: {CONF_ENTITY_ID: ["light.kitchen", "light.living_room"]},
        }
        file_path = init_automation_script("action_part_call_service_2", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_call_service_2,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        close_action_section(file_path)

        entities_call_service_2, end_position, real_pos = results
        assert len(entities_call_service_2) == 1
        assert entities_call_service_2[0].parent is None
        assert entities_call_service_2[0].position == 1
        assert entities_call_service_2[0].parameter_role == OUTPUT
        assert entities_call_service_2[0].integration == "light"
        assert entities_call_service_2[0].entity_name == "light.target_group"
        assert entities_call_service_2[0].expected_value == {
            CONF_SERVICE: "doSomething",
            CONF_ENTITY_ID: ["light.kitchen", "light.living_room"],
        }
        assert end_position == 1

        assert (await run_automation(file_path, [], [])) == [
            {"light.target_group": "doSomething"}
        ]

        assert real_pos == 0

        # Test case 3: Call service action for two entities, entities in a specific area and a device
        action_part_call_service_3 = {
            CONF_SERVICE: "light.doSomething",
            CONF_TARGET: {
                CONF_ENTITY_ID: ["light.kitchen", "light.living_room"],
                ATTR_AREA_ID: "area.living_room",
                CONF_DEVICE_ID: "device_id_1",
            },
        }
        file_path = init_automation_script("action_part_call_service_3", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_call_service_3,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        close_action_section(file_path)

        entities_call_service_3, end_position, real_pos = results
        assert len(entities_call_service_3) == 1
        assert entities_call_service_3[0].parent is None
        assert entities_call_service_3[0].position == 1
        assert entities_call_service_3[0].parameter_role == OUTPUT
        assert entities_call_service_3[0].integration == "light"
        assert entities_call_service_3[0].entity_name == "light.target_group"
        assert entities_call_service_3[0].expected_value == {
            CONF_SERVICE: "doSomething",
            CONF_ENTITY_ID: ["light.kitchen", "light.living_room"],
            ATTR_AREA_ID: "area.living_room",
            CONF_DEVICE_ID: "device_id_1",
        }
        assert end_position == 1

        assert (await run_automation(file_path, [], [])) == [
            {"light.target_group": "doSomething"}
        ]

        assert real_pos == 0

        # Test case 4: Call service action for one entity with data instead of target
        action_part_call_service_4 = {
            CONF_SERVICE: "light.doSomething",
            CONF_SERVICE_DATA: {"entity_id": "light.kitchen"},
        }
        file_path = init_automation_script("action_part_call_service_4", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_call_service_4,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        close_action_section(file_path)

        entities_call_service_4, end_position, real_pos = results
        assert len(entities_call_service_4) == 1
        assert entities_call_service_4[0].parent is None
        assert entities_call_service_4[0].position == 1
        assert entities_call_service_4[0].parameter_role == OUTPUT
        assert entities_call_service_4[0].integration == "light"
        assert entities_call_service_4[0].entity_name is not None
        assert entities_call_service_4[0].expected_value == {
            CONF_SERVICE: "doSomething",
            "entity_id": "light.kitchen",
        }
        assert end_position == 1

        result: dict = (await run_automation(file_path, [], []))[0]
        assert result.keys() is not None
        assert result.values() is not None

        assert real_pos == 0

        # Test case 5: Call service action for one entity with entity_id and at a specific position
        action_part_call_service_5 = {
            CONF_SERVICE: "light.doSomething",
            CONF_ENTITY_ID: "light.kitchen",
        }
        file_path = init_automation_script("action_part_call_service_5", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_call_service_5,
            position=20,
            parent=10,
            real_position=0,
            script_path=file_path,
        )
        close_action_section(file_path)

        entities_call_service_5, end_position, real_pos = results
        assert len(entities_call_service_5) == 1
        assert entities_call_service_5[0].parent == 10
        assert entities_call_service_5[0].position == 20
        assert entities_call_service_5[0].parameter_role == OUTPUT
        assert entities_call_service_5[0].integration == "light"
        assert entities_call_service_5[0].entity_name == "light.kitchen"
        assert end_position == 20

        assert (await run_automation(file_path, [], [])) == [
            {"light.kitchen": "doSomething"}
        ]

        assert real_pos == 0

        # Test case 6: Call service action for no entity
        action_part_call_service_6 = {
            CONF_SERVICE: "light.doSomething",
            CONF_ENTITY_ID: [],
        }
        file_path = init_automation_script("action_part_call_service_6", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_call_service_6,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        close_action_section(file_path)

        entities_call_service_6, end_position, real_pos = results
        assert len(entities_call_service_6) == 1
        assert entities_call_service_6[0].parent is None
        assert entities_call_service_6[0].position == 1
        assert entities_call_service_6[0].parameter_role == OUTPUT
        assert entities_call_service_6[0].integration == "light"
        assert entities_call_service_6[0].entity_name is not None
        assert entities_call_service_6[0].expected_value == {
            CONF_SERVICE: "doSomething"
        }
        assert end_position == 1

        result = (await run_automation(file_path, [], []))[0]
        assert result.keys() is not None
        assert result.values() is not None

        assert real_pos == 0

    async def test_action_branching():
        # Test case 1: Test branching action based on one condition
        action_part_if_1 = {
            SCRIPT_ACTION_IF: [
                {
                    CONF_CONDITION: "state",
                    CONF_ENTITY_ID: "sensor.temperature",
                    CONF_STATE: "on",
                }
            ],
            CONF_THEN: [
                {
                    CONF_SERVICE: "light.turn_on",
                    CONF_TARGET: {CONF_ENTITY_ID: "light.kitchen"},
                }
            ],
        }
        file_path = init_automation_script("action_part_if_1", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_if_1, position=1, real_position=0, script_path=file_path
        )
        close_action_section(file_path)

        entities_if_1, end_position, real_pos = results
        assert len(entities_if_1) == 2
        assert entities_if_1[0].parent is None
        assert entities_if_1[0].position == 1
        assert entities_if_1[0].parameter_role == ACTION_INPUT
        assert entities_if_1[0].integration == "sensor"
        assert entities_if_1[0].entity_name == "sensor.temperature"
        assert entities_if_1[0].expected_value == {"state": "on"}
        assert entities_if_1[1].parent is None
        assert entities_if_1[1].position == 2
        assert entities_if_1[1].parameter_role == OUTPUT
        assert entities_if_1[1].integration == "light"
        assert entities_if_1[1].entity_name == "light.kitchen"
        assert entities_if_1[1].expected_value == {CONF_SERVICE: "turn_on"}
        assert end_position == 2

        action_part_if_1_input = ["on"]
        assert (await run_automation(file_path, [], [], action_part_if_1_input)) == [
            {"light.kitchen": "turn_on"}
        ]

        action_part_if_1_input = ["off"]
        assert (await run_automation(file_path, [], [], action_part_if_1_input)) == []

        action_part_if_1_input = [None]
        assert (await run_automation(file_path, [], [], action_part_if_1_input)) == {
            "ValueError": "Action input values cannot be None"
        }

        assert real_pos == 1

        # Test case 2: Test branching action based on one condition but with an else
        action_part_if_2 = {
            SCRIPT_ACTION_IF: [
                {
                    CONF_CONDITION: "state",
                    CONF_ENTITY_ID: "sensor.temperature",
                    CONF_STATE: "on",
                }
            ],
            CONF_THEN: [
                {
                    CONF_SERVICE: "light.turn_on",
                    CONF_TARGET: {CONF_ENTITY_ID: "light.kitchen"},
                }
            ],
            CONF_ELSE: [
                {
                    CONF_SERVICE: "light.turn_off",
                    CONF_TARGET: {CONF_ENTITY_ID: "light.kitchen"},
                }
            ],
        }
        file_path = init_automation_script("action_part_if_2", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_if_2, position=1, real_position=0, script_path=file_path
        )
        close_action_section(file_path)

        entities_if_2, end_position, real_pos = results
        assert len(entities_if_2) == 3
        assert entities_if_2[0].parent is None
        assert entities_if_2[0].position == 1
        assert entities_if_2[0].parameter_role == ACTION_INPUT
        assert entities_if_2[0].integration == "sensor"
        assert entities_if_2[0].entity_name == "sensor.temperature"
        assert entities_if_2[0].expected_value == {"state": "on"}
        assert entities_if_2[1].parent is None
        assert entities_if_2[1].position == 2
        assert entities_if_2[1].parameter_role == OUTPUT
        assert entities_if_2[1].integration == "light"
        assert entities_if_2[1].entity_name == "light.kitchen"
        assert entities_if_2[1].expected_value == {CONF_SERVICE: "turn_on"}
        assert entities_if_2[2].parent is None
        assert entities_if_2[2].position == 3
        assert entities_if_2[2].parameter_role == OUTPUT
        assert entities_if_2[2].integration == "light"
        assert entities_if_2[2].entity_name == "light.kitchen"
        assert entities_if_2[2].expected_value == {CONF_SERVICE: "turn_off"}
        assert end_position == 3

        action_part_if_2_input = ["on"]
        assert (await run_automation(file_path, [], [], action_part_if_2_input)) == [
            {"light.kitchen": "turn_on"}
        ]

        action_part_if_2_input = ["someOtherValueThanOn"]
        assert (await run_automation(file_path, [], [], action_part_if_2_input)) == [
            {"light.kitchen": "turn_off"}
        ]

        action_part_if_2_input = [None]
        assert (await run_automation(file_path, [], [], action_part_if_2_input)) == {
            "ValueError": "Action input values cannot be None"
        }

        assert real_pos == 1

        # Test case 3: Test branching action based on one condition but without a then
        action_part_if_3 = {
            SCRIPT_ACTION_IF: [
                {
                    CONF_CONDITION: "state",
                    CONF_ENTITY_ID: "sensor.temperature",
                    CONF_STATE: "on",
                }
            ],
            CONF_ELSE: [
                {
                    CONF_SERVICE: "light.turn_off",
                    CONF_TARGET: {CONF_ENTITY_ID: "light.kitchen"},
                }
            ],
        }
        file_path = init_automation_script("action_part_if_3", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_if_3, position=1, real_position=0, script_path=file_path
        )
        close_action_section(file_path)

        entities_if_3, end_position, real_pos = results
        assert len(entities_if_3) == 2
        assert entities_if_3[0].parent is None
        assert entities_if_3[0].position == 1
        assert entities_if_3[0].parameter_role == ACTION_INPUT
        assert entities_if_3[0].integration == "sensor"
        assert entities_if_3[0].entity_name == "sensor.temperature"
        assert entities_if_3[0].expected_value == {"state": "on"}
        assert entities_if_3[1].parent is None
        assert entities_if_3[1].position == 2
        assert entities_if_3[1].parameter_role == OUTPUT
        assert entities_if_3[1].integration == "light"
        assert entities_if_3[1].entity_name == "light.kitchen"
        assert entities_if_3[1].expected_value == {CONF_SERVICE: "turn_off"}
        assert end_position == 2

        action_part_if_3_input = ["on"]
        assert (await run_automation(file_path, [], [], action_part_if_3_input)) == []

        action_part_if_3_input = ["someOtherValueThanOn"]
        assert (await run_automation(file_path, [], [], action_part_if_3_input)) == [
            {"light.kitchen": "turn_off"}
        ]

        action_part_if_3_input = [None]
        assert (await run_automation(file_path, [], [], action_part_if_3_input)) == {
            "ValueError": "Action input values cannot be None"
        }

        assert real_pos == 1

        # Test case 4: Test branching action with two conditions
        action_part_if_4 = {
            SCRIPT_ACTION_IF: [
                {
                    CONF_CONDITION: "state",
                    CONF_ENTITY_ID: "sensor.temperature",
                    CONF_STATE: "on",
                },
                {
                    CONF_CONDITION: "state",
                    CONF_ENTITY_ID: "sensor.humidity",
                    CONF_STATE: "off",
                },
            ],
            CONF_THEN: [
                {
                    CONF_SERVICE: "light.turn_on",
                    CONF_TARGET: {CONF_ENTITY_ID: "light.kitchen"},
                }
            ],
        }
        file_path = init_automation_script("action_part_if_4", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_if_4, position=1, real_position=0, script_path=file_path
        )
        close_action_section(file_path)

        entities_if_4, end_position, real_pos = results
        assert len(entities_if_4) == 3
        assert entities_if_4[0].parent == 1
        assert entities_if_4[0].position == 2
        assert entities_if_4[0].parameter_role == ACTION_INPUT
        assert entities_if_4[0].integration == "sensor"
        assert entities_if_4[0].entity_name == "sensor.temperature"
        assert entities_if_4[0].expected_value == {"state": "on"}
        assert entities_if_4[1].parent == 1
        assert entities_if_4[1].position == 3
        assert entities_if_4[1].parameter_role == ACTION_INPUT
        assert entities_if_4[1].integration == "sensor"
        assert entities_if_4[1].entity_name == "sensor.humidity"
        assert entities_if_4[1].expected_value == {"state": "off"}
        assert entities_if_4[2].parent is None
        assert entities_if_4[2].position == 4
        assert entities_if_4[2].parameter_role == OUTPUT
        assert entities_if_4[2].integration == "light"
        assert entities_if_4[2].entity_name == "light.kitchen"
        assert entities_if_4[2].expected_value == {CONF_SERVICE: "turn_on"}
        assert end_position == 4

        action_part_if_4_input = ["on", "off"]
        assert (await run_automation(file_path, [], [], action_part_if_4_input)) == [
            {"light.kitchen": "turn_on"}
        ]

        action_part_if_4_input = ["off", "off"]
        assert (await run_automation(file_path, [], [], action_part_if_4_input)) == []

        action_part_if_4_input = [None, None]
        assert (await run_automation(file_path, [], [], action_part_if_4_input)) == {
            "ValueError": "Action input values cannot be None"
        }

        assert real_pos == 2

        # Test case 11: Test branching action with two conditions, a then, else and at a specific position
        action_part_if_5 = {
            SCRIPT_ACTION_IF: [
                {
                    CONF_CONDITION: "state",
                    CONF_ENTITY_ID: "sensor.temperature",
                    CONF_STATE: "on",
                },
                {
                    CONF_CONDITION: "state",
                    CONF_ENTITY_ID: "sensor.humidity",
                    CONF_STATE: "off",
                },
            ],
            CONF_THEN: [
                {
                    CONF_SERVICE: "light.turn_on",
                    CONF_TARGET: {CONF_ENTITY_ID: "light.kitchen"},
                },
                {
                    CONF_SERVICE: "light.turn_on",
                    CONF_TARGET: {
                        CONF_ENTITY_ID: ["light.hallway", "light.living_room"],
                    },
                },
            ],
            CONF_ELSE: [
                {
                    CONF_SERVICE: "light.turn_off",
                    CONF_TARGET: {ATTR_AREA_ID: "living_room"},
                }
            ],
        }
        file_path = init_automation_script("action_part_if_5", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_if_5, position=27, real_position=4, script_path=file_path
        )
        close_action_section(file_path)

        entities_if_5, end_position, real_pos = results
        assert len(entities_if_5) == 5
        assert entities_if_5[0].parent == 27
        assert entities_if_5[0].position == 28
        assert entities_if_5[0].parameter_role == ACTION_INPUT
        assert entities_if_5[0].integration == "sensor"
        assert entities_if_5[0].entity_name == "sensor.temperature"
        assert entities_if_5[0].expected_value == {"state": "on"}
        assert entities_if_5[1].parent == 27
        assert entities_if_5[1].position == 29
        assert entities_if_5[1].parameter_role == ACTION_INPUT
        assert entities_if_5[1].integration == "sensor"
        assert entities_if_5[1].entity_name == "sensor.humidity"
        assert entities_if_5[1].expected_value == {"state": "off"}
        assert entities_if_5[2].parent == 30
        assert entities_if_5[2].position == 31
        assert entities_if_5[2].parameter_role == OUTPUT
        assert entities_if_5[2].integration == "light"
        assert entities_if_5[2].entity_name == "light.kitchen"
        assert entities_if_5[2].expected_value == {CONF_SERVICE: "turn_on"}
        assert entities_if_5[3].parent == 30
        assert entities_if_5[3].position == 32
        assert entities_if_5[3].parameter_role == OUTPUT
        assert entities_if_5[3].integration == "light"
        assert entities_if_5[3].entity_name == "light.target_group"
        assert entities_if_5[3].expected_value == {
            CONF_SERVICE: "turn_on",
            CONF_ENTITY_ID: ["light.hallway", "light.living_room"],
        }
        assert entities_if_5[4].parent is None
        assert entities_if_5[4].position == 33
        assert entities_if_5[4].parameter_role == OUTPUT
        assert entities_if_5[4].integration == "light"
        assert entities_if_5[4].entity_name == "light.target_group"
        assert entities_if_5[4].expected_value == {
            CONF_SERVICE: "turn_off",
            ATTR_AREA_ID: "living_room",
        }
        assert end_position == 33

        action_part_if_5_input = ["filler", "filler", "filler", "filler", "on", "off"]
        assert (await run_automation(file_path, [], [], action_part_if_5_input)) == [
            {"light.kitchen": "turn_on"},
            {"light.target_group": "turn_on"},
        ]

        action_part_if_5_input = ["filler", "filler", "filler", "filler", "off", "off"]
        assert (await run_automation(file_path, [], [], action_part_if_5_input)) == [
            {"light.target_group": "turn_off"}
        ]

        action_part_if_5_input = ["filler", "filler", "filler", "filler", None, None]
        assert (await run_automation(file_path, [], [], action_part_if_5_input)) == {
            "ValueError": "Action input values cannot be None"
        }
        assert real_pos == 6

        # Test case 6: Test branching action based on one condition but without a then
        action_part_if_6 = {
            SCRIPT_ACTION_IF: [],
            CONF_ELSE: [
                {
                    CONF_SERVICE: "light.turn_off",
                    CONF_TARGET: {CONF_ENTITY_ID: "light.kitchen"},
                }
            ],
        }
        file_path = init_automation_script("action_part_if_6", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_if_6, position=1, real_position=0, script_path=file_path
        )
        close_action_section(file_path)

        entities_if_6, end_position, real_pos = results
        assert len(entities_if_6) == 1
        assert entities_if_6[0].parent is None
        assert entities_if_6[0].position == 1
        assert entities_if_6[0].parameter_role == OUTPUT
        assert entities_if_6[0].integration == "light"
        assert entities_if_6[0].entity_name == "light.kitchen"
        assert entities_if_6[0].expected_value == {CONF_SERVICE: "turn_off"}
        assert end_position == 1

        assert (await run_automation(file_path, [], [])) == [
            {"light.kitchen": "turn_off"}
        ]

        assert real_pos == 0

    async def test_action_choose():
        # Test case 1: Test branching action with one option
        action_part_choose_1 = {
            CONF_CHOOSE: [
                {
                    CONF_CONDITION: "state",
                    CONF_ENTITY_ID: "sensor.temperature",
                    CONF_STATE: "on",
                    CONF_SEQUENCE: [
                        {
                            CONF_SERVICE: "light.turn_on",
                            CONF_TARGET: {CONF_ENTITY_ID: "light.kitchen"},
                        },
                        {
                            CONF_SERVICE: "light.turn_off",
                            CONF_TARGET: {CONF_ENTITY_ID: "light.living_room"},
                        },
                    ],
                },
            ],
        }
        file_path = init_automation_script("action_part_choose_1", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_choose_1, position=1, real_position=0, script_path=file_path
        )
        close_action_section(file_path)

        entities_choose_1, end_position, real_pos = results
        assert len(entities_choose_1) == 3
        assert entities_choose_1[0].parent == 1
        assert entities_choose_1[0].position == 2
        assert entities_choose_1[0].parameter_role == ACTION_INPUT
        assert entities_choose_1[0].integration == "sensor"
        assert entities_choose_1[0].entity_name == "sensor.temperature"
        assert entities_choose_1[0].expected_value == {"state": "on"}
        assert entities_choose_1[1].parent == 3
        assert entities_choose_1[1].position == 4
        assert entities_choose_1[1].parameter_role == OUTPUT
        assert entities_choose_1[1].integration == "light"
        assert entities_choose_1[1].entity_name == "light.kitchen"
        assert entities_choose_1[1].expected_value == {CONF_SERVICE: "turn_on"}
        assert entities_choose_1[2].parent == 3
        assert entities_choose_1[2].position == 5
        assert entities_choose_1[2].parameter_role == OUTPUT
        assert entities_choose_1[2].integration == "light"
        assert entities_choose_1[2].entity_name == "light.living_room"
        assert entities_choose_1[2].expected_value == {CONF_SERVICE: "turn_off"}
        assert end_position == 5

        action_part_choose_1_input = ["on"]
        assert (
            await run_automation(file_path, [], [], action_part_choose_1_input)
        ) == [
            {"light.kitchen": "turn_on"},
            {"light.living_room": "turn_off"},
        ]

        action_part_choose_1_input = ["off"]
        assert (
            await run_automation(file_path, [], [], action_part_choose_1_input)
        ) == []

        action_part_choose_1_input = [None]
        assert (
            await run_automation(file_path, [], [], action_part_choose_1_input)
        ) == {"ValueError": "Action input values cannot be None"}

        assert real_pos == 1

        # Test case 2: Test branching action with one option with two conditions
        action_part_choose_2 = {
            CONF_CHOOSE: [
                {
                    CONF_CONDITIONS: [
                        {
                            CONF_CONDITION: "state",
                            CONF_ENTITY_ID: "sensor.temperature",
                            CONF_STATE: "on",
                        },
                        {
                            CONF_CONDITION: "state",
                            CONF_ENTITY_ID: "sensor.humidity",
                            CONF_STATE: "off",
                        },
                    ],
                    CONF_SEQUENCE: [
                        {
                            CONF_SERVICE: "light.turn_on",
                            CONF_TARGET: {CONF_ENTITY_ID: "light.kitchen"},
                        },
                        {
                            CONF_SERVICE: "light.turn_off",
                            CONF_TARGET: {CONF_ENTITY_ID: "light.living_room"},
                        },
                    ],
                },
            ],
        }
        file_path = init_automation_script("action_part_choose_2", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_choose_2, position=1, real_position=0, script_path=file_path
        )
        close_action_section(file_path)

        entities_choose_2, end_position, real_pos = results
        assert len(entities_choose_2) == 4
        assert entities_choose_2[0].parent == 2
        assert entities_choose_2[0].position == 3
        assert entities_choose_2[0].parameter_role == ACTION_INPUT
        assert entities_choose_2[0].integration == "sensor"
        assert entities_choose_2[0].entity_name == "sensor.temperature"
        assert entities_choose_2[0].expected_value == {"state": "on"}
        assert entities_choose_2[1].parent == 2
        assert entities_choose_2[1].position == 4
        assert entities_choose_2[1].parameter_role == ACTION_INPUT
        assert entities_choose_2[1].integration == "sensor"
        assert entities_choose_2[1].entity_name == "sensor.humidity"
        assert entities_choose_2[1].expected_value == {"state": "off"}
        assert entities_choose_2[2].parent == 5
        assert entities_choose_2[2].position == 6
        assert entities_choose_2[2].parameter_role == OUTPUT
        assert entities_choose_2[2].integration == "light"
        assert entities_choose_2[2].entity_name == "light.kitchen"
        assert entities_choose_2[2].expected_value == {CONF_SERVICE: "turn_on"}
        assert entities_choose_2[3].parent == 5
        assert entities_choose_2[3].position == 7
        assert entities_choose_2[3].parameter_role == OUTPUT
        assert entities_choose_2[3].integration == "light"
        assert entities_choose_2[3].entity_name == "light.living_room"
        assert entities_choose_2[3].expected_value == {CONF_SERVICE: "turn_off"}
        assert end_position == 7

        action_part_choose_2_input = ["on", "off"]
        assert (
            await run_automation(file_path, [], [], action_part_choose_2_input)
        ) == [
            {"light.kitchen": "turn_on"},
            {"light.living_room": "turn_off"},
        ]

        action_part_choose_2_input = ["off", "off"]
        assert (
            await run_automation(file_path, [], [], action_part_choose_2_input)
        ) == []

        action_part_choose_2_input = [None, None]
        assert (
            await run_automation(file_path, [], [], action_part_choose_2_input)
        ) == {"ValueError": "Action input values cannot be None"}

        assert real_pos == 2

        # Test case 3: Test branching action with two options
        action_part_choose_3 = {
            CONF_CHOOSE: [
                {
                    CONF_CONDITIONS: [
                        {
                            CONF_CONDITION: "state",
                            CONF_ENTITY_ID: "sensor.temperature",
                            CONF_STATE: "on",
                        },
                        {
                            CONF_CONDITION: "state",
                            CONF_ENTITY_ID: "sensor.humidity",
                            CONF_STATE: "off",
                        },
                    ],
                    CONF_SEQUENCE: [
                        {
                            CONF_SERVICE: "light.turn_on",
                            CONF_TARGET: {CONF_ENTITY_ID: "light.kitchen"},
                        },
                        {
                            CONF_SERVICE: "light.turn_off",
                            CONF_TARGET: {CONF_ENTITY_ID: "light.living_room"},
                        },
                    ],
                },
                {
                    CONF_CONDITIONS: [
                        {
                            CONF_CONDITION: "state",
                            CONF_ENTITY_ID: "sensor.temperature",
                            CONF_STATE: "off",
                        },
                        {
                            CONF_CONDITION: "state",
                            CONF_ENTITY_ID: "sensor.humidity",
                            CONF_STATE: "on",
                        },
                    ],
                    CONF_SEQUENCE: [
                        {
                            CONF_SERVICE: "light.turn_off",
                            CONF_TARGET: {CONF_ENTITY_ID: "light.kitchen"},
                        },
                        {
                            CONF_SERVICE: "light.turn_on",
                            CONF_TARGET: {CONF_ENTITY_ID: "light.living_room"},
                        },
                    ],
                },
            ],
        }
        file_path = init_automation_script("action_part_choose_3", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_choose_3, position=1, real_position=0, script_path=file_path
        )
        close_action_section(file_path)

        entities_choose_3, end_position, real_pos = results
        assert len(entities_choose_3) == 8
        assert entities_choose_3[0].parent == 2
        assert entities_choose_3[0].position == 3
        assert entities_choose_3[0].parameter_role == ACTION_INPUT
        assert entities_choose_3[0].integration == "sensor"
        assert entities_choose_3[0].entity_name == "sensor.temperature"
        assert entities_choose_3[0].expected_value == {"state": "on"}
        assert entities_choose_3[1].parent == 2
        assert entities_choose_3[1].position == 4
        assert entities_choose_3[1].parameter_role == ACTION_INPUT
        assert entities_choose_3[1].integration == "sensor"
        assert entities_choose_3[1].entity_name == "sensor.humidity"
        assert entities_choose_3[1].expected_value == {"state": "off"}
        assert entities_choose_3[2].parent == 5
        assert entities_choose_3[2].position == 6
        assert entities_choose_3[2].parameter_role == OUTPUT
        assert entities_choose_3[2].integration == "light"
        assert entities_choose_3[2].entity_name == "light.kitchen"
        assert entities_choose_3[2].expected_value == {CONF_SERVICE: "turn_on"}
        assert entities_choose_3[3].parent == 5
        assert entities_choose_3[3].position == 7
        assert entities_choose_3[3].parameter_role == OUTPUT
        assert entities_choose_3[3].integration == "light"
        assert entities_choose_3[3].entity_name == "light.living_room"
        assert entities_choose_3[3].expected_value == {CONF_SERVICE: "turn_off"}
        assert entities_choose_3[4].parent == 8
        assert entities_choose_3[4].position == 9
        assert entities_choose_3[4].parameter_role == ACTION_INPUT
        assert entities_choose_3[4].integration == "sensor"
        assert entities_choose_3[4].entity_name == "sensor.temperature"
        assert entities_choose_3[4].expected_value == {"state": "off"}
        assert entities_choose_3[5].parent == 8
        assert entities_choose_3[5].position == 10
        assert entities_choose_3[5].parameter_role == ACTION_INPUT
        assert entities_choose_3[5].integration == "sensor"
        assert entities_choose_3[5].entity_name == "sensor.humidity"
        assert entities_choose_3[5].expected_value == {"state": "on"}
        assert entities_choose_3[6].parent == 11
        assert entities_choose_3[6].position == 12
        assert entities_choose_3[6].parameter_role == OUTPUT
        assert entities_choose_3[6].integration == "light"
        assert entities_choose_3[6].entity_name == "light.kitchen"
        assert entities_choose_3[6].expected_value == {CONF_SERVICE: "turn_off"}
        assert entities_choose_3[7].parent == 11
        assert entities_choose_3[7].position == 13
        assert entities_choose_3[7].parameter_role == OUTPUT
        assert entities_choose_3[7].integration == "light"
        assert entities_choose_3[7].entity_name == "light.living_room"
        assert entities_choose_3[7].expected_value == {CONF_SERVICE: "turn_on"}
        assert end_position == 13

        # both conditions pairs are met so only the first sequence is executed
        action_part_choose_3_input = ["on", "off", "off", "on"]
        assert (
            await run_automation(file_path, [], [], action_part_choose_3_input)
        ) == [
            {"light.kitchen": "turn_on"},
            {"light.living_room": "turn_off"},
        ]

        # only the second condition pair is met so the second sequence is executed
        action_part_choose_3_input = ["off", "on", "off", "on"]
        assert (
            await run_automation(file_path, [], [], action_part_choose_3_input)
        ) == [
            {"light.kitchen": "turn_off"},
            {"light.living_room": "turn_on"},
        ]

        # no condition pair is met so no sequence is executed
        action_part_choose_3_input = ["off", "off", "on", "on"]
        assert (
            await run_automation(file_path, [], [], action_part_choose_3_input)
        ) == []

        action_part_choose_3_input = [None, None, None, None]
        assert (
            await run_automation(file_path, [], [], action_part_choose_3_input)
        ) == {"ValueError": "Action input values cannot be None"}

        assert real_pos == 4

        # Test case 4: Test branching action with two options and a default
        action_part_choose_4 = {
            CONF_CHOOSE: [
                {
                    CONF_CONDITION: "state",
                    CONF_ENTITY_ID: "sensor.temperature",
                    CONF_STATE: "on",
                    CONF_SEQUENCE: [
                        {
                            CONF_SERVICE: "light.turn_on",
                            CONF_TARGET: {CONF_ENTITY_ID: "light.kitchen"},
                        }
                    ],
                },
                {
                    CONF_CONDITION: "state",
                    CONF_ENTITY_ID: "sensor.temperature",
                    CONF_STATE: "off",
                    CONF_SEQUENCE: [
                        {
                            CONF_SERVICE: "light.turn_off",
                            CONF_TARGET: {CONF_ENTITY_ID: "light.kitchen"},
                        }
                    ],
                },
            ],
            CONF_DEFAULT: [
                {
                    CONF_SERVICE: "light.toggle",
                    CONF_TARGET: {CONF_ENTITY_ID: "light.living_room"},
                }
            ],
        }

        file_path = init_automation_script("action_part_choose_4", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_choose_4, position=1, real_position=0, script_path=file_path
        )
        close_action_section(file_path)

        entities_choose_4, end_position, real_pos = results
        assert len(entities_choose_4) == 5
        assert entities_choose_4[0].parent == 1
        assert entities_choose_4[0].position == 2
        assert entities_choose_4[0].parameter_role == ACTION_INPUT
        assert entities_choose_4[0].integration == "sensor"
        assert entities_choose_4[0].entity_name == "sensor.temperature"
        assert entities_choose_4[0].expected_value == {"state": "on"}
        assert entities_choose_4[1].parent == 1
        assert entities_choose_4[1].position == 3
        assert entities_choose_4[1].parameter_role == OUTPUT
        assert entities_choose_4[1].integration == "light"
        assert entities_choose_4[1].entity_name == "light.kitchen"
        assert entities_choose_4[1].expected_value == {CONF_SERVICE: "turn_on"}
        assert entities_choose_4[2].parent == 1
        assert entities_choose_4[2].position == 4
        assert entities_choose_4[2].parameter_role == ACTION_INPUT
        assert entities_choose_4[2].integration == "sensor"
        assert entities_choose_4[2].entity_name == "sensor.temperature"
        assert entities_choose_4[2].expected_value == {"state": "off"}
        assert entities_choose_4[3].parent == 1
        assert entities_choose_4[3].position == 5
        assert entities_choose_4[3].parameter_role == OUTPUT
        assert entities_choose_4[3].integration == "light"
        assert entities_choose_4[3].entity_name == "light.kitchen"
        assert entities_choose_4[3].expected_value == {CONF_SERVICE: "turn_off"}
        assert entities_choose_4[4].parent == 1
        assert entities_choose_4[4].position == 6
        assert entities_choose_4[4].parameter_role == OUTPUT
        assert entities_choose_4[4].integration == "light"
        assert entities_choose_4[4].entity_name == "light.living_room"
        assert entities_choose_4[4].expected_value == {CONF_SERVICE: "toggle"}
        assert end_position == 6

        # both conditions are met so only the first sequence is executed
        action_part_choose_4_input = ["on", "off"]
        assert (
            await run_automation(file_path, [], [], action_part_choose_4_input)
        ) == [{"light.kitchen": "turn_on"}]

        # only the second condition is met so the second sequence is executed
        action_part_choose_4_input = ["off", "off"]
        assert (
            await run_automation(file_path, [], [], action_part_choose_4_input)
        ) == [{"light.kitchen": "turn_off"}]

        # no condition is met so the default sequence is executed
        action_part_choose_4_input = ["off", "on"]
        assert (
            await run_automation(file_path, [], [], action_part_choose_4_input)
        ) == [{"light.living_room": "toggle"}]

        action_part_choose_4_input = [None, None]
        assert (
            await run_automation(file_path, [], [], action_part_choose_4_input)
        ) == {"ValueError": "Action input values cannot be None"}

        assert real_pos == 2

        # Test case 6: Test branching action with two options and a default at a specific position
        action_part_choose_6 = {
            CONF_CHOOSE: [
                {
                    CONF_CONDITION: "state",
                    CONF_ENTITY_ID: "sensor.temperature",
                    CONF_STATE: "on",
                    CONF_SEQUENCE: [
                        {
                            CONF_SERVICE: "light.turn_on",
                            CONF_TARGET: {CONF_ENTITY_ID: "light.kitchen"},
                        }
                    ],
                },
                {
                    CONF_CONDITION: "state",
                    CONF_ENTITY_ID: "sensor.temperature",
                    CONF_STATE: "off",
                    CONF_SEQUENCE: [
                        {
                            CONF_SERVICE: "light.turn_off",
                            CONF_TARGET: {CONF_ENTITY_ID: "light.kitchen"},
                        }
                    ],
                },
            ],
        }
        file_path = init_automation_script("action_part_choose_6", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_choose_6, position=18, real_position=2, script_path=file_path
        )
        close_action_section(file_path)

        entities_choose_6, end_position, real_pos = results
        assert len(entities_choose_6) == 4
        assert entities_choose_6[0].parent == 18
        assert entities_choose_6[0].position == 19
        assert entities_choose_6[0].parameter_role == ACTION_INPUT
        assert entities_choose_6[0].integration == "sensor"
        assert entities_choose_6[0].entity_name == "sensor.temperature"
        assert entities_choose_6[0].expected_value == {"state": "on"}
        assert entities_choose_6[1].parent == 18
        assert entities_choose_6[1].position == 20
        assert entities_choose_6[1].parameter_role == OUTPUT
        assert entities_choose_6[1].integration == "light"
        assert entities_choose_6[1].entity_name == "light.kitchen"
        assert entities_choose_6[1].expected_value == {CONF_SERVICE: "turn_on"}
        assert entities_choose_6[2].parent == 18
        assert entities_choose_6[2].position == 21
        assert entities_choose_6[2].parameter_role == ACTION_INPUT
        assert entities_choose_6[2].integration == "sensor"
        assert entities_choose_6[2].entity_name == "sensor.temperature"
        assert entities_choose_6[2].expected_value == {"state": "off"}
        assert entities_choose_6[3].parent == 18
        assert entities_choose_6[3].position == 22
        assert entities_choose_6[3].parameter_role == OUTPUT
        assert entities_choose_6[3].integration == "light"
        assert entities_choose_6[3].entity_name == "light.kitchen"
        assert entities_choose_6[3].expected_value == {CONF_SERVICE: "turn_off"}
        assert end_position == 22

        # both conditions are met so only the first sequence is executed
        action_part_choose_6_input = ["filler", "filler", "on", "off"]
        assert (
            await run_automation(file_path, [], [], action_part_choose_6_input)
        ) == [{"light.kitchen": "turn_on"}]

        # only the second condition is met so the second sequence is executed
        action_part_choose_6_input = ["filler", "filler", "off", "off"]
        assert (
            await run_automation(file_path, [], [], action_part_choose_6_input)
        ) == [{"light.kitchen": "turn_off"}]

        action_part_choose_6_input = ["filler", "filler", None, None]
        assert (
            await run_automation(file_path, [], [], action_part_choose_6_input)
        ) == {"ValueError": "Action input values cannot be None"}

        assert real_pos == 4

    async def test_action_parallel():
        # Test case 1: parallel action with two actions
        action_part_parallel_1 = {
            CONF_PARALLEL: [
                {
                    CONF_SERVICE: "light.turn_on",
                    CONF_TARGET: {CONF_ENTITY_ID: "light.kitchen"},
                },
                {
                    CONF_SERVICE: "light.turn_on",
                    CONF_TARGET: {CONF_ENTITY_ID: "light.living_room"},
                },
            ],
        }
        file_path = init_automation_script("action_part_parallel_1", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_parallel_1, position=1, real_position=0, script_path=file_path
        )
        close_action_section(file_path)

        entities_parallel_1, end_position, real_pos = results
        assert len(entities_parallel_1) == 2
        assert entities_parallel_1[0].parent == 1
        assert entities_parallel_1[0].position == 2
        assert entities_parallel_1[0].parameter_role == OUTPUT
        assert entities_parallel_1[0].integration == "light"
        assert entities_parallel_1[0].entity_name == "light.kitchen"
        assert entities_parallel_1[0].expected_value == {CONF_SERVICE: "turn_on"}
        assert entities_parallel_1[1].parent == 1
        assert entities_parallel_1[1].position == 3
        assert entities_parallel_1[1].parameter_role == OUTPUT
        assert entities_parallel_1[1].integration == "light"
        assert entities_parallel_1[1].entity_name == "light.living_room"
        assert entities_parallel_1[1].expected_value == {CONF_SERVICE: "turn_on"}
        assert end_position == 3

        assert (await run_automation(file_path, [], [])) == [
            {"light.kitchen": "turn_on"},
            {"light.living_room": "turn_on"},
        ]
        assert real_pos == 0

        # Test case 2: parallel action with two actions and a specific position
        action_part_parallel_2 = {
            CONF_PARALLEL: [
                {
                    CONF_SERVICE: "light.turn_on",
                    CONF_TARGET: {CONF_ENTITY_ID: "light.kitchen"},
                },
                {
                    CONF_SERVICE: "light.turn_on",
                    CONF_TARGET: {CONF_ENTITY_ID: "light.living_room"},
                },
            ],
        }
        file_path = init_automation_script("action_part_parallel_2", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_parallel_2, position=20, real_position=5, script_path=file_path
        )
        close_action_section(file_path)

        entities_parallel_2, end_position, real_pos = results
        assert len(entities_parallel_2) == 2
        assert entities_parallel_2[0].parent == 20
        assert entities_parallel_2[0].position == 21
        assert entities_parallel_2[0].parameter_role == OUTPUT
        assert entities_parallel_2[0].integration == "light"
        assert entities_parallel_2[0].entity_name == "light.kitchen"
        assert entities_parallel_2[0].expected_value == {CONF_SERVICE: "turn_on"}
        assert entities_parallel_2[1].parent == 20
        assert entities_parallel_2[1].position == 22
        assert entities_parallel_2[1].parameter_role == OUTPUT
        assert entities_parallel_2[1].integration == "light"
        assert entities_parallel_2[1].entity_name == "light.living_room"
        assert entities_parallel_2[1].expected_value == {CONF_SERVICE: "turn_on"}
        assert end_position == 22

        assert (await run_automation(file_path, [], [])) == [
            {"light.kitchen": "turn_on"},
            {"light.living_room": "turn_on"},
        ]
        assert real_pos == 5

    async def test_action_repeat():
        # Test case 1: count repeat action with one action
        action_part_repeat_1 = {
            CONF_REPEAT: {
                CONF_SEQUENCE: [
                    {
                        CONF_SERVICE: "light.turn_on",
                        CONF_TARGET: {CONF_ENTITY_ID: "light.kitchen"},
                    },
                ],
                CONF_COUNT: 3,
            },
        }
        file_path = init_automation_script("action_part_repeat_1", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_repeat_1, position=1, real_position=0, script_path=file_path
        )
        close_action_section(file_path)

        entities_repeat_1, end_position, real_pos = results
        assert len(entities_repeat_1) == 1
        assert entities_repeat_1[0].parent is None
        assert entities_repeat_1[0].position == 1
        assert entities_repeat_1[0].parameter_role == OUTPUT
        assert entities_repeat_1[0].integration == "light"
        assert entities_repeat_1[0].entity_name == "light.kitchen"
        assert entities_repeat_1[0].expected_value == {CONF_SERVICE: "turn_on"}
        assert end_position == 1

        assert (await run_automation(file_path, [], [])) == [
            {"light.kitchen": "turn_on", "count": 3},
        ]
        assert real_pos == 0

        # Test case 2: while repeat action with one condition and one action
        action_part_repeat_2 = {
            CONF_REPEAT: {
                CONF_WHILE: {
                    CONF_CONDITION: "state",
                    CONF_ENTITY_ID: "sensor.temperature",
                    CONF_STATE: "on",
                },
                CONF_SEQUENCE: [
                    {
                        CONF_SERVICE: "light.turn_on",
                        CONF_TARGET: {CONF_ENTITY_ID: "light.kitchen"},
                    },
                ],
            },
        }
        file_path = init_automation_script("action_part_repeat_2", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_repeat_2, position=1, real_position=0, script_path=file_path
        )
        close_action_section(file_path)

        entities_repeat_2, end_position, real_pos = results
        assert len(entities_repeat_2) == 2
        assert entities_repeat_2[0].parent is None
        assert entities_repeat_2[0].position == 1
        assert entities_repeat_2[0].parameter_role == ACTION_INPUT
        assert entities_repeat_2[0].integration == "sensor"
        assert entities_repeat_2[0].entity_name == "sensor.temperature"
        assert entities_repeat_2[0].expected_value == {"state": "on"}
        assert entities_repeat_2[1].parent is None
        assert entities_repeat_2[1].position == 2
        assert entities_repeat_2[1].parameter_role == OUTPUT
        assert entities_repeat_2[1].integration == "light"
        assert entities_repeat_2[1].entity_name == "light.kitchen"
        assert entities_repeat_2[1].expected_value == {CONF_SERVICE: "turn_on"}
        assert end_position == 2

        action_part_repeat_2_input = ["off"]
        assert (
            await run_automation(file_path, [], [], action_part_repeat_2_input)
        ) == []

        action_part_repeat_2_input = ["on"]
        assert (
            await run_automation(file_path, [], [], action_part_repeat_2_input)
        ) == [
            {"light.kitchen": "turn_on", "count": "infinite"},
        ]

        action_part_repeat_2_input = [None]
        assert (
            await run_automation(file_path, [], [], action_part_repeat_2_input)
        ) == {"ValueError": "Action input values cannot be None"}
        assert real_pos == 1

        # Test case 3: until repeat action with one condition and one action
        action_part_repeat_3 = {
            CONF_REPEAT: {
                CONF_UNTIL: [
                    {
                        CONF_CONDITION: "state",
                        CONF_ENTITY_ID: "sensor.temperature",
                        CONF_STATE: "on",
                    }
                ],
                CONF_SEQUENCE: [
                    {
                        CONF_SERVICE: "light.turn_on",
                        CONF_TARGET: {CONF_ENTITY_ID: "light.kitchen"},
                    },
                ],
            },
        }
        file_path = init_automation_script("action_part_repeat_3", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_repeat_3, position=1, real_position=0, script_path=file_path
        )
        close_action_section(file_path)

        entities_repeat_3, end_position, real_pos = results
        assert len(entities_repeat_3) == 2
        assert entities_repeat_3[0].parent is None
        assert entities_repeat_3[0].position == 1
        assert entities_repeat_3[0].parameter_role == ACTION_INPUT
        assert entities_repeat_3[0].integration == "sensor"
        assert entities_repeat_3[0].entity_name == "sensor.temperature"
        assert entities_repeat_3[0].expected_value == {"state": "on"}
        assert entities_repeat_3[1].parent is None
        assert entities_repeat_3[1].position == 2
        assert entities_repeat_3[1].parameter_role == OUTPUT
        assert entities_repeat_3[1].integration == "light"
        assert entities_repeat_3[1].entity_name == "light.kitchen"
        assert entities_repeat_3[1].expected_value == {CONF_SERVICE: "turn_on"}
        assert end_position == 2

        action_part_repeat_3_input = ["off"]
        assert (
            await run_automation(file_path, [], [], action_part_repeat_3_input)
        ) == [
            {"light.kitchen": "turn_on", "count": "infinite"},
        ]

        action_part_repeat_3_input = ["on"]
        assert (
            await run_automation(file_path, [], [], action_part_repeat_3_input)
        ) == [
            {"light.kitchen": "turn_on", "count": 1},
        ]

        action_part_repeat_3_input = [None]
        assert (
            await run_automation(file_path, [], [], action_part_repeat_3_input)
        ) == {"ValueError": "Action input values cannot be None"}

        # Test case 4: until repeat action with two conditions
        action_part_repeat_4 = {
            CONF_REPEAT: {
                CONF_UNTIL: [
                    {
                        CONF_CONDITION: "state",
                        CONF_ENTITY_ID: "sensor.temperature",
                        CONF_STATE: "on",
                    },
                    {
                        CONF_CONDITION: "state",
                        CONF_ENTITY_ID: "sensor.humidity",
                        CONF_STATE: "off",
                    },
                ],
                CONF_SEQUENCE: [
                    {
                        CONF_SERVICE: "light.turn_on",
                        CONF_TARGET: {CONF_ENTITY_ID: "light.kitchen"},
                    },
                ],
            },
        }
        file_path = init_automation_script("action_part_repeat_4", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_repeat_4, position=1, real_position=0, script_path=file_path
        )
        close_action_section(file_path)

        entities_repeat_4, end_position, real_pos = results
        assert len(entities_repeat_4) == 3
        assert entities_repeat_4[0].parent == 1
        assert entities_repeat_4[0].position == 2
        assert entities_repeat_4[0].parameter_role == ACTION_INPUT
        assert entities_repeat_4[0].integration == "sensor"
        assert entities_repeat_4[0].entity_name == "sensor.temperature"
        assert entities_repeat_4[0].expected_value == {"state": "on"}
        assert entities_repeat_4[1].parent == 1
        assert entities_repeat_4[1].position == 3
        assert entities_repeat_4[1].parameter_role == ACTION_INPUT
        assert entities_repeat_4[1].integration == "sensor"
        assert entities_repeat_4[1].entity_name == "sensor.humidity"
        assert entities_repeat_4[1].expected_value == {"state": "off"}
        assert entities_repeat_4[2].parent is None
        assert entities_repeat_4[2].position == 4
        assert entities_repeat_4[2].parameter_role == OUTPUT
        assert entities_repeat_4[2].integration == "light"
        assert entities_repeat_4[2].entity_name == "light.kitchen"
        assert entities_repeat_4[2].expected_value == {CONF_SERVICE: "turn_on"}
        assert end_position == 4

        action_part_repeat_4_input = ["off", "off"]
        assert (
            await run_automation(file_path, [], [], action_part_repeat_4_input)
        ) == [
            {"light.kitchen": "turn_on", "count": "infinite"},
        ]

        action_part_repeat_4_input = ["on", "off"]
        assert (
            await run_automation(file_path, [], [], action_part_repeat_4_input)
        ) == [
            {"light.kitchen": "turn_on", "count": 1},
        ]

        action_part_repeat_4_input = ["on", "on"]
        assert (
            await run_automation(file_path, [], [], action_part_repeat_4_input)
        ) == [
            {"light.kitchen": "turn_on", "count": "infinite"},
        ]

        action_part_repeat_4_input = [None, "off"]
        assert (
            await run_automation(file_path, [], [], action_part_repeat_4_input)
        ) == {"ValueError": "Action input values cannot be None"}

        assert real_pos == 2

        # Test case 5: while repeat action with two conditions
        action_part_repeat_5 = {
            CONF_REPEAT: {
                CONF_WHILE: [
                    {
                        CONF_CONDITION: "state",
                        CONF_ENTITY_ID: "sensor.temperature",
                        CONF_STATE: "on",
                    },
                    {
                        CONF_CONDITION: "state",
                        CONF_ENTITY_ID: "sensor.humidity",
                        CONF_STATE: "off",
                    },
                ],
                CONF_SEQUENCE: [
                    {
                        CONF_SERVICE: "light.turn_on",
                        CONF_TARGET: {CONF_ENTITY_ID: "light.kitchen"},
                    },
                ],
            },
        }
        file_path = init_automation_script("action_part_repeat_5", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_repeat_5, position=1, real_position=0, script_path=file_path
        )
        close_action_section(file_path)

        entities_repeat_5, end_position, real_pos = results
        assert len(entities_repeat_5) == 3
        assert entities_repeat_5[0].parent == 1
        assert entities_repeat_5[0].position == 2
        assert entities_repeat_5[0].parameter_role == ACTION_INPUT
        assert entities_repeat_5[0].integration == "sensor"
        assert entities_repeat_5[0].entity_name == "sensor.temperature"
        assert entities_repeat_5[0].expected_value == {"state": "on"}
        assert entities_repeat_5[1].parent == 1
        assert entities_repeat_5[1].position == 3
        assert entities_repeat_5[1].parameter_role == ACTION_INPUT
        assert entities_repeat_5[1].integration == "sensor"
        assert entities_repeat_5[1].entity_name == "sensor.humidity"
        assert entities_repeat_5[1].expected_value == {"state": "off"}
        assert entities_repeat_5[2].parent is None
        assert entities_repeat_5[2].position == 4
        assert entities_repeat_5[2].parameter_role == OUTPUT
        assert entities_repeat_5[2].integration == "light"
        assert entities_repeat_5[2].entity_name == "light.kitchen"
        assert entities_repeat_5[2].expected_value == {CONF_SERVICE: "turn_on"}
        assert end_position == 4

        action_part_repeat_5_input = ["off", "off"]
        assert (
            await run_automation(file_path, [], [], action_part_repeat_5_input)
        ) == []

        action_part_repeat_5_input = ["on", "off"]
        assert (
            await run_automation(file_path, [], [], action_part_repeat_5_input)
        ) == [
            {"light.kitchen": "turn_on", "count": "infinite"},
        ]

        action_part_repeat_5_input = ["on", "on"]
        assert (
            await run_automation(file_path, [], [], action_part_repeat_5_input)
        ) == []

        action_part_repeat_5_input = [None, "off"]
        assert (
            await run_automation(file_path, [], [], action_part_repeat_5_input)
        ) == {"ValueError": "Action input values cannot be None"}

        assert real_pos == 2

        # Test case 6: repeat action with two actions
        action_part_repeat_6 = {
            CONF_REPEAT: {
                CONF_SEQUENCE: [
                    {
                        CONF_SERVICE: "light.turn_on",
                        CONF_TARGET: {CONF_ENTITY_ID: "light.kitchen"},
                    },
                    {
                        CONF_SERVICE: "light.turn_off",
                        CONF_TARGET: {CONF_ENTITY_ID: "light.kitchen"},
                    },
                ],
                CONF_COUNT: 15,
            },
        }
        file_path = init_automation_script("action_part_repeat_6", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_repeat_6, position=1, real_position=0, script_path=file_path
        )
        close_action_section(file_path)

        entities_repeat_6, end_position, real_pos = results
        assert len(entities_repeat_6) == 2
        assert entities_repeat_6[0].parent is None
        assert entities_repeat_6[0].position == 1
        assert entities_repeat_6[0].parameter_role == OUTPUT
        assert entities_repeat_6[0].integration == "light"
        assert entities_repeat_6[0].entity_name == "light.kitchen"
        assert entities_repeat_6[0].expected_value == {CONF_SERVICE: "turn_on"}
        assert entities_repeat_6[1].parent is None
        assert entities_repeat_6[1].position == 2
        assert entities_repeat_6[1].parameter_role == OUTPUT
        assert entities_repeat_6[1].integration == "light"
        assert entities_repeat_6[1].entity_name == "light.kitchen"
        assert entities_repeat_6[1].expected_value == {CONF_SERVICE: "turn_off"}
        assert end_position == 2

        assert (await run_automation(file_path, [], [])) == [
            {"light.kitchen": "turn_on", "count": 15},
            {"light.kitchen": "turn_off", "count": 15},
        ]

        assert real_pos == 0

        # Test case 7: while repeat action with two conditions and at a specific position
        action_part_repeat_7 = {
            CONF_REPEAT: {
                CONF_WHILE: [
                    {
                        CONF_CONDITION: "state",
                        CONF_ENTITY_ID: "sensor.temperature",
                        CONF_STATE: "on",
                    },
                    {
                        CONF_CONDITION: "state",
                        CONF_ENTITY_ID: "sensor.humidity",
                        CONF_STATE: "off",
                    },
                ],
                CONF_SEQUENCE: [
                    {
                        CONF_SERVICE: "light.turn_on",
                        CONF_TARGET: {CONF_ENTITY_ID: "light.kitchen"},
                    },
                    {
                        CONF_SERVICE: "light.turn_off",
                        CONF_TARGET: {CONF_ENTITY_ID: "light.kitchen"},
                    },
                ],
            },
        }
        file_path = init_automation_script("action_part_repeat_7", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_repeat_7, position=18, real_position=3, script_path=file_path
        )
        close_action_section(file_path)

        entities_repeat_7, end_position, real_pos = results
        assert len(entities_repeat_7) == 4
        assert entities_repeat_7[0].parent == 18
        assert entities_repeat_7[0].position == 19
        assert entities_repeat_7[0].parameter_role == ACTION_INPUT
        assert entities_repeat_7[0].integration == "sensor"
        assert entities_repeat_7[0].entity_name == "sensor.temperature"
        assert entities_repeat_7[0].expected_value == {"state": "on"}
        assert entities_repeat_7[1].parent == 18
        assert entities_repeat_7[1].position == 20
        assert entities_repeat_7[1].parameter_role == ACTION_INPUT
        assert entities_repeat_7[1].integration == "sensor"
        assert entities_repeat_7[1].entity_name == "sensor.humidity"
        assert entities_repeat_7[1].expected_value == {"state": "off"}
        assert entities_repeat_7[2].parent is None
        assert entities_repeat_7[2].position == 21
        assert entities_repeat_7[2].parameter_role == OUTPUT
        assert entities_repeat_7[2].integration == "light"
        assert entities_repeat_7[2].entity_name == "light.kitchen"
        assert entities_repeat_7[2].expected_value == {CONF_SERVICE: "turn_on"}
        assert entities_repeat_7[3].parent is None
        assert entities_repeat_7[3].position == 22
        assert entities_repeat_7[3].parameter_role == OUTPUT
        assert entities_repeat_7[3].integration == "light"
        assert entities_repeat_7[3].entity_name == "light.kitchen"
        assert entities_repeat_7[3].expected_value == {CONF_SERVICE: "turn_off"}
        assert end_position == 22

        action_part_repeat_7_input = ["filler", "filler", "filler", "off", "off"]
        assert (
            await run_automation(file_path, [], [], action_part_repeat_7_input)
        ) == []

        action_part_repeat_7_input = ["filler", "filler", "filler", "on", "off"]
        assert (
            await run_automation(file_path, [], [], action_part_repeat_7_input)
        ) == [
            {"light.kitchen": "turn_on", "count": "infinite"},
            {"light.kitchen": "turn_off", "count": "infinite"},
        ]

        action_part_repeat_7_input = ["filler", "filler", "filler", "on", None]
        assert (
            await run_automation(file_path, [], [], action_part_repeat_7_input)
        ) == {"ValueError": "Action input values cannot be None"}

    async def test_action_sequence():
        # Test case 1: sequence of action with one action
        action_part_sequence_1 = {
            CONF_SEQUENCE: [
                {
                    CONF_SERVICE: "light.turn_on",
                    CONF_TARGET: {CONF_ENTITY_ID: "light.kitchen"},
                },
            ],
        }
        file_path = init_automation_script("action_part_sequence_1", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_sequence_1, position=1, real_position=0, script_path=file_path
        )
        close_action_section(file_path)

        entities_sequence_1, end_position, real_pos = results
        assert len(entities_sequence_1) == 1
        assert entities_sequence_1[0].parent is None
        assert entities_sequence_1[0].position == 1
        assert entities_sequence_1[0].parameter_role == OUTPUT
        assert entities_sequence_1[0].integration == "light"
        assert entities_sequence_1[0].entity_name == "light.kitchen"
        assert entities_sequence_1[0].expected_value == {CONF_SERVICE: "turn_on"}
        assert end_position == 1

        assert (await run_automation(file_path, [], [])) == [
            {"light.kitchen": "turn_on"}
        ]
        assert real_pos == 0

        # Test case 2: sequence of action with three actions
        action_part_sequence_2 = {
            CONF_SEQUENCE: [
                {
                    CONF_SERVICE: "light.turn_on",
                    CONF_TARGET: {CONF_ENTITY_ID: "light.kitchen"},
                },
                {
                    CONF_SERVICE: "light.turn_off",
                    CONF_TARGET: {CONF_ENTITY_ID: "light.kitchen"},
                },
                {
                    CONF_SERVICE: "light.toggle",
                    CONF_TARGET: {CONF_ENTITY_ID: "light.living_room"},
                },
            ],
        }
        file_path = init_automation_script("action_part_sequence_2", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_sequence_2, position=1, real_position=0, script_path=file_path
        )
        close_action_section(file_path)

        entities_sequence_2, end_position, real_pos = results
        assert len(entities_sequence_2) == 3
        assert entities_sequence_2[0].parent is None
        assert entities_sequence_2[0].position == 1
        assert entities_sequence_2[0].parameter_role == OUTPUT
        assert entities_sequence_2[0].integration == "light"
        assert entities_sequence_2[0].entity_name == "light.kitchen"
        assert entities_sequence_2[0].expected_value == {CONF_SERVICE: "turn_on"}
        assert entities_sequence_2[1].parent is None
        assert entities_sequence_2[1].position == 2
        assert entities_sequence_2[1].parameter_role == OUTPUT
        assert entities_sequence_2[1].integration == "light"
        assert entities_sequence_2[1].entity_name == "light.kitchen"
        assert entities_sequence_2[1].expected_value == {CONF_SERVICE: "turn_off"}
        assert entities_sequence_2[2].parent is None
        assert entities_sequence_2[2].position == 3
        assert entities_sequence_2[2].parameter_role == OUTPUT
        assert entities_sequence_2[2].integration == "light"
        assert entities_sequence_2[2].entity_name == "light.living_room"
        assert entities_sequence_2[2].expected_value == {CONF_SERVICE: "toggle"}
        assert end_position == 3

        assert (await run_automation(file_path, [], [])) == [
            {"light.kitchen": "turn_on"},
            {"light.kitchen": "turn_off"},
            {"light.living_room": "toggle"},
        ]

        assert real_pos == 0

        # Test case 3: sequence of action with two actions at a specific position
        action_part_sequence_3 = {
            CONF_SEQUENCE: [
                {
                    CONF_SERVICE: "light.turn_on",
                    CONF_TARGET: {CONF_ENTITY_ID: "light.kitchen"},
                },
                {
                    CONF_SERVICE: "light.turn_off",
                    CONF_TARGET: {CONF_ENTITY_ID: "light.kitchen"},
                },
            ],
        }
        file_path = init_automation_script("action_part_sequence_3", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_sequence_3, position=557, real_position=9, script_path=file_path
        )
        close_action_section(file_path)

        entities_sequence_3, end_position, real_pos = results
        assert len(entities_sequence_3) == 2
        assert entities_sequence_3[0].parent is None
        assert entities_sequence_3[0].position == 557
        assert entities_sequence_3[0].parameter_role == OUTPUT
        assert entities_sequence_3[0].integration == "light"
        assert entities_sequence_3[0].entity_name == "light.kitchen"
        assert entities_sequence_3[0].expected_value == {CONF_SERVICE: "turn_on"}
        assert entities_sequence_3[1].parent is None
        assert entities_sequence_3[1].position == 558
        assert entities_sequence_3[1].parameter_role == OUTPUT
        assert entities_sequence_3[1].integration == "light"
        assert entities_sequence_3[1].entity_name == "light.kitchen"
        assert entities_sequence_3[1].expected_value == {CONF_SERVICE: "turn_off"}
        assert end_position == 558

        assert (await run_automation(file_path, [], [])) == [
            {"light.kitchen": "turn_on"},
            {"light.kitchen": "turn_off"},
        ]
        assert real_pos == 9

    async def test_action_condition():
        # Test case 1: condition action with one condition
        action_part_condition_1 = {
            CONF_CONDITION: "state",
            CONF_ENTITY_ID: "sensor.temperature",
            CONF_STATE: "on",
        }
        file_path = init_automation_script("action_part_condition_1", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_condition_1, position=1, real_position=0, script_path=file_path
        )
        create_dummy_action_return(file_path)
        close_action_section(file_path)

        entities_condition_1, end_position, real_pos = results
        assert len(entities_condition_1) == 1
        assert entities_condition_1[0].parent is None
        assert entities_condition_1[0].position == 1
        assert entities_condition_1[0].parameter_role == ACTION_INPUT
        assert entities_condition_1[0].integration == "sensor"
        assert entities_condition_1[0].entity_name == "sensor.temperature"
        assert entities_condition_1[0].expected_value == {"state": "on"}
        assert end_position == 1

        action_part_condition_1_input = ["on"]
        assert (
            await run_automation(file_path, [], [], action_part_condition_1_input)
        ) == [{"dummy.target": "doSomething"}]

        action_part_condition_1_input = ["off"]
        assert (
            await run_automation(file_path, [], [], action_part_condition_1_input)
        ) == []

        action_part_condition_1_input = [None]
        assert (
            await run_automation(file_path, [], [], action_part_condition_1_input)
        ) == {"ValueError": "Action input values cannot be None"}

        assert real_pos == 1

        # Test case 2: condition action with one conditions and at a specific position with a parent
        action_part_condition_2 = {
            CONF_CONDITION: "state",
            CONF_ENTITY_ID: "sensor.temperature",
            CONF_STATE: "on",
        }
        file_path = init_automation_script("action_part_condition_2", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_condition_2,
            position=10,
            real_position=0,
            script_path=file_path,
            parent=1,
        )
        create_dummy_action_return(file_path)
        close_action_section(file_path)

        entities_condition_2, end_position, real_pos = results
        assert len(entities_condition_2) == 1
        assert entities_condition_2[0].parent == 1
        assert entities_condition_2[0].position == 10
        assert entities_condition_2[0].parameter_role == ACTION_INPUT
        assert entities_condition_2[0].integration == "sensor"
        assert entities_condition_2[0].entity_name == "sensor.temperature"
        assert entities_condition_2[0].expected_value == {"state": "on"}
        assert end_position == 10

        action_part_condition_2_input = ["on"]
        assert (
            await run_automation(file_path, [], [], action_part_condition_2_input)
        ) == [{"dummy.target": "doSomething"}]

        action_part_condition_2_input = ["off"]
        assert (
            await run_automation(file_path, [], [], action_part_condition_2_input)
        ) == []

        action_part_condition_2_input = [None]
        assert (
            await run_automation(file_path, [], [], action_part_condition_2_input)
        ) == {"ValueError": "Action input values cannot be None"}

        assert real_pos == 1

        # Test case 3: condition action with two conditions
        action_part_condition_3 = {
            CONF_CONDITION: [
                {
                    CONF_CONDITION: "state",
                    CONF_ENTITY_ID: "sensor.temperature",
                    CONF_STATE: "on",
                },
                {
                    CONF_CONDITION: "state",
                    CONF_ENTITY_ID: "sensor.humidity",
                    CONF_STATE: "off",
                },
            ]
        }
        file_path = init_automation_script("action_part_condition_3", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_condition_3, position=1, real_position=0, script_path=file_path
        )
        create_dummy_action_return(file_path)
        close_action_section(file_path)

        entities_condition_3, end_position, real_pos = results
        assert len(entities_condition_3) == 2
        assert entities_condition_3[0].parent == 1
        assert entities_condition_3[0].position == 2
        assert entities_condition_3[0].parameter_role == ACTION_INPUT
        assert entities_condition_3[0].integration == "sensor"
        assert entities_condition_3[0].entity_name == "sensor.temperature"
        assert entities_condition_3[0].expected_value == {"state": "on"}
        assert entities_condition_3[1].parent == 1
        assert entities_condition_3[1].position == 3
        assert entities_condition_3[1].parameter_role == ACTION_INPUT
        assert entities_condition_3[1].integration == "sensor"
        assert entities_condition_3[1].entity_name == "sensor.humidity"
        assert entities_condition_3[1].expected_value == {"state": "off"}
        assert end_position == 3

        action_part_condition_3_input = ["on", "off"]
        assert (
            await run_automation(file_path, [], [], action_part_condition_3_input)
        ) == [{"dummy.target": "doSomething"}]

        action_part_condition_3_input = ["off", "on"]
        assert (
            await run_automation(file_path, [], [], action_part_condition_3_input)
        ) == []

        action_part_condition_3_input = ["on", "on"]
        assert (
            await run_automation(file_path, [], [], action_part_condition_3_input)
        ) == []

        action_part_condition_3_input = ["off", "off"]
        assert (
            await run_automation(file_path, [], [], action_part_condition_3_input)
        ) == []

        action_part_condition_3_input = [None, None]
        assert (
            await run_automation(file_path, [], [], action_part_condition_3_input)
        ) == {"ValueError": "Action input values cannot be None"}

        assert real_pos == 2

        # Test case 4: condition action with two conditions and at a specific position
        action_part_condition_4 = {
            CONF_CONDITION: [
                {
                    CONF_CONDITION: "state",
                    CONF_ENTITY_ID: "sensor.temperature",
                    CONF_STATE: "on",
                },
                {
                    CONF_CONDITION: "state",
                    CONF_ENTITY_ID: "sensor.humidity",
                    CONF_STATE: "off",
                },
            ]
        }
        file_path = init_automation_script("action_part_condition_4", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_condition_4,
            position=10,
            parent=5,
            real_position=2,
            script_path=file_path,
        )
        create_dummy_action_return(file_path)
        close_action_section(file_path)

        entities_condition_4, end_position, real_pos = results
        assert len(entities_condition_4) == 2
        assert entities_condition_4[0].parent == 10
        assert entities_condition_4[0].position == 11
        assert entities_condition_4[0].parameter_role == ACTION_INPUT
        assert entities_condition_4[0].integration == "sensor"
        assert entities_condition_4[0].entity_name == "sensor.temperature"
        assert entities_condition_4[0].expected_value == {"state": "on"}
        assert entities_condition_4[1].parent == 10
        assert entities_condition_4[1].position == 12
        assert entities_condition_4[1].parameter_role == ACTION_INPUT
        assert entities_condition_4[1].integration == "sensor"
        assert entities_condition_4[1].entity_name == "sensor.humidity"
        assert entities_condition_4[1].expected_value == {"state": "off"}
        assert end_position == 12

        action_part_condition_3_input = ["filler", "filler", "on", "off"]
        assert (
            await run_automation(file_path, [], [], action_part_condition_3_input)
        ) == [{"dummy.target": "doSomething"}]

        action_part_condition_3_input = ["filler", "filler", "off", "on"]
        assert (
            await run_automation(file_path, [], [], action_part_condition_3_input)
        ) == []

        action_part_condition_3_input = ["filler", "filler", "on", "on"]
        assert (
            await run_automation(file_path, [], [], action_part_condition_3_input)
        ) == []

        action_part_condition_3_input = ["filler", "filler", "off", "off"]
        assert (
            await run_automation(file_path, [], [], action_part_condition_3_input)
        ) == []

        action_part_condition_3_input = ["filler", "filler", None, None]
        assert (
            await run_automation(file_path, [], [], action_part_condition_3_input)
        ) == {"ValueError": "Action input values cannot be None"}

        assert real_pos == 4

    async def test_action_event():
        # Test case 1: event action with one event
        action_part_event_1 = {
            CONF_EVENT: "test_event",
            CONF_EVENT_DATA: {
                "test_data": "event_data",
            },
        }
        file_path = init_automation_script("action_part_event_1", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_event_1, position=1, real_position=0, script_path=file_path
        )
        close_action_section(file_path)

        entities_event_1, end_position, real_pos = results
        assert len(entities_event_1) == 1
        assert entities_event_1[0].parent is None
        assert entities_event_1[0].position == 1
        assert entities_event_1[0].parameter_role == OUTPUT
        assert entities_event_1[0].integration == "test_event"
        assert entities_event_1[0].entity_name is not None
        assert entities_event_1[0].expected_value == {
            CONF_EVENT_DATA: {"test_data": "event_data"}
        }
        assert end_position == 1

        action_part_event_1_input = []
        assert (await run_automation(file_path, [], [], action_part_event_1_input)) == [
            {"test_event": {"event_data": {"test_data": "event_data"}}}
        ]

        assert real_pos == 0

        # Test case 2: event action with one event and at a specific position
        action_part_event_2 = {
            CONF_EVENT: "test_event",
            CONF_EVENT_DATA: {
                "test_data": "event_data",
                "test_data_2": "event_data_2",
            },
        }
        file_path = init_automation_script("action_part_event_2", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_event_2, position=10, real_position=0, script_path=file_path
        )
        close_action_section(file_path)

        entities_event_2, end_position, real_pos = results
        assert len(entities_event_2) == 1
        assert entities_event_2[0].parent is None
        assert entities_event_2[0].position == 10
        assert entities_event_2[0].parameter_role == OUTPUT
        assert entities_event_2[0].integration == "test_event"
        assert entities_event_2[0].entity_name is not None
        assert entities_event_2[0].expected_value == {
            CONF_EVENT_DATA: {"test_data": "event_data", "test_data_2": "event_data_2"}
        }
        assert end_position == 10

        action_part_event_2_input = []
        assert (await run_automation(file_path, [], [], action_part_event_2_input)) == [
            {
                "test_event": {
                    "event_data": {
                        "test_data": "event_data",
                        "test_data_2": "event_data_2",
                    }
                }
            }
        ]

        assert real_pos == 0

    async def test_action_wait_for_trigger():
        # Test case 1: wait for trigger action with one trigger
        action_part_wait_for_trigger_1 = {
            SCRIPT_ACTION_WAIT_FOR_TRIGGER: [
                {
                    CONF_PLATFORM: "state",
                    CONF_ENTITY_ID: "sensor.temperature",
                    CONF_TO: "on",
                },
            ],
        }
        file_path = init_automation_script("action_part_wait_for_trigger_1", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_wait_for_trigger_1,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        create_dummy_action_return(file_path)
        close_action_section(file_path)

        entities_wait_for_trigger_1, end_position, real_pos = results
        assert len(entities_wait_for_trigger_1) == 1
        assert entities_wait_for_trigger_1[0].parent is None
        assert entities_wait_for_trigger_1[0].position == 1
        assert entities_wait_for_trigger_1[0].parameter_role == ACTION_INPUT
        assert entities_wait_for_trigger_1[0].integration == "sensor"
        assert entities_wait_for_trigger_1[0].entity_name == "sensor.temperature"
        assert entities_wait_for_trigger_1[0].expected_value == {"to": "on"}
        assert end_position == 1

        action_part_wait_for_trigger_1_input = ["on"]
        assert (
            await run_automation(
                file_path, [], [], action_part_wait_for_trigger_1_input
            )
        ) == [{"dummy.target": "doSomething"}]

        action_part_wait_for_trigger_1_input = ["off"]
        assert (
            await run_automation(
                file_path, [], [], action_part_wait_for_trigger_1_input
            )
        ) == []

        action_part_wait_for_trigger_1_input = [None]
        assert (
            await run_automation(
                file_path, [], [], action_part_wait_for_trigger_1_input
            )
        ) == {"ValueError": "Action input values cannot be None"}
        assert real_pos == 1

        # Test case 2: wait for trigger action with one trigger without a list
        action_part_wait_for_trigger_2 = {
            SCRIPT_ACTION_WAIT_FOR_TRIGGER: {
                CONF_PLATFORM: "state",
                CONF_ENTITY_ID: "sensor.temperature",
                CONF_TO: "on",
            },
        }
        file_path = init_automation_script("action_part_wait_for_trigger_2", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_wait_for_trigger_2,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        create_dummy_action_return(file_path)
        close_action_section(file_path)

        entities_wait_for_trigger_2, end_position, real_pos = results
        assert len(entities_wait_for_trigger_2) == 1
        assert entities_wait_for_trigger_2[0].parent is None
        assert entities_wait_for_trigger_2[0].position == 1
        assert entities_wait_for_trigger_2[0].parameter_role == ACTION_INPUT
        assert entities_wait_for_trigger_2[0].integration == "sensor"
        assert entities_wait_for_trigger_2[0].entity_name == "sensor.temperature"
        assert entities_wait_for_trigger_2[0].expected_value == {"to": "on"}
        assert end_position == 1

        action_part_wait_for_trigger_2_input = ["on"]
        assert (
            await run_automation(
                file_path, [], [], action_part_wait_for_trigger_2_input
            )
        ) == [{"dummy.target": "doSomething"}]

        action_part_wait_for_trigger_2_input = ["off"]
        assert (
            await run_automation(
                file_path, [], [], action_part_wait_for_trigger_2_input
            )
        ) == []

        action_part_wait_for_trigger_2_input = [None]
        assert (
            await run_automation(
                file_path, [], [], action_part_wait_for_trigger_2_input
            )
        ) == {"ValueError": "Action input values cannot be None"}
        assert real_pos == 1

        # Test case 3: wait for trigger action with multiple triggers
        action_part_wait_for_trigger_3 = {
            SCRIPT_ACTION_WAIT_FOR_TRIGGER: [
                {
                    CONF_PLATFORM: "state",
                    CONF_ENTITY_ID: "sensor.temperature",
                    CONF_TO: "on",
                },
                {
                    CONF_PLATFORM: "state",
                    CONF_ENTITY_ID: "sensor.humidity",
                    CONF_TO: "off",
                },
            ],
        }
        file_path = init_automation_script("action_part_wait_for_trigger_3", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_wait_for_trigger_3,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        create_dummy_action_return(file_path)
        close_action_section(file_path)

        entities_wait_for_trigger_3, end_position, real_pos = results
        assert len(entities_wait_for_trigger_3) == 2
        assert entities_wait_for_trigger_3[0].parent == 1
        assert entities_wait_for_trigger_3[0].position == 2
        assert entities_wait_for_trigger_3[0].parameter_role == ACTION_INPUT
        assert entities_wait_for_trigger_3[0].integration == "sensor"
        assert entities_wait_for_trigger_3[0].entity_name == "sensor.temperature"
        assert entities_wait_for_trigger_3[0].expected_value == {"to": "on"}
        assert entities_wait_for_trigger_3[1].parent == 1
        assert entities_wait_for_trigger_3[1].position == 3
        assert entities_wait_for_trigger_3[1].parameter_role == ACTION_INPUT
        assert entities_wait_for_trigger_3[1].integration == "sensor"
        assert entities_wait_for_trigger_3[1].entity_name == "sensor.humidity"
        assert entities_wait_for_trigger_3[1].expected_value == {"to": "off"}
        assert end_position == 3

        action_part_wait_for_trigger_3_input = ["on", "off"]
        assert (
            await run_automation(
                file_path, [], [], action_part_wait_for_trigger_3_input
            )
        ) == [{"dummy.target": "doSomething"}]

        action_part_wait_for_trigger_3_input = ["off", "off"]
        assert (
            await run_automation(
                file_path, [], [], action_part_wait_for_trigger_3_input
            )
        ) == [{"dummy.target": "doSomething"}]

        action_part_wait_for_trigger_3_input = ["off", "on"]
        assert (
            await run_automation(
                file_path, [], [], action_part_wait_for_trigger_3_input
            )
        ) == []

        action_part_wait_for_trigger_3_input = [None, None]
        assert (
            await run_automation(
                file_path, [], [], action_part_wait_for_trigger_3_input
            )
        ) == {"ValueError": "Action input values cannot be None"}

        assert real_pos == 2

        # Test case 4: wait for trigger action with multiple triggers and at a specific position
        action_part_wait_for_trigger_4 = {
            SCRIPT_ACTION_WAIT_FOR_TRIGGER: [
                {
                    CONF_PLATFORM: "state",
                    CONF_ENTITY_ID: "sensor.temperature",
                    CONF_TO: "on",
                },
                {
                    CONF_PLATFORM: "state",
                    CONF_ENTITY_ID: "sensor.humidity",
                    CONF_TO: "off",
                },
            ],
        }
        file_path = init_automation_script("action_part_wait_for_trigger_4", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_wait_for_trigger_4,
            position=10,
            real_position=5,
            script_path=file_path,
        )
        create_dummy_action_return(file_path)
        close_action_section(file_path)

        entities_wait_for_trigger_4, end_position, real_pos = results
        assert len(entities_wait_for_trigger_4) == 2
        assert entities_wait_for_trigger_4[0].parent == 10
        assert entities_wait_for_trigger_4[0].position == 11
        assert entities_wait_for_trigger_4[0].parameter_role == ACTION_INPUT
        assert entities_wait_for_trigger_4[0].integration == "sensor"
        assert entities_wait_for_trigger_4[0].entity_name == "sensor.temperature"
        assert entities_wait_for_trigger_4[0].expected_value == {"to": "on"}
        assert entities_wait_for_trigger_4[1].parent == 10
        assert entities_wait_for_trigger_4[1].position == 12
        assert entities_wait_for_trigger_4[1].parameter_role == ACTION_INPUT
        assert entities_wait_for_trigger_4[1].integration == "sensor"
        assert entities_wait_for_trigger_4[1].entity_name == "sensor.humidity"
        assert entities_wait_for_trigger_4[1].expected_value == {"to": "off"}
        assert end_position == 12

        action_part_wait_for_trigger_4_input = [
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "on",
            "off",
        ]
        assert (
            await run_automation(
                file_path, [], [], action_part_wait_for_trigger_4_input
            )
        ) == [{"dummy.target": "doSomething"}]

        action_part_wait_for_trigger_4_input = [
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            "off",
            "on",
        ]
        assert (
            await run_automation(
                file_path, [], [], action_part_wait_for_trigger_4_input
            )
        ) == []

        action_part_wait_for_trigger_4_input = [
            "filler",
            "filler",
            "filler",
            "filler",
            "filler",
            None,
            None,
        ]
        assert (
            await run_automation(
                file_path, [], [], action_part_wait_for_trigger_4_input
            )
        ) == {"ValueError": "Action input values cannot be None"}

        assert real_pos == 7

        # Test case 5: wait for trigger action with one trigger without a list and with a timeout
        action_part_wait_for_trigger_5 = {
            SCRIPT_ACTION_WAIT_FOR_TRIGGER: {
                CONF_PLATFORM: "state",
                CONF_ENTITY_ID: "sensor.temperature",
                CONF_TO: "on",
            },
            CONF_TIMEOUT: {"seconds": 5},
        }
        file_path = init_automation_script("action_part_wait_for_trigger_5", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_wait_for_trigger_5,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        create_dummy_action_return(file_path)
        close_action_section(file_path)

        entities_wait_for_trigger_5, end_position, real_pos = results
        assert len(entities_wait_for_trigger_5) == 1
        assert entities_wait_for_trigger_5[0].parent is None
        assert entities_wait_for_trigger_5[0].position == 1
        assert entities_wait_for_trigger_5[0].parameter_role == ACTION_INPUT
        assert entities_wait_for_trigger_5[0].integration == "sensor"
        assert entities_wait_for_trigger_5[0].entity_name == "sensor.temperature"
        assert entities_wait_for_trigger_5[0].expected_value == {"to": "on"}
        assert end_position == 1

        action_part_wait_for_trigger_5_input = ["on"]
        assert (
            await run_automation(
                file_path, [], [], action_part_wait_for_trigger_5_input
            )
        ) == [{"dummy.target": "doSomething"}]

        action_part_wait_for_trigger_5_input = ["off"]
        assert (
            await run_automation(
                file_path, [], [], action_part_wait_for_trigger_5_input
            )
        ) == [{"dummy.target": "doSomething"}]

        action_part_wait_for_trigger_5_input = [None]
        assert (
            await run_automation(
                file_path, [], [], action_part_wait_for_trigger_5_input
            )
        ) == {"ValueError": "Action input values cannot be None"}
        assert real_pos == 1

        # Test case 6: wait for trigger action with one trigger without a list and timeout but without continueing afterwards
        action_part_wait_for_trigger_6 = {
            SCRIPT_ACTION_WAIT_FOR_TRIGGER: {
                CONF_PLATFORM: "state",
                CONF_ENTITY_ID: "sensor.temperature",
                CONF_TO: "on",
            },
            CONF_TIMEOUT: {"seconds": 5},
            CONF_CONTINUE_ON_TIMEOUT: False,
        }
        file_path = init_automation_script("action_part_wait_for_trigger_6", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_wait_for_trigger_6,
            position=1,
            real_position=0,
            script_path=file_path,
        )
        create_dummy_action_return(file_path)
        close_action_section(file_path)

        entities_wait_for_trigger_6, end_position, real_pos = results
        assert len(entities_wait_for_trigger_6) == 1
        assert entities_wait_for_trigger_6[0].parent is None
        assert entities_wait_for_trigger_6[0].position == 1
        assert entities_wait_for_trigger_6[0].parameter_role == ACTION_INPUT
        assert entities_wait_for_trigger_6[0].integration == "sensor"
        assert entities_wait_for_trigger_6[0].entity_name == "sensor.temperature"
        assert entities_wait_for_trigger_6[0].expected_value == {"to": "on"}
        assert end_position == 1

        action_part_wait_for_trigger_6_input = ["on"]
        assert (
            await run_automation(
                file_path, [], [], action_part_wait_for_trigger_6_input
            )
        ) == [{"dummy.target": "doSomething"}]

        action_part_wait_for_trigger_6_input = ["off"]
        assert (
            await run_automation(
                file_path, [], [], action_part_wait_for_trigger_6_input
            )
        ) == []

        action_part_wait_for_trigger_6_input = [None]
        assert (
            await run_automation(
                file_path, [], [], action_part_wait_for_trigger_6_input
            )
        ) == {"ValueError": "Action input values cannot be None"}
        assert real_pos == 1

    async def test_action_device():
        # Test case 1: device action
        action_part_device_1 = {
            CONF_DEVICE_ID: "test_device",
            CONF_DOMAIN: "light",
            CONF_ENTITY_ID: "light.kitchen",
            CONF_TYPE: "turn_on",
        }
        file_path = init_automation_script("action_part_device_1", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_device_1, position=1, real_position=0, script_path=file_path
        )
        close_action_section(file_path)

        entities_device_1, end_position, real_pos = results
        assert len(entities_device_1) == 1
        assert entities_device_1[0].parent is None
        assert entities_device_1[0].position == 1
        assert entities_device_1[0].parameter_role == OUTPUT
        assert entities_device_1[0].integration == "light"
        assert entities_device_1[0].entity_name == "light.test_device"
        assert entities_device_1[0].expected_value == {
            CONF_ENTITY_ID: "light.kitchen",
            CONF_SERVICE: "turn_on",
        }
        assert end_position == 1

        assert (await run_automation(file_path, [], [])) == [
            {"light.test_device": "turn_on"}
        ]

        assert real_pos == 0

        # Test case 2: device action without entity id
        action_part_device_2 = {
            CONF_DEVICE_ID: "test_device",
            CONF_DOMAIN: "light",
            CONF_TYPE: "turn_on",
        }
        file_path = init_automation_script("action_part_device_2", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_device_2, position=1, real_position=0, script_path=file_path
        )
        close_action_section(file_path)

        entities_device_2, end_position, real_pos = results
        assert len(entities_device_2) == 1
        assert entities_device_2[0].parent is None
        assert entities_device_2[0].position == 1
        assert entities_device_2[0].parameter_role == OUTPUT
        assert entities_device_2[0].integration == "light"
        assert entities_device_2[0].entity_name == "light.test_device"
        assert entities_device_2[0].expected_value == {CONF_SERVICE: "turn_on"}
        assert end_position == 1

        assert (await run_automation(file_path, [], [])) == [
            {"light.test_device": "turn_on"}
        ]

        assert real_pos == 0

        # Test case 3: device action with a specific position
        action_part_device_3 = {
            CONF_DEVICE_ID: "test_device",
            CONF_DOMAIN: "light",
            CONF_ENTITY_ID: "light.kitchen",
            CONF_TYPE: "turn_on",
        }
        file_path = init_automation_script("action_part_device_3", ACTION_DIR)
        test_condition_fill(file_path)
        results = _action_entities(
            action_part_device_3, position=10, real_position=0, script_path=file_path
        )
        close_action_section(file_path)

        entities_device_3, end_position, real_pos = results
        assert len(entities_device_3) == 1
        assert entities_device_3[0].parent is None
        assert entities_device_3[0].position == 10
        assert entities_device_3[0].parameter_role == OUTPUT
        assert entities_device_3[0].integration == "light"
        assert entities_device_3[0].entity_name == "light.test_device"
        assert entities_device_3[0].expected_value == {
            CONF_ENTITY_ID: "light.kitchen",
            CONF_SERVICE: "turn_on",
        }
        assert end_position == 10

        assert (await run_automation(file_path, [], [])) == [
            {"light.test_device": "turn_on"}
        ]

        assert real_pos == 0

    async def test_action_all():
        await test_action_call_service()
        await test_action_branching()
        await test_action_choose()
        await test_action_parallel()
        await test_action_repeat()
        await test_action_sequence()
        await test_action_condition()
        await test_action_event()
        await test_action_wait_for_trigger()
        await test_action_device()

    await test_action_all()
    print("All action test cases passed!")


async def test_empty_config():
    """
    Test that an empty configuration raises a KeyError
    """
    empty_file = path.join("test_data", "yaml_files", "test_yaml", "empty.yaml")
    yaml_dict = yaml_loader.load_yaml(empty_file)
    file_path = init_automation_script("empty_script", TEST_DIR)
    try:
        create_procedure_list(yaml_dict, file_path)
    except TypeError as e:
        assert str(e) == "'NoneType' object is not subscriptable"

    print("Empty configuration test passed!")


async def test_bare_minimum_config():
    """
    Test a configuration with only an empty trigger and action list
    """
    bare_min_file = path.join("test_data", "yaml_files", "test_yaml", "bare_min.yaml")
    yaml_dict = yaml_loader.load_yaml(bare_min_file)
    file_path = init_automation_script("bare_min_script", TEST_DIR)
    results = create_procedure_list(yaml_dict, file_path)

    assert results == []

    print("Bare minimum configuration test passed!")


if __name__ == "__main__":
    if not path.exists(TEST_DIR):
        mkdir(TEST_DIR)

    async_run(test_empty_config())
    async_run(test_bare_minimum_config())

    async_run(test_trigger_entities())
    async_run(test_condition_entities())
    async_run(test_action_entities())
