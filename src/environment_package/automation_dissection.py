"""
This module is responsible for automating the desection of the data.

The information about the trigger functions are from:
https://www.home-assistant.io/docs/automation/trigger/
"""

import os
from environment_package.env_const import (
    AUTOMATION_SCRIPT,
    INPUT,
    OUTPUT,
    SINGLE,
    START,
)
from .ha_automation.home_assistant_automation_validation import AutomationConfig
from .ha_automation.home_assistant_const import (
    CONF_ABOVE,
    CONF_ACTION,
    CONF_ALLOWED_METHODS,
    CONF_AND,
    CONF_AT,
    CONF_ATTRIBUTE,
    CONF_BELOW,
    CONF_CALENDAR,
    CONF_COMMAND,
    CONF_CONDITION,
    CONF_CONDITIONS,
    CONF_CONVERSATION,
    CONF_DEVICE,
    CONF_DEVICE_ID,
    CONF_DOMAIN,
    CONF_ENABLED,
    CONF_ENTITY_ID,
    CONF_EVENT,
    CONF_EVENT_CONTEXT,
    CONF_EVENT_DATA,
    CONF_EVENT_TYPE,
    CONF_FOR,
    CONF_FROM,
    CONF_GEO_LOCATION,
    CONF_LOCAL,
    CONF_MAX,
    CONF_MODE,
    CONF_NOFITY_ID,
    CONF_NOT,
    CONF_NOT_FROM,
    CONF_NOT_TO,
    CONF_NUMERIC_STATE,
    CONF_OFFSET,
    CONF_OR,
    CONF_PAYLOAD,
    CONF_PERS_NOTIFICATION,
    CONF_PLATFORM,
    CONF_QOS,
    CONF_SERVICE,
    CONF_SOURCE,
    CONF_STATE,
    CONF_TEMPLATE,
    CONF_TIME,
    CONF_TIME_PATTERN,
    CONF_TO,
    CONF_TRIGGER,
    CONF_TYPE,
    CONF_UPDATE_TYPE,
    CONF_VALUE_TEMPLATE,
    CONF_WEBHOOK,
    CONF_WEBHOOK_ID,
    CONF_ZONE,
    HOURS,
    MINUTES,
    SECONDS,
    TAG_ID,
    test_leading_zero,
)
import re
import voluptuous as vol
import uuid


class Automation:
    """
    Class to represent an automation.
    """

    a_name: str = None
    autom_mode: int = None
    max_instances: int = None
    script: str = None
    project: str = None

    def __init__(
        self,
        automation_name,
        automation_script,
        project=None,
        automation_mode=SINGLE,
        max_instances=10,
    ):
        """
        Create an automation from the automation part.

        Args:
            automation_name (str): The name of the automation
            automation_mode (int): The mode of the automation
            max_instances (int): The maximum instances of the automation
            automation_script (str): The script of the automation
            project (str): The project of the automation

        Returns:
            dict: The automation as a dictionary
        """

        self.a_name = automation_name
        self.autom_mode = automation_mode
        self.max_instances = max_instances
        self.script = automation_script
        self.project = project


class Entity:
    """
    Class to represent an entity.
    """

    integration: str = None
    entity_name: str | list = None
    parameter_role: int = None
    parent: int = None
    position: int = None
    expected_value: dict = None

    def __init__(
        self,
        param_role,
        position,
        integration,
        entity_name,
        parent=None,
        expected_value=None,
    ):
        """
        Create an entity from the automation part.

        Args:
            integration (str): The integration of the entity
            entity_name (str): The name of the entity
            expected_value (int | str | dict): The possible value of the entity

        Returns:
            dict: The entity as a dictionary
        """

        self.parent = parent
        self.position = position
        self.parameter_role = param_role
        self.integration = integration
        self.entity_name = integration + "." + entity_name
        if expected_value == {} or expected_value is None:
            self.expected_value = None
        else:
            self.expected_value = expected_value.copy()

    def serialize(self):
        return {
            "integration": self.integration,
            "entity_name": self.entity_name,
            "parameter_role": self.parameter_role,
            "parent_position": self.parent,
            "position": self.position,
            "expected_value": self.expected_value,
        }


