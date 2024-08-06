# Home Assistant Utilities

The functions of the programs in this package enable loading YAML configuration files for automations and validating their structure and layout. In addition, constants used in Home Assistant are initialized to enable the functions and the dissection of the configuration files.

## Usage

To use the functions in this package, follow these steps:

1. Import the necessary modules:

    ```python
    from backend.ha_automation_utils import home_assistant_yaml_loader as yaml_loader
    from backend.ha_automation_utils import (
        home_assistant_automation_validation as ha_automation_config,
    )
    ```

2. Load the YAML configuration file:

    ```python
    config_file = path.join('test_data','yaml_files', 'test_yaml', 'basis_automation.yaml')
    automation_yaml = yaml_loader.load_yaml_dict(basis_file)
    ```

3. Validate the configuration file:

    ```python
    automation_config = asyncio.run(
        ha_automation_config.async_validate_config_item(automation_yaml)
    )
    if not (automation_config.validation_status == "ok") and not (automation_config.validation_status == "unknown_template"):
        print(
            automation_config.automation_name
            + " : \t "
            + automation_config.validation_status
            + " : \t"
            + str(automation_config.validation_error)
            + "\n"
        ) 
        return None

    ```

4. Use the validated configuration in your automations or other parts of your code.

That's it! You can now load and validate YAML configuration files for your automations using the functions provided in this package.

## Contributing

If you find any issues or have suggestions for improvements, please feel free to contribute by submitting a pull request or opening an issue on the GitHub repository.

Happy automating!

## Sources and Documentations

`home_assistant_automation_validation.py`

The script applies different schema to the configuration directory to validate the configuration of automations in Home Assistant.

This code is partly extracted from:

