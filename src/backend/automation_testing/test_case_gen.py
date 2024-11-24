from backend.database import db_create_test_cases

from backend.utils.env_helper import is_float_or_int
from backend.utils.env_helper_classes import Entity

from itertools import product


def add_test_cases_to_db(
    automation_id: int,
    combination_of_test_inputs: list,
    input_value_list: list,
    reqiurements: list,
    case_priorities: list,
):
    """
    Function to create a test case for the automation and add it to the database

    Args:
        automation_id (int): the id of the automation
        combination_of_test_inputs (list): the different test case input combinations
        input_value_list (list): the input value list for the automation entity
        reqiurements (list): the requirements for the test cases
        case_priorities (list): the priorities for the test cases

    Returns:
        list: the created test cases dictionary with the test case id and the input ids as a list
    """

    # create the test cases
    test_cases = []

    new_test_case = 0

    while new_test_case < len(combination_of_test_inputs):
        reqiurement_str = reqiurements[new_test_case]
        case_priority = case_priorities[new_test_case]

        # handle empty strings
        if reqiurement_str == "":
            reqiurement_str = None

        if case_priority == "":
            case_priority = None
        else:
            case_priority = int(case_priority)

        # create the test case
        new_test_case_id = db_create_test_cases.create_test_case(
            automation_id, reqiurement_str, case_priority
        )

        # create the test case inputs
        case_input_ids = _create_test_case_inputs(
            combination_of_test_inputs[new_test_case],
            input_value_list,
            new_test_case_id,
        )

        test_cases.append(
            {"test_case_id": new_test_case_id, "input_ids": case_input_ids}
        )

        new_test_case += 1

    return test_cases


def _create_test_case_inputs(
    test_case_input_values, input_value_list: list, case_id: int
):
    """
    Create the test case inputs for the test case

    Args:
        test_case_input_values (list): the test case input values for the test case
        input_value_list (list): the input value list for the automation entity
        new_case_id (int): the id of the test case

    Returns:
        list: the created test case input ids as a list
    """
    case_input_ids = []

    for i, test_case_input in enumerate(test_case_input_values):
        entity: Entity = input_value_list[i]["entity"]

        case_input_id = db_create_test_cases.create_test_case_input(
            test_value=is_float_or_int(test_case_input),
            test_case_id=case_id,
            a_id=input_value_list[i]["a_id"],
            e_id=entity.entity_id,
            p_role=entity.parameter_role,
            position=entity.position,
        )

        case_input_ids.append(case_input_id)

    return case_input_ids


def create_test_case_input_combinations(input_value_list: list):
    """
    Function to create the different test case input combinations for the test case

    Args:
        input_value_list (list): the input value list for the test values of the automation entities

    Returns:
        list: the different test case input combinations as a list
    """

    # get the different test cases and the needed input values
    test_case_input_values = []

    for input_values in input_value_list:
        input_values: dict

        test_values = input_values["test_value"]
        if isinstance(test_values, list):
            test_case_input_values.append(test_values)
        else:
            test_case_input_values.append([test_values])

    result = [list(item) for item in product(*test_case_input_values)]

    return result