def _trigger_entities(trigger_part: dict, position: int) -> list:
    """The function creates a list of entities for one trigger list element.

    Args:
        trigger_part (dict): The trigger list element

    Returns:
        list: A list of entities as Entity objects
    """

    platform = trigger_part[CONF_PLATFORM]
    # list of entities in the trigger part
    Entity_list = []
    # entity parameter role is start
    param_role = START

    # check if the trigger is enabled
    if CONF_ENABLED in trigger_part:
        if CONF_ENABLED is False:
            return [Entity_list, position]

    # if the trigger is an event
    if platform == CONF_EVENT:
        exp_value = {}
        # if the event has a data part
        if CONF_EVENT_DATA in trigger_part:
            event_data = {}
            for data_key in trigger_part[CONF_EVENT_DATA]:
                event_data[data_key] = trigger_part[CONF_EVENT_DATA][data_key]
            exp_value[CONF_EVENT_DATA] = event_data
        if CONF_EVENT_CONTEXT in trigger_part:
            context = {}
            for context_key in trigger_part[CONF_EVENT_CONTEXT]:
                context[context_key] = trigger_part[CONF_EVENT_CONTEXT][context_key]
            exp_value[CONF_EVENT_CONTEXT] = context
        
        # if the event type has multiple event entities
        if isinstance(trigger_part[CONF_EVENT_TYPE], list):
            parent = position
            # create all entities in the trigger part
            for event_type in trigger_part[CONF_EVENT_TYPE]:
                position += 1
                exp_value[CONF_EVENT_TYPE] = event_type
                entity_name = str(uuid.uuid4())
                new_entity = Entity(
                    parent=parent,
                    position=position,
                    param_role=param_role,
                    integration=CONF_EVENT,
                    entity_name=entity_name,
                    expected_value=exp_value,
                )
                Entity_list.append(new_entity)
        else:
            # create the single entity in the event_type part
            exp_value[CONF_EVENT_TYPE] = trigger_part[CONF_EVENT_TYPE]
            entity = Entity(
                position=position,
                param_role=param_role,
                integration=CONF_EVENT,
                entity_name=str(uuid.uuid4()),
                expected_value=exp_value,
            )
            Entity_list.append(entity)

    # if is a home_assistant start or shutdown event
    elif platform == "homeassistant":
        # create the home assistant entity
        exp_value = {CONF_EVENT: trigger_part[CONF_EVENT]}
        Entity_list.append(
            Entity(
                position=position,
                param_role=param_role,
                integration="homeassistant",
                entity_name="_",
                expected_value=exp_value,
            )
        )

    # if the trigger is a mqtt message
    elif platform == "mqtt":
        exp_value = {}

        # add the payload value to the entity
        if CONF_PAYLOAD in trigger_part:
            exp_value[CONF_PAYLOAD] = trigger_part[CONF_PAYLOAD]
            if CONF_VALUE_TEMPLATE in trigger_part:
                exp_value[CONF_VALUE_TEMPLATE] = trigger_part[CONF_VALUE_TEMPLATE]

        # add the qos of payload to the entity
        if CONF_QOS in trigger_part:
            exp_value[CONF_QOS] = trigger_part[CONF_QOS]

        # create the mqtt entity
        Entity_list.append(
            Entity(
                position=position,
                param_role=param_role,
                integration="mqtt",
                entity_name=trigger_part["topic"],
                expected_value=exp_value,
            )
        )

    # if the trigger is a numerical state change
    elif platform == CONF_NUMERIC_STATE:
        # add the possible value range to the entity/ies
        exp_value_str = "__VALUE__"
        if CONF_ABOVE in trigger_part:
            exp_value_str = str(trigger_part[CONF_ABOVE]) + " < " + exp_value_str
        if CONF_BELOW in trigger_part:
            exp_value_str = exp_value_str + " < " + str(trigger_part[CONF_BELOW])
        exp_value = {"value": exp_value_str}
        # TODO value_template is missing

        # add the time the value has to stay in the trigger range
        if CONF_FOR in trigger_part:
            exp_value[CONF_FOR] = trigger_part[CONF_FOR]

        # create all entities in the trigger part
        if isinstance(trigger_part[CONF_ENTITY_ID], list):
            parent = position
            for entity in trigger_part[CONF_ENTITY_ID]:
                position += 1
                entity_integration = entity.split(".")[0]
                entity_name = entity.split(".")[1]
                if CONF_ATTRIBUTE in trigger_part:
                    entity_name = entity_name + "." + str(trigger_part[CONF_ATTRIBUTE])
                Entity_list.append(
                    Entity(
                        parent=parent,
                        position=position,
                        param_role=param_role,
                        integration=entity_integration,
                        entity_name=entity_name,
                        expected_value=exp_value,
                    )
                )
        else:
            entity_name = trigger_part[CONF_ENTITY_ID].split(".")[1]
            if CONF_ATTRIBUTE in trigger_part:
                entity_name = entity_name + "." + str(trigger_part[CONF_ATTRIBUTE])
            # create the single entity in the event_type part
            Entity_list.append(
                Entity(
                    position=position,
                    param_role=param_role,
                    integration=trigger_part[CONF_ENTITY_ID].split(".")[0],
                    entity_name=entity_name,
                    expected_value=exp_value,
                )
            )

    # if the trigger is a state change
    elif platform == CONF_STATE:
        exp_value = {}
        # add the state values of the trigger
        if CONF_TO in trigger_part:
            exp_value[CONF_TO] = str(trigger_part[CONF_TO])
        elif CONF_NOT_TO in trigger_part:
            exp_value[CONF_NOT_TO] = str(trigger_part[CONF_NOT_TO])
        if CONF_FROM in trigger_part:
            exp_value[CONF_FROM] = str(trigger_part[CONF_FROM])
        elif CONF_NOT_FROM in trigger_part:
            exp_value[CONF_NOT_FROM] = str(trigger_part[CONF_NOT_FROM])
        if CONF_FOR in trigger_part:
            exp_value[CONF_FOR] = trigger_part[CONF_FOR]

        # create all entities in the trigger part
        if isinstance(trigger_part[CONF_ENTITY_ID], list):
            parent = position
            for entity in trigger_part[CONF_ENTITY_ID]:
                position += 1
                entity_integration = entity.split(".")[0]
                entity_name = entity.split(".")[1]
                if CONF_ATTRIBUTE in trigger_part:
                    entity_name = entity_name + "." + str(trigger_part[CONF_ATTRIBUTE])
                Entity_list.append(
                    Entity(
                        parent=parent,
                        position=position,
                        param_role=param_role,
                        integration=entity_integration,
                        entity_name=entity_name,
                        expected_value=exp_value,
                    )
                )
        else:
            entity_name = trigger_part[CONF_ENTITY_ID].split(".")[1]
            if CONF_ATTRIBUTE in trigger_part:
                entity_name = entity_name + "." + str(trigger_part[CONF_ATTRIBUTE])
            # create the single entity in the event_type part
            Entity_list.append(
                Entity(
                    position=position,
                    param_role=param_role,
                    integration=trigger_part[CONF_ENTITY_ID].split(".")[0],
                    entity_name=entity_name,
                    expected_value=exp_value,
                )
            )

    # if the trigger is the sunset or sunrise event
    elif platform == "sun":
        # add the offset value of the trigger
        exp_value = {CONF_EVENT: trigger_part[CONF_EVENT]}
        if CONF_OFFSET in trigger_part:
            exp_value[CONF_OFFSET] = trigger_part[CONF_OFFSET]

        # create the sun entity
        Entity_list.append(
            Entity(
                position=position,
                param_role=param_role,
                integration="sun",
                entity_name="sun",
                expected_value=exp_value,
            )
        )

    # if the trigger is tag scan
    elif platform == "tag":
        # add the devics/s as possible values for the scan
        if CONF_DEVICE_ID in trigger_part:
            if isinstance(trigger_part[CONF_DEVICE_ID], list):
                exp_value = {CONF_DEVICE_ID: []}
                for device in trigger_part[CONF_DEVICE_ID]:
                    exp_value[CONF_DEVICE_ID].append(device)
            else:
                exp_value = {CONF_DEVICE_ID: trigger_part[CONF_DEVICE_ID]}
        else:
            exp_value = None

        # create all tag entities in the trigger part
        if isinstance(trigger_part[TAG_ID], list):
            parent = position
            for tag_id in trigger_part[TAG_ID]:
                position += 1
                Entity_list.append(
                    Entity(
                        parent= parent,
                        position=position,
                        param_role=param_role,
                        integration="tag",
                        entity_name=tag_id,
                        expected_value=exp_value,
                    )
                )
        else:
            # create the single tag entity
            Entity_list.append(
                Entity(
                    position=position,
                    param_role=param_role,
                    integration="tag",
                    entity_name=trigger_part[TAG_ID],
                    expected_value=exp_value,
                )
            )

    # if the trigger is a template
    elif platform == CONF_TEMPLATE:
        # if trigger has a template string
        if CONF_VALUE_TEMPLATE in trigger_part:
            template_str = trigger_part[CONF_VALUE_TEMPLATE]

            # check if the string is a Jinja2 template
            if "{" in template_str and (
                "{%" in template_str or "{{" in template_str or "{#" in template_str
            ):
                # add the possible value of the template
                exp_value = {CONF_VALUE_TEMPLATE: template_str}
                # TODO could be a bit more accurate than just the whole string

                # add the time the value has to stay in the trigger range
                if CONF_FOR in trigger_part:
                    exp_value[CONF_FOR] = trigger_part[CONF_FOR]

                # search for entities in the template string
                entities = re.findall(r"\w+\.\w+", template_str)
                parent = position
                for entity in entities:
                    position += 1
                    entity_integration = entity.split(".")[0]
                    entity_name = entity.split(".")[1]
                    Entity_list.append(
                        Entity(
                            parent=parent,
                            position=position,
                            param_role=param_role,
                            integration=entity_integration,
                            entity_name=entity_name,
                            expected_value=exp_value,
                        )
                    )

    # if the trigger is a time event
    elif platform == CONF_TIME:
        if isinstance(trigger_part[CONF_AT], list):
            parent = position
            for time in trigger_part[CONF_AT]:
                position += 1
                # create the time entity
                Entity_list.append(
                    Entity(
                        parent=parent,
                        position=position,
                        param_role=param_role,
                        integration=CONF_TIME,
                        entity_name=CONF_TIME,
                        expected_value={CONF_AT: time},
                    )
                )
        else:
            # create the single time entity
            Entity_list.append(
                Entity(
                    position=position,
                    param_role=param_role,
                    integration=CONF_TIME,
                    entity_name=CONF_TIME,
                    expected_value={CONF_AT: trigger_part[CONF_AT]},
                )
            )

    # if the trigger is a time pattern event
    elif platform == CONF_TIME_PATTERN:
        exp_value = {}

        if HOURS in trigger_part:
            if test_leading_zero(trigger_part[HOURS]):
                raise vol.Invalid("Leading zero in hours is not allowed")
            exp_value[HOURS] = trigger_part[HOURS]
        if MINUTES in trigger_part:
            if test_leading_zero(trigger_part[MINUTES]):
                raise vol.Invalid("Leading zero in minutes is not allowed")
            exp_value[MINUTES] = trigger_part[MINUTES]
        if SECONDS in trigger_part:
            if test_leading_zero(trigger_part[SECONDS]):
                raise vol.Invalid("Leading zero in seconds is not allowed")
            exp_value[SECONDS] = trigger_part[SECONDS]
        # create the time pattern entity
        Entity_list.append(
            Entity(
                position=position,
                param_role=param_role,
                integration=CONF_TIME_PATTERN,
                entity_name=str(uuid.uuid4()),
                expected_value=exp_value,
            )
        )

    # if the trigger is a persistant notification
    elif platform == CONF_PERS_NOTIFICATION:
        # add the notification id as the entity name
        if CONF_NOFITY_ID in trigger_part:
            entity_name = trigger_part[CONF_NOFITY_ID]
        else:
            entity_name = str(uuid.uuid4())

        # add the update type as the possible value
        exp_value = {CONF_UPDATE_TYPE: trigger_part[CONF_UPDATE_TYPE]}

        # create the persistant notification entity
        Entity_list.append(
            Entity(
                position=position,
                param_role=param_role,
                integration=CONF_PERS_NOTIFICATION,
                entity_name=entity_name,
                expected_value=exp_value,
            )
        )

    # if the trigger is a webhook
    elif platform == CONF_WEBHOOK:
        if CONF_ALLOWED_METHODS in trigger_part:
            exp_value = {CONF_ALLOWED_METHODS: trigger_part[CONF_ALLOWED_METHODS]}
            if CONF_LOCAL in trigger_part:
                exp_value[CONF_LOCAL] = trigger_part[CONF_LOCAL]

        # create the webhook entity
        Entity_list.append(
            Entity(
                position=position,
                param_role=param_role,
                integration=CONF_WEBHOOK,
                entity_name=trigger_part[CONF_WEBHOOK_ID],
                expected_value=exp_value,
            )
        )

    # if the trigger is a zone event (enter or leave)
    elif platform == CONF_ZONE:
        # add the entity id of the person and the event type as the possible value
        exp_value = {CONF_EVENT: trigger_part[CONF_EVENT]}
        exp_value[CONF_ENTITY_ID] = trigger_part[CONF_ENTITY_ID]

        # create the zone entity
        Entity_list.append(
            Entity(
                position=position,
                param_role=param_role,
                integration=CONF_ZONE,
                entity_name=trigger_part[CONF_ZONE].split(".")[1],
                expected_value=exp_value,
            )
        )

    # if the trigger is a geo location event
    elif platform == CONF_GEO_LOCATION:
        # add the entity id of the person and the event type as the possible value
        exp_value = {CONF_EVENT: trigger_part[CONF_EVENT]}
        exp_value[CONF_SOURCE] = trigger_part[CONF_SOURCE]

        # create the zone entity
        Entity_list.append(
            Entity(
                position=position,
                param_role=param_role,
                integration=CONF_ZONE,
                entity_name=trigger_part[CONF_ZONE].split(".")[1],
                expected_value=exp_value,
            )
        )

    # if the trigger is a device event
    elif platform == CONF_DEVICE:
        # add the entity id and domain as the possible value
        exp_value = {CONF_ENTITY_ID: trigger_part[CONF_ENTITY_ID]}
        exp_value[CONF_TYPE] = trigger_part[CONF_TYPE]
        exp_value[CONF_DOMAIN] = trigger_part[CONF_DOMAIN]

        # create the device entity
        Entity_list.append(
            Entity(
                position=position,
                param_role=param_role,
                integration=CONF_DEVICE,
                entity_name=trigger_part[CONF_DEVICE_ID],
                expected_value=exp_value,
            )
        )

    # if the trigger is a calendar event
    elif platform == CONF_CALENDAR:
        # add the calendar event as the possible value
        exp_value = {CONF_EVENT: trigger_part[CONF_EVENT]}
        if CONF_OFFSET in trigger_part:
            exp_value[CONF_OFFSET] = trigger_part[CONF_OFFSET]

        # create the calendar entity
        Entity_list.append(
            Entity(
                position=position,
                param_role=param_role,
                integration=CONF_CALENDAR,
                entity_name=trigger_part[CONF_ENTITY_ID].split(".")[1],
                expected_value=exp_value,
            )
        )

    # if trigger is a sentence
    elif platform == CONF_CONVERSATION:
        if isinstance(trigger_part[CONF_COMMAND], list):
            parent = position
            for command in trigger_part[CONF_COMMAND]:
                position += 1
                # create the conversation entity
                Entity_list.append(
                    Entity(
                        parent=parent,
                        position=position,
                        param_role=param_role,
                        integration=CONF_CONVERSATION,
                        entity_name=str(uuid.uuid4()),
                        expected_value={CONF_COMMAND: command},
                    )
                )
        else:
            # create the conversation entity
            Entity_list.append(
                Entity(
                    position=position,
                    param_role=param_role,
                    integration=CONF_CONVERSATION,
                    entity_name=str(uuid.uuid4()),
                    expected_value={CONF_COMMAND: trigger_part[CONF_COMMAND]},
                )
            )

    return [Entity_list, position]


