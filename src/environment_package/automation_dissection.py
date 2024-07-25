"""
This module is responsible for automating the desection of the data.

The information about the trigger functions are from: 
https://www.home-assistant.io/docs/automation/trigger/
"""


import re
import uuid

import voluptuous as vol

from .ha_automation.home_assistant_automation_config import AutomationConfig
from .ha_automation.home_assistant_const import (CONF_ABOVE,
                                                 CONF_ALLOWED_METHODS, CONF_AT,
                                                 CONF_ATTRIBUTE, CONF_BELOW,
                                                 CONF_CALENDAR, CONF_COMMAND,
                                                 CONF_CONVERSATION,
                                                 CONF_DEVICE, CONF_DEVICE_ID,
                                                 CONF_DOMAIN, CONF_ENTITY_ID,
                                                 CONF_EVENT,
                                                 CONF_EVENT_CONTEXT,
                                                 CONF_EVENT_DATA,
                                                 CONF_EVENT_TYPE, CONF_FOR,
                                                 CONF_FROM, CONF_GEO_LOCATION,
                                                 CONF_LOCAL, CONF_NOFITY_ID,
                                                 CONF_NOT_FROM, CONF_NOT_TO,
                                                 CONF_NUMERIC_STATE,
                                                 CONF_OFFSET, CONF_PAYLOAD,
                                                 CONF_PERS_NOTIFICATION,
                                                 CONF_PLATFORM, CONF_QOS,
                                                 CONF_SOURCE, CONF_STATE,
                                                 CONF_TEMPLATE, CONF_TIME,
                                                 CONF_TIME_PATTERN, CONF_TO,
                                                 CONF_TRIGGER, CONF_TYPE,
                                                 CONF_UPDATE_TYPE,
                                                 CONF_VALUE_TEMPLATE,
                                                 CONF_WEBHOOK, CONF_WEBHOOK_ID,
                                                 CONF_ZONE, HOURS, MINUTES,
                                                 SECONDS, TAG_ID,
                                                 test_leading_zero)


