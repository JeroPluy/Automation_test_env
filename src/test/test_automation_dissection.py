""" Test cases for automation deselection module.
    The python_path needs to be set to the src directory: (for venv) $env:PYTHONPATH = "D:\\Workspace\\Python\\custom_Tkinker_tryout\\src"

"""

import uuid
from environment_package.automation_dissection import _trigger_entities
from environment_package.ha_automation.home_assistant_const import CONF_ABOVE, CONF_ALLOWED_METHODS, CONF_AT, CONF_ATTRIBUTE, CONF_BELOW, CONF_COMMAND, CONF_DEVICE_ID, CONF_DOMAIN, CONF_ENTITY_ID, CONF_EVENT, CONF_EVENT_CONTEXT, CONF_EVENT_DATA, CONF_EVENT_TYPE, CONF_FOR, CONF_FROM, CONF_LOCAL, CONF_NOFITY_ID, CONF_NOT_FROM, CONF_NOT_TO, CONF_NUMERIC_STATE, CONF_OFFSET, CONF_PAYLOAD, CONF_PLATFORM, CONF_QOS, CONF_SOURCE, CONF_STATE, CONF_TO, CONF_TYPE, CONF_UPDATE_TYPE, CONF_VALUE_TEMPLATE, CONF_WEBHOOK_ID, CONF_ZONE, HOURS, MINUTES, SECONDS, TAG_ID
import voluptuous as vol