def _condition_entities(condition_part: dict, position: int) -> list:
    """The function creates a list of entities for one condition list element.

    Args:
        condition_part (dict): The condition list element

    Returns:
        list: A list of entities as Entity objects
    """

    # check if the condition is a pure template
    if CONF_CONDITION in condition_part:
        condition = condition_part[CONF_CONDITION]
    else:
        condition = CONF_TEMPLATE

    # list of entities in the trigger part
    Entity_list = []
    # entity parameter role is start
    param_role = INPUT

    # check if the condition is enabled
    if CONF_ENABLED in condition_part:
        if CONF_ENABLED is False:
            return [Entity_list, position]

    if condition == CONF_OR or condition == CONF_AND or condition == CONF_NOT:
        if CONF_CONDITIONS in condition_part:
            for sub_condition in condition_part[CONF_CONDITIONS]:
                Entity_list += _condition_entities(sub_condition, position)
                if condition == CONF_OR:
                    position += 1
                    # TODO test the position increment / decrements - the or condition should have a smaller position than the and / not conditions its nested in

    elif condition == CONF_NUMERIC_STATE:
        # add the value range to the entity
        exp_value_str = "__VALUE__"
        if CONF_ABOVE in condition_part:
            exp_value_str = str(condition_part[CONF_ABOVE]) + " < " + exp_value_str
        if CONF_BELOW in condition_part:
            exp_value_str = exp_value_str + " < " + str(condition_part[CONF_BELOW])
        exp_value = {"value": exp_value_str}
        # TODO value_template is missing

        # check if multiple entities has to reach the condition
        if isinstance(condition_part[CONF_ENTITY_ID], list):
            for entity in condition_part[CONF_ENTITY_ID]:
                entity_integration = entity.split(".")[0]
                entity_name = entity.split(".")[1]
                if CONF_ATTRIBUTE in condition_part:
                    entity_name = (
                        entity_name + "." + str(condition_part[CONF_ATTRIBUTE])
                    )
                Entity_list.append(
                    Entity(
                        position=position,
                        param_role=param_role,
                        integration=entity_integration,
                        entity_name=entity_name,
                        expected_value=exp_value,
                    )
                )
        else:
            entity_name = condition_part[CONF_ENTITY_ID].split(".")[1]
            if CONF_ATTRIBUTE in condition_part:
                entity_name = entity_name + "." + str(condition_part[CONF_ATTRIBUTE])
            # create a single entity in the condion part
            Entity_list.append(
                Entity(
                    position=position,
                    param_role=param_role,
                    integration=condition_part[CONF_ENTITY_ID].split(".")[0],
                    entity_name=entity_name,
                    expected_value=exp_value,
                )
            )

    elif condition == CONF_STATE:
        # add the state value/s of the condition
        exp_value = {CONF_STATE: str(condition_part[CONF_STATE])}
        if CONF_FOR in condition_part:
            exp_value[CONF_FOR] = condition_part[CONF_FOR]

        # TODO CONF_MANY

        if isinstance(condition_part[CONF_ENTITY_ID], list):
            for entity in condition_part[CONF_ENTITY_ID]:
                entity_integration = entity.split(".")[0]
                entity_name = entity.split(".")[1]
                if CONF_ATTRIBUTE in condition_part:
                    entity_name = (
                        entity_name + "." + str(condition_part[CONF_ATTRIBUTE])
                    )
                Entity_list.append(
                    Entity(
                        position=position,
                        param_role=param_role,
                        integration=entity_integration,
                        entity_name=entity_name,
                        expected_value=exp_value,
                    )
                )
        else:
            entity_name = condition_part[CONF_ENTITY_ID].split(".")[1]
            if CONF_ATTRIBUTE in condition_part:
                entity_name = entity_name + "." + str(condition_part[CONF_ATTRIBUTE])

            # create the entity in the condition part
            Entity_list.append(
                Entity(
                    position=position,
                    param_role=param_role,
                    integration=condition_part[CONF_ENTITY_ID].split(".")[0],
                    entity_name=entity_name,
                    expected_value=exp_value,
                )
            )

    elif condition == CONF_TEMPLATE:
        if CONF_VALUE_TEMPLATE in condition:
            template_str = condition_part[CONF_VALUE_TEMPLATE]
        else:
            template_str = condition_part

        # check if the string is a Jinja2 template
        if "{" in template_str and (
            "{%" in template_str or "{{" in template_str or "{#" in template_str
        ):
            # add the possible value of the template
            exp_value = {CONF_VALUE_TEMPLATE: template_str}

            # search for entities in the template string
            entities = re.findall(r"\w+\.\w+", template_str)
            for entity in entities:
                entity_integration = entity.split(".")[0]
                entity_name = entity.split(".")[1]
                Entity_list.append(
                    Entity(
                        position=position,
                        param_role=param_role,
                        integration=entity_integration,
                        entity_name=entity_name,
                        expected_value=exp_value,
                    )
                )
        elif condition == CONF_TIME:
            # create the time entity
            Entity_list.append(
                Entity(
                    position=position,
                    param_role=param_role,
                    integration=CONF_TIME,
                    entity_name=CONF_TIME,
                    expected_value={CONF_AT: condition_part[CONF_AT]},
                )
            )

    # TODO time
    elif condition == CONF_TIME:
        pass

    # TODO trigger
    elif condition == CONF_TRIGGER:
        pass

    # TODO zone
    elif condition == CONF_ZONE:
        pass

    # TODO device
    elif condition == CONF_DEVICE:
        pass

    return [Entity_list, position]


