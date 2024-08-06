import json
import os

"""This constants are used to define different parts in the test enviroment."""

# parameter roles
START = 0
INPUT = 1
OUTPUT = 2

# autoamtion modes
SINGLE = 0
RESTART = 1
QUEUED = 2
PARALLEL = 3

# automation script path
# Load the settings.json file
SETTINGS_FILE = os.path.join('src','frontend','settings', 'settings.json')
with open(SETTINGS_FILE) as f:
    settings = json.load(f)

# Extract the automation_script_path
AUTOMATION_SCRIPT = os.path.join(*settings['automation_script_path'])

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