def test_trigger_entities():
    # Test case 1: Event trigger with single event type
    trigger_part_event_1 = {
        CONF_PLATFORM: CONF_EVENT,
        CONF_EVENT_TYPE: "event_type_1"
    }
    entities_event_1 = _trigger_entities(trigger_part_event_1, position=1)
    assert len(entities_event_1) == 1
    assert entities_event_1[0].integration == CONF_EVENT
    assert entities_event_1[0].entity_name != None
    assert entities_event_1[0].expected_value == {CONF_EVENT_TYPE: "event_type_1"}

    # Test case 2: Event trigger with multiple event types
    trigger_part_event_2 = {
        CONF_PLATFORM: CONF_EVENT,
        CONF_EVENT_TYPE: ["event_type_2", "event_type_3"]
    }
    entities_event_2 = _trigger_entities(trigger_part_event_2, position=1)
    assert len(entities_event_2) == 2
    assert entities_event_2[0].integration == CONF_EVENT
    assert entities_event_2[0].entity_name != None
    assert entities_event_2[0].expected_value == {CONF_EVENT_TYPE: "event_type_2"}
    assert entities_event_2[1].integration == CONF_EVENT
    assert entities_event_2[1].entity_name != None
    assert entities_event_2[1].expected_value == {CONF_EVENT_TYPE: "event_type_3"}

    trigger_part_event_3 = {
        CONF_PLATFORM: CONF_EVENT,
        CONF_EVENT_TYPE: "event_type_3",
        CONF_EVENT_DATA: {
            "key_1": "value_1",
            "key_2": "value_2"
        },
        CONF_EVENT_CONTEXT: {
            "key_3-2": [
                "value_3-2-1",
                "value_3-2-2"
            ]
        }
    }
    entities_event_3 = _trigger_entities(trigger_part_event_3, position=1)
    assert len(entities_event_3) == 1
    assert entities_event_3[0].integration == CONF_EVENT
    assert entities_event_3[0].entity_name != None
    assert entities_event_3[0].expected_value == { CONF_EVENT_TYPE : "event_type_3" ,CONF_EVENT_DATA : { "key_1": "value_1", "key_2": "value_2" }, CONF_EVENT_CONTEXT : { "key_3-2": ["value_3-2-1", "value_3-2-2"] } }
    
    # Test case 3: MQTT trigger with qos
    trigger_part_mqtt_1 = {
        CONF_PLATFORM: "mqtt",
        "topic": "mqtt_topic",
        CONF_QOS: 0
    }
    entities_mqtt_1 = _trigger_entities(trigger_part_mqtt_1, position=1)
    assert len(entities_mqtt_1) == 1
    assert entities_mqtt_1[0].integration == "mqtt"
    assert entities_mqtt_1[0].entity_name == "mqtt.mqtt_topic"
    assert entities_mqtt_1[0].expected_value == {CONF_QOS: 0}

    # Test case 4: MQTT trigger with payload
    trigger_part_mqtt_2 = {
        CONF_PLATFORM: "mqtt",
        "topic": "mqtt_topic",
        CONF_PAYLOAD: "mqtt_payload"
    }
    entities_mqtt_2 = _trigger_entities(trigger_part_mqtt_2, position=1)
    assert len(entities_mqtt_2) == 1
    assert entities_mqtt_2[0].integration == "mqtt"
    assert entities_mqtt_2[0].entity_name == "mqtt.mqtt_topic"
    assert entities_mqtt_2[0].expected_value == {CONF_PAYLOAD: "mqtt_payload"}

    # Test case 5: MQTT trigger with qos and payload
    trigger_part_mqtt_3 = {
        CONF_PLATFORM: "mqtt",
        "topic": "mqtt_topic",
        CONF_PAYLOAD: "mqtt_payload",
        CONF_QOS: 0
    }
    entities_mqtt_3 = _trigger_entities(trigger_part_mqtt_3, position=1)
    assert len(entities_mqtt_3) == 1
    assert entities_mqtt_3[0].integration == "mqtt"
    assert entities_mqtt_3[0].entity_name == "mqtt.mqtt_topic"
    assert entities_mqtt_3[0].expected_value == {CONF_PAYLOAD: "mqtt_payload", CONF_QOS: 0}


    # Test case 6: Numerical state trigger with below values
    trigger_part_num_state_1 = {
        CONF_PLATFORM: CONF_NUMERIC_STATE,
        CONF_ENTITY_ID: "sensor.temperature",
        CONF_BELOW: 30
    }
    entities_num_state_1 = _trigger_entities(trigger_part_num_state_1, position=1)
    assert len(entities_num_state_1) == 1
    assert entities_num_state_1[0].integration == "sensor"
    assert entities_num_state_1[0].entity_name == "sensor.temperature"
    assert entities_num_state_1[0].expected_value == {"value": "__VALUE__ < 30"}

    # Test case 7: Numerical state trigger with above value
    trigger_part_num_state_2 = {
        CONF_PLATFORM: CONF_NUMERIC_STATE,
        CONF_ENTITY_ID: "sensor.temperature",
        CONF_ABOVE: 20
    }
    entities_num_state_2 = _trigger_entities(trigger_part_num_state_2, position=1)
    assert len(entities_num_state_2) == 1
    assert entities_num_state_2[0].integration == "sensor"
    assert entities_num_state_2[0].entity_name == "sensor.temperature"
    assert entities_num_state_2[0].expected_value == {"value":"20 < __VALUE__"}

    # Test case 8: Numerical state trigger with above and below values
    trigger_part_num_state_3 = {
        CONF_PLATFORM: CONF_NUMERIC_STATE,
        CONF_ENTITY_ID: "sensor.temperature",
        CONF_ABOVE: 20,
        CONF_BELOW: 30
    }
    entities_num_state_3 = _trigger_entities(trigger_part_num_state_3, position=1)
    assert len(entities_num_state_3) == 1
    assert entities_num_state_3[0].integration == "sensor"
    assert entities_num_state_3[0].entity_name == "sensor.temperature"
    assert entities_num_state_3[0].expected_value == {"value":"20 < __VALUE__ < 30"}
    
    # Test case 9: Numerical state trigger with above, below, and for values
    trigger_part_num_state_4 = {
        CONF_PLATFORM: CONF_NUMERIC_STATE,
        CONF_ENTITY_ID: "sensor.temperature",
        CONF_ABOVE: 20,
        CONF_BELOW: 30,
        CONF_FOR: "00:01:00"
    }
    entities_num_state_4 = _trigger_entities(trigger_part_num_state_4, position=1)
    assert len(entities_num_state_4) == 1
    assert entities_num_state_4[0].integration == "sensor"
    assert entities_num_state_4[0].entity_name == "sensor.temperature"
    assert entities_num_state_4[0].expected_value == {"value":"20 < __VALUE__ < 30", CONF_FOR: "00:01:00"}

    # Test case 10: State trigger with on values
    trigger_part_state_1 = {
        CONF_PLATFORM: CONF_STATE,
        CONF_ENTITY_ID: "binary_sensor.motion",
        CONF_TO: "on"
    }
    entities_state_1 = _trigger_entities(trigger_part_state_1, position=1)
    assert len(entities_state_1) == 1
    assert entities_state_1[0].integration == "binary_sensor"
    assert entities_state_1[0].entity_name == "binary_sensor.motion"
    assert entities_state_1[0].expected_value == {
        CONF_TO: "on"
    }

    # Test case 11: State trigger with from and to values
    trigger_part_state_2 = {
        CONF_PLATFORM: CONF_STATE,
        CONF_ENTITY_ID: "binary_sensor.motion",
        CONF_FROM: "off",
        CONF_TO: "on"
    }
    entities_state_2 = _trigger_entities(trigger_part_state_2, position=1)
    assert len(entities_state_2) == 1
    assert entities_state_2[0].integration == "binary_sensor"
    assert entities_state_2[0].entity_name == "binary_sensor.motion"
    assert entities_state_2[0].expected_value == {
        CONF_TO: "on",
        CONF_FROM: "off"
    }

    # Test case 12: State trigger with from, to, and for values
    trigger_part_state_3 = {
        CONF_PLATFORM: CONF_STATE,
        CONF_ENTITY_ID: "binary_sensor.motion",
        CONF_FROM: "off",
        CONF_TO: "on",
        CONF_FOR: "00:01:00"
    }
    entities_state_3 = _trigger_entities(trigger_part_state_3, position=1)
    assert len(entities_state_3) == 1
    assert entities_state_3[0].integration == "binary_sensor"
    assert entities_state_3[0].entity_name == "binary_sensor.motion"
    assert entities_state_3[0].expected_value == {
        CONF_TO: "on",
        CONF_FROM: "off",
        CONF_FOR: "00:01:00"
    }

    # Test case 13: State trigger with not from and not to values
    trigger_part_state_4 = {
        CONF_PLATFORM: CONF_STATE,
        CONF_ENTITY_ID: "binary_sensor.motion",
        CONF_NOT_TO: "on",
        CONF_NOT_FROM: "off"
    }
    entities_state_4 = _trigger_entities(trigger_part_state_4, position=1)
    assert len(entities_state_4) == 1
    assert entities_state_4[0].integration == "binary_sensor"
    assert entities_state_4[0].entity_name == "binary_sensor.motion"
    assert entities_state_4[0].expected_value == {
        CONF_NOT_TO: "on",
        CONF_NOT_FROM: "off"
    }

    # Test case 14: State trigger with attribute value
    trigger_part_state_5 = {
        CONF_PLATFORM: CONF_STATE,
        CONF_ENTITY_ID: "binary_sensor.motion",
        CONF_ATTRIBUTE: "attribute_1",
        CONF_TO: "temp2",
        CONF_FROM: "temp1"
    }
    entities_state_5 = _trigger_entities(trigger_part_state_5, position=1)
    assert len(entities_state_5) == 1
    assert entities_state_5[0].integration == "binary_sensor"
    assert entities_state_5[0].entity_name == "binary_sensor.motion.attribute_1"
    assert entities_state_5[0].expected_value == {
        CONF_TO: "temp2",
        CONF_FROM: "temp1"
    }

    # Test case 15: Sun trigger
    trigger_part_sun_1 = {
        CONF_PLATFORM: "sun",
        CONF_EVENT: "sunset"
    }
    entities_sun_1 = _trigger_entities(trigger_part_sun_1, position=1)
    assert len(entities_sun_1) == 1
    assert entities_sun_1[0].integration == "sun"
    assert entities_sun_1[0].entity_name == "sun.sun"
    assert entities_sun_1[0].expected_value == {
        CONF_EVENT: "sunset"
    }

    # Test case 16: Sun trigger with offset
    trigger_part_sun_2 = {
        CONF_PLATFORM: "sun",
        CONF_EVENT: "sunset",
        CONF_OFFSET: "-01:00:00"
    }
    entities_sun_2 = _trigger_entities(trigger_part_sun_2, position=1)
    assert len(entities_sun_2) == 1
    assert entities_sun_2[0].integration == "sun"
    assert entities_sun_2[0].entity_name == "sun.sun"
    assert entities_sun_2[0].expected_value == {
        CONF_EVENT: "sunset",
        CONF_OFFSET: "-01:00:00"
    }

    # Test case 17: Tag trigger with single device
    trigger_part_tag_1 = {
        CONF_PLATFORM: "tag",
        TAG_ID: "tag_id_1",
        CONF_DEVICE_ID: "device_id_1"
    }
    entities_tag_1 = _trigger_entities(trigger_part_tag_1, position=1)
    assert len(entities_tag_1) == 1
    assert entities_tag_1[0].integration == "tag"
    assert entities_tag_1[0].entity_name == "tag.tag_id_1"
    assert entities_tag_1[0].expected_value == {
        CONF_DEVICE_ID: "device_id_1"
    }

    # Test case 18: Tag trigger with multiple devices
    trigger_part_tag_2 = {
        CONF_PLATFORM: "tag",
        TAG_ID: "tag_id_2",
        CONF_DEVICE_ID: ["device_id_2", "device_id_3"]
    }
    entities_tag_2 = _trigger_entities(trigger_part_tag_2, position=1)
    assert len(entities_tag_2) == 1
    assert entities_tag_2[0].integration == "tag"
    assert entities_tag_2[0].entity_name == "tag.tag_id_2"
    assert entities_tag_2[0].expected_value == {
        CONF_DEVICE_ID: ["device_id_2", "device_id_3"]
    }

    # Test case 19: Tag trigger with multiple tags and devices
    trigger_part_tag_3 = {	
        CONF_PLATFORM: "tag",
        TAG_ID: ["tag_id_2", "tag_id_3"],
        CONF_DEVICE_ID: ["device_id_2", "device_id_3"]
    }
    entities_tag_3 = _trigger_entities(trigger_part_tag_3, position=1)
    assert len(entities_tag_3) == 2
    assert entities_tag_3[0].integration == "tag"
    assert entities_tag_3[0].entity_name == "tag.tag_id_2"
    assert entities_tag_3[0].expected_value == {
        CONF_DEVICE_ID: ["device_id_2", "device_id_3"]
    }
    assert entities_tag_3[1].integration == "tag"
    assert entities_tag_3[1].entity_name == "tag.tag_id_3"
    assert entities_tag_3[1].expected_value == {
        CONF_DEVICE_ID: ["device_id_2", "device_id_3"]
    }

    # Test case 20: Template trigger with a value
    trigger_part_template_1 = {
        CONF_PLATFORM: "template",
        CONF_VALUE_TEMPLATE: "{% if is_state('device_tracker.paulus', 'home') %}true{% endif %}"
    }
    entities_template_1 = _trigger_entities(trigger_part_template_1, position=1)
    assert len(entities_template_1) == 1
    assert entities_template_1[0].integration == "device_tracker"
    assert entities_template_1[0].entity_name == "device_tracker.paulus"
    assert entities_template_1[0].expected_value == {
        CONF_VALUE_TEMPLATE: "{% if is_state('device_tracker.paulus', 'home') %}true{% endif %}"
    }

    # Test case 21: Template trigger with two values
    trigger_part_template_2 = {
        CONF_PLATFORM: "template",
        CONF_VALUE_TEMPLATE: "{{ is_state('device_tracker.paulus', 'home') and is_state('device_tracker.anne_therese', 'home') }}"
    }
    entities_template_2 = _trigger_entities(trigger_part_template_2, position=1)
    assert len(entities_template_2) == 2
    assert entities_template_2[0].integration == "device_tracker"
    assert entities_template_2[0].entity_name == "device_tracker.paulus"
    assert entities_template_2[0].expected_value == {
        CONF_VALUE_TEMPLATE: "{{ is_state('device_tracker.paulus', 'home') and is_state('device_tracker.anne_therese', 'home') }}"
    }
    assert entities_template_2[1].integration == "device_tracker"
    assert entities_template_2[1].entity_name == "device_tracker.anne_therese"
    assert entities_template_2[1].expected_value == {
        CONF_VALUE_TEMPLATE: "{{ is_state('device_tracker.paulus', 'home') and is_state('device_tracker.anne_therese', 'home') }}"
    }

    # Test case 22: Template trigger with value and for
    trigger_part_template_3 = {
        CONF_PLATFORM: "template",
        CONF_VALUE_TEMPLATE: "{{ is_state('device_tracker.paulus', 'home') }}",
        CONF_FOR: "00:01:00"
    }
    entities_template_3 = _trigger_entities(trigger_part_template_3, position=1)
    assert len(entities_template_3) == 1
    assert entities_template_3[0].integration == "device_tracker"
    assert entities_template_3[0].entity_name == "device_tracker.paulus"
    assert entities_template_3[0].expected_value == {
        CONF_VALUE_TEMPLATE: "{{ is_state('device_tracker.paulus', 'home') }}",
        CONF_FOR: "00:01:00"
    }

    # Test case 23: Time trigger at 06:05:02
    trigger_part_time_1 = {
        CONF_PLATFORM: "time",
        CONF_AT: "06:05:02"
    }
    entities_time_1 = _trigger_entities(trigger_part_time_1, position=1)
    assert len(entities_time_1) == 1
    assert entities_time_1[0].integration == "time"
    assert entities_time_1[0].entity_name == "time.time"
    assert entities_time_1[0].expected_value == { CONF_AT: "06:05:02" }
        
    # Test case 24: Time pattern trigger at **:**:02 seconds
    trigger_part_time_pattern_1 = {
        CONF_PLATFORM: "time_pattern",
        SECONDS: 2
    }
    entities_time_pattern_1 = _trigger_entities(trigger_part_time_pattern_1, position=1)
    assert len(entities_time_1) == 1
    assert entities_time_pattern_1[0].integration == "time_pattern"
    assert entities_time_pattern_1[0].entity_name != None
    assert entities_time_pattern_1[0].expected_value == {
        SECONDS: 2
    }

    # Test case 25: Time pattern trigger at **:02:00
    trigger_part_time_pattern_2 = {
        CONF_PLATFORM: "time_pattern",
        MINUTES: 2
    }
    entities_time_pattern_2 = _trigger_entities(trigger_part_time_pattern_2, position=1)
    assert len(entities_time_pattern_2) == 1
    assert entities_time_pattern_2[0].integration == "time_pattern"
    assert entities_time_pattern_2[0].entity_name != None
    assert entities_time_pattern_2[0].expected_value == {
        MINUTES: 2
    }

    # Test case 25: Time pattern trigger at 02:00:00
    trigger_part_time_pattern_3 = {
        CONF_PLATFORM: "time_pattern",
        HOURS: 2
    }
    entities_time_pattern_3 = _trigger_entities(trigger_part_time_pattern_3, position=1)
    assert len(entities_time_pattern_3) == 1
    assert entities_time_pattern_3[0].integration == "time_pattern"
    assert entities_time_pattern_3[0].entity_name != None
    assert entities_time_pattern_3[0].expected_value == {
        HOURS: 2
    }

    # Test case 26: Time pattern trigger at 06:05:02 AM with leading zero in hours
    trigger_part_time_pattern_4 = {
        CONF_PLATFORM: "time_pattern",
        HOURS: "06",
        MINUTES: "5",
        SECONDS: "2"
    }
    try:
        entities_time_pattern_4 = _trigger_entities(trigger_part_time_pattern_4, position=1)
        assert False  # The function should raise an exception
    except vol.Invalid as e:
        assert str(e) == "Leading zero in hours is not allowed"

    # Test case 27: Time pattern trigger at 6:05:02 AM with leading zero in minutes
    trigger_part_time_pattern_5 = {
        CONF_PLATFORM: "time_pattern",
        HOURS: 6,
        MINUTES: "05",
        SECONDS: 2
    }
    try:
        entities_time_pattern_5 = _trigger_entities(trigger_part_time_pattern_5, position=1)
        assert False  # The function should raise an exception
    except vol.Invalid as e:
        assert str(e) == "Leading zero in minutes is not allowed"

    # Test case 28: Time pattern trigger at 6:05:02 AM with leading zero in seconds
    trigger_part_time_pattern_6 = {
        CONF_PLATFORM: "time_pattern",
        HOURS: 6,
        MINUTES: 5,
        SECONDS: "02"
    }
    try:
        entities_time_pattern_6 = _trigger_entities(trigger_part_time_pattern_6, position=1)
        assert False  # The function should raise an exception
    except vol.Invalid as e:
        assert str(e) == "Leading zero in seconds is not allowed"
    
    # Test case 29: Time pattern trigger at every 5 minutes
    trigger_part_time_pattern_7 = {
        CONF_PLATFORM: "time_pattern",
        MINUTES: '/5'
    }
    entities_time_pattern_7 = _trigger_entities(trigger_part_time_pattern_7, position=1)
    assert len(entities_time_pattern_7) == 1
    assert entities_time_pattern_7[0].integration == "time_pattern"
    assert entities_time_pattern_7[0].entity_name != None
    assert entities_time_pattern_7[0].expected_value == {
        MINUTES: '/5'
    }

    # Test case 30: Trigger at the creation of a persistent notification
    trigger_part_pers_notify_1 = {
        CONF_PLATFORM: "persistent_notification",
        CONF_UPDATE_TYPE: "create"
    }
    entities_pers_notify_1 = _trigger_entities(trigger_part_pers_notify_1, position=1)
    assert len(entities_pers_notify_1) == 1
    assert entities_pers_notify_1[0].integration == "persistent_notification"
    assert entities_pers_notify_1[0].entity_name != None
    assert entities_pers_notify_1[0].expected_value == {
        CONF_UPDATE_TYPE: "create"
    }

    # Test case 31: Trigger at the creation of a persistent notification with the id "notify_id_1"
    trigger_part_pers_notify_2 = {
        CONF_PLATFORM: "persistent_notification",
        CONF_UPDATE_TYPE: "create",
        CONF_NOFITY_ID: "notify_id_1"
    }
    entities_pers_notify_2 = _trigger_entities(trigger_part_pers_notify_2, position=1)
    assert len(entities_pers_notify_2) == 1
    assert entities_pers_notify_2[0].integration == "persistent_notification"
    assert entities_pers_notify_2[0].entity_name == "persistent_notification.notify_id_1"
    assert entities_pers_notify_2[0].expected_value == {
        CONF_UPDATE_TYPE: "create"
    }

    # Test case 32: Trigger at the post or get of a webhook with id "webhook_id_1"
    trigger_part_webhook_1 = {
        CONF_PLATFORM: "webhook",
        CONF_WEBHOOK_ID: "webhook_id_1",
        CONF_ALLOWED_METHODS: ["POST", "GET"]
    }
    entities_webhook_1 = _trigger_entities(trigger_part_webhook_1, position=1)
    assert len(entities_webhook_1) == 1
    assert entities_webhook_1[0].integration == "webhook"
    assert entities_webhook_1[0].entity_name == "webhook.webhook_id_1"
    assert entities_webhook_1[0].expected_value == {
        CONF_ALLOWED_METHODS: ["POST", "GET"]
    }

    # Test case 33: Trigger at the post of a webhook with id "webhook_id_2" only locally
    trigger_part_webhook_2 = {
        CONF_PLATFORM: "webhook",
        CONF_WEBHOOK_ID: "webhook_id_2",
        CONF_ALLOWED_METHODS: ["POST"],
        CONF_LOCAL: True
    }
    entities_webhook_2 = _trigger_entities(trigger_part_webhook_2, position=1)
    assert len(entities_webhook_2) == 1
    assert entities_webhook_2[0].integration == "webhook"
    assert entities_webhook_2[0].entity_name == "webhook.webhook_id_2"
    assert entities_webhook_2[0].expected_value == {
        CONF_ALLOWED_METHODS: ["POST"],
        CONF_LOCAL: True
    }

    # Test case 34: Trigger when paulus enters the home zone
    trigger_part_zone_1 = {
        CONF_PLATFORM: "zone",
        CONF_ZONE: "zone.home",
        CONF_EVENT: "enter",
        CONF_ENTITY_ID: "device_tracker.paulus"
    }
    entities_zone_1 = _trigger_entities(trigger_part_zone_1, position=1)
    assert len(entities_zone_1) == 1
    assert entities_zone_1[0].integration == "zone"
    assert entities_zone_1[0].entity_name == "zone.home"
    assert entities_zone_1[0].expected_value == {
        CONF_EVENT: "enter",
        CONF_ENTITY_ID: "device_tracker.paulus"
    }

    # Test case 35: Trigger when paulus enters the home zone with a local device
    trigger_part_geo_local_1 = {
        CONF_PLATFORM: "geo_location",
        CONF_ZONE: "zone.home",
        CONF_EVENT: "enter",
        CONF_SOURCE: "geo_location-source"
    }
    entities_geo_local_1 = _trigger_entities(trigger_part_geo_local_1, position=1)
    assert len(entities_geo_local_1) == 1
    assert entities_geo_local_1[0].integration == "zone"
    assert entities_geo_local_1[0].entity_name == "zone.home"
    assert entities_geo_local_1[0].expected_value == {
        CONF_EVENT: "enter",
        CONF_SOURCE: "geo_location-source"
    }

    # Test case 36: Trigger when device_id_1 does something
    trigger_part_device_1 = {
        CONF_PLATFORM: "device",
        CONF_DEVICE_ID: "device_id_1",
        CONF_ENTITY_ID: "test_entity_id",
        CONF_TYPE: "do something",
        CONF_DOMAIN: "domain"
    }
    entities_device_1 = _trigger_entities(trigger_part_device_1, position=1)
    assert len(entities_device_1) == 1
    assert entities_device_1[0].integration == "device"
    assert entities_device_1[0].entity_name == "device.device_id_1"
    assert entities_device_1[0].expected_value == {
        CONF_ENTITY_ID: "test_entity_id",
        CONF_TYPE: "do something",
        CONF_DOMAIN: "domain"
    }

    # Test case 37: Trigger when calender_name has an event event_name
    trigger_part_calendar_1 = {
        CONF_PLATFORM: "calendar",
        CONF_ENTITY_ID: "calendar.calendar_name",
        CONF_EVENT: "event_name"
    }
    entities_calendar_1 = _trigger_entities(trigger_part_calendar_1, position=1)
    assert len(entities_calendar_1) == 1
    assert entities_calendar_1[0].integration == "calendar"
    assert entities_calendar_1[0].entity_name == "calendar.calendar_name"
    assert entities_calendar_1[0].expected_value == {
        CONF_EVENT: "event_name"
    }

    # Test case 38: Trigger when calender_name has an event event_name with an offset of -01:00:00
    trigger_part_calendar_2 = {
        CONF_PLATFORM: "calendar",
        CONF_ENTITY_ID: "calendar.calendar_name",
        CONF_EVENT: "event_name",
        CONF_OFFSET: "-01:00:00"
    }
    entities_calendar_2 = _trigger_entities(trigger_part_calendar_2, position=1)
    assert len(entities_calendar_2) == 1
    assert entities_calendar_2[0].integration == "calendar"
    assert entities_calendar_2[0].entity_name == "calendar.calendar_name"
    assert entities_calendar_2[0].expected_value == {
        CONF_EVENT: "event_name",
        CONF_OFFSET: "-01:00:00"
    }

    trigger_part_conversation_1 = {
        CONF_PLATFORM: "conversation",
        CONF_COMMAND: "intent_name"
    }
    entities_conversation_1 = _trigger_entities(trigger_part_conversation_1, position=1)
    assert len(entities_conversation_1) == 1
    assert entities_conversation_1[0].integration == "conversation"
    assert entities_conversation_1[0].entity_name != None
    assert entities_conversation_1[0].expected_value == {
        CONF_COMMAND: "intent_name"
    }

    # Test case x: Unsupported platform
    trigger_part_x = {
        CONF_PLATFORM: "unsupported"
    }
    entities_x = _trigger_entities(trigger_part_x, position=1)
    assert len(entities_x) == 0

    print("All test cases passed!")

if __name__ == "__main__":
    test_trigger_entities()