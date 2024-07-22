"""The script applies different schema to the configuration directory to validate the configuration of automations in Home Assistant.

    This code is partly extracted from:
        - core/homeassistant/components/trace/__init__.py : https://github.com/home-assistant/core/blob/dev/homeassistant/components/trace/__init__.py
            (VERSION: 02.07.2024 - parent
        - core/homeassistant/components/automation/config.py : https://github.com/home-assistant/core/blob/dev/homeassistant/components/automation/config.py
            (VERSION: 17.05.2024 - parent 4edee94 commit 87bb7ce)

"""

from contextlib import suppress
from enum import StrEnum
from typing import Any, Mapping

import voluptuous as vol
from voluptuous.humanize import humanize_error

from ha_automation.home_assistant_config_validation import (CONDITIONS_SCHEMA, SCRIPT_SCHEMA,
                                              SCRIPT_VARIABLES_SCHEMA,
                                              TRIGGER_SCHEMA, boolean, string)
from ha_automation.home_assistant_const import (CONF_ACTION, CONF_ALIAS, CONF_CONDITION,
                                  CONF_DESCRIPTION, CONF_ID,
                                  CONF_INITIAL_STATE, CONF_MODE,
                                  CONF_STORED_TRACES, CONF_TRACE, CONF_TRIGGER,
                                  CONF_TRIGGER_VARIABLES, CONF_VARIABLES,
                                  DEFAULT_STORED_TRACES, SCRIPT_MODE_CHOICES,
                                  SCRIPT_MODE_SINGLE, ConfigType,
                                  make_script_schema, positive_int)


# schema for the automation mode configuration
MODE_CONFIG_SCHEMA = {
    vol.Optional(CONF_MODE, default=SCRIPT_MODE_SINGLE): SCRIPT_MODE_CHOICES
}

# ----- trace/__init__.py -----
# schema for the trace configuration
TRACE_CONFIG_SCHEMA = {
    vol.Optional(CONF_STORED_TRACES, default=DEFAULT_STORED_TRACES): positive_int
}
# -----------------------------

# ----- automation/config.py -----
# schema for the basic description keys of an automation configuration
_MINIMAL_PLATFORM_SCHEMA = vol.Schema(
    {
        CONF_ID: str,
        CONF_ALIAS: string,
        vol.Optional(CONF_DESCRIPTION): string,
    },
    extra=vol.ALLOW_EXTRA,
)

# schema of the basic parameters of an automation configuration
PLATFORM_SCHEMA = vol.All(
    make_script_schema(
        {
            # str on purpose
            CONF_ID: str,
            CONF_ALIAS: string,
            vol.Optional(CONF_DESCRIPTION): string,
            vol.Optional(CONF_TRACE, default={}): TRACE_CONFIG_SCHEMA,
            vol.Optional(CONF_INITIAL_STATE): boolean,
            vol.Required(CONF_TRIGGER): TRIGGER_SCHEMA,
            vol.Optional(CONF_CONDITION): CONDITIONS_SCHEMA,
            vol.Optional(CONF_VARIABLES): SCRIPT_VARIABLES_SCHEMA,
            vol.Optional(CONF_TRIGGER_VARIABLES): SCRIPT_VARIABLES_SCHEMA,
            vol.Required(CONF_ACTION): SCRIPT_SCHEMA,
        },
        SCRIPT_MODE_SINGLE,
    ),
)

class ValidationStatus(StrEnum):
    """
    What part produces an invalid configuration.


    """

    FAILED_ACTIONS = "failed_actions"
    FAILED_BLUEPRINT = "failed_blueprint"
    FAILED_CONDITIONS = "failed_conditions"
    FAILED_SCHEMA = "failed_schema"
    FAILED_TRIGGERS = "failed_triggers"
    OK = "ok"


class AutomationConfig(dict):
    """
    Dummy class to allow adding attributes to the automation configuration.


    """

    raw_config: dict[str, Any] | None = None
    raw_blueprint_inputs: dict[str, Any] | None = None
    automation_name: str = "Unnamed automation" 
    validation_status: ValidationStatus = ValidationStatus.OK
    validation_error: str | None = None


