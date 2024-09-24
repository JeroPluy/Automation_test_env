"""
This module contains the functions for breaking down the actions of an automation and creating their contained entities.
Within this function, the functions for creating the action part for the automation script are also called.

The information about the action functions are from:
https://www.home-assistant.io/docs/scripts
"""

import uuid

import voluptuous as vol

from ..ha_automation_utils.home_assistant_automation_validation import AutomationConfig
from ..ha_automation_utils.home_assistant_const import (
    ATTR_AREA_ID,
    CONF_ACTION,
    CONF_CHOOSE,
    CONF_CONDITION,
    CONF_CONDITIONS,
    CONF_CONTINUE_ON_TIMEOUT,
    CONF_COUNT,
    CONF_DEFAULT,
    CONF_DEVICE,
    CONF_DEVICE_ID,
    CONF_DOMAIN,
    CONF_ELSE,
    CONF_ENABLED,
    CONF_ENTITY_ID,
    CONF_EVENT,
    CONF_EVENT_DATA,
    CONF_FOR,
    CONF_FOR_EACH,
    CONF_OR,
    CONF_PARALLEL,
    CONF_REPEAT,
    CONF_SEQUENCE,
    CONF_SERVICE,
    CONF_SERVICE_DATA,
    CONF_STOP,
    CONF_TARGET,
    CONF_THEN,
    CONF_TIMEOUT,
    CONF_TYPE,
    CONF_UNTIL,
    CONF_VARIABLES,
    CONF_WHILE,
    CONF_ZONE,
    SCRIPT_ACTION_IF,
    SCRIPT_ACTION_WAIT_FOR_TRIGGER,
    SCRIPT_ACTION_WAIT_TEMPLATE,
)
from ..utils.env_const import (
    ACTION_INPUT,
    OUTPUT,
)
from ..utils.env_helper import is_jinja_template
from ..utils.env_helper_classes import Entity
from . import automation_script_gen as asg
from .condtion_dissection import _condition_entities
from .trigger_dissection import _trigger_entities


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

                first_element = True

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

                    if len(results[0]) > 0:
                        if first_element:
                            first_element = False

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
            exp_value = {CONF_EVENT: action_part[CONF_EVENT]}
            for data_key in action_part[CONF_EVENT_DATA]:
                event_data[data_key] = action_part[CONF_EVENT_DATA][data_key]
            exp_value[CONF_EVENT_DATA] = event_data
        # prohibit the use of 'context' in action events

        # create the entity

        entity = Entity(
            parent=parent,
            position=position,
            param_role=param_role,
            integration=CONF_EVENT,
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
    elif CONF_SERVICE in action_part or CONF_ACTION in action_part:
        if CONF_SERVICE in action_part:
            service = action_part[CONF_SERVICE]
        else:
            service = action_part[CONF_ACTION]

        # TODO templates use could be more accurate
        integration = service.split(".")[0]
        entity_name = str(uuid.uuid4())

        exp_value = {CONF_ACTION: service.split(".")[1]}

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
            action_type=CONF_ACTION,
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

                # set the parameter role to action input
                for entity in results[0]:
                    entity.parameter_role = ACTION_INPUT

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
        exp_value[CONF_ACTION] = action_part[CONF_TYPE]

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


def extract_all_actions(automation_config: AutomationConfig, script_path: str) -> list:
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
                action_enitiy.parameter_role == ACTION_INPUT
                and not action_enitiy.integration == CONF_ZONE
            ):
                num_action_entities += 1

    if num_action_entities != real_position:
        raise vol.Invalid("The amount of entities and the real position do not match")

    asg.close_action_section(script_path)
    return action_entities
