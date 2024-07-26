"""Test cases for automation deselection module.
The python_path needs to be set to the src directory: (for venv) $env:PYTHONPATH = "D:\\Workspace\\Python\\custom_Tkinker_tryout\\src"

"""

import voluptuous as vol

from environment_package.automation_dissection import _condition_entities, _trigger_entities
from environment_package.env_const import INPUT, START
from environment_package.ha_automation.home_assistant_const import (
    CONF_ABOVE,
    CONF_ALLOWED_METHODS,
    CONF_AT,
    CONF_ATTRIBUTE,
    CONF_BELOW,
    CONF_COMMAND,
    CONF_CONDITION,
    CONF_DEVICE_ID,
    CONF_DOMAIN,
    CONF_ENTITY_ID,
    CONF_EVENT,
    CONF_EVENT_CONTEXT,
    CONF_EVENT_DATA,
    CONF_EVENT_TYPE,
    CONF_FOR,
    CONF_FROM,
    CONF_LOCAL,
    CONF_NOFITY_ID,
    CONF_NOT_FROM,
    CONF_NOT_TO,
    CONF_NUMERIC_STATE,
    CONF_OFFSET,
    CONF_PAYLOAD,
    CONF_PLATFORM,
    CONF_QOS,
    CONF_SOURCE,
    CONF_STATE,
    CONF_TO,
    CONF_TYPE,
    CONF_UPDATE_TYPE,
    CONF_VALUE_TEMPLATE,
    CONF_WEBHOOK_ID,
    CONF_ZONE,
    HOURS,
    MINUTES,
    SECONDS,
    TAG_ID,
)


