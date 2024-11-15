# Automation Generation

This package contains all the modules to disassemble a loaded automation configuration from a .yaml-file and create a list of all its entities. Additionally, a Python script is created that can imitate the functionality of the automation and thereby determine the outputs of variable inputs such as triggers or conditions.

The `automation_script_gen` package is responsible for generating automation scripts and the list of contained entities.
It consists of multiple scripts, each contributing to a specific part of the automation process.

The `config_dissection.py` script is the bundle of all sections and enables the holistic creation of an automation
with its entities as well as an executable automation script.

## TODO

1. At the moment there is no way to change the integration of an entity after the configuration file is disassembled. The integration in the database isn't be stored correctly in the database and the automation script can't be adjusted automaticly by changing the entity integration.

> The problem could be avoided by changing the integration prefix of the entity in the configuration yaml before it is inserted into the test environment.

2. If an entity which has no possible values stored in the database like for example: `sensor_string` the possible values has to be added for every `automation_entity` because there is currently no way to link the possible values to the entity itself.  