class Entity():
    """
    Class to represent an entity.
    """

    integration: str = None
    entity_name : str | list = None
    expected_value: dict = None

    def __init__(self, integration, entity_name, expected_value=None):
        """
        Create an entity from the automation part.

        Args:
            integration (str): The integration of the entity
            entity_name (str): The name of the entity
            expected_value (int | str | dict): The possible value of the entity

        Returns:
            dict: The entity as a dictionary
        """

        self.integration = integration
        self.entity_name = integration + "." + entity_name
        if expected_value == {}:
            self.expected_value = None
        else:
            self.expected_value = expected_value.copy()
    
    def get_name(self) -> str:
        """
        Get the name of the entity.
        """
        return self.entity_name
    
    def get_integration(self) -> str:
        """
        Get the integration of the entity.
        """
        return self.integration

    def get_expected_value(self) -> dict:
        """
        Get the possible value of the entity.
        """
        return self.expected_value

    
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
    
    # if the trigger is an event
    if platform ==  CONF_EVENT:
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
            # create all entities in the trigger part 
            for event_type in trigger_part[CONF_EVENT_TYPE]:
                exp_value[CONF_EVENT_TYPE] = event_type
                entity_name = str(uuid.uuid4())
                new_entity = Entity(integration=CONF_EVENT, entity_name=entity_name, expected_value=exp_value)
                Entity_list.append(new_entity)
        else:
            # create the single entity in the event_type part 
            exp_value[CONF_EVENT_TYPE] = trigger_part[CONF_EVENT_TYPE]
            entity = Entity(integration=CONF_EVENT, entity_name=str(uuid.uuid4()), expected_value=exp_value)
            Entity_list.append(entity)
    
    # if is a home_assistant start or shutdown event
    elif platform == "homeassistant":
        # create the home assistant entity
        exp_value = {CONF_EVENT : trigger_part[CONF_EVENT]}
        Entity_list.append(Entity(integration="homeassistant", entity_name="_", expected_value=exp_value))
    
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
        Entity_list.append(Entity(integration="mqtt", entity_name=trigger_part["topic"], expected_value=exp_value))

    # if the trigger is a numerical state change
    elif platform == CONF_NUMERIC_STATE:

        # add the possible value range to the entity/ies
        exp_value_str = "__VALUE__"
        if CONF_ABOVE in trigger_part:
            exp_value_str = str(trigger_part[CONF_ABOVE]) + " < " + exp_value_str
        if CONF_BELOW in trigger_part:
            exp_value_str = exp_value_str + " < " + str(trigger_part[CONF_BELOW])
        exp_value = {"value": exp_value_str}
        
        # add the time the value has to stay in the trigger range
        if CONF_FOR in trigger_part:
            exp_value[CONF_FOR] = trigger_part[CONF_FOR]

        # create all entities in the trigger part 
        if isinstance(trigger_part[CONF_ENTITY_ID], list):
            for entity in trigger_part[CONF_ENTITY_ID]:
                entity_integration = entity.split(".")[0]
                entity_name = entity.split(".")[1]
                Entity_list.append(Entity(integration=entity_integration, entity_name=entity_name, expected_value=exp_value))
        else:
            # create the single entity in the event_type part 
            Entity_list.append(Entity(integration=trigger_part[CONF_ENTITY_ID].split(".")[0], entity_name=trigger_part[CONF_ENTITY_ID].split(".")[1], expected_value=exp_value))
    
    # if the trigger is a state change
    elif platform == CONF_STATE:

        # add the state values of the trigger
        if CONF_TO in trigger_part:
            exp_value = {CONF_TO : str(trigger_part[CONF_TO])}
        else:
            exp_value = {CONF_NOT_TO : str(trigger_part[CONF_NOT_TO])}
        if CONF_FROM in trigger_part:
            exp_value[CONF_FROM] = trigger_part[CONF_FROM]
        elif CONF_NOT_FROM in trigger_part:
            exp_value[CONF_NOT_FROM] = trigger_part[CONF_NOT_FROM]
        if CONF_FOR in trigger_part:
            exp_value[CONF_FOR] = trigger_part[CONF_FOR]

        # create all entities in the trigger part
        if isinstance(trigger_part[CONF_ENTITY_ID], list):
            for entity in trigger_part[CONF_ENTITY_ID]:
                entity_integration = entity.split(".")[0]
                entity_name = entity.split(".")[1]
                if CONF_ATTRIBUTE in trigger_part:
                    entity_name = entity_name + "." + str(trigger_part[CONF_ATTRIBUTE])
                Entity_list.append(Entity(integration=entity_integration, entity_name=entity_name, expected_value=exp_value))
        else:
            entity_name = trigger_part[CONF_ENTITY_ID].split(".")[1]
            if CONF_ATTRIBUTE in trigger_part:
                    entity_name = entity_name + "." + str(trigger_part[CONF_ATTRIBUTE])
            # create the single entity in the event_type part 
            Entity_list.append(Entity(integration=trigger_part[CONF_ENTITY_ID].split(".")[0], entity_name=entity_name, expected_value=exp_value))

    # if the trigger is the sunset or sunrise event
    elif platform == "sun":
        
        # add the offset value of the trigger
        exp_value = {CONF_EVENT : trigger_part[CONF_EVENT]}
        if CONF_OFFSET in trigger_part:
            exp_value[CONF_OFFSET] = trigger_part[CONF_OFFSET]

        # create the sun entity
        Entity_list.append(Entity(integration="sun", entity_name="sun", expected_value=exp_value))

    # if the trigger is tag scan
    elif platform == "tag":

        # add the devics/s as possible values for the scan
        if CONF_DEVICE_ID in trigger_part:
            if isinstance(trigger_part[CONF_DEVICE_ID], list):
                exp_value = {CONF_DEVICE_ID : []}
                for device in trigger_part[CONF_DEVICE_ID]:
                    exp_value[CONF_DEVICE_ID].append(device)
            else:
                exp_value = {CONF_DEVICE_ID : trigger_part[CONF_DEVICE_ID]}
        else:
            exp_value = None

        # create all tag entities in the trigger part
        if isinstance(trigger_part[TAG_ID], list):
            for tag_id in trigger_part[TAG_ID]:
                Entity_list.append(Entity(integration="tag", entity_name=tag_id, expected_value=exp_value))
        else:
            # create the single tag entity
            Entity_list.append(Entity(integration="tag", entity_name=trigger_part[TAG_ID], expected_value=exp_value))

    # if the trigger is a template
    elif platform == CONF_TEMPLATE:
        # if trigger has a template string
        if CONF_VALUE_TEMPLATE in trigger_part:
            template_str = trigger_part[CONF_VALUE_TEMPLATE]

            # check if the string is a Jinja2 template
            if "{" in template_str and ("{%" in template_str or "{{" in template_str or "{#" in template_str):
                
                # add the possible value of the template
                exp_value = {CONF_VALUE_TEMPLATE : template_str}
                
                # add the time the value has to stay in the trigger range
                if CONF_FOR in trigger_part:
                    exp_value[CONF_FOR] = trigger_part[CONF_FOR]

                # search for entities in the template string
                entities = re.findall(r"\w+\.\w+", template_str)
                for entity in entities:
                    entity_integration = entity.split(".")[0]
                    entity_name = entity.split(".")[1]
                    Entity_list.append(Entity(integration=entity_integration, entity_name=entity_name, expected_value=exp_value))
                    
    # if the trigger is a time event
    elif platform == CONF_TIME:
        # create the time entity
        Entity_list.append(Entity(integration=CONF_TIME, entity_name=CONF_TIME, expected_value={CONF_AT : trigger_part[CONF_AT]}))

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
        Entity_list.append(Entity(integration=CONF_TIME_PATTERN, entity_name=str(uuid.uuid4()), expected_value=exp_value))

    # if the trigger is a persistant notification
    elif platform == CONF_PERS_NOTIFICATION:

        # add the notification id as the entity name
        if CONF_NOFITY_ID in trigger_part:
            entity_name = trigger_part[CONF_NOFITY_ID]
        else:
            entity_name = str(uuid.uuid4())

        # add the update type as the possible value
        exp_value = {CONF_UPDATE_TYPE : trigger_part[CONF_UPDATE_TYPE]}

        # create the persistant notification entity
        Entity_list.append(Entity(integration=CONF_PERS_NOTIFICATION, entity_name=entity_name, expected_value=exp_value))

    # if the trigger is a webhook
    elif platform == CONF_WEBHOOK:

        if CONF_ALLOWED_METHODS in trigger_part:
            exp_value = {CONF_ALLOWED_METHODS : trigger_part[CONF_ALLOWED_METHODS]}
            if CONF_LOCAL in trigger_part:
                exp_value[CONF_LOCAL] = trigger_part[CONF_LOCAL]

        # create the webhook entity
        Entity_list.append(Entity(integration=CONF_WEBHOOK, entity_name=trigger_part[CONF_WEBHOOK_ID], expected_value=exp_value))

    # if the trigger is a zone event (enter or leave)
    elif platform == CONF_ZONE:
            
        # add the entity id of the person and the event type as the possible value
        exp_value = {CONF_EVENT : trigger_part[CONF_EVENT]}
        exp_value[CONF_ENTITY_ID] = trigger_part[CONF_ENTITY_ID]

        # create the zone entity
        Entity_list.append(Entity(integration=CONF_ZONE, entity_name=trigger_part[CONF_ZONE].split(".")[1], expected_value=exp_value))

    # if the trigger is a geo location event
    elif platform == CONF_GEO_LOCATION:
        
        # add the entity id of the person and the event type as the possible value
        exp_value = {CONF_EVENT : trigger_part[CONF_EVENT]}
        exp_value[CONF_SOURCE] = trigger_part[CONF_SOURCE]

        # create the zone entity
        Entity_list.append(Entity(integration=CONF_ZONE, entity_name=trigger_part[CONF_ZONE].split(".")[1], expected_value=exp_value))

    # if the trigger is a device event
    elif platform == CONF_DEVICE:

        # add the entity id and domain as the possible value
        exp_value = {CONF_ENTITY_ID : trigger_part[CONF_ENTITY_ID]}
        exp_value[CONF_TYPE] = trigger_part[CONF_TYPE]
        exp_value[CONF_DOMAIN] = trigger_part[CONF_DOMAIN]

        # create the device entity
        Entity_list.append(Entity(integration=CONF_DEVICE, entity_name=trigger_part[CONF_DEVICE_ID], expected_value=exp_value))

    # if the trigger is a calendar event
    elif platform == CONF_CALENDAR:

        # add the calendar event as the possible value
        exp_value = {CONF_EVENT : trigger_part[CONF_EVENT]}
        if CONF_OFFSET in trigger_part:
            exp_value[CONF_OFFSET] = trigger_part[CONF_OFFSET]
        
        # create the calendar entity
        Entity_list.append(Entity(integration=CONF_CALENDAR, entity_name=trigger_part[CONF_ENTITY_ID].split(".")[1], expected_value=exp_value))
        
    # if trigger is a sentence
    elif platform == CONF_CONVERSATION:
            
        # create the conversation entity
        Entity_list.append(Entity(integration=CONF_CONVERSATION, entity_name=str(uuid.uuid4()), expected_value={CONF_COMMAND : trigger_part[CONF_COMMAND]}))

    return Entity_list


