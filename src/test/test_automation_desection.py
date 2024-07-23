"""Test cases for automation deselection module.
"""

from environment_package.automation_desection import trigger_entities
from environment_package.ha_automation.home_assistant_const import CONF_ABOVE, CONF_BELOW, CONF_DEVICE_ID, CONF_ENTITY_ID, CONF_EVENT, CONF_EVENT_TYPE, CONF_FOR, CONF_FROM, CONF_NUMERICAL_STATE, CONF_OFFSET, CONF_PAYLOAD, CONF_PLATFORM, CONF_STATE, CONF_TO, TAG_ID

# run test cases for trigger_entities with:
# & d:/Workspace/Python/custom_Tkinker_tryout/venv/Scripts/python.exe -m test.test_automation_desection

def test_trigger_entities():
    # Test case 1: Event trigger with single event type
    trigger_part_1 = {
        CONF_PLATFORM: CONF_EVENT,
        CONF_EVENT_TYPE: "event_type_1"
    }
    entities_1 = trigger_entities(trigger_part_1)
    assert len(entities_1) == 1
    assert entities_1[0].integration == CONF_EVENT
    assert entities_1[0].entity_name == f"{CONF_EVENT}.event_type_1"
    assert entities_1[0].pos_value is None

    # Test case 2: Event trigger with multiple event types
    trigger_part_2 = {
        CONF_PLATFORM: CONF_EVENT,
        CONF_EVENT_TYPE: ["event_type_2", "event_type_3"]
    }
    entities_2 = trigger_entities(trigger_part_2)
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
    entities_3 = trigger_entities(trigger_part_3)
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
    entities_4 = trigger_entities(trigger_part_4)
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
    entities_5 = trigger_entities(trigger_part_5)
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
    entities_6 = trigger_entities(trigger_part_6)
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
    entities_7 = trigger_entities(trigger_part_7)
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
    entities_8 = trigger_entities(trigger_part_8)
    assert len(entities_8) == 1
    assert entities_8[0].integration == "tag"
    assert entities_8[0].entity_name == "tag.tag_id_2"
    assert entities_8[0].pos_value == {
        CONF_DEVICE_ID: ["device_id_2", "device_id_3"]
    }

    # Test case 9: Unsupported platform
    trigger_part_9 = {
        CONF_PLATFORM: "unsupported"
    }
    entities_9 = trigger_entities(trigger_part_9)
    assert len(entities_9) == 0

    print("All test cases passed!")


if __name__ == "__main__":
    test_trigger_entities()