def _action_entities(action_part: dict, position: int) -> list:
    """The function creates a list of entities for one action list element.

    Args:
        action_part (dict): The action list element

    Returns:
        list: A list of entities as Entity objects
    """

    service = action_part[CONF_SERVICE]
    # list of entities in the trigger part
    Entity_list = []
    # entity parameter role is start
    param_role = OUTPUT

    # check if the action is enabled
    if CONF_ENABLED in action_part:
        if CONF_ENABLED is False:
            return [Entity_list,position]

    pass


def _extract_all_trigger(automation_config: AutomationConfig) -> list:
    """
    Extracts the trigger from the data.

    Args:
        automation_config (AutomationConfig): The automation configuration data.

    Returns:
        list: A list of trigger entities extracted from the data.
    """
    trigger_entities = []
    triggers = automation_config[CONF_TRIGGER]
    position = 0
    for trigger in triggers:
        return_list = _trigger_entities(trigger, position)
        trigger_entities += return_list[0]
        position = return_list[1] + 1
    return trigger_entities


def _extract_all_conditions(automation_config: AutomationConfig) -> list:
    """
    Extract the condition from the data.
    """
    condition_entities = []
    conditions = automation_config[CONF_CONDITION]
    position = 0
    for condition in conditions:
        condition_entities += _condition_entities(condition, position)
        position += 1
    return condition_entities