async def _async_validate_config_item(config: ConfigType) -> AutomationConfig:
    """
    Validate the different parts of automation configurations.
    
    """
    raw_config = None
    raw_blueprint_inputs = None
    uses_blueprint = False
    with suppress(ValueError):
        raw_config = dict(config)

    def _humanize(err: Exception, config: ConfigType) -> str:
        """Humanize vol.Invalid, stringify other exceptions."""
        if isinstance(err, vol.Invalid):
            return humanize_error(config, err)
        return str(err)

    def _set_validation_status(
        automation_config: AutomationConfig,
        validation_status: ValidationStatus,
        validation_error: Exception,
        config: ConfigType,
    ) -> None:
        """Set validation status."""
        if uses_blueprint:
            validation_status = ValidationStatus.FAILED_BLUEPRINT
        automation_config.validation_status = validation_status
        automation_config.validation_error = _humanize(validation_error, config)

    def _minimal_config(
        validation_status: ValidationStatus,
        validation_error: Exception,
        config: ConfigType,
    ) -> AutomationConfig:
        """
        Try validating id, alias and description.

        """
        try:
            minimal_config = _MINIMAL_PLATFORM_SCHEMA(config)
        except (vol.Invalid, vol.MultipleInvalid ) as err :

            # ID, alias or description produce an error
            automation_config = AutomationConfig()
            _set_validation_status(
                automation_config, ValidationStatus.FAILED_SCHEMA, err, config
                )
            automation_config.automation_name = "Invalid automation"
            return automation_config
        
        # ID, alias and description are valid
        automation_config = AutomationConfig(minimal_config)
        automation_config.raw_blueprint_inputs = raw_blueprint_inputs
        automation_config.raw_config = raw_config
        _set_validation_status(
            automation_config, validation_status, validation_error, config
        )
        return automation_config


    try:
        validated_config = PLATFORM_SCHEMA(config)
    except (vol.Invalid, vol.MultipleInvalid ) as err :
        # print(err, "could not be validated", config)
        return _minimal_config(ValidationStatus.FAILED_SCHEMA, err, config)
    
    automation_config = AutomationConfig(validated_config)
    automation_config.raw_blueprint_inputs = raw_blueprint_inputs
    automation_config.raw_config = raw_config

    # if the config is valid  
    if isinstance(config, Mapping):
        if CONF_ALIAS in config:
            automation_config.automation_name = f"Automation with alias '{config[CONF_ALIAS]}'"
        elif CONF_ID in config:
            automation_config.automation_name = f"Automation with ID '{config[CONF_ID]}'"

    return automation_config

async def async_validate_config_item(
    config: dict[str, Any],
) -> AutomationConfig:
    """
        Function to await the results of the validation function
    """
    return await _async_validate_config_item(config)


# TODO: check if the following methods are needed for the enviroment or delete them

# async def _try_async_validate_config_item(
#     config: dict[str, Any],
# ) -> AutomationConfig | None:
#     """Validate config item."""
#     try:
#         return await _async_validate_config_item(config)
#     except (vol.MultipleInvalid):
#         return None

# def extract_domain_configs(config: ConfigType, domain: str) -> Sequence[str]:
#     """Extract keys from config for given domain name.

#     Async friendly.
#     """
#     domain_configs = []
#     for key in config:
#         with suppress(vol.Invalid):
#             if domain_key(key) != domain:
#                 continue
#             domain_configs.append(key)
#     return domain_configs

# def config_per_platform(
#     config: ConfigType, domain: str
# ) -> Iterable[tuple[str | None, ConfigType]]:
#     """Break a component config into different platforms.

#     For example, will find 'switch', 'switch 2', 'switch 3', .. etc
#     Async friendly.
#     """
#     for config_key in extract_domain_configs(config, domain):
#         if not (platform_config := config[config_key]):
#             continue

#         if not isinstance(platform_config, list):
#             platform_config = [platform_config]

#         item: ConfigType
#         platform: str | None
#         for item in platform_config:
#             try:
#                 platform = item.get(CONF_PLATFORM)
#             except AttributeError:
#                 platform = None

#             yield platform, item

# def config_without_domain(config: ConfigType, domain: str) -> ConfigType:
#     """Return a config with all configuration for a domain removed."""
#     filter_keys = extract_domain_configs(config, domain)
#     return {key: value for key, value in config.items() if key not in filter_keys}

# async def async_validate_config(config: ConfigType) -> ConfigType:
#     """Validate config."""
#     # No gather here since _try_async_validate_config_item is unlikely to suspend
#     # and the cost of creating many tasks is not worth the benefit.
#     automations = list(
#         filter(
#             lambda x: x is not None,
#             [
#                 await _try_async_validate_config_item(p_config)
#                 for _, p_config in config_per_platform(config, DOMAIN)
#             ],
#         )
#     )

#     # Create a copy of the configuration with all config for current
#     # component removed and add validated config back in.
#     config = config_without_domain(config, DOMAIN)
#     config[DOMAIN] = automations

#     return config