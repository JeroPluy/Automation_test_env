"""
This module is responsible for automating the desection of the data.
"""

from .ha_automation.home_assistant_automation_config import AutomationConfig
from .ha_automation.home_assistant_const import CONF_ABOVE, CONF_ATTRIBUTE, CONF_BELOW, CONF_DEVICE_ID, CONF_ENTITY_ID, CONF_EVENT, CONF_EVENT_CONTEXT, CONF_EVENT_DATA, CONF_EVENT_TYPE, CONF_FOR, CONF_FROM, CONF_NOT_FROM, CONF_NOT_TO, CONF_NUMERICAL_STATE, CONF_OFFSET, CONF_PAYLOAD, CONF_PLATFORM, CONF_STATE, CONF_TEMPLATE, CONF_TIME, CONF_TIME_PATTERN, CONF_TO, CONF_TRIGGER, CONF_WEBHOOK, TAG_ID

class Entity():
    """
    Class to represent an entity.
    """

    integration: str = None
    entity_name : str | list = None
    pos_value: int | str | dict = None

    def __init__(self, integration, entity_name, possible_value=None):
        """
        Create an entity from the automation part.

        Args:
            integration (str): The integration of the entity
            entity_name (str): The name of the entity
            possible_value (int | str | dict): The possible value of the entity

        Returns:
            dict: The entity as a dictionary
        """

        self.integration = integration
        self.entity_name = integration + "." + entity_name
        if possible_value == {}:
            self.pos_value = None
        else:
            self.pos_value = possible_value

    
