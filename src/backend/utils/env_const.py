"""
This module contains the constants used in the test environment beside the constants provided by Home Assistant.
"""

import json
from os import path

# parameter roles
START = 0
INPUT = 1
ACTION_INPUT = 2
OUTPUT = 3

# autoamtion modes
SINGLE = 0
RESTART = 1
QUEUED = 2
PARALLEL = 3

LATEST = "2024.08.02"

# automation script path
# Load the settings.json file
SETTINGS_FILE = path.join('src','frontend','settings', 'settings.json')
with open(SETTINGS_FILE) as f:
    settings = json.load(f)

# path to the generated automation scripts
# extracted from the settings
AUTOMATION_SCRIPT = path.join(*settings['automation_script_path'])

# path to the database of the automation test environment
DATABASE = path.join("data", "automation_test_env.sqlite")

# path to the templates for the automation script generation
TEMPLATE_PATH = path.join("src", "backend", "automation_gen", "automation_script_gen", "templates")

# needed sql-Files
INIT_FILE = path.join("src", "backend", "database", "schema", "database_creation.sql")
INTEG_DATA = path.join("src", "backend", "database", "schema", "insert_integrations.sql")

# example automation path
EXAMPLE_AUTOMATION_PATH = path.join("test_data", "yaml_files", "example_automations")
TEST_YAML_PATH = path.join("test_data", "yaml_files", "test_yaml")

# standard integrations
standard_integrations = {
    "None": 0,
    "alarm_control_panel": 1,
    "binary_sensor": 2,
    "button": 3,
    "calendar": 4,
    "camera": 5,
    "climate": 6,
    "conversation": 7,
    "cover": 8,
    "date": 9,
    "datetime": 10,
    "device_tracker": 11,
    "event": 12,
    "fan": 13,
    "humidifier": 14,
    "image": 15,
    "lawn_mower": 16,
    "light": 17,
    "lock": 18,
    "media_player": 19,
    "notify": 20,
    "number": 21,
    "remote": 22,
    "scene": 23,
    "select": 24,
    "sensor_float": 25,
    "sensor_string": 26,
    "sensor_enum": 27,
    "siren": 28,
    "stt": 29,
    "switch": 30,
    "text": 31,
    "time": 32,
    "todo": 33,
    "tts": 34,
    "update": 35,
    "vacuum": 36,
    "valve": 37,
    "wake_word": 38,
    "water_heater": 39,
    "weather": 40,
    "homeassistant": 41,
    "mqtt": 42,
    "sun": 43,
    "tag": 44,
    "time_pattern": 45,
    "persistent_notification": 46,
    "webhook": 47,
    "zone": 48,
    "device": 49,
    'trigger':50,
    'automation':51,
    'script':52,
    'person':53,
}

