"""
Test the creation of automations in the database
"""

from datetime import datetime, timezone
from backend.database.src import db_create_autom

from backend.utils.env_const import DATABASE

from os import path
import sqlite3 as sqlite

from backend.utils.env_helper_classes import Automation
from backend.automation_gen.automation_creation import load_new_automation_data


def test_create_automation(test_file: str = None):
    """
    Test the creation of an automation in the database

    Args:
        test_file (str): the path to the test file

    """

    # check if the test file is given
    if test_file is None:
        test_file_path = path.join(
            "test_data",
            "yaml_files",
            "example_automations",
            "lock_the_house.yaml",
        )

    # create the automation information
    automation_data: dict = load_new_automation_data(test_file_path)
    automation_info: Automation = automation_data["infos"]

    # create the automation in the database
    try:
        automation_id = db_create_autom.add_automation(automation_data)
    except Exception as e:
        print(e)
        print("Error creating automation, please change the integration name of the entity or add the integration to the database")

    # check if the automation was created
    assert automation_id is not None

    with sqlite.connect(DATABASE) as con:
        cur = con.cursor()
        SELECT_AUTOMATION = "SELECT * FROM automation WHERE a_id = ?"
        cur.execute(SELECT_AUTOMATION, (automation_id,))
        result = cur.fetchone()

        # check if the automation is in the database
        assert result is not None
        assert result[0] == automation_id
        assert result[1] == automation_info.a_name

        # get the current utc time because the created time is in utc timezone
        # but without timezone info so it can be subtracted from the database time
        utc_now = datetime.now(timezone.utc).replace(tzinfo=None)
        time_diff = (
            (utc_now - datetime.strptime(result[2], "%Y-%m-%d %H:%M:%S")).total_seconds()
        )
        # created time should be within 10 seconds of now
        assert 10 > time_diff >= 0

        assert result[3] == automation_info.autom_mode
        assert result[4] == automation_info.max_instances
        assert result[5] == automation_info.script
        # error should be None
        assert result[6] is None

        print(result)


def test_create_integration():
    pass


if __name__ == "__main__":
    # delete_automation()
    test_create_automation()
