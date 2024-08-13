"""
This module contains the tests for the utility functions of the automation script generator.
"""

from os import path, remove

from backend.automation_gen.automation_script_gen.utils import (
    init_automation_script,
    append_script_context_to_script,
    close_script,
    create_locked_message,
)
from backend.utils.env_const import AUTOMATION_SCRIPT, TEMPLATE_PATH

TEST_DIR = path.join("src", "test", "test_automation_gen", "test_scripts")


def remove_test_files():
    """
    Remove the test files.
    """
    test_files = [
        path.join(TEST_DIR, "test_automation_V_1.py"),
        path.join(AUTOMATION_SCRIPT, "test_automation_V_1.py"),
    ]
    for file in test_files:
        if path.exists(file):
            remove(file)


def test_init_automation_script():
    """
    Test the initialization of the automation script.
    """
    
    # get the template content for comparison
    init_template = path.join(TEMPLATE_PATH, "init_template.py")
    with open(init_template, "r") as file:
        compare_content = file.read()
        compare_content = compare_content.replace("    ", "\t")


    # Test case 1: test the initialization of the automation script without a automation name
    try:
        init_automation_script(automation_name=None, dir_path=TEST_DIR)
    except ValueError as e:
        error_message = str(e)
        assert error_message == "The automation name must be provided"
        
    
    # Test case 2: test the initialization of the automation script
    init_automation_script(automation_name="test_automation", dir_path=TEST_DIR)
    with open(path.join(TEST_DIR, "test_automation_V_1.py"), "r") as file:
        script_content = file.read()
        script_content = script_content.replace("    ", "\t")
        assert script_content == compare_content
    
    
    # Test case 3: test the initialization of the automation script in the script directory
    init_automation_script(automation_name="test_automation")
    with open(path.join(AUTOMATION_SCRIPT, "test_automation_V_1.py"), "r") as file:
        script_content = file.read()
        assert script_content == compare_content
        
    remove_test_files()


def test_append_script_context_to_script():
    """
    Test the appending of the script context to the automation script.
    """
    
    # create the test automation script
    init_automation_script(automation_name="test_automation", dir_path=TEST_DIR)
    
    # Test case 1: test the appending of the script context to the automation script
    added_content = "context = {\"test\": 1}"
    append_script_context_to_script(added_content, path.join(TEST_DIR, "test_automation_V_1.py"))
    with open(path.join(TEST_DIR, "test_automation_V_1.py"), "r") as file:
        script_content = file.read()
        last_line = script_content.splitlines()[-1]
        assert last_line == added_content
        

def test_close_script():
    pass

def test_create_locked_message():
    pass


if __name__ == "__main__":
    test_init_automation_script()
    print("All tests passed.")