def _extract_trigger(automation_config: AutomationConfig) -> list:
    """
    Extracts the trigger from the data.

    Args:
        automation_config (AutomationConfig): The automation configuration data.

    Returns:
        list: A list of trigger entities extracted from the data.
    """
    trigger_entities = []
    triggers = automation_config[CONF_TRIGGER]
    for trigger in triggers:
        trigger_entities += _trigger_entities(trigger)
    return trigger_entities



def _extract_condition(automation_config: AutomationConfig) -> list:
    """
    Extract the condition from the data.
    """
    pass


def _extract_action(automation_config: AutomationConfig) -> list:
    """
    Extract the action from the data.
    """
    pass


def create_entity_list(automation_config: AutomationConfig) -> list:
    """
    Create a list of entities from the automation configuration.
    """
    Entity_list = []
    Entity_list += _extract_trigger(automation_config)
    # Entity_list += _extract_condition(automation_config)
    # Entity_list += _extract_action(automation_config)
    return Entity_list

def create_automation_script(automation_config: AutomationConfig) -> str:
    """
    Create the automation script.
    """
    pass


def desect_information(automation_config: AutomationConfig) -> dict:
    """
    Extract the information from the data.
    """
    automation_data = {}
    automation_data["entities"] = create_entity_list(automation_config)
    automation_data["script"] = create_automation_script(automation_config)
    return automation_data