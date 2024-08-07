"""
This module contains the functions for breaking down the conditions of an automation and creating its contained entities.
Within this function, the functions for creating the condition part for the automation script are also called.


The information about the condition functions are from:
https://www.home-assistant.io/docs/scripts/conditions
"""

from . import automation_script_gen as asg

from ..utils.env_const import INPUT

from ..utils.env_helper import Entity, is_jinja_template
from ..ha_automation_utils.home_assistant_config_validation import (
    valid_entity_id,
)
from ..ha_automation_utils.home_assistant_automation_validation import AutomationConfig
from ..ha_automation_utils.home_assistant_const import (
    CONF_ABOVE,
    CONF_AFTER,
    CONF_AFTER_OFFSET,
    CONF_AND,
    CONF_ATTRIBUTE,
    CONF_BEFORE,
    CONF_BEFORE_OFFSET,
    CONF_BELOW,
    CONF_CONDITION,
    CONF_CONDITIONS,
    CONF_DATETIME,
    CONF_DEVICE,
    CONF_DEVICE_ID,
    CONF_DOMAIN,
    CONF_ENABLED,
    CONF_ENTITY_ID,
    CONF_FOR,
    CONF_ID,
    CONF_NOT,
    CONF_NUMERIC_STATE,
    CONF_OR,
    CONF_STATE,
    CONF_TEMPLATE,
    CONF_TIME,
    CONF_TRIGGER,
    CONF_TYPE,
    CONF_VALUE_TEMPLATE,
    CONF_WEEKDAY,
    CONF_ZONE,
)

import re
import voluptuous as vol
import uuid


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
            if not isinstance(exp_value[CONF_ABOVE], float) and valid_entity_id(
                str(exp_value[CONF_ABOVE])
            ):
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
            if not isinstance(exp_value[CONF_BELOW], float) and valid_entity_id(
                str(exp_value[CONF_BELOW])
            ):
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


def extract_all_conditions(
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
    if CONF_CONDITION in automation_config:
        conditions = automation_config[CONF_CONDITION]
    else:
        conditions = []
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