def _extract_all_actions(automation_config: AutomationConfig) -> list:
    """
    Extract the action from the data.
    """
    action_entities = []
    actions = automation_config[CONF_ACTION]
    position = 0
    for action in actions:
        action_entities += _action_entities(action, position)
        position += 1
    return action_entities


def create_entity_list(automation_config: AutomationConfig) -> list:
    """
    Create a list of entities from the automation configuration.
    """
    Entity_list = []
    Entity_list += _extract_all_trigger(automation_config)
    Entity_list += _extract_all_conditions(automation_config)
    # Entity_list += _extract_all_actions(automation_config)
    return Entity_list


def _create_automation_script(automation_config: AutomationConfig) -> str:
    """
    Create the automation script which simulates the automation.

    Args:
        automation_config (AutomationConfig): The automation configuration data.
    """
    file_name = automation_config.automation_name + ".py"
    filepath = os.path.join(AUTOMATION_SCRIPT, file_name)

    script_content = """
import sys
import json

# Argumente auslesen
serialized_entities = sys.argv[1]
    
entities_list = json.loads(serialized_entities)
    
for item in entities_list:
    # print(item)   
"""

    with open(filepath, "w") as script:
        script.write(script_content)
    return filepath


def create_automation(automation_config: AutomationConfig) -> Automation:
    """
    Create an automation from the automation configuration.
    """
    automation_name = automation_config.automation_name
    automation_script = _create_automation_script(automation_config)

    if CONF_MODE in automation_config:
        mode = automation_config[CONF_MODE]
    else:
        mode = SINGLE

    if CONF_MAX in automation_config:
        max_instances = automation_config[CONF_MAX]
    else:
        max_instances = 10

    automation = Automation(
        automation_name=automation_name,
        automation_script=automation_script,
        automation_mode=mode,
        max_instances=max_instances,
    )
    return automation


def dissect_information(automation_config: AutomationConfig) -> dict:
    """
    Extract the information from the data.
    """
    automation_data = {}
    automation_data["entities"] = create_entity_list(automation_config)
    automation_data["infos"] = create_automation(automation_config)
    return automation_data
