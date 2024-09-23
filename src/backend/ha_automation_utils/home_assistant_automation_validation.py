"""
The script applies different schema to the configuration directory to validate the configuration of automations in Home Assistant.

This code is partly extracted from:
    - core/homeassistant/components/trace/__init__.py : https://github.com/home-assistant/core/blob/dev/homeassistant/components/trace/__init__.py
        (VERSION: 17.05.2024 - parent 4edee94 commit 87bb7ce)
    - core/homeassistant/components/automation/config.py : https://github.com/home-assistant/core/blob/dev/homeassistant/components/automation/config.py
        (VERSION: 17.05.2024 - parent 4edee94 commit 87bb7ce)

"""

from contextlib import suppress
from enum import StrEnum
from typing import Any

import voluptuous as vol
from voluptuous.humanize import humanize_error

from .home_assistant_config_validation import (CONDITIONS_SCHEMA,
                                               SCRIPT_SCHEMA,
                                               SCRIPT_VARIABLES_SCHEMA,
                                               TRIGGER_SCHEMA, boolean, string)
from .home_assistant_const import (CONF_ACTION, CONF_ALIAS, CONF_CONDITION,
                                   CONF_DESCRIPTION, CONF_ID,
                                   CONF_INITIAL_STATE, CONF_MODE,
                                   CONF_STORED_TRACES, CONF_TRACE,
                                   CONF_TRIGGER, CONF_TRIGGER_VARIABLES,
                                   CONF_VARIABLES, DEFAULT_STORED_TRACES,
                                   SCRIPT_MODE_CHOICES, SCRIPT_MODE_SINGLE,
                                   ConfigType, make_script_schema,
                                   positive_int)

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
    UNKNOWN_TEMPLATE = "unknown_template"
    OK = "ok"


class AutomationConfig(dict):
    """
    Dummy class to allow adding attributes to the automation configuration.
    
    """

    raw_config: dict[str, Any] | None = None
    raw_blueprint_inputs: dict[str, Any] | None = None
    automation_name: str = None
    validation_status: ValidationStatus = ValidationStatus.OK
    validation_error: str | None = None


async def _async_validate_config_item(config: ConfigType, name_given: bool) -> AutomationConfig:
    """
    Validate the different parts of automation configurations.
    
    Returns:
        AutomationConfig: The automation configuration with the validation status and error.
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

    def _name_or_id(config: ConfigType) -> str:
        """Return the alias or ID of an automation as automation name."""
        if CONF_ID in config:
            return f"id_{config[CONF_ID]}".replace(" ", "_")
        elif CONF_ALIAS in config:
            return f"{config[CONF_ALIAS]}".replace(" ", "_")
        else:
            return "unnamed_automation"

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
        except (vol.Invalid, vol.MultipleInvalid) as err:
            # ID, alias or description produce an error
            automation_config = AutomationConfig()
            _set_validation_status(
                automation_config, ValidationStatus.FAILED_SCHEMA, err, config
            )
            automation_config.automation_name = "!invalid_automation"
            return automation_config

        # ID, alias and description are valid
        automation_config = AutomationConfig(minimal_config)
        automation_config.raw_blueprint_inputs = raw_blueprint_inputs
        automation_config.raw_config = raw_config
        _set_validation_status(
            automation_config, validation_status, validation_error, config
        )
        automation_config.automation_name = _name_or_id(config)
        return automation_config

    try:
        validated_config = PLATFORM_SCHEMA(config)
    except (vol.Invalid, vol.MultipleInvalid) as err:
        # print(err, "could not be validated", config)
        if err.error_message == "template (type: <class 'jinja2.exceptions.TemplateError'>) could not be validated ":
            return _minimal_config(ValidationStatus.UNKNOWN_TEMPLATE, err, config)
        return _minimal_config(ValidationStatus.FAILED_SCHEMA, err, config)

    automation_config = AutomationConfig(validated_config)
    automation_config.raw_blueprint_inputs = raw_blueprint_inputs
    automation_config.raw_config = raw_config
    if not name_given:
        automation_config.automation_name = _name_or_id(config)

    return automation_config


async def async_validate_config_item(
    config: dict[str, Any], name_given: bool=False, version: str = "latest" 
) -> AutomationConfig:
    """
    Function to await the results of the validation function
    
    Returns:
        AutomationConfig: The automation configuration with the validation status and error.
    """
    return await _async_validate_config_item(config, name_given)