def test_trigger_entities():
    # Test case 1: Event trigger with single event type
    trigger_part_event_1 = {CONF_PLATFORM: CONF_EVENT, CONF_EVENT_TYPE: "event_type_1"}
    results = _trigger_entities(trigger_part_event_1, position=1)
    entities_event_1, end_position = results
    assert len(entities_event_1) == 1
    assert entities_event_1[0].parent is None
    assert entities_event_1[0].position == 1
    assert entities_event_1[0].parameter_role == START
    assert entities_event_1[0].integration == CONF_EVENT
    assert entities_event_1[0].entity_name is not None
    assert entities_event_1[0].expected_value == {CONF_EVENT_TYPE: "event_type_1"}
    assert end_position == 1

    # Test case 2: Event trigger with multiple event types
    trigger_part_event_2 = {
        CONF_PLATFORM: CONF_EVENT,
        CONF_EVENT_TYPE: ["event_type_2", "event_type_3"],
    }
    results = _trigger_entities(trigger_part_event_2, position=1)
    entities_event_2, end_position = results
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

    # Test case 3: Event trigger with event data and context
    trigger_part_event_3 = {
        CONF_PLATFORM: CONF_EVENT,
        CONF_EVENT_TYPE: "event_type_3",
        CONF_EVENT_DATA: {"key_1": "value_1", "key_2": "value_2"},
        CONF_EVENT_CONTEXT: {"key_3-2": ["value_3-2-1", "value_3-2-2"]},
    }
    results = _trigger_entities(trigger_part_event_3, position=1)
    entities_event_3, end_position = results
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

    # Test case 4: Home Assistant trigger with single event
    trigger_part_ha_1 = {CONF_PLATFORM: "homeassistant", CONF_EVENT: "start"}
    results = _trigger_entities(trigger_part_ha_1, position=1)
    entities_ha_1, end_position = results
    assert len(entities_ha_1) == 1
    assert entities_ha_1[0].parent is None
    assert entities_ha_1[0].position == 1
    assert entities_ha_1[0].parameter_role == START
    assert entities_ha_1[0].integration == "homeassistant"
    assert entities_ha_1[0].entity_name == "homeassistant._"
    assert entities_ha_1[0].expected_value == {CONF_EVENT: "start"}
    assert end_position == 1
    
    # Test case 5: Home Assistant trigger with single event
    trigger_part_ha_2 = {CONF_PLATFORM: "homeassistant", CONF_EVENT: "shutdown"}
    results = _trigger_entities(trigger_part_ha_2, position=1)
    entities_ha_2, end_position = results
    assert len(entities_ha_2) == 1
    assert entities_ha_2[0].parent is None
    assert entities_ha_2[0].position == 1
    assert entities_ha_2[0].parameter_role == START
    assert entities_ha_2[0].integration == "homeassistant"
    assert entities_ha_2[0].entity_name == "homeassistant._"
    assert entities_ha_2[0].expected_value == {CONF_EVENT: "shutdown"}
    assert end_position == 1
    
    # Test case 6: MQTT trigger with qos
    trigger_part_mqtt_1 = {CONF_PLATFORM: "mqtt", "topic": "mqtt_topic", CONF_QOS: 0}
    results = _trigger_entities(trigger_part_mqtt_1, position=1)
    entities_mqtt_1, end_position = results
    assert len(entities_mqtt_1) == 1
    assert entities_mqtt_1[0].parent is None
    assert entities_mqtt_1[0].position == 1
    assert entities_mqtt_1[0].parameter_role == START
    assert entities_mqtt_1[0].integration == "mqtt"
    assert entities_mqtt_1[0].entity_name == "mqtt.mqtt_topic"
    assert entities_mqtt_1[0].expected_value == {CONF_QOS: 0}
    assert end_position == 1

    # Test case 7: MQTT trigger with payload
    trigger_part_mqtt_2 = {
        CONF_PLATFORM: "mqtt",
        "topic": "mqtt_topic",
        CONF_PAYLOAD: "mqtt_payload",
    }
    results = _trigger_entities(trigger_part_mqtt_2, position=1)
    entities_mqtt_2, end_position = results
    assert len(entities_mqtt_2) == 1
    assert entities_mqtt_2[0].parent is None
    assert entities_mqtt_2[0].position == 1
    assert entities_mqtt_2[0].parameter_role == START
    assert entities_mqtt_2[0].integration == "mqtt"
    assert entities_mqtt_2[0].entity_name == "mqtt.mqtt_topic"
    assert entities_mqtt_2[0].expected_value == {CONF_PAYLOAD: "mqtt_payload"}
    assert end_position == 1

    # Test case 8: MQTT trigger with qos and payload
    trigger_part_mqtt_3 = {
        CONF_PLATFORM: "mqtt",
        "topic": "mqtt_topic",
        CONF_PAYLOAD: "mqtt_payload",
        CONF_QOS: 0,
    }
    results = _trigger_entities(trigger_part_mqtt_3, position=1)
    entities_mqtt_3, end_position = results
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

    # Test case 9: Numerical state trigger with below values
    trigger_part_num_state_1 = {
        CONF_PLATFORM: CONF_NUMERIC_STATE,
        CONF_ENTITY_ID: "sensor.temperature",
        CONF_BELOW: 30,
    }
    results = _trigger_entities(trigger_part_num_state_1, position=1)
    entities_num_state_1, end_position = results
    assert len(entities_num_state_1) == 1
    assert entities_num_state_1[0].parent is None
    assert entities_num_state_1[0].position == 1
    assert entities_num_state_1[0].parameter_role == START
    assert entities_num_state_1[0].integration == "sensor"
    assert entities_num_state_1[0].entity_name == "sensor.temperature"
    assert entities_num_state_1[0].expected_value == {"value": "__VALUE__ < 30"}
    assert end_position == 1

    # Test case 10: Numerical state trigger with above value
    trigger_part_num_state_2 = {
        CONF_PLATFORM: CONF_NUMERIC_STATE,
        CONF_ENTITY_ID: "sensor.temperature",
        CONF_ABOVE: 20,
    }
    results = _trigger_entities(trigger_part_num_state_2, position=1)
    entities_num_state_2, end_position = results
    assert len(entities_num_state_2) == 1
    assert entities_num_state_2[0].parent is None
    assert entities_num_state_2[0].position == 1
    assert entities_num_state_2[0].parameter_role == START
    assert entities_num_state_2[0].integration == "sensor"
    assert entities_num_state_2[0].entity_name == "sensor.temperature"
    assert entities_num_state_2[0].expected_value == {"value": "20 < __VALUE__"}
    assert end_position == 1

    # Test case 11: Numerical state trigger with above and below values
    trigger_part_num_state_3 = {
        CONF_PLATFORM: CONF_NUMERIC_STATE,
        CONF_ENTITY_ID: "sensor.temperature",
        CONF_ABOVE: 20,
        CONF_BELOW: 30,
    }
    results = _trigger_entities(trigger_part_num_state_3, position=1)
    entities_num_state_3, end_position = results
    assert len(entities_num_state_3) == 1
    assert entities_num_state_3[0].parent is None
    assert entities_num_state_3[0].position == 1
    assert entities_num_state_3[0].parameter_role == START
    assert entities_num_state_3[0].integration == "sensor"
    assert entities_num_state_3[0].entity_name == "sensor.temperature"
    assert entities_num_state_3[0].expected_value == {"value": "20 < __VALUE__ < 30"}
    assert end_position == 1

    # Test case 12: Numerical state trigger with above, below, and for values
    trigger_part_num_state_4 = {
        CONF_PLATFORM: CONF_NUMERIC_STATE,
        CONF_ENTITY_ID: "sensor.temperature",
        CONF_ABOVE: 20,
        CONF_BELOW: 30,
        CONF_FOR: "00:01:00",
    }
    results = _trigger_entities(trigger_part_num_state_4, position=1)
    entities_num_state_4, end_position = results
    assert len(entities_num_state_4) == 1
    assert entities_num_state_4[0].parent is None
    assert entities_num_state_4[0].position == 1
    assert entities_num_state_4[0].parameter_role == START
    assert entities_num_state_4[0].integration == "sensor"
    assert entities_num_state_4[0].entity_name == "sensor.temperature"
    assert entities_num_state_4[0].expected_value == {
        "value": "20 < __VALUE__ < 30",
        CONF_FOR: "00:01:00",
    }
    assert end_position == 1
    
    # Test case 13: Numerical state trigger with above value for an attribute
    trigger_part_num_state_5 = {
        CONF_PLATFORM: CONF_NUMERIC_STATE,
        CONF_ENTITY_ID: "sensor.temperature",
        CONF_ATTRIBUTE: "attribute_1",
        CONF_ABOVE: 20,
    }
    results = _trigger_entities(trigger_part_num_state_5, position=1)
    entities_num_state_5, end_position = results
    assert len(entities_num_state_5) == 1
    assert entities_num_state_5[0].parent is None
    assert entities_num_state_5[0].position == 1
    assert entities_num_state_5[0].parameter_role == START
    assert entities_num_state_5[0].integration == "sensor"
    assert entities_num_state_5[0].entity_name == "sensor.temperature.attribute_1"
    assert entities_num_state_5[0].expected_value == {"value": "20 < __VALUE__"}
    assert end_position == 1
           
    
     # Test case 14: State trigger with on values
    trigger_part_state_0 = {
        CONF_PLATFORM: CONF_STATE,
        CONF_ENTITY_ID: "binary_sensor.motion",
    }
    results = _trigger_entities(trigger_part_state_0, position=1)
    entities_state_0, end_position = results
    assert len(entities_state_0) == 1
    assert entities_state_0[0].parent is None
    assert entities_state_0[0].position == 1
    assert entities_state_0[0].parameter_role == START
    assert entities_state_0[0].integration == "binary_sensor"
    assert entities_state_0[0].entity_name == "binary_sensor.motion"
    assert entities_state_0[0].expected_value is None
    assert end_position == 1

    # Test case 15: State trigger with on values
    trigger_part_state_1 = {
        CONF_PLATFORM: CONF_STATE,
        CONF_ENTITY_ID: "binary_sensor.motion",
        CONF_TO: "on",
    }
    results = _trigger_entities(trigger_part_state_1, position=1)
    entities_state_1, end_position = results
    assert len(entities_state_1) == 1
    assert entities_state_1[0].parent is None
    assert entities_state_1[0].position == 1
    assert entities_state_1[0].parameter_role == START
    assert entities_state_1[0].integration == "binary_sensor"
    assert entities_state_1[0].entity_name == "binary_sensor.motion"
    assert entities_state_1[0].expected_value == {CONF_TO: "on"}
    assert end_position == 1

    # Test case 16: State trigger with from and to values
    trigger_part_state_2 = {
        CONF_PLATFORM: CONF_STATE,
        CONF_ENTITY_ID: "binary_sensor.motion",
        CONF_FROM: "off",
        CONF_TO: "on",
    }
    results = _trigger_entities(trigger_part_state_2, position=1)
    entities_state_2, end_position = results
    assert len(entities_state_2) == 1
    assert entities_state_2[0].parent is None
    assert entities_state_2[0].position == 1
    assert entities_state_2[0].parameter_role == START
    assert entities_state_2[0].integration == "binary_sensor"
    assert entities_state_2[0].entity_name == "binary_sensor.motion"
    assert entities_state_2[0].expected_value == {CONF_TO: "on", CONF_FROM: "off"}
    assert end_position == 1

    # Test case 17: State trigger with from, to, and for values
    trigger_part_state_3 = {
        CONF_PLATFORM: CONF_STATE,
        CONF_ENTITY_ID: "binary_sensor.motion",
        CONF_FROM: "off",
        CONF_TO: "on",
        CONF_FOR: "00:01:00",
    }
    results = _trigger_entities(trigger_part_state_3, position=1)
    entities_state_3, end_position = results
    assert len(entities_state_3) == 1
    assert entities_state_3[0].parent is None
    assert entities_state_3[0].position == 1
    assert entities_state_3[0].parameter_role == START
    assert entities_state_3[0].integration == "binary_sensor"
    assert entities_state_3[0].entity_name == "binary_sensor.motion"
    assert entities_state_3[0].expected_value == {
        CONF_TO: "on",
        CONF_FROM: "off",
        CONF_FOR: "00:01:00",
    }
    assert end_position == 1

    # Test case 18: State trigger with not from and not to values
    trigger_part_state_4 = {
        CONF_PLATFORM: CONF_STATE,
        CONF_ENTITY_ID: "binary_sensor.motion",
        CONF_NOT_TO: "on",
        CONF_NOT_FROM: "off",
    }
    results = _trigger_entities(trigger_part_state_4, position=1)
    entities_state_4, end_position = results
    assert len(entities_state_4) == 1
    assert entities_state_4[0].parent is None
    assert entities_state_4[0].position == 1
    assert entities_state_4[0].parameter_role == START
    assert entities_state_4[0].integration == "binary_sensor"
    assert entities_state_4[0].entity_name == "binary_sensor.motion"
    assert entities_state_4[0].expected_value == {
        CONF_NOT_TO: "on",
        CONF_NOT_FROM: "off",
    }
    assert end_position == 1

    # Test case 19: State trigger with attribute value
    trigger_part_state_5 = {
        CONF_PLATFORM: CONF_STATE,
        CONF_ENTITY_ID: "binary_sensor.motion",
        CONF_ATTRIBUTE: "attribute_1",
        CONF_TO: "temp2",
        CONF_FROM: "temp1",
    }
    results = _trigger_entities(trigger_part_state_5, position=1)
    entities_state_5, end_position = results
    assert len(entities_state_5) == 1
    assert entities_state_5[0].parent is None
    assert entities_state_5[0].position == 1
    assert entities_state_5[0].parameter_role == START
    assert entities_state_5[0].integration == "binary_sensor"
    assert entities_state_5[0].entity_name == "binary_sensor.motion.attribute_1"
    assert entities_state_5[0].expected_value == {CONF_TO: "temp2", CONF_FROM: "temp1"}
    assert end_position == 1

    # Test case 20: Sun trigger
    trigger_part_sun_1 = {CONF_PLATFORM: "sun", CONF_EVENT: "sunset"}
    results = _trigger_entities(trigger_part_sun_1, position=1)
    entities_sun_1, end_position = results
    assert len(entities_sun_1) == 1
    assert entities_sun_1[0].parent is None
    assert entities_sun_1[0].position == 1
    assert entities_sun_1[0].parameter_role == START
    assert entities_sun_1[0].integration == "sun"
    assert entities_sun_1[0].entity_name == "sun.sun"
    assert entities_sun_1[0].expected_value == {CONF_EVENT: "sunset"}
    assert end_position == 1

    # Test case 21: Sun trigger with offset
    trigger_part_sun_2 = {
        CONF_PLATFORM: "sun",
        CONF_EVENT: "sunset",
        CONF_OFFSET: "-01:00:00",
    }
    results = _trigger_entities(trigger_part_sun_2, position=1)
    entities_sun_2, end_position = results
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

    # Test case 22: Tag trigger with single device
    trigger_part_tag_1 = {
        CONF_PLATFORM: "tag",
        TAG_ID: "tag_id_1",
        CONF_DEVICE_ID: "device_id_1",
    }
    results = _trigger_entities(trigger_part_tag_1, position=1)
    entities_tag_1, end_position = results
    assert len(entities_tag_1) == 1
    assert entities_tag_1[0].parent is None
    assert entities_tag_1[0].position == 1
    assert entities_tag_1[0].parameter_role == START
    assert entities_tag_1[0].integration == "tag"
    assert entities_tag_1[0].entity_name == "tag.tag_id_1"
    assert entities_tag_1[0].expected_value == {CONF_DEVICE_ID: "device_id_1"}
    assert end_position == 1
    
    # Test case 23: Tag trigger with multiple devices
    trigger_part_tag_2 = {
        CONF_PLATFORM: "tag",
        TAG_ID: "tag_id_2",
        CONF_DEVICE_ID: ["device_id_2", "device_id_3"],
    }
    results = _trigger_entities(trigger_part_tag_2, position=1)
    entities_tag_2, end_position = results
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

    # Test case 24: Tag trigger with multiple tags and devices
    trigger_part_tag_3 = {
        CONF_PLATFORM: "tag",
        TAG_ID: ["tag_id_2", "tag_id_3"],
        CONF_DEVICE_ID: ["device_id_2", "device_id_3"],
    }
    results = _trigger_entities(trigger_part_tag_3, position=1)
    entities_tag_3, end_position = results
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

    # Test case 25: Template trigger with a value
    trigger_part_template_1 = {
        CONF_PLATFORM: "template",
        CONF_VALUE_TEMPLATE: "{% if is_state('device_tracker.paulus', 'home') %}true{% endif %}",
    }
    results = _trigger_entities(trigger_part_template_1, position=1)
    entities_template_1, end_position = results
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

    # Test case 26: Template trigger with two values
    trigger_part_template_2 = {
        CONF_PLATFORM: "template",
        CONF_VALUE_TEMPLATE: "{{ is_state('device_tracker.paulus', 'home') and is_state('device_tracker.anne_therese', 'home') }}",
    }
    results = _trigger_entities(trigger_part_template_2, position=1)
    entities_template_2, end_position = results
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
    
    # Test case 27: Template trigger with value and for
    trigger_part_template_3 = {
        CONF_PLATFORM: "template",
        CONF_VALUE_TEMPLATE: "{{ is_state('device_tracker.paulus', 'home') }}",
        CONF_FOR: "00:01:00",
    }
    results = _trigger_entities(trigger_part_template_3, position=1)
    entities_template_3, end_position = results
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

    # Test case 28: Time trigger at 06:05:02
    trigger_part_time_1 = {CONF_PLATFORM: "time", CONF_AT: "06:05:02"}
    results = _trigger_entities(trigger_part_time_1, position=1)
    entities_time_1, end_position = results
    assert len(entities_time_1) == 1
    assert entities_time_1[0].parent is None
    assert entities_time_1[0].position == 1
    assert entities_time_1[0].parameter_role == START
    assert entities_time_1[0].integration == "time"
    assert entities_time_1[0].entity_name == "time.time"
    assert entities_time_1[0].expected_value == {CONF_AT: "06:05:02"}
    assert end_position == 1
    
    # Test case 29: Time trigger at 06:05 and 06:10
    trigger_part_time_2 = {CONF_PLATFORM: "time", CONF_AT: ["06:05", "06:10"]}
    results = _trigger_entities(trigger_part_time_2, position=1)
    entities_time_2, end_position = results
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

    # Test case 30: Time pattern trigger at **:**:02 seconds
    trigger_part_time_pattern_1 = {CONF_PLATFORM: "time_pattern", SECONDS: 2}
    results = _trigger_entities(trigger_part_time_pattern_1, position=1)
    entities_time_pattern_1, end_position = results
    assert len(entities_time_1) == 1
    assert entities_time_pattern_1[0].parent is None
    assert entities_time_pattern_1[0].position == 1
    assert entities_time_pattern_1[0].parameter_role == START
    assert entities_time_pattern_1[0].integration == "time_pattern"
    assert entities_time_pattern_1[0].entity_name is not None
    assert entities_time_pattern_1[0].expected_value == {SECONDS: 2}
    assert end_position == 1

    # Test case 31: Time pattern trigger at **:02:00
    trigger_part_time_pattern_2 = {CONF_PLATFORM: "time_pattern", MINUTES: 2}
    results = _trigger_entities(trigger_part_time_pattern_2, position=1)
    entities_time_pattern_2, end_position = results
    assert len(entities_time_pattern_2) == 1
    assert entities_time_pattern_2[0].parent is None
    assert entities_time_pattern_2[0].position == 1
    assert entities_time_pattern_2[0].parameter_role == START
    assert entities_time_pattern_2[0].integration == "time_pattern"
    assert entities_time_pattern_2[0].entity_name is not None
    assert entities_time_pattern_2[0].expected_value == {MINUTES: 2}
    assert end_position == 1

    # Test case 32: Time pattern trigger at 02:00:00
    trigger_part_time_pattern_3 = {CONF_PLATFORM: "time_pattern", HOURS: 2}
    results = _trigger_entities(trigger_part_time_pattern_3, position=1)
    entities_time_pattern_3, end_position = results
    assert len(entities_time_pattern_3) == 1
    assert entities_time_pattern_3[0].parent is None
    assert entities_time_pattern_3[0].position == 1
    assert entities_time_pattern_3[0].parameter_role == START
    assert entities_time_pattern_3[0].integration == "time_pattern"
    assert entities_time_pattern_3[0].entity_name is not None
    assert entities_time_pattern_3[0].expected_value == {HOURS: 2}
    assert end_position == 1

    # Test case 33: Time pattern trigger at 06:05:02 AM with leading zero in hours
    trigger_part_time_pattern_4 = {
        CONF_PLATFORM: "time_pattern",
        HOURS: "06",
        MINUTES: "5",
        SECONDS: "2",
    }
    try:
        _trigger_entities(trigger_part_time_pattern_4, position=1)
        assert False  # The function should raise an exception
    except vol.Invalid as e:
        assert str(e) == "Leading zero in hours is not allowed"

    # Test case 34: Time pattern trigger at 6:05:02 AM with leading zero in minutes
    trigger_part_time_pattern_5 = {
        CONF_PLATFORM: "time_pattern",
        HOURS: 6,
        MINUTES: "05",
        SECONDS: 2,
    }
    try:
        _trigger_entities(trigger_part_time_pattern_5, position=1)
        assert False  # The function should raise an exception
    except vol.Invalid as e:
        assert str(e) == "Leading zero in minutes is not allowed"

    # Test case 35: Time pattern trigger at 6:05:02 AM with leading zero in seconds
    trigger_part_time_pattern_6 = {
        CONF_PLATFORM: "time_pattern",
        HOURS: 6,
        MINUTES: 5,
        SECONDS: "02",
    }
    try:
        _trigger_entities(trigger_part_time_pattern_6, position=1)
        assert False  # The function should raise an exception
    except vol.Invalid as e:
        assert str(e) == "Leading zero in seconds is not allowed"

    # Test case 36: Time pattern trigger at every 5 minutes
    trigger_part_time_pattern_7 = {CONF_PLATFORM: "time_pattern", MINUTES: "/5"}
    results = _trigger_entities(trigger_part_time_pattern_7, position=1)
    entities_time_pattern_7, end_position = results
    assert len(entities_time_pattern_7) == 1
    assert entities_time_pattern_7[0].parent is None
    assert entities_time_pattern_7[0].position == 1
    assert entities_time_pattern_7[0].parameter_role == START
    assert entities_time_pattern_7[0].integration == "time_pattern"
    assert entities_time_pattern_7[0].entity_name is not None
    assert entities_time_pattern_7[0].expected_value == {MINUTES: "/5"}
    assert end_position == 1

    # Test case 37: Trigger at the creation of a persistent notification
    trigger_part_pers_notify_1 = {
        CONF_PLATFORM: "persistent_notification",
        CONF_UPDATE_TYPE: "create",
    }
    results = _trigger_entities(trigger_part_pers_notify_1, position=1)
    entities_pers_notify_1, end_position = results
    assert len(entities_pers_notify_1) == 1
    assert entities_pers_notify_1[0].parent is None
    assert entities_pers_notify_1[0].position == 1
    assert entities_pers_notify_1[0].parameter_role == START
    assert entities_pers_notify_1[0].integration == "persistent_notification"
    assert entities_pers_notify_1[0].entity_name is not None
    assert entities_pers_notify_1[0].expected_value == {CONF_UPDATE_TYPE: "create"}
    assert end_position == 1

    # Test case 38: Trigger at the creation of a persistent notification with the id "notify_id_1"
    trigger_part_pers_notify_2 = {
        CONF_PLATFORM: "persistent_notification",
        CONF_UPDATE_TYPE: "create",
        CONF_NOFITY_ID: "notify_id_1",
    }
    results = _trigger_entities(trigger_part_pers_notify_2, position=1)
    entities_pers_notify_2, end_position = results
    assert len(entities_pers_notify_2) == 1
    assert entities_pers_notify_2[0].parent is None
    assert entities_pers_notify_2[0].position == 1
    assert entities_pers_notify_2[0].parameter_role == START
    assert entities_pers_notify_2[0].integration == "persistent_notification"
    assert (
        entities_pers_notify_2[0].entity_name == "persistent_notification.notify_id_1"
    )
    assert entities_pers_notify_2[0].expected_value == {CONF_UPDATE_TYPE: "create"}
    assert end_position == 1

    # Test case 39: Trigger at the post or get of a webhook with id "webhook_id_1"
    trigger_part_webhook_1 = {
        CONF_PLATFORM: "webhook",
        CONF_WEBHOOK_ID: "webhook_id_1",
        CONF_ALLOWED_METHODS: ["POST", "GET"],
    }
    results = _trigger_entities(trigger_part_webhook_1, position=1)
    entities_webhook_1, end_position = results
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

    # Test case 40: Trigger at the post of a webhook with id "webhook_id_2" only locally
    trigger_part_webhook_2 = {
        CONF_PLATFORM: "webhook",
        CONF_WEBHOOK_ID: "webhook_id_2",
        CONF_ALLOWED_METHODS: ["POST"],
        CONF_LOCAL: True,
    }
    results = _trigger_entities(trigger_part_webhook_2, position=1)
    entities_webhook_2, end_position = results
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

    # Test case 41: Trigger when paulus enters the home zone
    trigger_part_zone_1 = {
        CONF_PLATFORM: "zone",
        CONF_ZONE: "zone.home",
        CONF_EVENT: "enter",
        CONF_ENTITY_ID: "device_tracker.paulus",
    }
    results = _trigger_entities(trigger_part_zone_1, position=1)
    entities_zone_1, end_position = results
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

    # Test case 42: Trigger when paulus enters the home zone with a local device
    trigger_part_geo_local_1 = {
        CONF_PLATFORM: "geo_location",
        CONF_ZONE: "zone.home",
        CONF_EVENT: "enter",
        CONF_SOURCE: "geo_location-source",
    }
    results = _trigger_entities(trigger_part_geo_local_1, position=1)
    entities_geo_local_1, end_position = results
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

    # Test case 43: Trigger when device_id_1 does something
    trigger_part_device_1 = {
        CONF_PLATFORM: "device",
        CONF_DEVICE_ID: "device_id_1",
        CONF_ENTITY_ID: "test_entity_id",
        CONF_TYPE: "do something",
        CONF_DOMAIN: "domain",
    }
    results = _trigger_entities(trigger_part_device_1, position=1)
    entities_device_1, end_position = results
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

    # Test case 44: Trigger when calender_name has an event event_name
    trigger_part_calendar_1 = {
        CONF_PLATFORM: "calendar",
        CONF_ENTITY_ID: "calendar.calendar_name",
        CONF_EVENT: "event_name",
    }
    results = _trigger_entities(trigger_part_calendar_1, position=1)
    entities_calendar_1, end_position = results
    assert len(entities_calendar_1) == 1
    assert entities_calendar_1[0].parent is None
    assert entities_calendar_1[0].position == 1
    assert entities_calendar_1[0].parameter_role == START
    assert entities_calendar_1[0].integration == "calendar"
    assert entities_calendar_1[0].entity_name == "calendar.calendar_name"
    assert entities_calendar_1[0].expected_value == {CONF_EVENT: "event_name"}
    assert end_position == 1

    # Test case 45: Trigger when calender_name has an event event_name with an offset of -01:00:00
    trigger_part_calendar_2 = {
        CONF_PLATFORM: "calendar",
        CONF_ENTITY_ID: "calendar.calendar_name",
        CONF_EVENT: "event_name",
        CONF_OFFSET: "-01:00:00",
    }
    results = _trigger_entities(trigger_part_calendar_2, position=1)
    entities_calendar_2, end_position = results
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

    # Test case 46: Trigger when conversation has an intentional_name command
    trigger_part_conversation_1 = {
        CONF_PLATFORM: "conversation",
        CONF_COMMAND: "intentional_name",
    }
    results = _trigger_entities(trigger_part_conversation_1, position=1)
    entities_conversation_1, end_position = results
    assert len(entities_conversation_1) == 1
    assert entities_conversation_1[0].parent is None
    assert entities_conversation_1[0].position == 1
    assert entities_conversation_1[0].parameter_role == START
    assert entities_conversation_1[0].integration == "conversation"
    assert entities_conversation_1[0].entity_name is not None
    assert entities_conversation_1[0].expected_value == {CONF_COMMAND: "intentional_name"}
    assert end_position == 1

    # Test case 47: Trigger when conversation has a be my guest command or a intentional_name command
    trigger_part_conversation_2 = {
        CONF_PLATFORM: "conversation",
        CONF_COMMAND: ["intentional_name", "be my guest"],
    }
    results = _trigger_entities(trigger_part_conversation_2, position=1)
    entities_conversation_2, end_position = results
    assert len(entities_conversation_2) == 2
    assert entities_conversation_2[0].parent == 1
    assert entities_conversation_2[0].position == 2
    assert entities_conversation_2[0].parameter_role == START
    assert entities_conversation_2[0].integration == "conversation"
    assert entities_conversation_2[0].entity_name is not None
    assert entities_conversation_2[0].expected_value == {CONF_COMMAND: "intentional_name"}
    assert entities_conversation_2[1].position == 3
    assert entities_conversation_2[1].parameter_role == START
    assert entities_conversation_2[1].integration == "conversation"
    assert entities_conversation_2[1].entity_name is not None
    assert entities_conversation_2[1].expected_value == {CONF_COMMAND: "be my guest"}
    assert end_position == 3
        
    # Test case 48: Unsupported platform
    trigger_part_x = {CONF_PLATFORM: "unsupported"}
    results = _trigger_entities(trigger_part_x, position=1)
    entities_x, end_position = results
    assert len(entities_x) == 0

    print("All trigger test cases passed!")

