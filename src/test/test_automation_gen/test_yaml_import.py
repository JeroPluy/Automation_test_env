"""
The test_yaml_import.py module contains the test functions for the home_assistant_yaml_loader.py module.
It tests the import of the test automations from the test_data/yaml_files/test_yaml directory and the
import of all the preconfigured automations from the test_data/yaml_files directory.
"""

import json
from os import listdir, path
from backend.ha_automation_utils import home_assistant_yaml_loader as yaml_loader

def check_test_yaml_dir(test_files: list = None):
    """
    This function checks if all the test yaml files of the test_data/yaml_files/test_yaml directory are included into the test.

    Raises:
        Exception: If a file is not included in the test.
    """
    test_file_dir = path.join("test_data", "yaml_files", "test_yaml")

    for file in listdir(test_file_dir):
        if file.endswith(".yaml") and test_files is not None and file not in test_files:
            raise Exception("Unknown file: " + file)


def test_import_test_automations():
    """
    Test importing all the test automations from the test_data/yaml_files/test_yaml directory
    and validate the imported dictionaries by asserting them to the expected dictionaries.
    """

    test_files = [
        "empty.yaml",
        "bare_min.yaml",
        "basis_automation.yaml",
        "entity_extraction_test.yaml",
        "huge_automation.yaml",
    ]

    check_test_yaml_dir(test_files=test_files)

    # Test loading an empty yaml file
    config_file = path.join("test_data", "yaml_files", "test_yaml", "empty.yaml")
    automation_yaml = yaml_loader.load_yaml_dict(config_file)
    assert automation_yaml is not None and automation_yaml == {}

    # Test loading a valid yaml file with the bare minimum of valid data
    config_file = path.join("test_data", "yaml_files", "test_yaml", "bare_min.yaml")
    automation_yaml = yaml_loader.load_yaml_dict(config_file)
    assert automation_yaml is not None and automation_yaml == {
        "trigger": [],
        "action": [],
    }

    # Test loading a valid yaml file with all configuration variables
    config_file = path.join(
        "test_data", "yaml_files", "test_yaml", "basis_automation.yaml"
    )
    automation_yaml = yaml_loader.load_yaml_dict(config_file)
    assert automation_yaml is not None and automation_yaml == {
        "alias": "test automation alias",
        "id": "1600000000000",
        "description": "This automation just a test automation to test the yaml file validation.",
        "initial_state": True,
        "trace": {"stored_traces": 6},
        "variables": {"testVar": "test"},
        "trigger_variables": {"testVar": "test"},
        "trigger": [
            {
                "alias": "moving object",
                "platform": "state",
                "entity_id": ["binary_sensor.moving_living_room"],
                "from": "off",
                "to": "on",
                "id": "trigger_1",
            },
            {
                "platform": "state",
                "entity_id": ["binary_sensor.person_living_room"],
                "from": "off",
                "to": "on",
                "alias": "person dectected",
                "enabled": False,
                "variables": {"testVar2": "test_2"},
            },
        ],
        "condition": [
            {
                "alias": "sun is not shining",
                "condition": "sun",
                "after": "sunrise",
            },
            {
                "condition": "state",
                "entity_id": "light.main_light_living_room",
                "state": "on",
                "alias": "light is off",
            },
        ],
        "action": [
            {
                "alias": "turn on light",
                "service": "input_boolean.turn_on",
                "data": {},
            },
            {
                "alias": "is Krista in the room",
                "condition": "state",
                "entity_id": "sensor.whos_in_living_room",
                "state": "Krista",
            },
            {
                "alias": "turn on music",
                "service": "media_player.media_play",
                "target": {"entity_id": "media_player.living_room"},
                "data": {},
            },
        ],
        "mode": "single",
        "max": 1,
        "max_exceeded": "warning",
    }

    # Test loading the test configuration file with all different types of triggers and conditions
    config_file = path.join(
        "test_data", "yaml_files", "test_yaml", "entity_extraction_test.yaml"
    )
    automation_yaml = yaml_loader.load_yaml_dict(config_file)
    assert automation_yaml is not None and automation_yaml == {
        "alias": "entity extraction test",
        "description": 'This automation is a bundle of different triggers, conditions and actions. It is used to test the parameter extraction and the automation script generation.',
        "trigger": [
            {
                "platform": "state",
                "entity_id": ["media_player.bedroom"],
                "enabled": False,
                "id": "1",
            },
            {
                "platform": "event",
                "event_type": "test",
                "id": "2",
                "event_data": {"test": "tst1"},
                "context": {"user_id": ["6f8af16663684b4db69e8ec90e6e4e42"]},
            },
            {
                "platform": "event",
                "event_type": ["test", "test2"],
                "id": "2",
                "event_data": {"test": "tst1"},
            },
            {
                "platform": "numeric_state",
                "entity_id": ["sensor.carbon_monoxide"],
                "above": 10,
                "below": 50000,
                "id": "3",
            },
            {
                "platform": "persistent_notification",
                "update_type": ["added", "removed"],
                "notification_id": "test_id",
                "id": "4",
            },
            {
                "platform": "numeric_state",
                "entity_id": ["sensor.light_living_room"],
                "for": {"hours": 0, "minutes": 10, "seconds": 0},
                "above": "sensor.carbon_dioxide",
                "below": 4000,
                "id": "5",
            },
            {
                "platform": "mqtt",
                "topic": "topic/topic",
                "payload": "test_payload",
                "qos": 1,
                "id": "6",
            },
            {
                "platform": "zone",
                "entity_id": "person.admin",
                "zone": "zone.home",
                "event": "enter",
                "id": "7",
            },
            {
                "platform": "calendar",
                "event": "start",
                "entity_id": "calendar.calendar_1",
            },
            {
                "platform": "template",
                "value_template": "{{ isState(device_tracker.demo_paulus, 'on') }}",
                "for": {"hours": 3, "minutes": 0, "seconds": 0, "milliseconds": 0},
                "id": "8",
            },
            {
                "platform": "zone",
                "entity_id": "device_tracker.demo_anne_therese",
                "zone": "zone.home",
                "event": "enter",
            },
            {
                "platform": "state",
                "entity_id": ["light.bed_light"],
                "to": "{{ states('light.atmo_lights_living_room')}}",
                "id": "12",
            },
            {
                "platform": "device",
                "type": "turned_off",
                "device_id": "7a0da52b720a09ec110abc1176236897",
                "entity_id": "39673709b7df2572bb84431e672ebef5",
                "domain": "light",
            },
            {"platform": "time_pattern", "hours": "8"},
            {
                "platform": "webhook",
                "allowed_methods": ["POST", "PUT"],
                "local_only": True,
                "webhook_id": "enitity-test-auto-ClWjVtOqwDlC4LmtIEIl8tKg",
            },
            {
                "platform": "geo_location",
                "source": "test-souce",
                "zone": "zone.home",
                "event": "enter",
            },
            {"platform": "conversation", "command": "test"},
            {
                "platform": "state",
                "entity_id": ["humidifier.hygrostat"],
                "attribute": "humidity",
                "to": [1, "20", "sensor.outside_humidity"],
            },
            {"platform": "homeassistant", "event": "start"},
            {"platform": "tag", "tag_id": "e8f49c73-5394-44e1-a6c1-9c6088840ce8"},
            {"platform": "sun", "event": "sunrise", "offset": 0},
            {"platform": "time", "at": "10:00:00"},
            {
                "platform": "state",
                "entity_id": [
                    "binary_sensor.moving_living_room",
                    "binary_sensor.basement_floor_wet",
                ],
                "not_to": "on",
            },
        ],
        "condition": [
            {
                "condition": "state",
                "entity_id": "media_player.lounge_room",
                "attribute": "device_class",
                "state": ["media_player.bedroom", "media_player.kitchen"],
            },
            {
                "condition": "state",
                "entity_id": "media_player.walkman",
                "state": "playing",
            },
            {
                "condition": "device",
                "type": "is_off",
                "device_id": "7a0da52b720a09ec110abc1176236897",
                "entity_id": "39673709b7df2572bb84431e672ebef5",
                "domain": "light",
            },
            {
                "condition": "numeric_state",
                "entity_id": "sensor.carbon_monoxide",
                "above": 5,
            },
            {"condition": "sun", "before": "sunrise", "after_offset": "55"},
            {
                "condition": "time",
                "after": "10:00:00",
                "before": "10:00:00",
                "weekday": ["mon", "sun"],
            },
            {
                "condition": "zone",
                "entity_id": [
                    "device_tracker.demo_paulus",
                    "device_tracker.demo_anne_therese",
                ],
                "zone": "zone.home",
            },
            {
                "condition": "not",
                "conditions": [
                    {
                        "condition": "and",
                        "conditions": [
                            {
                                "condition": "or",
                                "conditions": [
                                    {
                                        "condition": "device",
                                        "type": "is_off",
                                        "device_id": "7f6e169dcdf4b5ef7904aeff83333410",
                                        "entity_id": "c6ff22d2817f164c951419c23a07a12b",
                                        "domain": "switch",
                                    },
                                    {
                                        "type": "is_moist",
                                        "condition": "device",
                                        "device_id": "95d8bd3158c6e1b06af0b8442196743d",
                                        "entity_id": "aeb94a72d8da8a617a540ae7d72a2f24",
                                        "domain": "binary_sensor",
                                    },
                                ],
                            },
                            {
                                "condition": "state",
                                "entity_id": "vacuum.0_ground_floor",
                                "state": "unavailable",
                            },
                        ],
                    },
                    {
                        "condition": "numeric_state",
                        "entity_id": "sensor.carbon_dioxide",
                        "above": 10,
                    },
                ],
            },
            {"condition": "trigger", "id": ""},
            {"condition": "template", "value_template": "{{ TRUE }}"},
            {"condition": "template", "value_template": "{{ False }}"},
            {"condition": "or", "conditions": []},
            {
                "condition": "state",
                "entity_id": "light.bed_light",
                "state": "{{ states('light.atmo_lights_living_room')}}",
            },
            {"condition": "trigger", "id": ["1"]},
            {
                "condition": "zone",
                "entity_id": "device_tracker.paulus",
                "zone": "zone.home",
            },
            {"condition": "state", "entity_id": "script.lampe_togglen", "state": ""},
        ],
        "action": [
            {
                "service": "persistent_notification.create",
                "metadata": {},
                "data": {"message": "geht"},
            },
            {
                "service": "cover.set_cover_tilt_position",
                "metadata": {},
                "data": {},
                "target": {"entity_id": "cover.living_room_window"},
            },
            {
                "choose": [
                    {
                        "conditions": [
                            {
                                "condition": "zone",
                                "entity_id": "device_tracker.demo_anne_therese",
                                "zone": "zone.kuche",
                            },
                            {
                                "condition": "state",
                                "entity_id": "vacuum.0_ground_floor",
                                "state": "cleaning",
                            },
                        ],
                        "sequence": [],
                    },
                    {
                        "conditions": [
                            {
                                "condition": "numeric_state",
                                "entity_id": "sensor.light_living_room",
                                "above": 102,
                            }
                        ],
                        "sequence": [
                            {
                                "service": "fan.turn_on",
                                "metadata": {},
                                "data": {},
                                "target": {"entity_id": "fan.ceiling_fan"},
                            }
                        ],
                    },
                ],
                "default": [
                    {
                        "service": "cover.open_cover",
                        "metadata": {},
                        "data": {},
                        "target": {"entity_id": "cover.garage_door"},
                    }
                ],
            },
            {
                "repeat": {
                    "sequence": [
                        {
                            "service": "cover.set_cover_tilt_position",
                            "metadata": {},
                            "data": {},
                            "target": {"entity_id": "cover.living_room_window"},
                        },
                        {
                            "service": "alarm_control_panel.alarm_arm_night",
                            "metadata": {},
                            "data": {},
                            "target": {"entity_id": "alarm_control_panel.security"},
                        },
                    ],
                    "while": [
                        {
                            "condition": "state",
                            "entity_id": "vacuum.1_first_floor",
                            "state": "docked",
                        }
                    ],
                }
            },
            {
                "event": "test",
                "event_data": {"test": "test data", "test2": "test_data2"},
            },
            {
                "wait_for_trigger": [
                    {
                        "platform": "state",
                        "entity_id": ["binary_sensor.moving_living_room"],
                    },
                    {"platform": "state", "entity_id": ["light.bed_light"]},
                ]
            },
            {"service": "todo.update_item", "metadata": {}, "data": {}},
            {
                "type": "turn_off",
                "device_id": "7f6e169dcdf4b5ef7904aeff83333410",
                "entity_id": "c6ff22d2817f164c951419c23a07a12b",
                "domain": "switch",
            },
            {
                "wait_for_trigger": [
                    {"platform": "state", "entity_id": []},
                    {"platform": "state", "entity_id": ["light.bed_light"], "to": "on"},
                ]
            },
            {
                "condition": "state",
                "entity_id": "vacuum.2_second_floor",
                "state": "unavailable",
            },
        ],
        "mode": "single",
        "trace": {"stored_traces": 6},
    }

    # Test loading the test configuration file with alot of different types of variables, trigger, conditions and actions
    config_file = path.join(
        "test_data", "yaml_files", "test_yaml", "huge_automation.yaml"
    )
    automation_json = path.join(
        "test_data", "yaml_files", "test_yaml", "huge_automation.json"
    )
    automation_dict: dict = None
    automation_yaml = yaml_loader.load_yaml_dict(config_file)
    with open(automation_json, "r") as json_file:
        automation_dict = json.load(json_file)
    assert automation_yaml is not None and automation_yaml == automation_dict

    print("Test load_yaml_dict passed")