- [core/homeassistant/components/trace/__init__.py](https://github.com/home-assistant/core/blob/dev/homeassistant/components/trace/__init__.py)
  - (VERSION: 17.05.2024 - parent 4edee94 commit 87bb7ce)
- [core/homeassistant/components/automation/config.py](https://github.com/home-assistant/core/blob/dev/homeassistant/components/automation/config.py)
  - (VERSION: 17.05.2024 - parent 4edee94 commit 87bb7ce)
  
---

`home_assistant_config_validation`

This script implements helpers for the config validation using voluptuous schemes.

This code is partly extracted from:

- [core/homeassistant/core.py](https://github.com/home-assistant/core/blob/dev/homeassistant/core.py)
  - (VERSION: 04.07.2024 - parent ad1ba1a commit d126465)
- [core/homeassistant/helpers/config_validation.py](https://github.com/home-assistant/core/blob/dev/homeassistant/helpers/config_validation.py)
  - (VERSION: 26.06.2024 - parent fcfb580 commit 6bceb8e)

---
`home_assistant_const.py`

This module provides constants and types for the yaml import and the validation of the Home Assistant configuration files.

This code is partly extracted from:

- [core/homeassistant/const.py](https://github.com/home-assistant/core/blob/dev/homeassistant/const.py)
  - (VERSION: 26.06.2024 - parent f5c640e - commit 33b4f40)
- [core/homeassistant/helpers/config_validation.py](<https://github.com/home-assistant/core/blob/dev/homeassistant/helpers/config_validation.py>)
  - (VERSION: 26.06.2024 - parent fcfb580 commit 6bceb8e)
- [core/homeassistant/core.py](https://github.com/home-assistant/core/blob/dev/homeassistant/core.py)
  - (VERSION: 04.07.2024 - parent  ad1ba1a commit d126465)
- [core/homeassistant/components/logger/const.py](https://github.com/home-assistant/core/blob/dev/homeassistant/components/logger/const.py)
  - (VERSION: 17.03.2024 - parent b8e1862 commit 929bcb9)
- [core/homeassistant/automation/const.py](https://github.com/home-assistant/core/blob/dev/homeassistant/components/automation/const.py)
  - (VERSION: 08.03.2024 - parent cb8c144 commit 2c06d4f)
- [core/homeassistant/helpers/script.py](https://github.com/home-assistant/core/blob/dev/homeassistant/helpers/script.py)
  - (VERSION: 17.07.2024 - parent a0f91d2 commit efb7bed)
- [core/homeassistant/helpers/trace/const.py](https://github.com/home-assistant/core/blob/dev/homeassistant/components/trace/const.py)
  - (VERSION: 19.10.2021 - parent 29c062f commit 961ee71)
- [core/homeassistant/helpers/typing.py](https://github.com/home-assistant/core/blob/dev/homeassistant/helpers/typing.py)
  - (VERSION: 25.06.2024 - parent 53f5dec commit b4eee16)
- [core/homeassistant/generated/countries.py](https://github.com/home-assistant/core/blob/dev/homeassistant/generated/countries.py)
  - (VERSION: 22.03.2024 - parent 1985a2a commit 2e68363)
- [core/homeassistant/generated/languages.py](https://github.com/home-assistant/core/blob/dev/homeassistant/generated/languages.py)
  - (VERSION: 27.06.2023 - parent fe28067 commit 071d3a4)
- [core/homeassistant/generated/currencies.py](https://github.com/home-assistant/core/blob/dev/homeassistant/generated/currencies.py)
  - (VERSION: 03.03.2023 - parent 4a3c0cd commit 699cc6c)
- [core/homeassistant/components/homeassistant/triggers/event.py](https://github.com/home-assistant/core/blob/dev/homeassistant/components/homeassistant/triggers/event.py)
  - (VERSION: 06.05.2024 - parent 460c05d commit b456d97)
- [core/homeassistant/components/homeassistant/triggers/state.py](https://github.com/home-assistant/core/blob/dev/homeassistant/components/homeassistant/triggers/state.py)
  - (VERSION: 04.04.2024 - parent 0f03079 commit 3c5089b)
- [core/homeassistant/components/tag/const.py](https://github.com/home-assistant/core/blob/dev/homeassistant/components/tag/const.py)
  - (VERSION: 29.05.2024 - parent f37edc2 commit 9e3e7f5)

---

`home_assistant_exception.py`

Home Assistant exception modules for handling errors in a Home Assistant context.

This code is partly extracted from:

- [core/homeassistant/exceptions.py](https://github.com/home-assistant/core/blob/dev/homeassistant/exceptions.py)
  - (Version: 01.07.2024 parent aa5ebaf commit ca55986)

---

`home_assistant_helper_classes.py`

This module contains helper classes for Home Assistant Automations.

This code is partly extracted from:

- [core/homeassistant/helpers/script_variables.py](https://github.com/home-assistant/core/blob/dev/homeassistant/helpers/script_variables.py)
  - (VERSION: 08.03.2024 - parent c773d57 commit 19ab3d6)
- [core/homeassistant/const.py](https://github.com/home-assistant/core/blob/dev/homeassistant/const.py)
  - (VERSION: 26.06.2024 - parent f5c640e - commit 33b4f40)
- [[core/homeassistant/util/yaml/objects.py]](https://github.com/home-assistant/core/blob/dev/homeassistant/util/yaml/objects.py)
  - (VERSION: 02.07.2024 - parent 0d0ca22 commit 0e52d14)
- [[core/homeassistant/helpers/template.py]](https://github.com/home-assistant/core/blob/dev/homeassistant/helpers/template.py)
  - (VERSION: 21.07.2024 - parent 0ab1ccc commit a8cbfe5)

---

`home_assistant_yaml_loader.py`

This script provides functions for loading and parsing YAML files from Home Assistant.

It is a partical copy of the original script from Home Assistant.

- [core/homeassistant/util/yaml/loader.py](https://github.com/home-assistant/core/blob/dev/homeassistant/util/yaml/loader.py)
  - (VERSION: 17.05.2024 parent 4edee94 commit 87bb7ce)

---