def trigger_entities(trigger_part: dict) -> list:
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
        pos_value = {}
        # if the event has a data part
        if CONF_EVENT_DATA in trigger_part:
            pos_value[CONF_EVENT_DATA] = trigger_part[CONF_EVENT_DATA]
        if CONF_EVENT_CONTEXT in trigger_part:
            for context_key in trigger_part[CONF_EVENT_CONTEXT]:
                pos_value[context_key] = trigger_part[CONF_EVENT_CONTEXT][context_key]
        
        # if the event type has multiple event entities
        if isinstance(trigger_part[CONF_EVENT_TYPE], list):
            # create all entities in the trigger part 
            for event in trigger_part[CONF_EVENT_TYPE]:
                Entity_list.append(Entity(integration=CONF_EVENT, entity_name=event, possible_value=pos_value))
        else:
            print(trigger_part[CONF_EVENT_TYPE])
            # create the single entity in the event_type part 
            entity = Entity(integration=CONF_EVENT, entity_name=trigger_part[CONF_EVENT_TYPE], possible_value=pos_value)
            Entity_list.append(entity)
    
    # if is a home_assistant start or shutdown event
    elif platform == "homeassistant":
        # create the home assistant entity
        Entity_list.append(Entity(integration="homeassistant", entity_name=trigger_part[CONF_EVENT]))
    
    # if the trigger is a mqtt message
    elif platform == "mqtt":
        if CONF_PAYLOAD in trigger_part:
            pos_value = trigger_part[CONF_PAYLOAD]
        else:
            pos_value = None

        # create the mqtt entity
        Entity_list.append(Entity(integration="mqtt", entity_name=trigger_part["topic"], possible_value=pos_value))

    # if the trigger is a numerical state change
    elif platform == CONF_NUMERICAL_STATE:

        # add the possible value range to the entity/ies
        pos_value = "__VALUE__"
        if CONF_ABOVE in trigger_part:
            pos_value = str(trigger_part[CONF_ABOVE]) + " < " + pos_value
        if CONF_BELOW in trigger_part:
            pos_value = pos_value + " < " + str(trigger_part[CONF_BELOW])

        # create all entities in the trigger part 
        if isinstance(trigger_part[CONF_ENTITY_ID], list):
            for entity in trigger_part[CONF_ENTITY_ID]:
                entity_integration = entity.split(".")[0]
                entity_name = entity.split(".")[1]
                Entity_list.append(Entity(integration=entity_integration, entity_name=entity_name, possible_value=pos_value))
        else:
            # create the single entity in the event_type part 
            Entity_list.append(Entity(integration=trigger_part[CONF_ENTITY_ID].split(".")[0], entity_name=trigger_part[CONF_ENTITY_ID].split(".")[1], possible_value=pos_value))
    
    # if the trigger is a state change
    elif platform == CONF_STATE:

        # add the state values of the trigger
        if CONF_TO in trigger_part:
            pos_value = {CONF_TO : str(trigger_part[CONF_TO])}
        else:
            pos_value = {CONF_NOT_TO : str(trigger_part[CONF_NOT_TO])}
        if CONF_FROM in trigger_part:
            pos_value[CONF_FROM] = trigger_part[CONF_FROM]
        elif CONF_NOT_FROM in trigger_part:
            pos_value[CONF_NOT_FROM] = trigger_part[CONF_NOT_FROM]
        if CONF_FOR in trigger_part:
            pos_value[CONF_FOR] = trigger_part[CONF_FOR]

        # create all entities in the trigger part
        if isinstance(trigger_part[CONF_ENTITY_ID], list):
            for entity in trigger_part[CONF_ENTITY_ID]:
                entity_integration = entity.split(".")[0]
                entity_name = entity.split(".")[1]
                if CONF_ATTRIBUTE in trigger_part:
                    entity_name = entity_name + "." + str(trigger_part[CONF_ATTRIBUTE])
                Entity_list.append(Entity(integration=entity_integration, entity_name=entity_name, possible_value=pos_value))
        else:
            # create the single entity in the event_type part 
            Entity_list.append(Entity(integration=trigger_part[CONF_ENTITY_ID].split(".")[0], entity_name=trigger_part[CONF_ENTITY_ID].split(".")[1], possible_value=pos_value))

    # if the trigger is the sunset or sunrise event
    elif platform == "sun":
        
        # add the offset value of the trigger
        pos_value = {CONF_EVENT : trigger_part[CONF_EVENT]}
        if CONF_OFFSET in trigger_part:
            pos_value[CONF_OFFSET] = trigger_part[CONF_OFFSET]

        # create the sun entity
        Entity_list.append(Entity(integration="sun", entity_name="sun", possible_value=pos_value))

    # if the trigger is tag scan
    elif platform == "tag":

        # add the devics/s as possible values for the scan
        if CONF_DEVICE_ID in trigger_part:
            if isinstance(trigger_part[CONF_DEVICE_ID], list):
                pos_value = {CONF_DEVICE_ID : []}
                for device in trigger_part[CONF_DEVICE_ID]:
                    pos_value[CONF_DEVICE_ID].append(device)
            else:
                pos_value = {CONF_DEVICE_ID : trigger_part[CONF_DEVICE_ID]}
        else:
            pos_value = None

        # create all tag entities in the trigger part
        if isinstance(trigger_part[TAG_ID], list):
            for entity in trigger_part[TAG_ID]:
                entity_integration = entity.split(".")[0]
                entity_name = entity.split(".")[1]
                if CONF_ATTRIBUTE in trigger_part:
                    entity_name = entity_name + "." + str(trigger_part[CONF_ATTRIBUTE])
                Entity_list.append(Entity(integration=entity_integration, entity_name=entity_name, possible_value=pos_value))
        else:
            # create the single tag entity
            Entity_list.append(Entity(integration="tag", entity_name=trigger_part[TAG_ID], possible_value=pos_value))

    # # TODO
    # elif platform == CONF_TEMPLATE:
    #     pass

    # # TODO
    # elif platform == CONF_TIME:
    #     pass

    # # TODO
    # elif platform == CONF_TIME_PATTERN:
    #     pass

    # # TODO
    # elif platform == CONF_PERS_NOTIFICATION:
    #     pass

    # # TODO
    # elif platform == CONF_WEBHOOK:
    #     pass

    # # TODO
    # elif platform == CONF_ZONE:
    #     pass

    # # TODO
    # elif platform == CONF_GEO_LOCATION:
    #     pass

    # # TODO
    # elif platform == CONF_DEVICE:
    #     pass

    # # TODO
    # elif platform == CALENDAR:
    #     pass

    # # TODO
    # elif platform == SENTENCE:
    #     pass

    return Entity_list


def _extract_trigger(automation_config: AutomationConfig) -> dict:
    """
    Extract the trigger from the data.
    """
    triggers : list = automation_config[CONF_TRIGGER]
    for trigger in triggers:
        print(trigger)


    


def desect_information(automation_config: AutomationConfig) -> None:
    """
    Extract the information from the data.
    """
    _extract_trigger(automation_config)