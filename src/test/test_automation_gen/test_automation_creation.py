"""
This test module is used to test the functionality of the create automation
function and its sub functions on complete automations.
"""

from backend.automation_gen import validate_automation_config
 
from backend.automation_gen.automation_script_gen import init_automation_script

from backend.automation_gen.action_dissection import extract_all_actions
from backend.automation_gen.condtion_dissection import extract_all_conditions
from backend.automation_gen.trigger_dissection import extract_all_trigger

from backend.automation_gen.config_dissection import (
    create_automation,
    create_procedure_list,
)

from backend.ha_automation_utils import home_assistant_yaml_loader as yaml_loader
from backend.ha_automation_utils import (
    home_assistant_automation_validation as ha_automation_config,
)

from backend.utils.env_helper_classes import Automation, Entity


from os import listdir, mkdir, path

import asyncio

TEST_SCRIPT_DIR = path.join("src", "test", "test_automation_gen", "test_scripts")


def print_entity_data(entity: Entity):
    """
    This function prints the entity data

    Args:
        entity (Entity): the entity to print out
    """
    # make the parameter role readable (0=start, 1=condition, 2=action-condition, 3=action)
    role = (
        "start"
        if entity.parameter_role == 0
        else "con"
        if entity.parameter_role == 1
        else "action-con"
        if entity.parameter_role == 2
        else "out"
        if entity.parameter_role == 3
        else "unknown"
    )

    indentation = ": \t" if entity.parameter_role == 2 else ": \t\t"

    print(
        role
        + indentation
        + str(entity.parent)
        + ": \t"
        + str(entity.position)
        + ": \t"
        + entity.entity_name
        + " : \t"
        + str(entity.expected_value)
    )


def print_automation_data(automation_data: dict):
    """
    This function prints the automation data

    Args:
        automation_data (dict): the automation data to print out
                    contains entities and infos keys
    """
    # get the automation information in form of a dictionary
    automation_infos: Automation = automation_data["infos"]
    automation_dict = automation_infos.serialize()

    # print the automation information
    for key, value in automation_dict.items():
        print(key + ": \t" + str(value))

    # print the entities
    print("Entities:")
    entity: Entity = None
    for entity in automation_data["entities"]:
        print_entity_data(entity)


def test_script_init(basis_file: str = None) -> str:
    """
    Test the script initialization and return the path of the generated script

    Args:
        basis_file (str): the path to the yaml file

    Returns:
        str: the path of the generated script
    """

    TEST_SCRIPT_DIR = path.join("src", "test", "test_automation_gen", "test_scripts")

    # init the basis file if not given
    if basis_file is None:
        basis_file = path.join(
            "test_data", "yaml_files", "test_yaml", "entity_extraction_test.yaml"
        )

    automation_yaml = yaml_loader.load_yaml_dict(basis_file)
    automation_config = validate_automation_config(automation_yaml)
    if automation_config is not None:
        script_path = init_automation_script(
            automation_config.automation_name, TEST_SCRIPT_DIR
        )
        return script_path


def test_trigger_entities(basis_file: str = None):
    """
    Test the extraction of all trigger entities in entity_extraction_test.yaml

    Args:
        basis_file (str): the path to the yaml file

    """

    # init the basis file if not given
    if basis_file is None:
        basis_file = path.join(
            "test_data", "yaml_files", "test_yaml", "entity_extraction_test.yaml"
        )

    script_file = test_script_init(basis_file)
    automation_yaml = yaml_loader.load_yaml_dict(basis_file)
    automation_config = validate_automation_config(automation_yaml)
    if automation_config is not None:
        print(" --- TRIGGER: " + automation_config.automation_name + " --- ")
        extracted_entities = extract_all_trigger(automation_config, script_file)
        entity: Entity = None
        for entity in extracted_entities:
            print_entity_data(entity)


def test_condition_entities(basis_file: str = None):
    """
    Test the extraction of all condition entities in entity_extraction_test.yaml

    Args:
        basis_file (str): the path to the yaml file
    """

    # init the basis file if not given
    if basis_file is None:
        basis_file = path.join(
            "test_data", "yaml_files", "test_yaml", "entity_extraction_test.yaml"
        )

    script_file = test_script_init(basis_file)
    automation_yaml = yaml_loader.load_yaml_dict(basis_file)
    automation_config = validate_automation_config(automation_yaml)
    if automation_config is not None:
        print(" --- CONDTION: " + automation_config.automation_name + " --- ")
        extracted_entities = extract_all_conditions(automation_config, script_file)
        entity: Entity = None
        for entity in extracted_entities:
            print_entity_data(entity)