def test_all_preconfigured_automations():
    """
    Test importing all the preconfigured automations from the test_data/yaml_files directory and
    validate the imported dictionaries by printing them to the console.
    """

    yaml_path = path.join("test_data", "yaml_files", "example_automations")
    for dir in listdir(yaml_path):
        automation_dir = path.join(yaml_path, dir)
        print("--- " + dir + " ---")
        for file in listdir(automation_dir):
            if file.endswith(".yaml"):
                automation_yaml = yaml_loader.load_yaml_dict(path.join(automation_dir, file))
                print("\n\nTest " + file)
                assert automation_yaml is not None
                print(automation_yaml)

def test_save_automation():
    """
    Test the save_automation function from the home_assistant_yaml_loader.py module with the basis_automation.yaml file.
    """

    automation_txt = [
        'alias: test automation alias\n',
        'id: "1600000000000"\n',
        'description: >-\n',
        '  This automation just a test automation to test the yaml file validation.\n',
        'initial_state: true\n',
        'trace:\n',
        '  stored_traces: 6\n',
        'variables: \n',
        '  testVar: "test"\n',
        'trigger_variables:\n',
        '  testVar: "test"\n',
        'trigger:\n',
        '  - alias: moving object\n',
        '    platform: state\n',
        '    entity_id:\n',
        '      - binary_sensor.moving_living_room\n',
        '    from: "off"\n',
        '    to: "on"\n',
        '    id: "trigger_1"\n',
        '  - platform: state\n',
        '    entity_id:\n',
        '      - binary_sensor.person_living_room\n',
        '    from: "off"\n',
        '    to: "on"\n',
        '    alias: person dectected\n',
        '    enabled: false\n',
        '    variables:\n',
        '      testVar2: "test_2"\n',
        'condition:\n',
        '  - alias: sun is not shining\n',
        '    condition: sun\n',
        '    after: sunrise\n',
        '  - condition: state\n',
        '    entity_id: light.main_light_living_room\n',
        '    state: "on"\n',
        '    alias: light is off\n',
        'action:\n',
        '  - alias: turn on light\n',
        '    service: input_boolean.turn_on\n',
        '    data: {}\n',
        '  - alias: is Krista in the room\n',
        '    condition: state\n',
        '    entity_id: sensor.whos_in_living_room\n',
        '    state: Krista\n',
        '  - alias: turn on music\n',
        '    service: media_player.media_play\n',
        '    target:\n',
        '      entity_id: media_player.living_room\n',
        '    data: {}\n',
        'mode: single\n',
        'max: 1\n',
        'max_exceeded: warning',
    ]

    text_file_path = yaml_loader.save_automation(automation_txt)
    yaml_file_path = path.join("test_data", "yaml_files", "test_yaml", "basis_automation.yaml")
    
    with open (text_file_path, "r") as file:
        text_file = file.readlines()
    
    with open (yaml_file_path, "r") as file:
        yaml_file = file.readlines()
    
    assert text_file == yaml_file
       


if __name__ == "__main__":
    # test_import_test_automations()
    # test_all_preconfigured_automations()
    test_save_automation()
