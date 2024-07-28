"""
This module is responsible for automating the desection of the data.

The information about the trigger functions are from:
https://www.home-assistant.io/docs/automation/trigger/

The information about the condition functions are from:
https://www.home-assistant.io/docs/scripts/conditions

The information about the action functions are from:
https://www.home-assistant.io/docs/scripts
"""

from environment_package.env_const import (
    INPUT,
    OUTPUT,
    SINGLE,
    START,
)
from .ha_automation.home_assistant_automation_validation import AutomationConfig
from .ha_automation.home_assistant_const import (
    ATTR_AREA_ID,
    CONF_ABOVE,
    CONF_ACTION,
    CONF_AFTER,
    CONF_AFTER_OFFSET,
    CONF_ALLOWED_METHODS,
    CONF_AND,
    CONF_AT,
    CONF_ATTRIBUTE,
    CONF_BEFORE,
    CONF_BEFORE_OFFSET,
    CONF_BELOW,
    CONF_CALENDAR,
    CONF_CHOOSE,
    CONF_COMMAND,
    CONF_CONDITION,
    CONF_CONDITIONS,
    CONF_CONVERSATION,
    CONF_DATETIME,
    CONF_DEFAULT,
    CONF_DEVICE,
    CONF_DEVICE_ID,
    CONF_DOMAIN,
    CONF_ELSE,
    CONF_ENABLED,
    CONF_ENTITY_ID,
    CONF_EVENT,
    CONF_EVENT_CONTEXT,
    CONF_EVENT_DATA,
    CONF_EVENT_TYPE,
    CONF_FOR,
    CONF_FROM,
    CONF_GEO_LOCATION,
    CONF_ID,
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
    CONF_PARALLEL,
    CONF_PAYLOAD,
    CONF_PERS_NOTIFICATION,
    CONF_PLATFORM,
    CONF_QOS,
    CONF_REPEAT,
    CONF_SEQUENCE,
    CONF_SERVICE,
    CONF_SERVICE_DATA,
    CONF_SOURCE,
    CONF_STATE,
    CONF_TARGET,
    CONF_TEMPLATE,
    CONF_THEN,
    CONF_TIME,
    CONF_TIME_PATTERN,
    CONF_TO,
    CONF_TRIGGER,
    CONF_TYPE,
    CONF_UNTIL,
    CONF_UPDATE_TYPE,
    CONF_VALUE_TEMPLATE,
    CONF_VARIABLES,
    CONF_WEBHOOK,
    CONF_WEBHOOK_ID,
    CONF_WEEKDAY,
    CONF_WHILE,
    CONF_ZONE,
    HOURS,
    MINUTES,
    SCRIPT_ACTION_IF,
    SCRIPT_ACTION_WAIT_FOR_TRIGGER,
    SCRIPT_ACTION_WAIT_TEMPLATE,
    SECONDS,
    TAG_ID,
    test_leading_zero,
)
from environment_package.automation_script_gen import create_automation_script
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


def _is_jinja_template(template_str: str) -> bool:
    return "{" in template_str and (
        "{%" in template_str or "{{" in template_str or "{#" in template_str
    )


