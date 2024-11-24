"""
This module contains the functions to create test cases and test case collections in the database.
"""

from backend.utils.env_const import DATABASE

import sqlite3 as sqlite


def create_test_case(
    automation_id: int, requirement: str = None, case_prio: int = None
) -> int:
    """
    Create a test case for the automation in the database

    Args:
        automation_id (int): the id of the automation
        requirement (str): the requirement string for the automation. Defaults to None.
        case_prio (int): the priority of the test case. Defaults to None.

    Returns:
        int: the id of the created test case
    """

    CREATE_TEST_CASE = """
        INSERT INTO test_case (a_id, requirement, case_priority)
        VALUES (?, ?, ?)
        """

    with sqlite.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute(CREATE_TEST_CASE, (automation_id, requirement, case_prio))
        con.commit()
        return cur.lastrowid


def create_test_case_input(
    test_value, test_case_id: int, a_id: int, e_id: int, p_role: int, position: int
) -> int:
    """
    Create a test case input for the test case in the database

    Args:
        test_value : the value of the test case input
        test_case_id (int): the id of the test case
        a_id (int): the id of the automation
        e_id (int): the id of the entity
        p_role (int): the role of the entity
        position (int): the position of the entity

    Returns:
        int: the id of the created test case input
    """

    CREATE_TEST_CASE_INPUT = """
        INSERT INTO test_case_input (test_value, case_id, a_id, e_id, p_role, position)
        VALUES (?, ?, ?, ?, ?, ?)
        """

    with sqlite.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute(
            CREATE_TEST_CASE_INPUT,
            (test_value, test_case_id, a_id, e_id, p_role, position),
        )
        con.commit()

        return cur.lastrowid


def create_test_case_collection(name: str, a_id: int) -> int:
    """
    Create a test case collection in the database for the automation

    Args:
        name (str): the name of the test case collection
        a_id (int): the id of the automation

    Returns:
        int: the id of the created test case collection
    """

    CREATE_CASE_COLLECTION = """
        INSERT INTO test_case_collection (tcc_name, a_id) 
        VALUES (?, ?)
        """

    with sqlite.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute(CREATE_CASE_COLLECTION, (name, a_id))
        con.commit()

        return cur.lastrowid


def add_test_case_2_collection(test_case_id: int, case_collection_id: int):
    """
    Add a test case to a test case collection

    Args:
        test_case_id (int): the id of the test case
        case_collection_id (int): the id of the test case collection
    """

    ADD_CASE_2_COLLECTION = """
        INSERT INTO case_collection_test_cases (tcc_id, case_id) 
        VALUES (?, ?)
        """

    with sqlite.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute(ADD_CASE_2_COLLECTION, (case_collection_id, test_case_id))
        con.commit()
