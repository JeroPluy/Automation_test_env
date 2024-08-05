"""
This module is responsible for automating the desection of the data.

The information about the trigger functions are from:
https://www.home-assistant.io/docs/automation/trigger/

The information about the condition functions are from:
https://www.home-assistant.io/docs/scripts/conditions

The information about the action functions are from:
https://www.home-assistant.io/docs/scripts
"""

import automation_script_gen as asg

from .utils.env_const import (
    INPUT,
    OUTPUT,
    SINGLE,
    START,
)
from .utils.env_helper import Automation, Entity, is_jinja_template
from .ha_automation.home_assistant_config_validation import (
    valid_entity_id,
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
    CONF_CONTINUE_ON_TIMEOUT,
    CONF_CONVERSATION,
    CONF_COUNT,
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
    CONF_FOR_EACH,
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
    CONF_STOP,
    CONF_TARGET,
    CONF_TEMPLATE,
    CONF_THEN,
    CONF_TIME,
    CONF_TIME_PATTERN,
    CONF_TIMEOUT,
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


import re
import voluptuous as vol
import uuid


def _trigger_entities(
    trigger_part: dict,
    position: int,
    real_position: int,
    script_path: str,
    parent: int = None,
    indentation_level: int = 1,
    source: str = "trigger",
) -> list:
    """The function creates a list of entities for one trigger list element.

    Args:
        trigger_part (dict): The trigger list element
        position (int): The position of the entity in the list
        real_position (int): The real position of the entity for the input value into the script
        script_path (str): The path to the script
        parent (int): The parent entity of the entity
        indentation_level (int): The indentation level of the entity in the script
        source (str): The source of the entity

    Returns:
        list: A list of entities as Entity objects
    """

    platform = trigger_part[CONF_PLATFORM]
    # list of entities in the trigger part
    entity_list = []
    # entity parameter role is start
    param_role = START

    trigger_id = None

    # check if the trigger is enabled
    if CONF_ENABLED in trigger_part:
        try:
            bool_val = trigger_part[CONF_ENABLED]
        except TypeError:
            bool_val = None
        if bool_val is False:
            return [entity_list, position, real_position]

    if CONF_ID in trigger_part:
        trigger_id = trigger_part[CONF_ID]

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
            new_entity_list = []
            # create all entities in the trigger part
            for event_type in trigger_part[CONF_EVENT_TYPE]:
                position += 1
                exp_value[CONF_EVENT_TYPE] = event_type
                # TODO limited templating as input
                entity_name = str(uuid.uuid4())
                new_entity_list.append(
                    Entity(
                        parent=parent,
                        position=position,
                        param_role=param_role,
                        integration=CONF_EVENT,
                        entity_name=entity_name,
                        expected_value=exp_value,
                    )
                )
            # create the script for the combination of the event trigger
            real_position = asg.asg.create_combination_trigger_script(
                trigger_type=CONF_EVENT,
                entity_list=new_entity_list,
                trigger_pos=real_position,
                trigger_id=trigger_id,
                filepath=script_path,
                indentation_lvl=indentation_level,
                source=source,
            )
            # add the new entities to the entity list
            entity_list += new_entity_list

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
            real_position = asg.create_trigger_script(
                trigger_type=CONF_EVENT,
                entity=entity,
                trigger_pos=real_position,
                trigger_id=trigger_id,
                filepath=script_path,
                indentation_lvl=indentation_level,
                source=source,
            )
            entity_list.append(entity)

    # if is a home_assistant start or shutdown event
    elif platform == "homeassistant":
        # create the home assistant entity
        exp_value = {CONF_EVENT: trigger_part[CONF_EVENT]}
        entity = Entity(
            position=position,
            param_role=param_role,
            integration="homeassistant",
            entity_name="_",
            expected_value=exp_value,
        )
        entity_list.append(entity)
        real_position = asg.create_trigger_script(
            trigger_type="homeassistant",
            entity=entity,
            trigger_pos=real_position,
            trigger_id=trigger_id,
            filepath=script_path,
            indentation_lvl=indentation_level,
            source=source,
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
        entity = Entity(
            position=position,
            param_role=param_role,
            integration="mqtt",
            entity_name=trigger_part["topic"],
            expected_value=exp_value,
        )
        entity_list.append(entity)
        real_position = asg.create_trigger_script(
            trigger_type="mqtt",
            entity=entity,
            trigger_pos=real_position,
            trigger_id=trigger_id,
            filepath=script_path,
            indentation_lvl=indentation_level,
            source=source,
        )

    # if the trigger is a numerical state change
    elif platform == CONF_NUMERIC_STATE:
        # cache the new entities for potential comparing entities
        new_entity_list = []
        exp_value_entity_list = []
        parent = parent

        # add the possible value range to the entity/ies
        # TODO value_template is missing
        exp_value = {}
        if CONF_ABOVE in trigger_part:
            exp_value[CONF_ABOVE] = trigger_part[CONF_ABOVE]
            # create the comparing entities for the numerical state trigger
            if valid_entity_id(str(exp_value[CONF_ABOVE])):
                parent = position
                position += 1

                exp_value_entity_list.append(
                    Entity(
                        parent=parent,
                        position=None,
                        param_role=param_role,
                        integration=trigger_part[CONF_ABOVE].split(".")[0],
                        entity_name=trigger_part[CONF_ABOVE].split(".")[1],
                        expected_value={
                            CONF_BELOW: ""
                        },  # added after the generation of the comparing entity/ies
                    )
                )

        if CONF_BELOW in trigger_part:
            exp_value[CONF_BELOW] = trigger_part[CONF_BELOW]
            # create the comparing entities for the numerical state trigger
            if valid_entity_id(str(exp_value[CONF_BELOW])):
                # set the parent entity for the comparing entity/ies if no above entity exists
                if parent is None:
                    parent = position
                    position += 1

                exp_value_entity_list.append(
                    Entity(
                        parent=parent,
                        position=None,
                        param_role=param_role,
                        integration=trigger_part[CONF_BELOW].split(".")[0],
                        entity_name=trigger_part[CONF_BELOW].split(".")[1],
                        expected_value={
                            CONF_ABOVE: ""
                        },  # added after the generation of the comparing entity/ies
                    )
                )

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
                new_entity_list.append(
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
                    return [entity_list, position, real_position]
                entity_name = trigger_part[CONF_ENTITY_ID][0].split(".")[1]
                integration = trigger_part[CONF_ENTITY_ID][0].split(".")[0]
            else:
                entity_name = trigger_part[CONF_ENTITY_ID].split(".")[1]
                integration = trigger_part[CONF_ENTITY_ID].split(".")[0]

            if CONF_ATTRIBUTE in trigger_part:
                entity_name = entity_name + "." + str(trigger_part[CONF_ATTRIBUTE])

            # create the single entity in the event_type part
            new_entity_list.append(
                Entity(
                    parent=parent,
                    position=position,
                    param_role=param_role,
                    integration=integration,
                    entity_name=entity_name,
                    expected_value=exp_value,
                )
            )

        # get all the names of the new entities and create the script for the number trigger
        entity_names = []
        if len(new_entity_list) > 1:
            entity_names = []
            for entity in new_entity_list:
                entity_names.append(entity.entity_name)
            real_position = asg.create_combination_trigger_script(
                trigger_type=CONF_NUMERIC_STATE,
                entity_list=new_entity_list,
                trigger_pos=real_position,
                trigger_id=trigger_id,
                filepath=script_path,
                indentation_lvl=indentation_level,
                source=source,
            )
        else:
            entity_names = new_entity_list[0].entity_name
            real_position = asg.create_trigger_script(
                trigger_type=CONF_NUMERIC_STATE,
                entity=new_entity_list[0],
                trigger_pos=real_position,
                trigger_id=trigger_id,
                filepath=script_path,
                indentation_lvl=indentation_level,
                source=source,
            )
        # add the names of the entities to the expected value of the comparing entities
        for entity in exp_value_entity_list:
            position += 1
            entity.position = position
            if CONF_BELOW in entity.expected_value:
                entity.expected_value[CONF_BELOW] = entity_names
            if CONF_ABOVE in entity.expected_value:
                entity.expected_value[CONF_ABOVE] = entity_names

        # add the comparing entities to the entity list
        new_entity_list += exp_value_entity_list
        # append the new entities to the entity list
        entity_list += new_entity_list

    # if the trigger is a state change
    elif platform == CONF_STATE:
        new_entity_list = []
        exp_value_entity_list = []
        exp_value = {}
        to_trigger = None

        # add the state values of the trigger
        if CONF_TO in trigger_part:
            to_trigger = CONF_TO
            if isinstance(trigger_part[CONF_TO], list):
                exp_value[CONF_TO] = trigger_part[CONF_TO]
            else:
                exp_value[CONF_TO] = str(trigger_part[CONF_TO])

        elif CONF_NOT_TO in trigger_part:
            to_trigger = CONF_NOT_TO
            if isinstance(trigger_part[CONF_NOT_TO], list):
                exp_value[CONF_NOT_TO] = trigger_part[CONF_NOT_TO]
            else:
                exp_value[CONF_NOT_TO] = str(trigger_part[CONF_NOT_TO])

        if to_trigger is not None:
            if isinstance(exp_value[to_trigger], list):
                _has_entity_id = False
                # check if entity ids are upon the values
                for value in exp_value[to_trigger]:
                    if valid_entity_id(str(value)):
                        _has_entity_id = True
                        break
                if _has_entity_id:
                    parent = position
                    position += 1
                    for value in exp_value[to_trigger]:
                        # because the list can contain entity ids and strings status values
                        if valid_entity_id(str(value)):
                            # create the comparing entities for the state trigger
                            exp_value_entity_list.append(
                                Entity(
                                    parent=parent,
                                    position=None,
                                    param_role=param_role,
                                    integration=value.split(".")[0],
                                    entity_name=value.split(".")[1],
                                    # expected value could be taken from the same entity in another trigger maybe later
                                )
                            )
            elif isinstance(exp_value[to_trigger], str) and valid_entity_id(
                str(exp_value[to_trigger])
            ):
                # create the comparing entities for the state trigger
                parent = position
                position += 1
                exp_value_entity_list.append(
                    Entity(
                        parent=parent,
                        position=None,
                        param_role=param_role,
                        integration=trigger_part[to_trigger].split(".")[0],
                        entity_name=trigger_part[to_trigger].split(".")[1],
                        # expected value could be taken from the same entity in another trigger maybe later
                    )
                )

        if CONF_FROM in trigger_part:
            exp_value[CONF_FROM] = str(trigger_part[CONF_FROM])
        elif CONF_NOT_FROM in trigger_part:
            exp_value[CONF_NOT_FROM] = str(trigger_part[CONF_NOT_FROM])
            # TODO create entity/ies for the state from trigger

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
                new_entity_list.append(
                    Entity(
                        parent=parent,
                        position=position,
                        param_role=param_role,
                        integration=entity_integration,
                        entity_name=entity_name,
                        expected_value=exp_value,
                    )
                )
            # create the script for the combination of the state trigger
            real_position = asg.create_combination_trigger_script(
                trigger_type=CONF_STATE,
                entity_list=new_entity_list,
                trigger_pos=real_position,
                trigger_id=trigger_id,
                filepath=script_path,
                indentation_lvl=indentation_level,
                source=source,
            )

        else:
            if isinstance(trigger_part[CONF_ENTITY_ID], list):
                if len(trigger_part[CONF_ENTITY_ID]) == 0:
                    return [entity_list, position, real_position]
                entity_name = trigger_part[CONF_ENTITY_ID][0].split(".")[1]
                integration = trigger_part[CONF_ENTITY_ID][0].split(".")[0]
            else:
                entity_name = trigger_part[CONF_ENTITY_ID].split(".")[1]
                integration = trigger_part[CONF_ENTITY_ID].split(".")[0]
            if CONF_ATTRIBUTE in trigger_part:
                entity_name = entity_name + "." + str(trigger_part[CONF_ATTRIBUTE])
            # create the single entity in the event_type part
            entity = Entity(
                parent=parent,
                position=position,
                param_role=param_role,
                integration=integration,
                entity_name=entity_name,
                expected_value=exp_value,
            )

            real_position = asg.create_trigger_script(
                trigger_type=CONF_STATE,
                entity=entity,
                trigger_pos=real_position,
                trigger_id=trigger_id,
                filepath=script_path,
                indentation_lvl=indentation_level,
                source=source,
            )

            new_entity_list.append(entity)

        # add the names of the entities to the expected value of the comparing entities
        for entity in exp_value_entity_list:
            position += 1
            entity.position = position

        # add the comparing entities to the entity list
        new_entity_list += exp_value_entity_list
        # append the new entities to the entity list
        entity_list += new_entity_list

    # if the trigger is the sunset or sunrise event
    elif platform == "sun":
        # add the offset value of the trigger
        exp_value = {CONF_EVENT: trigger_part[CONF_EVENT]}
        if CONF_OFFSET in trigger_part:
            exp_value[CONF_OFFSET] = trigger_part[CONF_OFFSET]

        # create the sun entity
        entity = Entity(
            position=position,
            param_role=param_role,
            integration="sun",
            entity_name="sun",
            expected_value=exp_value,
        )
        entity_list.append(entity)
        real_position = asg.create_trigger_script(
            trigger_type="sun",
            entity=entity,
            trigger_pos=real_position,
            trigger_id=trigger_id,
            filepath=script_path,
            indentation_lvl=indentation_level,
            source=source,
        )

    # if the trigger is tag scan
    elif platform == "tag":
        new_entity_list = []

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
            new_entity_list = []

            for tag_id in trigger_part[TAG_ID]:
                position += 1

                new_entity_list.append(
                    Entity(
                        parent=parent,
                        position=position,
                        param_role=param_role,
                        integration="tag",
                        entity_name=tag_id,
                        expected_value=exp_value,
                    )
                )
            # create the script for the combination of the tag trigger
            real_position = asg.create_combination_trigger_script(
                trigger_type="tag",
                entity_list=new_entity_list,
                trigger_pos=real_position,
                trigger_id=trigger_id,
                filepath=script_path,
                indentation_lvl=indentation_level,
                source=source,
            )
            entity_list += new_entity_list

        else:
            # create the single tag entity in the trigger part
            entity = Entity(
                position=position,
                param_role=param_role,
                integration="tag",
                entity_name=trigger_part[TAG_ID],
                expected_value=exp_value,
            )
            real_position = asg.create_trigger_script(
                trigger_type="tag",
                entity=entity,
                trigger_pos=real_position,
                trigger_id=trigger_id,
                filepath=script_path,
                indentation_lvl=indentation_level,
                source=source,
            )
            entity_list.append(entity)

    # if the trigger is a template
    elif platform == CONF_TEMPLATE:
        # if trigger has a template string
        if CONF_VALUE_TEMPLATE in trigger_part:
            template_str = trigger_part[CONF_VALUE_TEMPLATE]

            # check if the string is a Jinja2 template
            if is_jinja_template(template_str):
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
                new_entity_list = []

                for entity in entities:
                    position += 1
                    entity_integration = entity.split(".")[0]
                    entity_name = entity.split(".")[1]
                    new_entity_list.append(
                        Entity(
                            parent=parent,
                            position=position,
                            param_role=param_role,
                            integration=entity_integration,
                            entity_name=entity_name,
                            expected_value=exp_value,
                        )
                    )
                # create the script for the combination of the template trigger
                real_position = asg.create_combination_trigger_script(
                    trigger_type=CONF_TEMPLATE,
                    entity_list=new_entity_list,
                    trigger_pos=real_position,
                    trigger_id=trigger_id,
                    filepath=script_path,
                    indentation_lvl=indentation_level,
                    source=source,
                )
                entity_list += new_entity_list

    # if the trigger is a time event
    elif platform == CONF_TIME:
        # TODO extract entity input in AT
        if isinstance(trigger_part[CONF_AT], list):
            parent = position
            new_entity_list = []

            for time in trigger_part[CONF_AT]:
                position += 1
                # create the time entity
                new_entity_list.append(
                    Entity(
                        parent=parent,
                        position=position,
                        param_role=param_role,
                        integration=CONF_TIME,
                        entity_name=CONF_TIME,
                        expected_value={CONF_AT: time},
                    )
                )
            # create the script for the combination of the time trigger
            real_position = asg.create_combination_trigger_script(
                trigger_type=CONF_TIME,
                entity_list=new_entity_list,
                trigger_pos=real_position,
                trigger_id=trigger_id,
                filepath=script_path,
                indentation_lvl=indentation_level,
                source=source,
            )

            entity_list += new_entity_list
        else:
            # create the single time entity
            entity = Entity(
                position=position,
                param_role=param_role,
                integration=CONF_TIME,
                entity_name=CONF_TIME,
                expected_value={CONF_AT: trigger_part[CONF_AT]},
            )
            real_position = asg.create_trigger_script(
                trigger_type=CONF_TIME,
                entity=entity,
                trigger_pos=real_position,
                trigger_id=trigger_id,
                filepath=script_path,
                indentation_lvl=indentation_level,
                source=source,
            )
            entity_list.append(entity)

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
        entity = Entity(
            position=position,
            param_role=param_role,
            integration=CONF_TIME_PATTERN,
            entity_name=str(uuid.uuid4()),
            expected_value=exp_value,
        )
        real_position = asg.create_trigger_script(
            trigger_type=CONF_TIME_PATTERN,
            entity=entity,
            trigger_pos=real_position,
            trigger_id=trigger_id,
            filepath=script_path,
            indentation_lvl=indentation_level,
            source=source,
        )
        entity_list.append(entity)

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
        entity = Entity(
            position=position,
            param_role=param_role,
            integration=CONF_PERS_NOTIFICATION,
            entity_name=entity_name,
            expected_value=exp_value,
        )
        real_position = asg.create_trigger_script(
            trigger_type=CONF_PERS_NOTIFICATION,
            entity=entity,
            trigger_pos=real_position,
            trigger_id=trigger_id,
            filepath=script_path,
            indentation_lvl=indentation_level,
            source=source,
        )
        entity_list.append(entity)

    # if the trigger is a webhook
    elif platform == CONF_WEBHOOK:
        if CONF_ALLOWED_METHODS in trigger_part:
            exp_value = {CONF_ALLOWED_METHODS: trigger_part[CONF_ALLOWED_METHODS]}
            if CONF_LOCAL in trigger_part:
                exp_value[CONF_LOCAL] = trigger_part[CONF_LOCAL]

        # create the webhook entity
        entity = Entity(
            position=position,
            param_role=param_role,
            integration=CONF_WEBHOOK,
            entity_name=trigger_part[CONF_WEBHOOK_ID],
            expected_value=exp_value,
        )
        real_position = asg.create_trigger_script(
            trigger_type=CONF_WEBHOOK,
            entity=entity,
            trigger_pos=real_position,
            trigger_id=trigger_id,
            filepath=script_path,
            indentation_lvl=indentation_level,
            source=source,
        )
        entity_list.append(entity)

    # if the trigger is a zone event (enter or leave)
    elif platform == CONF_ZONE:
        # add the entity id of the person and the event type as the possible value
        exp_value = {CONF_EVENT: trigger_part[CONF_EVENT]}
        exp_value[CONF_ENTITY_ID] = trigger_part[CONF_ENTITY_ID]

        # create the zone entity
        entity = Entity(
            position=position,
            param_role=param_role,
            integration=CONF_ZONE,
            entity_name=trigger_part[CONF_ZONE].split(".")[1],
            expected_value=exp_value,
        )
        real_position = asg.create_trigger_script(
            trigger_type=CONF_ZONE,
            entity=entity,
            trigger_pos=real_position,
            trigger_id=trigger_id,
            filepath=script_path,
            indentation_lvl=indentation_level,
            source=source,
        )
        entity_list.append(entity)

    # if the trigger is a geo location event
    elif platform == CONF_GEO_LOCATION:
        # add the entity id of the person and the event type as the possible value
        exp_value = {CONF_EVENT: trigger_part[CONF_EVENT]}
        exp_value[CONF_SOURCE] = trigger_part[CONF_SOURCE]

        # create the zone entity
        entity = Entity(
            position=position,
            param_role=param_role,
            integration=CONF_ZONE,
            entity_name=trigger_part[CONF_ZONE].split(".")[1],
            expected_value=exp_value,
        )
        real_position = asg.create_trigger_script(
            trigger_type=CONF_GEO_LOCATION,
            entity=entity,
            trigger_pos=real_position,
            trigger_id=trigger_id,
            filepath=script_path,
            indentation_lvl=indentation_level,
            source=source,
        )
        entity_list.append(entity)

    # if the trigger is a device event
    elif platform == CONF_DEVICE:
        # add the entity id and domain as the possible value
        exp_value = {CONF_ENTITY_ID: trigger_part[CONF_ENTITY_ID]}
        exp_value[CONF_TYPE] = trigger_part[CONF_TYPE]
        exp_value[CONF_DOMAIN] = trigger_part[CONF_DOMAIN]

        # create the device entity
        entity = Entity(
            position=position,
            param_role=param_role,
            integration=CONF_DEVICE,
            entity_name=trigger_part[CONF_DEVICE_ID],
            expected_value=exp_value,
        )
        real_position = asg.create_trigger_script(
            trigger_type=CONF_DEVICE,
            entity=entity,
            trigger_pos=real_position,
            trigger_id=trigger_id,
            filepath=script_path,
            indentation_lvl=indentation_level,
            source=source,
        )
        entity_list.append(entity)

    # if the trigger is a calendar event
    elif platform == CONF_CALENDAR:
        # add the calendar event as the possible value
        exp_value = {CONF_EVENT: trigger_part[CONF_EVENT]}
        if CONF_OFFSET in trigger_part:
            exp_value[CONF_OFFSET] = trigger_part[CONF_OFFSET]

        # create the calendar entity
        entity = Entity(
            position=position,
            param_role=param_role,
            integration=CONF_CALENDAR,
            entity_name=trigger_part[CONF_ENTITY_ID].split(".")[1],
            expected_value=exp_value,
        )
        real_position = asg.create_trigger_script(
            trigger_type=CONF_CALENDAR,
            entity=entity,
            trigger_pos=real_position,
            trigger_id=trigger_id,
            filepath=script_path,
            indentation_lvl=indentation_level,
            source=source,
        )
        entity_list.append(entity)

    # if trigger is a sentence
    elif platform == CONF_CONVERSATION:
        if isinstance(trigger_part[CONF_COMMAND], list):
            parent = position
            new_entity_list = []

            for command in trigger_part[CONF_COMMAND]:
                position += 1
                # create the conversation entity
                new_entity_list.append(
                    Entity(
                        parent=parent,
                        position=position,
                        param_role=param_role,
                        integration=CONF_CONVERSATION,
                        entity_name=str(uuid.uuid4()),
                        expected_value={CONF_COMMAND: command},
                    )
                )
            # create the script for the combination of the conversation trigger
            real_position = asg.create_combination_trigger_script(
                trigger_type=CONF_CONVERSATION,
                entity_list=new_entity_list,
                trigger_pos=real_position,
                trigger_id=trigger_id,
                filepath=script_path,
                indentation_lvl=indentation_level,
                source=source,
            )

            entity_list += new_entity_list

        else:
            # create the conversation entity
            entity = Entity(
                position=position,
                param_role=param_role,
                integration=CONF_CONVERSATION,
                entity_name=str(uuid.uuid4()),
                expected_value={CONF_COMMAND: trigger_part[CONF_COMMAND]},
            )
            real_position = asg.create_trigger_script(
                trigger_type=CONF_CONVERSATION,
                entity=entity,
                trigger_pos=real_position,
                trigger_id=trigger_id,
                filepath=script_path,
                indentation_lvl=indentation_level,
                source=source,
            )
            entity_list.append(entity)

    return [entity_list, position, real_position]


def _condition_entities(
    condition_part: dict,
    position: int,
    real_position: int,
    script_path: str,
    parent: int = None,
    indentation_level: int = 2,
    first_element: bool = True,
    source: str = CONF_CONDITION,
    combinator: str = CONF_AND,
) -> list:
    """The function creates a list of entities for one condition list element.

    Args:
        condition_part (dict): The condition list element
        position (int): The position of the entity in the list
        real_position (int):  The real position of the entity for the input value into the script
        script_path (str): The path to the script file
        parent (int): The parent entity of the entity

    Returns:
        list: A list of entities as Entity objects
    """

    # list of entities in the trigger part
    entity_list = []
    # entity parameter role is start
    param_role = INPUT

    # check if the condition is enabled
    if CONF_ENABLED in condition_part:
        try:
            bool_val = condition_part[CONF_ENABLED]
        except TypeError:
            bool_val = None
        if bool_val is False:
            return [entity_list, position, real_position]

    # check if the condition is a pure template
    if len(condition_part) > 1 and not isinstance(condition_part, str):
        if CONF_CONDITION in condition_part:
            condition = condition_part[CONF_CONDITION]
    else:
        condition = CONF_TEMPLATE

    # processes a combination of multiple conditions
    if condition == CONF_OR or condition == CONF_AND or condition == CONF_NOT:
        if CONF_CONDITIONS in condition_part:
            indentation_level = asg.start_logic_function_block(
                condition_type=condition,
                filepath=script_path,
                indentation_lvl=indentation_level,
                first_element=first_element,
            )
            new_parent = position
            num_of_conditions = len(condition_part[CONF_CONDITIONS])
            for x in range(0, num_of_conditions):
                if x == 0:
                    first_element = True
                else:
                    first_element = False
                sub_condition = condition_part[CONF_CONDITIONS][x]

                position += 1
                result_list = _condition_entities(
                    condition_part=sub_condition,
                    position=position,
                    parent=new_parent,
                    script_path=script_path,
                    real_position=real_position,
                    indentation_level=indentation_level,
                    first_element=first_element,
                    source=source,
                    combinator=condition,
                )
                entity_list += result_list[0]
                position = result_list[1]
                real_position = result_list[2]
            asg.close_logic_function_block(
                filepath=script_path, indentation_lvl=(indentation_level - 1)
            )

    # processes a numeric state condition
    elif condition == CONF_NUMERIC_STATE:
        # cache the new entities for potential comparing entities
        new_entity_list = []
        exp_value_entity_list = []
        new_parent = parent

        # add the possible value range to the entity/ies
        # TODO value_template is missing
        exp_value = {}
        if CONF_ABOVE in condition_part:
            exp_value[CONF_ABOVE] = condition_part[CONF_ABOVE]
            # create the comparing entities for the numerical state trigger
            if valid_entity_id(str(exp_value[CONF_ABOVE])):
                new_parent = position
                position += 1

                exp_value_entity_list.append(
                    Entity(
                        parent=new_parent,
                        position=None,
                        param_role=param_role,
                        integration=condition_part[CONF_ABOVE].split(".")[0],
                        entity_name=condition_part[CONF_ABOVE].split(".")[1],
                        expected_value={
                            CONF_BELOW: ""
                        },  # added after the generation of the comparing entity/ies
                    )
                )

        if CONF_BELOW in condition_part:
            exp_value[CONF_BELOW] = condition_part[CONF_BELOW]
            # create the comparing entities for the numerical state trigger
            if valid_entity_id(str(exp_value[CONF_BELOW])):
                # set the parent entity for the comparing entity/ies if no above entity exists
                if new_parent is None:
                    new_parent = position
                    position += 1

                exp_value_entity_list.append(
                    Entity(
                        parent=new_parent,
                        position=None,
                        param_role=param_role,
                        integration=condition_part[CONF_BELOW].split(".")[0],
                        entity_name=condition_part[CONF_BELOW].split(".")[1],
                        expected_value={
                            CONF_ABOVE: ""
                        },  # added after the generation of the comparing entity/ies
                    )
                )
        # add the time the value has to stay in the trigger range
        if CONF_FOR in condition_part:
            exp_value[CONF_FOR] = condition_part[CONF_FOR]
            # TODO limited templating as input

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
                new_entity_list.append(
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
                    return [entity_list, position, real_position]
                entity_name = condition_part[CONF_ENTITY_ID][0].split(".")[1]
                integration = condition_part[CONF_ENTITY_ID][0].split(".")[0]
            else:
                entity_name = condition_part[CONF_ENTITY_ID].split(".")[1]
                integration = condition_part[CONF_ENTITY_ID].split(".")[0]
            if CONF_ATTRIBUTE in condition_part:
                entity_name = entity_name + "." + str(condition_part[CONF_ATTRIBUTE])
            # create a single entity in the condion part
            new_entity_list.append(
                Entity(
                    parent=new_parent,
                    position=position,
                    param_role=param_role,
                    integration=integration,
                    entity_name=entity_name,
                    expected_value=exp_value,
                )
            )

        # get all the names of the new entities and create the script for the number trigger
        entity_names = []
        if len(new_entity_list) > 1:
            entity_names = []
            for entity in new_entity_list:
                entity_names.append(entity.entity_name)
            real_position = asg.create_combination_condition_script(
                CONF_NUMERIC_STATE,
                new_entity_list,
                real_position,
                script_path,
                indentation_lvl=indentation_level,
                first_element=first_element,
                source=source,
                combinator=combinator,
            )
        else:
            entity_names = new_entity_list[0].entity_name
            real_position = asg.create_condition_script(
                CONF_NUMERIC_STATE,
                new_entity_list[0],
                real_position,
                script_path,
                indentation_lvl=indentation_level,
                first_element=first_element,
                source=source,
                combinator=combinator,
            )
        # add the names of the entities to the expected value of the comparing entities
        for entity in exp_value_entity_list:
            position += 1
            entity.position = position
            if CONF_BELOW in entity.expected_value:
                entity.expected_value[CONF_BELOW] = entity_names
            if CONF_ABOVE in entity.expected_value:
                entity.expected_value[CONF_ABOVE] = entity_names

        # add the comparing entities to the entity list
        new_entity_list += exp_value_entity_list
        # append the new entities to the entity list
        entity_list += new_entity_list

    # processes a state condition
    elif condition == CONF_STATE:
        new_entity_list = []
        exp_value_entity_list = []
        exp_value = {}

        # add the state value/s of the condition
        exp_value = {CONF_STATE: condition_part[CONF_STATE]}
        if isinstance(exp_value[CONF_STATE], list):
            _has_entity_id = False
            # check if entity ids are upon the values
            for value in exp_value[CONF_STATE]:
                if valid_entity_id(str(value)):
                    _has_entity_id = True
                    break
            if _has_entity_id:
                parent = position
                position += 1
                for value in exp_value[CONF_STATE]:
                    # because the list can contain entity ids and strings status values
                    if valid_entity_id(str(value)):
                        # create the comparing entities for the state trigger
                        exp_value_entity_list.append(
                            Entity(
                                parent=parent,
                                position=None,
                                param_role=param_role,
                                integration=value.split(".")[0],
                                entity_name=value.split(".")[1],
                                # expected value could be taken from the same entity in another trigger maybe later
                            )
                        )
        elif isinstance(exp_value[CONF_STATE], str) and valid_entity_id(
            str(exp_value[CONF_STATE])
        ):
            # create the comparing entities for the state trigger
            parent = position
            position += 1
            exp_value_entity_list.append(
                Entity(
                    parent=parent,
                    position=None,
                    param_role=param_role,
                    integration=condition_part[CONF_STATE].split(".")[0],
                    entity_name=condition_part[CONF_STATE].split(".")[1],
                    # expected value could be taken from the same entity in another trigger maybe later
                )
            )

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
                new_entity_list.append(
                    Entity(
                        parent=new_parent,
                        position=position,
                        param_role=param_role,
                        integration=entity_integration,
                        entity_name=entity_name,
                        expected_value=exp_value,
                    )
                )
            # create the script for the combination of the state trigger
            real_position = asg.create_combination_condition_script(
                CONF_STATE,
                new_entity_list,
                real_position,
                script_path,
                indentation_lvl=indentation_level,
                first_element=first_element,
                source=source,
                combinator=combinator,
            )
        else:
            if isinstance(condition_part[CONF_ENTITY_ID], list):
                if len(condition_part[CONF_ENTITY_ID]) == 0:
                    return [entity_list, position, real_position]
                entity_name = condition_part[CONF_ENTITY_ID][0].split(".")[1]
                integration = condition_part[CONF_ENTITY_ID][0].split(".")[0]
            else:
                entity_name = condition_part[CONF_ENTITY_ID].split(".")[1]
                integration = condition_part[CONF_ENTITY_ID].split(".")[0]
            if CONF_ATTRIBUTE in condition_part:
                entity_name = entity_name + "." + str(condition_part[CONF_ATTRIBUTE])

            # create the entity in the condition part
            entity = Entity(
                parent=parent,
                position=position,
                param_role=param_role,
                integration=integration,
                entity_name=entity_name,
                expected_value=exp_value,
            )

            real_position = asg.create_condition_script(
                CONF_STATE,
                entity,
                real_position,
                script_path,
                indentation_lvl=indentation_level,
                first_element=first_element,
                source=source,
                combinator=combinator,
            )

            new_entity_list.append(entity)

        # add the names of the entities to the expected value of the comparing entities
        for entity in exp_value_entity_list:
            position += 1
            entity.position = position

        # add the comparing entities to the entity list
        new_entity_list += exp_value_entity_list
        # append the new entities to the entity list
        entity_list += new_entity_list

    # processes a device condition
    elif condition == CONF_DEVICE:
        # add the entity id and domain as the possible value
        exp_value = {CONF_ENTITY_ID: condition_part[CONF_ENTITY_ID]}
        exp_value[CONF_TYPE] = condition_part[CONF_TYPE]
        exp_value[CONF_DOMAIN] = condition_part[CONF_DOMAIN]

        # create the device entity

        entity = Entity(
            parent=parent,
            position=position,
            param_role=param_role,
            integration=CONF_DEVICE,
            entity_name=condition_part[CONF_DEVICE_ID],
            expected_value=exp_value,
        )
        entity_list.append(entity)

        real_position = asg.create_condition_script(
            CONF_DEVICE,
            entity,
            real_position,
            script_path,
            indentation_lvl=indentation_level,
            first_element=first_element,
            source=source,
            combinator=combinator,
        )

    # processes a sun condition
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
        entity = Entity(
            parent=parent,
            position=position,
            param_role=param_role,
            integration="sun",
            entity_name="sun",
            expected_value=exp_value,
        )
        real_position = asg.create_condition_script(
            "sun",
            entity,
            real_position,
            script_path,
            indentation_lvl=indentation_level,
            first_element=first_element,
            source=source,
            combinator=combinator,
        )
        entity_list.append(entity)

    # processes a template condition
    elif condition == CONF_TEMPLATE:
        if CONF_VALUE_TEMPLATE in condition_part:
            template_str = condition_part[CONF_VALUE_TEMPLATE]
            # TODO could be a bit more accurate than just the whole string
        else:
            # because the condition_part with the template string is still a dict
            template_str = condition_part[0]
            # TODO could be a bit more accurate than just the whole string

        # check if the string is a Jinja2 template
        if is_jinja_template(template_str):
            # add the possible value of the template
            exp_value = {CONF_VALUE_TEMPLATE: template_str}

            # search for entities in the template string
            entities = re.findall(r"\w+\.\w+", template_str)
            if len(entities) > 1:
                # create a virtual and block
                new_parent = position
                new_entity_list = []

                for entity in entities:
                    position += 1
                    entity_integration = entity.split(".")[0]
                    entity_name = entity.split(".")[1]
                    new_entity_list.append(
                        Entity(
                            parent=new_parent,
                            position=position,
                            param_role=param_role,
                            integration=entity_integration,
                            entity_name=entity_name,
                            expected_value=exp_value,
                        )
                    )
                # create the script for the combination of the template condition
                real_position = asg.create_combination_condition_script(
                    CONF_TEMPLATE,
                    new_entity_list,
                    real_position,
                    script_path,
                    indentation_lvl=indentation_level,
                    first_element=first_element,
                    source=source,
                    combinator=combinator,
                )
                entity_list += new_entity_list
            else:
                if len(entities) == 1:
                    entity_integration = entities[0].split(".")[0]
                    entity_name = entities[0].split(".")[1]
                else:
                    entity_integration = "template"
                    entity_name = str(uuid.uuid4())
                entity = Entity(
                    parent=parent,
                    position=position,
                    param_role=param_role,
                    integration=entity_integration,
                    entity_name=entity_name,
                    expected_value=exp_value,
                )
                entity_list.append(entity)
                # create the script for the template condition
                real_position = asg.create_condition_script(
                    CONF_TEMPLATE,
                    entity,
                    real_position,
                    script_path,
                    indentation_lvl=indentation_level,
                    first_element=first_element,
                    source=source,
                    combinator=combinator,
                )

    # processes a time condition
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

        entity = Entity(
            parent=parent,
            position=position,
            param_role=param_role,
            integration=CONF_DATETIME,
            entity_name=str(uuid.uuid4()),
            expected_value=exp_value,
        )
        entity_list.append(entity)
        real_position = asg.create_condition_script(
            CONF_TIME,
            entity,
            real_position,
            script_path,
            indentation_lvl=indentation_level,
            first_element=first_element,
            source=source,
            combinator=combinator,
        )

    # processes a trigger based condition
    elif condition == CONF_TRIGGER:
        # create all trigger entities that are needed for the condition
        if (
            isinstance(condition_part[CONF_ID], list)
            and len(condition_part[CONF_ID]) > 1
        ):
            new_parent = position
            new_trigger_entity_list = []
            for trigger_id in condition_part[CONF_ID]:
                position += 1
                # add the trigger id of the trigger as the expected value
                exp_value = {CONF_ID: str(trigger_id)}
                new_trigger_entity_list.append(
                    Entity(
                        parent=new_parent,
                        position=position,
                        param_role=param_role,
                        integration=CONF_TRIGGER,
                        entity_name=str(uuid.uuid4()),
                        expected_value=exp_value,
                    )
                )
            real_position = asg.create_combination_condition_script(
                CONF_TRIGGER,
                new_trigger_entity_list,
                real_position,
                script_path,
                indentation_lvl=indentation_level,
                first_element=first_element,
                source=source,
                combinator=combinator,
            )
            entity_list += new_trigger_entity_list

        else:
            # create the single trigger entity
            if isinstance(condition_part[CONF_ID], list):
                exp_value = {CONF_ID: str(condition_part[CONF_ID][0])}
            else:
                exp_value = {CONF_ID: str(condition_part[CONF_ID])}

            # create the trigger entity
            entity = Entity(
                parent=parent,
                position=position,
                param_role=param_role,
                integration=CONF_TRIGGER,
                entity_name=str(uuid.uuid4()),
                expected_value=exp_value,
            )
            entity_list.append(entity)
            real_position = asg.create_condition_script(
                CONF_TRIGGER,
                entity,
                real_position,
                script_path,
                indentation_lvl=indentation_level,
                first_element=first_element,
                source=source,
                combinator=combinator,
            )

    # processes a zone condition
    elif condition == CONF_ZONE:
        exp_value = {}
        if CONF_ZONE in condition_part:
            parent = position
            position += 1
            # add the entity id of the person/s as the possible value
            if (
                isinstance(condition_part[CONF_ENTITY_ID], list)
                and len(condition_part[CONF_ENTITY_ID]) > 1
            ):
                new_exp_entity_list = []
                new_parent = position
                # create all the person entities in the condition part
                for person in condition_part[CONF_ENTITY_ID]:
                    position += 1
                    if valid_entity_id(str(person)):
                        entity = Entity(
                            parent=new_parent,
                            position=position,
                            param_role=param_role,
                            integration=person.split(".")[0],
                            entity_name=person.split(".")[1],
                            expected_value={CONF_ZONE: condition_part[CONF_ZONE]},
                        )
                    else:
                        entity = Entity(
                            parent=new_parent,
                            position=position,
                            param_role=param_role,
                            integration="person",
                            entity_name=person,
                            expected_value={CONF_ZONE: condition_part[CONF_ZONE]},
                        )
                    new_exp_entity_list.append(entity)

                exp_value = {CONF_ENTITY_ID: condition_part[CONF_ENTITY_ID]}

                real_position = asg.create_condition_script(
                    CONF_ZONE,
                    new_exp_entity_list,
                    real_position,
                    script_path,
                    indentation_lvl=indentation_level,
                    first_element=first_element,
                    source=source,
                    combinator=combinator,
                )
                entity_list += new_exp_entity_list
            else:
                if isinstance(condition_part[CONF_ENTITY_ID], list):
                    person = condition_part[CONF_ENTITY_ID][0]
                else:
                    person = condition_part[CONF_ENTITY_ID]

                # create a single person entity
                exp_value = {CONF_ENTITY_ID: person}
                if valid_entity_id(str(person)):
                    integration = person.split(".")[0]
                    entity_name = person.split(".")[1]
                else:
                    integration = "person"
                    entity_name = person
                entity = Entity(
                    parent=parent,
                    position=position,
                    param_role=param_role,
                    integration=integration,
                    entity_name=entity_name,
                    expected_value={CONF_ZONE: condition_part[CONF_ZONE]},
                )
                entity_list.append(entity)
                real_position = asg.create_condition_script(
                    CONF_ZONE,
                    entity,
                    real_position,
                    script_path,
                    indentation_lvl=indentation_level,
                    first_element=first_element,
                    source=source,
                    combinator=combinator,
                )

            position += 1
            # create the zone entity
            entity = Entity(
                parent=parent,
                position=position,
                param_role=param_role,
                integration=CONF_ZONE,
                entity_name=condition_part[CONF_ZONE].split(".")[1],
                expected_value=exp_value,
            )
            entity_list.append(entity)

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
        #         entity_list.append(
        #             Entity(
        #                 parent=new_parent,
        #                 position=position,
        #                 param_role=param_role,
        #                 integration=CONF_ZONE,
        #                 entity_name=zone.split(".")[1],
        #                 expected_value=exp_value,
        #             )
        #         )

    return [entity_list, position, real_position]


def _action_entities(
    action_part: dict,
    position: int,
    real_position: int,
    script_path: str,
    parent: int = None,
    indentation_level: int = 1,
    first_element: bool = True,
    loop_action: bool = False,
) -> list:
    """The function creates a list of entities for one action list element.

    Args:
        action_part (dict): The action list element
        position (int): The position of the entity in the list
        parent (int): The parent entity of condition entities

    Returns:
        list: A list of entities as Entity objects
    """

    # list of entities in the trigger part
    entity_list = []
    # entity parameter role is start
    param_role = OUTPUT

    # check if the action is enabled
    if CONF_ENABLED in action_part:
        try:
            bool_val = action_part[CONF_ENABLED]
        except TypeError:
            bool_val = None
        if bool_val is False:
            return [entity_list, position, real_position]

    # processes a conditional action
    if SCRIPT_ACTION_IF in action_part:
        indentation_level = asg.start_action_condition_block(
            filepath=script_path,
            indentation_lvl=indentation_level,
            first_element=first_element,
            not_condition=False,
        )

        if_entities = []
        # make it a list if it is not
        if not isinstance(action_part[SCRIPT_ACTION_IF], list):
            conditions = [action_part]
        else:
            conditions = action_part[SCRIPT_ACTION_IF]

        # group the conditions together if there are multiple
        if len(conditions) > 1:
            new_parent = position
            position += 1
        else:
            new_parent = parent

        first_element = True
        no_entities = False
        then_block = False

        # create all condition entities which are needed for the action
        for condition in conditions:
            if_results = _condition_entities(
                condition_part=condition,
                position=position,
                parent=new_parent,
                real_position=real_position,
                script_path=script_path,
                indentation_level=indentation_level,
                first_element=first_element,
                source=CONF_ACTION,
            )

            if len(if_results[0]) > 0:
                if first_element:
                    first_element = False

            if_entities += if_results[0]
            # set the position for the next condition
            position = if_results[1] + 1
            real_position = if_results[2]

        if len(if_entities) > 0:
            entity_list += if_entities
        else:
            no_entities = True

        # close the condition block
        asg.close_action_condition_block(
            filepath=script_path,
            indentation_lvl=indentation_level,
            no_condition=no_entities,
        )

        # processes the then action of the conditional action
        if CONF_THEN in action_part:
            then_block = True

            then_entities = []
            # make it a list if it is not
            if not isinstance(action_part[CONF_THEN], list):
                actions = [action_part[CONF_THEN]]
            else:
                actions = action_part[CONF_THEN]

            # group the actions together if there are multiple
            if len(actions) > 1:
                new_parent = position
                position += 1
            else:
                new_parent = parent

            first_element = True

            for action in actions:
                then_results = _action_entities(
                    action_part=action,
                    position=position,
                    parent=new_parent,
                    real_position=real_position,
                    script_path=script_path,
                    indentation_level=indentation_level,
                    first_element=first_element,
                    loop_action=loop_action,
                )

                if len(then_results[0]) > 0:
                    if first_element:
                        first_element = False

                then_entities += then_results[0]
                # set the position for the next action
                position = then_results[1] + 1
                real_position = then_results[2]

            # set the position back to the last entity
            position -= 1
            entity_list += then_entities

            if len(then_entities) == 0:
                asg.create_empty_action_section(
                    filepath=script_path, indentation_lvl=indentation_level
                )
        else:
            asg.create_empty_action_section(
                filepath=script_path, indentation_lvl=indentation_level
            )

        if CONF_ELSE in action_part:
            if then_block:
                position += 1

            asg.create_else_action_section(
                filepath=script_path, indentation_lvl=indentation_level
            )

            else_entities = []
            # make it a list if it is not
            if not isinstance(action_part[CONF_ELSE], list):
                actions = [action_part[CONF_ELSE]]
            else:
                actions = action_part[CONF_ELSE]

            # group the actions together if there are multiple
            if len(actions) > 1:
                new_parent = position
                position += 1
            else:
                new_parent = parent

            first_element = True

            for action in actions:
                else_results = _action_entities(
                    action_part=action,
                    position=position,
                    parent=new_parent,
                    real_position=real_position,
                    script_path=script_path,
                    indentation_level=indentation_level,
                    first_element=first_element,
                    loop_action=loop_action,
                )

                if len(else_results[0]) > 0:
                    if first_element:
                        first_element = False

                else_entities += else_results[0]
                # set the position for the next action
                position = else_results[1] + 1
                real_position = else_results[2]

            # set the position back to the last entity
            position -= 1
            entity_list += else_entities

            if len(else_entities) == 0:
                asg.create_empty_action_section(
                    filepath=script_path, indentation_lvl=indentation_level
                )

            indentation_level -= 1

    # processes a conditional action with multiple options
    elif CONF_CHOOSE in action_part:
        choose = action_part[CONF_CHOOSE]
        first_entity = True

        # create the parent entity for all entities in the choose block
        parent = position
        position += 1

        for option in choose:
            if CONF_CONDITIONS in option or CONF_CONDITION in option:
                if first_entity:
                    first_element = True
                else:
                    first_element = False

                indentation_level = asg.start_action_condition_block(
                    filepath=script_path,
                    indentation_lvl=indentation_level,
                    first_element=first_element,
                    not_condition=False,
                )

                new_entity_list = []
                # make it a list if it is not
                if CONF_CONDITIONS in option:
                    conditions = option[CONF_CONDITIONS]
                else:
                    conditions = [option]

                # group the conditions together if there are multiple
                if len(conditions) > 1:
                    new_parent = position
                    position += 1
                else:
                    new_parent = parent

                first_element = True
                no_entities = False

                for condition in conditions:
                    results = _condition_entities(
                        condition_part=condition,
                        position=position,
                        parent=new_parent,
                        script_path=script_path,
                        real_position=real_position,
                        indentation_level=indentation_level,
                        first_element=first_element,
                        source=CONF_ACTION,
                    )

                    if len(results[0]) > 0:
                        if first_element:
                            first_element = False
                            first_entity = False

                    new_entity_list += results[0]
                    # set the position for the next condition
                    position = results[1] + 1
                    real_position = results[2]

                if len(new_entity_list) > 0:
                    entity_list += new_entity_list
                else:
                    no_entities = True

                # close the condition block
                asg.close_action_condition_block(
                    filepath=script_path,
                    indentation_lvl=indentation_level,
                    no_condition=no_entities,
                )

            if CONF_SEQUENCE in option:
                if first_entity:
                    position += 1
                    first_entity = False

                action_list = []
                # make it a list if it is not
                if not isinstance(option[CONF_SEQUENCE], list):
                    actions = [option[CONF_SEQUENCE]]
                else:
                    actions = option[CONF_SEQUENCE]

                if len(actions) > 1:
                    new_parent = position
                    position += 1
                else:
                    new_parent = parent

                for action in actions:
                    results = _action_entities(
                        action_part=action,
                        position=position,
                        real_position=real_position,
                        script_path=script_path,
                        parent=new_parent,
                        indentation_level=indentation_level,
                        first_element=first_element,
                        loop_action=loop_action,
                    )
                    action_list += results[0]
                    # set the position for the next action
                    position = results[1] + 1
                    real_position = results[2]

                entity_list += action_list
                if len(action_list) == 0:
                    asg.create_empty_action_section(
                        filepath=script_path, indentation_lvl=indentation_level
                    )
            else:
                asg.create_empty_action_section(
                    filepath=script_path, indentation_lvl=indentation_level
                )
            indentation_level -= 1

        # processes the default action/s of the choose action with multiple options
        if CONF_DEFAULT in action_part:
            indentation_level += 1

            asg.create_else_action_section(
                filepath=script_path, indentation_lvl=indentation_level
            )

            action_list = []

            # make it a list if it is not
            if not isinstance(action_part[CONF_DEFAULT], list):
                default_actions = [action_part[CONF_DEFAULT]]
            else:
                default_actions = action_part[CONF_DEFAULT]

            if len(default_actions) > 1:
                new_parent = position
                position += 1
            else:
                new_parent = parent

            first_element = True

            for action in default_actions:
                results = _action_entities(
                    action_part=action,
                    position=position,
                    real_position=real_position,
                    script_path=script_path,
                    parent=new_parent,
                    indentation_level=indentation_level,
                    first_element=first_element,
                    loop_action=loop_action,
                )
                action_list += results[0]
                # set the position for the next action
                position = results[1] + 1
                real_position = results[2]

            entity_list += action_list

        # set the position back to the last entity
        position -= 1

    # processes a parallel grouping action
    elif CONF_PARALLEL in action_part:
        # make it a list if it is not
        if isinstance(action_part[CONF_PARALLEL], list):
            action_list = action_part[CONF_PARALLEL]
        else:
            action_list = [action_part[CONF_PARALLEL]]

        if len(action_list) > 1:
            new_parent = position
            position += 1
        else:
            new_parent = parent

        for action in action_list:
            results = _action_entities(
                action_part=action,
                position=position,
                real_position=real_position,
                script_path=script_path,
                parent=new_parent,
                indentation_level=indentation_level,
                first_element=first_element,
                loop_action=loop_action,
            )
            entity_list += results[0]
            # set the position for the next action
            position = results[1] + 1
        # set the position back to the last entity
        position -= 1

    # processes a repeat grouping action
    elif CONF_REPEAT in action_part:
        repeat_part = action_part[CONF_REPEAT]
        conditions = []
        loop_tpye = None
        loop_setting = []
        is_infinite = False

        if CONF_WHILE in repeat_part:
            conditions = repeat_part[CONF_WHILE]
            loop_tpye = CONF_WHILE
        elif CONF_UNTIL in repeat_part:
            conditions = repeat_part[CONF_UNTIL]
            loop_tpye = CONF_UNTIL
        elif CONF_FOR_EACH in repeat_part:
            loop_setting = repeat_part[CONF_FOR_EACH]
            loop_tpye = CONF_FOR_EACH
        elif CONF_COUNT in repeat_part:
            loop_setting = [0, repeat_part[CONF_COUNT]]
            loop_tpye = CONF_FOR

        indentation_level = asg.start_action_loop_block(
            loop_type=loop_tpye,
            filepath=script_path,
            indentation_lvl=indentation_level,
            loop_settings=loop_setting,
        )

        if loop_tpye == CONF_WHILE or loop_tpye == CONF_UNTIL:
            if loop_tpye == CONF_UNTIL:
                not_condition = False
            else:
                not_condition = True

            indentation_level = asg.start_action_condition_block(
                filepath=script_path,
                indentation_lvl=indentation_level,
                first_element=True,
                not_condition=not_condition,
            )

            condition_entities = []
            # make it a list if it is not
            if not isinstance(conditions, list):
                conditions = [conditions]

            # group all condition entities in a new parent if there are more than one
            if len(conditions) > 1:
                new_parent = position
                position += 1
            else:
                new_parent = parent

            first_element = True
            no_entities = False

            # create all condition entities which are needed for the repeated action/s
            for condition in conditions:
                results = _condition_entities(
                    condition_part=condition,
                    position=position,
                    parent=new_parent,
                    script_path=script_path,
                    real_position=real_position,
                    indentation_level=indentation_level,
                    first_element=first_element,
                    source=CONF_ACTION,
                )
                if len(results[0]) > 0:
                    if first_element:
                        first_element = False

                condition_entities += results[0]
                # set the position for the next condition
                position = results[1] + 1
                real_position = results[2]

            if len(condition_entities) > 0:
                entity_list += condition_entities

            else:
                if loop_tpye == CONF_UNTIL:
                    is_infinite = True
                no_entities = True

            # close the condition block
            asg.close_action_condition_block(
                filepath=script_path,
                indentation_lvl=indentation_level,
                no_condition=no_entities,
            )

            # reset the indentation level back to the last entity
            indentation_level -= 1

            # set the loop_is_running varible to false
            asg.create_action_loop_stop(
                filepath=script_path,
                indentation_lvl=indentation_level,
                loop_type=loop_tpye,
            )

        if CONF_SEQUENCE in repeat_part:
            loop_action = True

            if isinstance(repeat_part[CONF_SEQUENCE], list):
                for action in repeat_part[CONF_SEQUENCE]:
                    results = _action_entities(
                        action_part=action,
                        position=position,
                        real_position=real_position,
                        script_path=script_path,
                        parent=parent,
                        indentation_level=indentation_level,
                        first_element=first_element,
                        loop_action=loop_action,
                    )
                    entity_list += results[0]
                    # set the position for the next action
                    position = results[1] + 1
                # set the position back to the last entity
                position -= 1

            # close the loop block
            indentation_level = asg.close_action_loop_block(
                filepath=script_path,
                indentation_lvl=indentation_level,
                is_infinite=is_infinite,
                loop_tpye=loop_tpye,
            )

    # processes a sequencal grouping action
    elif CONF_SEQUENCE in action_part:
        if isinstance(action_part[CONF_SEQUENCE], list):
            for action in action_part[CONF_SEQUENCE]:
                results = _action_entities(
                    action_part=action,
                    position=position,
                    real_position=real_position,
                    script_path=script_path,
                    parent=parent,
                    indentation_level=indentation_level,
                    first_element=first_element,
                    loop_action=loop_action,
                )
                entity_list += results[0]
                # set the position for the next action
                position = results[1] + 1
            # set the position back to the last entity
            position -= 1

    # processes a condition in the action part
    elif CONF_CONDITION in action_part:
        indentation_level = asg.start_action_condition_block(
            filepath=script_path,
            indentation_lvl=indentation_level,
            first_element=first_element,
            not_condition=True,
        )

        new_entity_list = []
        # make it a list if it is not
        if not isinstance(action_part[CONF_CONDITION], list):
            conditions = [action_part]
        else:
            conditions = action_part[CONF_CONDITION]

        # group all condition entities in a new parent if there are more than one
        if len(conditions) > 1:
            new_parent = position
            position += 1
        else:
            new_parent = parent

        first_element = True

        for condition in conditions:
            results = _condition_entities(
                condition_part=condition,
                position=position,
                parent=new_parent,
                script_path=script_path,
                real_position=real_position,
                indentation_level=indentation_level,
                first_element=first_element,
                source=CONF_ACTION,
            )
            if len(results[0]) > 0:
                if first_element:
                    first_element = False

            new_entity_list += results[0]
            # set the position for the next condition
            position = results[1] + 1
            real_position = results[2]

        # reset the position back to the last entity
        position -= 1

        entity_list += new_entity_list

        # close the condition block
        asg.close_action_condition_block(
            filepath=script_path, indentation_lvl=indentation_level, timeout=False
        )

    # processes a event action
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

        entity = Entity(
            parent=parent,
            position=position,
            param_role=param_role,
            integration=action_part[CONF_EVENT],
            entity_name=str(uuid.uuid4()),
            expected_value=exp_value,
        )
        entity_list.append(entity)
        asg.create_action_script(
            action_type=CONF_EVENT,
            entity=entity,
            filepath=script_path,
            indentation_lvl=indentation_level,
            loop_action=loop_action,
        )

    # processes a service action
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
                        elif is_jinja_template(entity):
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
        entity = Entity(
            parent=parent,
            position=position,
            param_role=param_role,
            integration=integration,
            entity_name=entity_name,
            expected_value=exp_value,
        )
        entity_list.append(entity)
        asg.create_action_script(
            action_type=CONF_SERVICE,
            entity=entity,
            filepath=script_path,
            indentation_lvl=indentation_level,
            loop_action=loop_action,
        )

    # processes a wait for a trigger action
    elif SCRIPT_ACTION_WAIT_FOR_TRIGGER in action_part:
        indentation_level = asg.start_action_condition_block(
            filepath=script_path,
            indentation_lvl=indentation_level,
            first_element=True,
            not_condition=True,
        )

        new_entity_list = []
        # make it a list if it is not
        if not isinstance(action_part[SCRIPT_ACTION_WAIT_FOR_TRIGGER], list):
            trigger_list = [action_part[SCRIPT_ACTION_WAIT_FOR_TRIGGER]]
        else:
            trigger_list = action_part[SCRIPT_ACTION_WAIT_FOR_TRIGGER]

        # group all trigger entities in a new parent if there are more than one
        if len(trigger_list) > 1:
            new_parent = position
            position += 1
        else:
            new_parent = parent

        first_element = True

        # create all trigger entities which are needed for the action
        for trigger in trigger_list:
            if not first_element:
                asg.create_next_logic_condition_part(
                    condition_type=CONF_OR,
                    filepath=script_path,
                    indentation_lvl=indentation_level,
                )

            results = _trigger_entities(
                trigger_part=trigger,
                position=position,
                real_position=real_position,
                script_path=script_path,
                parent=new_parent,
                indentation_level=indentation_level,
                source=CONF_ACTION,
            )

            if len(results[0]) > 0:
                if first_element:
                    first_element = False

                # set the parameter role to input
                for entity in results[0]:
                    entity.parameter_role = INPUT

                new_entity_list += results[0]
                real_position = results[2]
                # set the position for the next trigger
                position = results[1] + 1

        # set the position back to the last entity
        position -= 1
        # add the new entities to the entity list
        entity_list += new_entity_list

        if len(results[0]) > 0:
            if CONF_TIMEOUT in action_part:
                if CONF_CONTINUE_ON_TIMEOUT in action_part:
                    continue_action = action_part[CONF_CONTINUE_ON_TIMEOUT]
                else:
                    continue_action = True
            else:
                continue_action = False

            asg.close_action_condition_block(
                script_path, indentation_level, timeout=continue_action
            )

    # processes a device action
    elif CONF_DEVICE_ID in action_part:
        integration = action_part[CONF_DOMAIN]
        entity_name = action_part[CONF_DEVICE_ID]
        exp_value = {}
        if CONF_ENTITY_ID in action_part:
            exp_value[CONF_ENTITY_ID] = action_part[CONF_ENTITY_ID]
        exp_value[CONF_SERVICE] = action_part[CONF_TYPE]

        # create the entity
        entity = Entity(
            parent=parent,
            position=position,
            param_role=param_role,
            integration=integration,
            entity_name=entity_name,
            expected_value=exp_value,
        )
        entity_list.append(entity)

        asg.create_action_script(
            action_type=CONF_DEVICE,
            entity=entity,
            filepath=script_path,
            indentation_lvl=indentation_level,
            loop_action=loop_action,
        )

    elif CONF_STOP in action_part:
        asg.create_stopping_action(script_path, indentation_level, False)

    # TODO add variables for more detailed template actionss
    # processes variables in the action part
    elif CONF_VARIABLES in action_part:
        pass

    # TODO add variables for more detailed template actionss
    # processes a wait for a template action
    elif SCRIPT_ACTION_WAIT_TEMPLATE in action_part:
        pass

    return [entity_list, position, real_position]


def _extract_all_trigger(automation_config: AutomationConfig, script_path: str) -> list:
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
    real_position = 0
    for trigger in triggers:
        return_list = _trigger_entities(trigger, position, real_position, script_path)
        trigger_entities += return_list[0]
        position = return_list[1] + 1
        real_position = return_list[2]
    if len(trigger_entities) != real_position:
        raise vol.Invalid("The amount of entities and the real position do not match")
    asg.close_trigger_section(script_path)
    return trigger_entities


def _extract_all_conditions(
    automation_config: AutomationConfig, script_path: str
) -> list:
    """
    Extract the condition from the data.

    Args:
        automation_config (AutomationConfig): The automation configuration data.

    Returns:
        list: A list of condition entities extracted from the data.
    """
    asg.init_condition_part(script_path)
    condition_entities = []
    conditions = automation_config[CONF_CONDITION]
    position = 0
    real_position = 0
    num_condition_entities = 0

    for condition in conditions:
        if position != 0:
            first_element = False
        else:
            first_element = True

        return_list = _condition_entities(
            condition, position, real_position, script_path, first_element=first_element
        )
        condition_entities += return_list[0]
        position = return_list[1] + 1
        real_position = return_list[2]

        num_condition_entities += len(return_list[0])
        if return_list[0] != []:
            if (
                return_list[0][-1].integration == "zone"
                or return_list[0][-1].integration == "trigger"
            ):
                num_condition_entities -= 1

    if num_condition_entities != real_position:
        raise vol.Invalid("The amount of entities and the real position do not match")
    asg.close_condition_section(script_path)
    return condition_entities


def _extract_all_actions(automation_config: AutomationConfig, script_path: str) -> list:
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
    real_position = 0
    num_action_entities = 0

    asg.init_action_part(script_path)

    for action in actions:
        return_list = _action_entities(
            action_part=action,
            position=position,
            real_position=real_position,
            script_path=script_path,
            first_element=True,
            parent=None,
            loop_action=False,
        )

        action_entities += return_list[0]
        position = return_list[1] + 1
        real_position = return_list[2]

        for action_enitiy in return_list[0]:
            if (
                action_enitiy.parameter_role == INPUT
                and not action_enitiy.integration == CONF_ZONE
            ):
                num_action_entities += 1

    if num_action_entities != real_position:
        raise vol.Invalid("The amount of entities and the real position do not match")

    asg.close_action_section(script_path)
    return action_entities


def create_procedure_list(
    automation_config: AutomationConfig, script_path: str
) -> list:
    """
    Create a list of entities from the automation configuration.
    """
    entity_list = []
    entity_list += _extract_all_trigger(automation_config, script_path)
    entity_list += _extract_all_conditions(automation_config, script_path)
    entity_list += _extract_all_actions(automation_config, script_path)
    return entity_list


def create_automation(automation_config: AutomationConfig) -> dict:
    """
    Create an automation from the automation configuration.
    """
    automation_data = {}

    automation_name = automation_config.automation_name
    automation_script = init_automation_script(automation_name)

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

    automation_data["entities"] = create_procedure_list(
        automation_config, automation_script
    )
    automation_data["infos"] = automation

    return automation_data