def test_condition_entities():
    
    # Test case 1: Numeric state condition with below value and on entity
    condition_part_num_state_1 = {
        CONF_CONDITION: CONF_NUMERIC_STATE,
        CONF_ENTITY_ID: "sensor.temperature",
        CONF_BELOW: 30,
    }
    results = _condition_entities(condition_part_num_state_1, position=1)
    entities_num_state_1, end_position = results
    assert len(entities_num_state_1) == 1
    assert entities_num_state_1[0].parent is None
    assert entities_num_state_1[0].position == 1
    assert entities_num_state_1[0].parameter_role == INPUT
    assert entities_num_state_1[0].integration == "sensor"
    assert entities_num_state_1[0].entity_name == "sensor.temperature"
    assert entities_num_state_1[0].expected_value == {"value": "__VALUE__ < 30"}
    assert end_position == 1
    
    
    # Test case 2: Numeric state condition with above value and on entity
    condition_part_num_state_2 = {
        CONF_CONDITION: CONF_NUMERIC_STATE,
        CONF_ENTITY_ID: "sensor.temperature",
        CONF_ABOVE: 20,
    }
    results = _condition_entities(condition_part_num_state_2, position=1)
    entities_num_state_2, end_position = results
    assert len(entities_num_state_2) == 1
    
    print("All condition test cases passed!")
    

if __name__ == "__main__":
    test_trigger_entities()
    test_condition_entities()