def test_action_entities(basis_file: str = None):
    """
    Test the exctraction of all action entities in basis_file

    Args:
        basis_file (str): the path to the yaml file
    """

    # init the basis file if not given
    if basis_file is None:
        basis_file = path.join(
            "test_data", "yaml_files", "test_yaml", "entity_extraction_test.yaml"
        )
    script_file = test_script_init(basis_file)
    automation_yaml = yaml_loader.load_yaml_dict(basis_file)
    automation_config = validate_automation_config(automation_yaml)
    if automation_config is not None:
        print(" --- ACTION: " + automation_config.automation_name + " --- ")
        extracted_entities = extract_all_actions(automation_config, script_file)
        entity: Entity = None
        for entity in extracted_entities:
            print_entity_data(entity)


def test_create_single_automation(basis_file: str = None):
    """
    Test the extraction of all entities in basis_file

    Args:
        basis_file (str, optional): the path to the yaml file.
        Defaults to None and then entity_extraction_test.yaml is used.
    """

    # init the basis file if not given
    if basis_file is None:
        basis_file = path.join(
            "test_data", "yaml_files", "test_yaml", "entity_extraction_test.yaml"
        )

    script_file = script_file = test_script_init(basis_file)
    automation_yaml = yaml_loader.load_yaml_dict(basis_file)
    automation_config = validate_automation_config(automation_yaml)
    if automation_config is not None:
        print(" --- " + automation_config.automation_name + " --- ")
        extracted_entities = create_procedure_list(automation_config, script_file)
        entity: Entity = None
        for entity in extracted_entities:
            print_entity_data(entity)


def test_create_all_example_automation() -> list:
    """
    Test all example automations in the test_data/yaml_files/example_automation/ directory
    and creates their test scripts in the automation_script_path set in the frontend/settings/settings.json file.

    Returns:
        list: list of the automation data from the automations with their extracted entities and information
    """
    automations = []
    yaml_dir = path.join("test_data", "yaml_files", "example_automations")
    for dir in listdir(yaml_dir):
         dir_path = path.join("test_data", "yaml_files", "example_automations")
    for dir in listdir(dir_path):
        automation_dir = path.join(yaml_dir, dir)
        print("--- " + dir + " ---")
        for file in listdir(automation_dir):
            if file.endswith(".yaml"):
                # get the yaml file path
                basis_file = path.join(automation_dir, file)
                # load the yaml file as a dictionary
                automation_yaml = yaml_loader.load_yaml_dict(basis_file)
                # validate the yaml dictionary
                automation_config = asyncio.run(
                    ha_automation_config.async_validate_config_item(automation_yaml)
                )

                print(
                    f"{automation_config.automation_name} - validation status: {automation_config.validation_status}"
                )

                # check if the validation was not successful
                if not (automation_config.validation_status == "ok") and not (
                    automation_config.validation_status == "unknown_template"
                ):
                    print(
                        automation_config.automation_name
                        + " : \t "
                        + automation_config.validation_status
                        + " : \t"
                        + str(automation_config.validation_error)
                        + "\n"
                    )
                else:
                    # print the automation name and the validation status for automations with templates
                    if automation_config.validation_status == "unknown_template":
                        print(
                            "--- Template-Status ---\n"
                            + str(automation_config.validation_error)
                            + "-------------------"
                        )

                    # create the automation and extract the entities
                    extract_information = create_automation(automation_config)
                    automations.append(extract_information)

    print("--- All automations imported ---\n")

    return automations


if __name__ == "__main__":
    # create the test script directory if it does not exist
    if not path.exists(TEST_SCRIPT_DIR):
        mkdir(TEST_SCRIPT_DIR)

    # Automation path for the test (only needed if you want to test a specific automation)
    # basis_file = path.join("test_data", "yaml_files", "test_yaml", "entity_extraction_test.yaml")
    basis_file = None

    test_case = 4

    # 1. Test the script initialization
    if test_case == 1:
        print("Script created at: " + test_script_init(basis_file=basis_file))

        # repeat the test with the same basis file to check if the versioning works
        print("Script created at: " + test_script_init(basis_file=basis_file))

    # 2. Test the entity extraction function for specific parts of the automation
    elif test_case == 2:
        test_trigger_entities(basis_file=basis_file)
        test_condition_entities(basis_file=basis_file)
        test_action_entities(basis_file=basis_file)

    # 3. Test the extraction of all entities and the automation information and create the automation script
    elif test_case == 3:
        test_create_single_automation(basis_file=basis_file)

    # 4. Test the import of all example automations (automation_data plus script creation)
    elif test_case == 4:
        automations = test_create_all_example_automation()
        for automation in automations:
            print_automation_data(automation)
            print("\n")