def _trigger_entities(trigger_part: dict, position: int) -> list:
    """The function creates a list of entities for one trigger list element.

    Args:
        trigger_part (dict): The trigger list element
        position (int): The position of the entity in the list

    Returns:
        list: A list of entities as Entity objects
    """

    platform = trigger_part[CONF_PLATFORM]
    # list of entities in the trigger part
    Entity_list = []
    # entity parameter role is start
    param_role = START

    # check if the trigger is enabled
    if f'{CONF_ENABLED}:' in trigger_part:
        if trigger_part[CONF_ENABLED] is False:
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
                # TODO limited templating as input
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
            # TODO limited templating
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

        # TODO value_template is missing

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
            # TODO extract entity input
        if CONF_BELOW in trigger_part:
            exp_value_str = exp_value_str + " < " + str(trigger_part[CONF_BELOW])
            # TODO extract entity input
        exp_value = {"value": exp_value_str}
        # TODO value_template is missing

        # add the time the value has to stay in the trigger range
        if CONF_FOR in trigger_part:
            exp_value[CONF_FOR] = trigger_part[CONF_FOR]
            # TODO limited templating as input

        # create all entities in the trigger part
        if (
            isinstance(trigger_part[CONF_ENTITY_ID], list)
            and len(trigger_part[CONF_ENTITY_ID]) > 1
        ):
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
            if isinstance(trigger_part[CONF_ENTITY_ID], list):
                entity_name = trigger_part[CONF_ENTITY_ID][0].split(".")[1]
                integration = trigger_part[CONF_ENTITY_ID][0].split(".")[0]
            else:
                entity_name = trigger_part[CONF_ENTITY_ID].split(".")[1]
                integration = trigger_part[CONF_ENTITY_ID].split(".")[0]

            if CONF_ATTRIBUTE in trigger_part:
                entity_name = entity_name + "." + str(trigger_part[CONF_ATTRIBUTE])
            # create the single entity in the event_type part
            Entity_list.append(
                Entity(
                    position=position,
                    param_role=param_role,
                    integration=integration,
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
            # TODO limited templating as input

        # create all entities in the trigger part
        if (
            isinstance(trigger_part[CONF_ENTITY_ID], list)
            and len(trigger_part[CONF_ENTITY_ID]) > 1
        ):
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
            if isinstance(trigger_part[CONF_ENTITY_ID], list):
                if len(trigger_part[CONF_ENTITY_ID]) == 0:
                    return [Entity_list, position]
                entity_name = trigger_part[CONF_ENTITY_ID][0].split(".")[1]
                integration = trigger_part[CONF_ENTITY_ID][0].split(".")[0]
            else:
                entity_name = trigger_part[CONF_ENTITY_ID].split(".")[1]
                integration = trigger_part[CONF_ENTITY_ID].split(".")[0]
            if CONF_ATTRIBUTE in trigger_part:
                entity_name = entity_name + "." + str(trigger_part[CONF_ATTRIBUTE])
            # create the single entity in the event_type part
            Entity_list.append(
                Entity(
                    position=position,
                    param_role=param_role,
                    integration=integration,
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
                        parent=parent,
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
            if _is_jinja_template(template_str):
                # add the possible value of the template
                exp_value = {CONF_VALUE_TEMPLATE: template_str}
                # TODO could be a bit more accurate than just the whole string

                # add the time the value has to stay in the trigger range
                if CONF_FOR in trigger_part:
                    exp_value[CONF_FOR] = trigger_part[CONF_FOR]
                    # TODO limited templating as input

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
        # TODO extract entity input in AT
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


def _condition_entities(
    condition_part: dict, position: int, parent: int = None
) -> list:
    """The function creates a list of entities for one condition list element.

    Args:
        condition_part (dict): The condition list element
        position (int): The position of the entity in the list
        parent (int): The parent entity of the entity

    Returns:
        list: A list of entities as Entity objects
    """

    # list of entities in the trigger part
    Entity_list = []
    # entity parameter role is start
    param_role = INPUT

    # check if the condition is enabled

    if f'{CONF_ENABLED}:' in condition_part:
        if condition_part[CONF_ENABLED] is False:
            return [Entity_list, position]

    # check if the condition is a pure template
    if len(condition_part) > 1 and not isinstance(condition_part, str):
        if CONF_CONDITION in condition_part:
            condition = condition_part[CONF_CONDITION]
    else:
        condition = CONF_TEMPLATE

    if condition == CONF_OR or condition == CONF_AND or condition == CONF_NOT:
        if CONF_CONDITIONS in condition_part:
            new_parent = position
            for sub_condition in condition_part[CONF_CONDITIONS]:
                position += 1
                result_list = _condition_entities(
                    sub_condition, position, parent=new_parent
                )
                Entity_list += result_list[0]
                position = result_list[1]

    elif condition == CONF_NUMERIC_STATE:
        # add the value range to the entity
        exp_value_str = "__VALUE__"
        if CONF_ABOVE in condition_part:
            exp_value_str = str(condition_part[CONF_ABOVE]) + " < " + exp_value_str
            # TODO extract entity input
        if CONF_BELOW in condition_part:
            exp_value_str = exp_value_str + " < " + str(condition_part[CONF_BELOW])
            # TODO extract entity input
        exp_value = {"value": exp_value_str}
        # TODO value_template is missing

        # check if multiple entities has to reach the condition
        if (
            isinstance(condition_part[CONF_ENTITY_ID], list)
            and len(condition_part[CONF_ENTITY_ID]) > 1
        ):
            # create a virtual and block
            new_parent = position
            # create all entities in the condition part under a new parent
            for entity in condition_part[CONF_ENTITY_ID]:
                position += 1
                entity_integration = entity.split(".")[0]
                entity_name = entity.split(".")[1]
                if CONF_ATTRIBUTE in condition_part:
                    entity_name = (
                        entity_name + "." + str(condition_part[CONF_ATTRIBUTE])
                    )
                Entity_list.append(
                    Entity(
                        parent=new_parent,
                        position=position,
                        param_role=param_role,
                        integration=entity_integration,
                        entity_name=entity_name,
                        expected_value=exp_value,
                    )
                )
        else:
            if isinstance(condition_part[CONF_ENTITY_ID], list):
                if len(condition_part[CONF_ENTITY_ID]) == 0:
                    return [Entity_list, position]
                entity_name = condition_part[CONF_ENTITY_ID][0].split(".")[1]
                integration = condition_part[CONF_ENTITY_ID][0].split(".")[0]
            else:
                entity_name = condition_part[CONF_ENTITY_ID].split(".")[1]
                integration = condition_part[CONF_ENTITY_ID].split(".")[0]
            if CONF_ATTRIBUTE in condition_part:
                entity_name = entity_name + "." + str(condition_part[CONF_ATTRIBUTE])
            # create a single entity in the condion part
            Entity_list.append(
                Entity(
                    parent=parent,
                    position=position,
                    param_role=param_role,
                    integration=integration,
                    entity_name=entity_name,
                    expected_value=exp_value,
                )
            )

    elif condition == CONF_STATE:
        # add the state value/s of the condition
        exp_value = {CONF_STATE: condition_part[CONF_STATE]}
        if CONF_FOR in condition_part:
            exp_value[CONF_FOR] = condition_part[CONF_FOR]
            # TODO limited templating as input

        if (
            isinstance(condition_part[CONF_ENTITY_ID], list)
            and len(condition_part[CONF_ENTITY_ID]) > 1
        ):
            # create a virtual and / or block
            new_parent = position
            # create all entities in the condition part under a new parent
            for entity in condition_part[CONF_ENTITY_ID]:
                position += 1
                entity_integration = entity.split(".")[0]
                entity_name = entity.split(".")[1]
                if CONF_ATTRIBUTE in condition_part:
                    entity_name = (
                        entity_name + "." + str(condition_part[CONF_ATTRIBUTE])
                    )
                Entity_list.append(
                    Entity(
                        parent=new_parent,
                        position=position,
                        param_role=param_role,
                        integration=entity_integration,
                        entity_name=entity_name,
                        expected_value=exp_value,
                    )
                )
        else:
            if isinstance(condition_part[CONF_ENTITY_ID], list):
                if len(condition_part[CONF_ENTITY_ID]) == 0:
                    return [Entity_list, position]
                entity_name = condition_part[CONF_ENTITY_ID][0].split(".")[1]
                integration = condition_part[CONF_ENTITY_ID][0].split(".")[0]
            else:
                entity_name = condition_part[CONF_ENTITY_ID].split(".")[1]
                integration = condition_part[CONF_ENTITY_ID].split(".")[0]
            if CONF_ATTRIBUTE in condition_part:
                entity_name = entity_name + "." + str(condition_part[CONF_ATTRIBUTE])

            # create the entity in the condition part
            Entity_list.append(
                Entity(
                    parent=parent,
                    position=position,
                    param_role=param_role,
                    integration=integration,
                    entity_name=entity_name,
                    expected_value=exp_value,
                )
            )

    elif condition == CONF_DEVICE:
        # add the entity id and domain as the possible value
        exp_value = {CONF_ENTITY_ID: condition_part[CONF_ENTITY_ID]}
        exp_value[CONF_TYPE] = condition_part[CONF_TYPE]
        exp_value[CONF_DOMAIN] = condition_part[CONF_DOMAIN]

        # create the device entity
        Entity_list.append(
            Entity(
                parent=parent,
                position=position,
                param_role=param_role,
                integration=CONF_DEVICE,
                entity_name=condition_part[CONF_DEVICE_ID],
                expected_value=exp_value,
            )
        )

    elif condition == "sun":
        exp_value = {}
        if CONF_AFTER in condition_part:
            exp_value[CONF_AFTER] = condition_part[CONF_AFTER]
            if CONF_AFTER_OFFSET in condition_part:
                exp_value[CONF_AFTER_OFFSET] = condition_part[CONF_AFTER_OFFSET]
        if CONF_BEFORE in condition_part:
            exp_value[CONF_BEFORE] = condition_part[CONF_BEFORE]
            if CONF_BEFORE_OFFSET in condition_part:
                exp_value[CONF_BEFORE_OFFSET] = condition_part[CONF_BEFORE_OFFSET]

        # create the sun entity
        Entity_list.append(
            Entity(
                parent=parent,
                position=position,
                param_role=param_role,
                integration="sun",
                entity_name="sun",
                expected_value=exp_value,
            )
        )

    elif condition == CONF_TEMPLATE:
        if CONF_VALUE_TEMPLATE in condition_part:
            template_str = condition_part[CONF_VALUE_TEMPLATE]
            # TODO could be a bit more accurate than just the whole string
        else:
            # because the condition_part with the template string is still a dict
            template_str = condition_part[0]
            # TODO could be a bit more accurate than just the whole string

        # check if the string is a Jinja2 template
        if _is_jinja_template(template_str):
            # add the possible value of the template
            exp_value = {CONF_VALUE_TEMPLATE: template_str}

            # search for entities in the template string
            entities = re.findall(r"\w+\.\w+", template_str)
            if len(entities) > 1:
                # create a virtual and block
                new_parent = position
                for entity in entities:
                    position += 1
                    entity_integration = entity.split(".")[0]
                    entity_name = entity.split(".")[1]
                    Entity_list.append(
                        Entity(
                            parent=new_parent,
                            position=position,
                            param_role=param_role,
                            integration=entity_integration,
                            entity_name=entity_name,
                            expected_value=exp_value,
                        )
                    )
            else:
                if len(entities) == 1:
                    entity_integration = entities[0].split(".")[0]
                    entity_name = entities[0].split(".")[1]
                else:
                    entity_integration = "template"
                    entity_name = str(uuid.uuid4())
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

    elif condition == CONF_TIME:
        exp_value = {}
        if CONF_AFTER in condition_part:
            exp_value[CONF_AFTER] = condition_part[CONF_AFTER]
            # TODO extract entity input
        if CONF_BEFORE in condition_part:
            exp_value[CONF_BEFORE] = condition_part[CONF_BEFORE]
            # TODO extract entity input
        if CONF_WEEKDAY in condition_part:
            exp_value[CONF_WEEKDAY] = condition_part[CONF_WEEKDAY]

        # create the time entity
        Entity_list.append(
            Entity(
                parent=parent,
                position=position,
                param_role=param_role,
                integration=CONF_DATETIME,
                entity_name=str(uuid.uuid4()),
                expected_value=exp_value,
            )
        )

    elif condition == CONF_TRIGGER:
        # create all trigger entities that are needed for the condition
        if (
            isinstance(condition_part[CONF_ID], list)
            and len(condition_part[CONF_ID]) > 1
        ):
            new_parent = position
            for trigger_id in condition_part[CONF_ID]:
                position += 1
                # add the trigger id of the trigger as the expected value
                exp_value = {CONF_ID: trigger_id}
                # create the trigger entity
                Entity_list.append(
                    Entity(
                        parent=new_parent,
                        position=position,
                        param_role=param_role,
                        integration=CONF_TRIGGER,
                        entity_name=str(uuid.uuid4()),
                        expected_value=exp_value,
                    )
                )
        else:
            # create the single trigger entity
            if isinstance(condition_part[CONF_ID], list):
                exp_value = {CONF_ID: condition_part[CONF_ID][0]}
            else:
                exp_value = {CONF_ID: condition_part[CONF_ID]}
            # create the trigger entity
            Entity_list.append(
                Entity(
                    parent=parent,
                    position=position,
                    param_role=param_role,
                    integration=CONF_TRIGGER,
                    entity_name=str(uuid.uuid4()),
                    expected_value=exp_value,
                )
            )

    elif condition == CONF_ZONE:
        exp_value = {}
        if CONF_ZONE in condition_part:
            # add the entity id of the person/s as the possible value
            if CONF_ENTITY_ID in condition_part:
                if isinstance(condition_part[CONF_ENTITY_ID], list):
                    exp_value = {CONF_ENTITY_ID: []}
                    for entity in condition_part[CONF_ENTITY_ID]:
                        exp_value[CONF_ENTITY_ID].append(entity)
                else:
                    exp_value = {CONF_ENTITY_ID: condition_part[CONF_ENTITY_ID]}
            else:
                exp_value = {CONF_ENTITY_ID: None}

            # create the zone entity
            Entity_list.append(
                Entity(
                    parent=parent,
                    position=position,
                    param_role=param_role,
                    integration=CONF_ZONE,
                    entity_name=condition_part[CONF_ZONE].split(".")[1],
                    expected_value=exp_value,
                )
            )
        # This part is still in the documentation but is not validated anymore by the config schema
        # https://github.com/home-assistant/home-assistant.io/issues/33993
        # else:
        #     # add the entity id of the person/s as the possible value
        #     if CONF_ENTITY_ID in condition_part:
        #         if isinstance(condition_part[CONF_ENTITY_ID], list):
        #             exp_value = {CONF_ENTITY_ID: []}
        #             for entity in condition_part[CONF_ENTITY_ID]:
        #                 exp_value[CONF_ENTITY_ID].append(entity)
        #         else:
        #             exp_value = {CONF_ENTITY_ID: condition_part[CONF_ENTITY_ID]}
        #     else:
        #         exp_value = {CONF_ENTITY_ID: None}

        #     new_parent = position
        #     # create the possible zone entity/ies
        #     for zone in condition_part[CONF_STATE]:
        #         position += 1
        #         # create the zone entity
        #         Entity_list.append(
        #             Entity(
        #                 parent=new_parent,
        #                 position=position,
        #                 param_role=param_role,
        #                 integration=CONF_ZONE,
        #                 entity_name=zone.split(".")[1],
        #                 expected_value=exp_value,
        #             )
        #         )

    return [Entity_list, position]


def _action_entities(action_part: dict, position: int, parent: int = None) -> list:
    """The function creates a list of entities for one action list element.

    Args:
        action_part (dict): The action list element
        position (int): The position of the entity in the list
        parent (int): The parent entity of condition entities

    Returns:
        list: A list of entities as Entity objects
    """

    # list of entities in the trigger part
    Entity_list = []
    # entity parameter role is start
    param_role = OUTPUT

    # check if the action is enabled
    if f'{CONF_ENABLED}:' in action_part:
        if action_part[CONF_ENABLED] is False:
            return [Entity_list, position]

    if SCRIPT_ACTION_IF in action_part:
        conditions = action_part[SCRIPT_ACTION_IF]
        if len(conditions) > 1:
            has_cons = True
            new_parent = position
            # create all condition entities which are needed for the action
            for condition in conditions:
                position += 1
                results = _condition_entities(condition, position, new_parent)
                Entity_list += results[0]
                position = results[1]
        else:
            has_cons = True
            results = _condition_entities(conditions[0], position)
            Entity_list += results[0]
            position = results[1]

        if CONF_THEN in action_part:
            if has_cons:
                position += 1
            actions = action_part[CONF_THEN]
            for action in actions:
                results = _action_entities(action, position)
                Entity_list += results[0]
                # set the position for the next action
                position = results[1] + 1
            # set the position back to the last entity
            position -= 1

        if CONF_ELSE in action_part:
            if has_cons:
                position += 1
            actions = action_part[CONF_ELSE]
            for action in actions:
                results = _action_entities(action, position)
                Entity_list += results[0]
                # set the position for the next action
                position = results[1] + 1
            # set the position back to the last entity
            position -= 1

    elif CONF_CHOOSE in action_part:
        choose = action_part[CONF_CHOOSE]
        has_cons = False
        for option in choose:
            if CONF_CONDITIONS in option:
                has_cons = True
                new_parent = position
                # create all condition entities which are needed for the following action
                for condition in option[CONF_CONDITIONS]:
                    position += 1
                    results = _condition_entities(condition, position, new_parent)
                    Entity_list += results[0]
                    position = results[1]

            elif CONF_CONDITION in option:
                has_cons = True
                results = _condition_entities(option, position)
                Entity_list += results[0]
                position = results[1]

            if CONF_SEQUENCE in option:
                if isinstance(option[CONF_SEQUENCE], list):
                    # increase because the sequence has condition/s
                    if has_cons:
                        position += 1
                    for action in option[CONF_SEQUENCE]:
                        results = _action_entities(action, position)
                        Entity_list += results[0]
                        # set the position for the next action
                        position = results[1] + 1
                    has_cons = False
        # set the position back to the last entity                    
        position -= 1

    elif CONF_DEFAULT in action_part:
        default_actions = action_part[CONF_DEFAULT]
        for action in default_actions:
            results = _action_entities(action, position)
            Entity_list += results[0]
            # set the position for the next action
            position = results[1] + 1
        # set the position back to the last entity
        position -= 1

    elif CONF_PARALLEL in action_part:
        if isinstance(action_part[CONF_PARALLEL], list):
            for action in action_part[CONF_PARALLEL]:
                results = _action_entities(action, position)
                Entity_list += results[0]
                # set the position for the next action
                position = results[1] + 1
            # set the position back to the last entity
            position -= 1

    elif CONF_REPEAT in action_part:
        repeat_part = action_part[CONF_REPEAT]
        has_cons = False
        conditions = []
        
        if CONF_WHILE in repeat_part:
            conditions = repeat_part[CONF_WHILE]
        elif CONF_UNTIL in repeat_part:
            conditions = repeat_part[CONF_UNTIL]
        
        if isinstance(conditions, list):
            if len(conditions) > 1:
                has_cons = True
                new_parent = position
                # create all condition entities which are needed for the repeated action/s
                for condition in conditions:
                    position += 1
                    results = _condition_entities(condition, position, new_parent) 
                    Entity_list += results[0]
                    position = results[1]
            elif len(conditions) == 1:
                has_cons = True
                results = _condition_entities(conditions[0], position)
                Entity_list += results[0]
                position = results[1]
        

        if CONF_SEQUENCE in repeat_part:
            if has_cons:
                position += 1
            if isinstance(repeat_part[CONF_SEQUENCE], list):
                for action in repeat_part[CONF_SEQUENCE]:
                    results = _action_entities(action, position)
                    Entity_list += results[0]
                    # set the position for the next action
                    position = results[1] + 1
                # set the position back to the last entity
                position -= 1

    elif CONF_SEQUENCE in action_part:
        if isinstance(action_part[CONF_SEQUENCE], list):
            for action in action_part[CONF_SEQUENCE]:
                results = _action_entities(action, position)
                Entity_list += results[0]
                # set the position for the next action
                position = results[1] + 1
            # set the position back to the last entity
            position -= 1

    elif CONF_CONDITION in action_part:
        results = _condition_entities(action_part, position, parent)
        Entity_list += results[0]
        position = results[1]

    elif CONF_EVENT in action_part:
        # if the event has a data part
        if CONF_EVENT_DATA in action_part:
            event_data = {}
            exp_value = {}
            for data_key in action_part[CONF_EVENT_DATA]:
                event_data[data_key] = action_part[CONF_EVENT_DATA][data_key]
            exp_value[CONF_EVENT_DATA] = event_data
        # prohibit the use of 'context' in action events
        
        # create the entity
        Entity_list.append(
            Entity(
                parent=parent,
                position=position,
                param_role=param_role,
                integration=action_part[CONF_EVENT],
                entity_name=str(uuid.uuid4()),
                expected_value=exp_value,
            )
        )

    elif CONF_SERVICE in action_part:
        service = action_part[CONF_SERVICE]
        # TODO templates use could be more accurate
        integration = service.split(".")[0]
        entity_name = str(uuid.uuid4())

        exp_value = {CONF_SERVICE: service.split(".")[1]}

        if CONF_TARGET in action_part:
            if isinstance(action_part[CONF_TARGET], dict):
                entity_name = "target_group"
                if CONF_ENTITY_ID in action_part[CONF_TARGET]:
                    entity = action_part[CONF_TARGET][CONF_ENTITY_ID]
                    if isinstance(entity, list) and len(entity) > 1:
                        exp_value[CONF_ENTITY_ID] = entity
                    else:
                        if isinstance(entity, list):
                            entity_name = entity[0].split(".")[1]
                        elif _is_jinja_template(entity):
                            entity_name = entity
                        else:
                            entity_name = entity.split(".")[1]
                if ATTR_AREA_ID in action_part[CONF_TARGET]:
                    area = action_part[CONF_TARGET][ATTR_AREA_ID]
                    exp_value[ATTR_AREA_ID] = area
                if CONF_DEVICE_ID in action_part[CONF_TARGET]:
                    devices = action_part[CONF_TARGET][CONF_DEVICE_ID]
                    exp_value[CONF_DEVICE_ID] = devices
                    if isinstance(devices, list):
                        exp_value[CONF_DEVICE_ID] = devices

        elif CONF_ENTITY_ID in action_part:
            if action_part[CONF_ENTITY_ID] != []:
                entity_name = action_part[CONF_ENTITY_ID].split(".")[1]

        elif CONF_SERVICE_DATA in action_part:
            service_data = action_part[CONF_SERVICE_DATA]
            for data_key in service_data:
                exp_value[data_key] = service_data[data_key]

        # create the entity
        Entity_list.append(
            Entity(
                parent=parent,
                position=position,
                param_role=param_role,
                integration=integration,
                entity_name=entity_name,
                expected_value=exp_value,
            )
        )

    elif SCRIPT_ACTION_WAIT_FOR_TRIGGER in action_part:
        # just one of the triggers has to be true to continue (or-block)
        if isinstance(action_part[SCRIPT_ACTION_WAIT_FOR_TRIGGER], list):
            trigger_list = action_part[SCRIPT_ACTION_WAIT_FOR_TRIGGER]
            for trigger in trigger_list:
                results = _trigger_entities(trigger, position)
                for entity in results[0]:
                    entity.parameter_role = INPUT
                Entity_list += results[0]
                # set the position for the next trigger
                position = results[1] + 1
            # set the position back to the last entity
            position -= 1
        else:
            trigger = action_part[SCRIPT_ACTION_WAIT_FOR_TRIGGER]
            results = _trigger_entities(trigger, position)
            for entity in results[0]:
                entity.parameter_role = INPUT
            Entity_list += results[0]
            position = results[1]

    elif CONF_DEVICE_ID in action_part:
        integration = action_part[CONF_DOMAIN]
        entity_name = action_part[CONF_DEVICE_ID]
        exp_value = {}
        if CONF_ENTITY_ID in action_part:
            exp_value[CONF_ENTITY_ID] = action_part[CONF_ENTITY_ID]
        exp_value[CONF_SERVICE] = action_part[CONF_TYPE]

        # create the entity
        Entity_list.append(
            Entity(
                parent=parent,
                position=position,
                param_role=param_role,
                integration=integration,
                entity_name=entity_name,
                expected_value=exp_value,
            )
        )

    # TODO add variables for more detailed template actionss
    elif CONF_VARIABLES in action_part:
        pass

    # TODO add variables for more detailed template actionss
    elif SCRIPT_ACTION_WAIT_TEMPLATE in action_part:
        pass

    return [Entity_list, position]


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
    
    Args:
        automation_config (AutomationConfig): The automation configuration data.
    
    Returns:
        list: A list of condition entities extracted from the data.
    """
    condition_entities = []
    conditions = automation_config[CONF_CONDITION]
    position = 0
    for condition in conditions:
        return_list = _condition_entities(condition, position)
        condition_entities += return_list[0]
        position = return_list[1] + 1
    return condition_entities


def _extract_all_actions(automation_config: AutomationConfig) -> list:
    """
    Extract the action from the data.
    
    Args:
        automation_config (AutomationConfig): The automation configuration data.
    
    Returns:
        list: A list of action entities extracted from the data
    """
    action_entities = []
    actions = automation_config[CONF_ACTION]
    position = 0
    for action in actions:
        return_list = _action_entities(action, position)
        action_entities += return_list[0]
        position = return_list[1] + 1
    return action_entities


def create_entity_list(automation_config: AutomationConfig) -> list:
    """
    Create a list of entities from the automation configuration.
    """
    Entity_list = []
    Entity_list += _extract_all_trigger(automation_config)
    Entity_list += _extract_all_conditions(automation_config)
    Entity_list += _extract_all_actions(automation_config)
    return Entity_list


def create_automation(automation_config: AutomationConfig) -> Automation:
    """
    Create an automation from the automation configuration.
    """
    automation_name = automation_config.automation_name
    automation_script = create_automation_script(automation_config)

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
