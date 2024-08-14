"""
This module contains the functions to break down the triggers of an automation and create their contained entities.
Within this function, the functions to create the trigger part for the automation script are also called.

The information about the trigger functions are from:
https://www.home-assistant.io/docs/automation/trigger/
"""

from . import automation_script_gen as asg

from ..utils.env_const import START

from ..utils.env_helper_classes import Entity
from ..utils.env_helper import is_jinja_template

from ..ha_automation_utils.home_assistant_config_validation import (
    valid_entity_id,
)
from ..ha_automation_utils.home_assistant_automation_validation import AutomationConfig
from ..ha_automation_utils.home_assistant_const import (
    CONF_ABOVE,
    CONF_ALLOWED_METHODS,
    CONF_AT,
    CONF_ATTRIBUTE,
    CONF_BELOW,
    CONF_CALENDAR,
    CONF_COMMAND,
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
    CONF_ID,
    CONF_LOCAL,
    CONF_NOFITY_ID,
    CONF_NOT_FROM,
    CONF_NOT_TO,
    CONF_NUMERIC_STATE,
    CONF_OFFSET,
    CONF_PAYLOAD,
    CONF_PERS_NOTIFICATION,
    CONF_PLATFORM,
    CONF_QOS,
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
            real_position = asg.create_combination_trigger_script(
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
            if not isinstance(exp_value[CONF_ABOVE], float) and valid_entity_id(
                str(exp_value[CONF_ABOVE])
            ):
                parent = position
                position += 1

                # change the integration to sensor_float if the entity is a sensor
                integration = trigger_part[CONF_ABOVE].split(".")[0]
                if integration == "sensor":
                    integration = "sensor_float"
                    # rename the entity name in the expected value of the main entity
                    exp_value[CONF_ABOVE] = integration + "." + trigger_part[CONF_ABOVE].split(".")[1]

                exp_value_entity_list.append(
                    Entity(
                        parent=parent,
                        position=None,
                        param_role=param_role,
                        integration=integration,
                        entity_name=trigger_part[CONF_ABOVE].split(".")[1],
                        expected_value={
                            CONF_BELOW: ""
                        },  # added after the generation of the comparing entity/ies
                    )
                )

        if CONF_BELOW in trigger_part:
            exp_value[CONF_BELOW] = trigger_part[CONF_BELOW]
            # create the comparing entities for the numerical state trigger
            if not isinstance(exp_value[CONF_BELOW], float) and valid_entity_id(
                str(exp_value[CONF_BELOW])
            ):
                # set the parent entity for the comparing entity/ies if no above entity exists
                if parent is None:
                    parent = position
                    position += 1

                # change the integration to sensor_float if the entity is a sensor
                integration = trigger_part[CONF_BELOW].split(".")[0]
                if integration == "sensor":
                    integration = "sensor_float"
                    # rename the entity name in the expected value of the main entity
                    exp_value[CONF_BELOW] = integration + "." +  trigger_part[CONF_BELOW].split(".")[1]

                exp_value_entity_list.append(
                    Entity(
                        parent=parent,
                        position=None,
                        param_role=param_role,
                        integration=integration,
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
                # change the integration to sensor_float if the entity is a sensor
                if entity_integration == "sensor":
                    entity_integration = "sensor_float"

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
            
            # change the integration to sensor_float if the entity is a sensor
            if integration == "sensor":
                integration = "sensor_float"

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


def extract_all_trigger(automation_config: AutomationConfig, script_path: str) -> list:
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
