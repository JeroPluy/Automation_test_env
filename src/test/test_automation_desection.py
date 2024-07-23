""" Test cases for automation deselection module.
    The python_path needs to be set to the src directory: (for venv) $env:PYTHONPATH = "D:\Workspace\Python\custom_Tkinker_tryout\src"

"""

from environment_package.automation_desection import _trigger_entities
from environment_package.ha_automation.home_assistant_const import CONF_ABOVE, CONF_BELOW, CONF_DEVICE_ID, CONF_ENTITY_ID, CONF_EVENT, CONF_EVENT_TYPE, CONF_FOR, CONF_FROM, CONF_NUMERICAL_STATE, CONF_OFFSET, CONF_PAYLOAD, CONF_PLATFORM, CONF_STATE, CONF_TO, CONF_VALUE_TEMPLATE, HOURS, MINUTES, SECONDS, TAG_ID
import voluptuous as vol

def test_trigger_entities():
    # Test case 1: Event trigger with single event type
    trigger_part_1 = {
        CONF_PLATFORM: CONF_EVENT,
        CONF_EVENT_TYPE: "event_type_1"
    }
    entities_1 = _trigger_entities(trigger_part_1)
    assert len(entities_1) == 1
    assert entities_1[0].integration == CONF_EVENT
    assert entities_1[0].entity_name == f"{CONF_EVENT}.event_type_1"
    assert entities_1[0].pos_value is None

    # Test case 2: Event trigger with multiple event types
    trigger_part_2 = {
        CONF_PLATFORM: CONF_EVENT,
        CONF_EVENT_TYPE: ["event_type_2", "event_type_3"]
    }
    entities_2 = _trigger_entities(trigger_part_2)
    assert len(entities_2) == 2
    assert entities_2[0].integration == CONF_EVENT
    assert entities_2[0].entity_name == f"{CONF_EVENT}.event_type_2"
    assert entities_2[0].pos_value is None
    assert entities_2[1].integration == CONF_EVENT
    assert entities_2[1].entity_name == f"{CONF_EVENT}.event_type_3"
    assert entities_2[1].pos_value is None

    # Test case 3: MQTT trigger with payload
    trigger_part_3 = {
        CONF_PLATFORM: "mqtt",
        "topic": "mqtt_topic",
        CONF_PAYLOAD: "mqtt_payload"
    }
    entities_3 = _trigger_entities(trigger_part_3)
    assert len(entities_3) == 1
    assert entities_3[0].integration == "mqtt"
    assert entities_3[0].entity_name == "mqtt.mqtt_topic"
    assert entities_3[0].pos_value == "mqtt_payload"

    # Test case 4: Numerical state trigger with above and below values
    trigger_part_4 = {
        CONF_PLATFORM: CONF_NUMERICAL_STATE,
        CONF_ENTITY_ID: "sensor.temperature",
        CONF_ABOVE: 20,
        CONF_BELOW: 30
    }
    entities_4 = _trigger_entities(trigger_part_4)
    assert len(entities_4) == 1
    assert entities_4[0].integration == "sensor"
    assert entities_4[0].entity_name == "sensor.temperature"
    assert entities_4[0].pos_value == "20 < __VALUE__ < 30"

    # Test case 5: State trigger with from, to, and for values
    trigger_part_5 = {
        CONF_PLATFORM: CONF_STATE,
        CONF_ENTITY_ID: "binary_sensor.motion",
        CONF_FROM: "off",
        CONF_TO: "on",
        CONF_FOR: "00:01:00"
    }
    entities_5 = _trigger_entities(trigger_part_5)
    assert len(entities_5) == 1
    assert entities_5[0].integration == "binary_sensor"
    assert entities_5[0].entity_name == "binary_sensor.motion"
    assert entities_5[0].pos_value == {
        CONF_TO: "on",
        CONF_FROM: "off",
        CONF_FOR: "00:01:00"
    }

    # Test case 6: Sun trigger with offset
    trigger_part_6 = {
        CONF_PLATFORM: "sun",
        CONF_EVENT: "sunset",
        CONF_OFFSET: "-01:00:00"
    }
    entities_6 = _trigger_entities(trigger_part_6)
    assert len(entities_6) == 1
    assert entities_6[0].integration == "sun"
    assert entities_6[0].entity_name == "sun.sun"
    assert entities_6[0].pos_value == {
        CONF_EVENT: "sunset",
        CONF_OFFSET: "-01:00:00"
    }

    # Test case 7: Tag trigger with single device
    trigger_part_7 = {
        CONF_PLATFORM: "tag",
        TAG_ID: "tag_id_1",
        CONF_DEVICE_ID: "device_id_1"
    }
    entities_7 = _trigger_entities(trigger_part_7)
    assert len(entities_7) == 1
    assert entities_7[0].integration == "tag"
    assert entities_7[0].entity_name == "tag.tag_id_1"
    assert entities_7[0].pos_value == {
        CONF_DEVICE_ID: "device_id_1"
    }

    # Test case 8: Tag trigger with multiple devices
    trigger_part_8 = {
        CONF_PLATFORM: "tag",
        TAG_ID: "tag_id_2",
        CONF_DEVICE_ID: ["device_id_2", "device_id_3"]
    }
    entities_8 = _trigger_entities(trigger_part_8)
    assert len(entities_8) == 1
    assert entities_8[0].integration == "tag"
    assert entities_8[0].entity_name == "tag.tag_id_2"
    assert entities_8[0].pos_value == {
        CONF_DEVICE_ID: ["device_id_2", "device_id_3"]
    }

    # Test case 9: Template trigger with a value
    trigger_part_9 = {
        CONF_PLATFORM: "template",
        CONF_VALUE_TEMPLATE: "{% if is_state('device_tracker.paulus', 'home') %}true{% endif %}",
        CONF_FOR: "00:01:00"
    }
    entities_9 = _trigger_entities(trigger_part_9)
    assert len(entities_9) == 1
    assert entities_9[0].integration == "device_tracker"
    assert entities_9[0].entity_name == "device_tracker.paulus"
    assert entities_9[0].pos_value == {
        CONF_VALUE_TEMPLATE: "{% if is_state('device_tracker.paulus', 'home') %}true{% endif %}",
        CONF_FOR: "00:01:00"
    }

    # Test case 10: Template trigger with two values
    trigger_part_10 = {
        CONF_PLATFORM: "template",
        CONF_VALUE_TEMPLATE: "{{ is_state('device_tracker.paulus', 'home') and is_state('device_tracker.anne_therese', 'home') }}",
        CONF_FOR: "00:01:00"
    }
    entities_10 = _trigger_entities(trigger_part_10)
    assert len(entities_10) == 2
    assert entities_10[0].integration == "device_tracker"
    assert entities_10[0].entity_name == "device_tracker.paulus"
    assert entities_10[0].pos_value == {
        CONF_VALUE_TEMPLATE: "{{ is_state('device_tracker.paulus', 'home') and is_state('device_tracker.anne_therese', 'home') }}",
        CONF_FOR: "00:01:00"
    }
    assert entities_10[1].integration == "device_tracker"
    assert entities_10[1].entity_name == "device_tracker.anne_therese"
    assert entities_10[1].pos_value == {
        CONF_VALUE_TEMPLATE: "{{ is_state('device_tracker.paulus', 'home') and is_state('device_tracker.anne_therese', 'home') }}",
        CONF_FOR: "00:01:00"
    }

    # Test case 11: Time pattern trigger at 6:05:02 AM
    trigger_part_11 = {
        CONF_PLATFORM: "time_pattern",
        HOURS: 6,
        MINUTES: 5,
        SECONDS: 2
    }
    entities_11 = _trigger_entities(trigger_part_11)
    assert len(entities_11) == 1
    assert entities_11[0].integration == "time_pattern"
    assert entities_11[0].entity_name == "time_pattern._"
    assert entities_11[0].pos_value == {
        HOURS: 6,
        MINUTES: 5,
        SECONDS: 2
    }

    # Test case 12: Time pattern trigger at 06:05:02 AM with leading zero in hours
    trigger_part_12 = {
        CONF_PLATFORM: "time_pattern",
        HOURS: "06",
        MINUTES: "5",
        SECONDS: "2"
    }
    try:
        entities_12 = _trigger_entities(trigger_part_12)
        assert False  # The function should raise an exception
    except vol.Invalid as e:
        assert str(e) == "Leading zero in hours is not allowed"

    # Test case 13: Time pattern trigger at 6:05:02 AM with leading zero in minutes
    trigger_part_13 = {
        CONF_PLATFORM: "time_pattern",
        HOURS: 6,
        MINUTES: "05",
        SECONDS: 2
    }
    try:
        entities_13 = _trigger_entities(trigger_part_13)
        assert False  # The function should raise an exception
    except vol.Invalid as e:
        assert str(e) == "Leading zero in minutes is not allowed"

    # Test case 14: Time pattern trigger at 6:05:02 AM with leading zero in seconds
    trigger_part_14 = {
        CONF_PLATFORM: "time_pattern",
        HOURS: 6,
        MINUTES: 5,
        SECONDS: "02"
    }
    try:
        entities_14 = _trigger_entities(trigger_part_14)
        assert False  # The function should raise an exception
    except vol.Invalid as e:
        assert str(e) == "Leading zero in seconds is not allowed"
    
    # Test case x: Unsupported platform
    trigger_part_x = {
        CONF_PLATFORM: "unsupported"
    }
    entities_x = _trigger_entities(trigger_part_x)
    assert len(entities_x) == 0

    print("All test cases passed!")

if __name__ == "__main__":
    test_trigger_entities()