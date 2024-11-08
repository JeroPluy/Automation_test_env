""" 
This module contains the classes Automation and Entity, which are used to represent an automation and an entity, respectively.
"""

from datetime import datetime
from .env_const import SINGLE


class Automation:
    """
    Class to represent an automation.
    
    a_name: str = None
    autom_mode: int = None
    max_instances: int = None
    script: str = None
    project: str = None
    """

    a_name: str = None
    autom_mode: int = None
    max_instances: int = None
    script: str = None
    project: str = None
    created: datetime = None
    error: str = None

    def __init__(
        self,
        automation_name,
        automation_script,
        project=None,
        automation_mode=SINGLE,
        max_instances=10,
        created: datetime = None,
        error: str = None
    ):
        """
        Create an automation from the automation part.

        Args:
            automation_name (str): The name of the automation
            automation_mode (int): The mode of the automation
            max_instances (int): The maximum instances of the automation
            automation_script (str): The script of the automation
            project (str): The project of the automation

        Returns:
            dict: The automation as a dictionary
        """

        self.a_name = automation_name
        self.autom_mode = automation_mode
        self.max_instances = max_instances
        self.script = automation_script
        self.project = project
        self.created = created
        self.error = error

    def serialize(self)->dict:
        """
        Serialize the automation into a dictionary.

        Returns:
            dict: The automation as a dictionary
        """
        return {
            "automation_name": self.a_name,
            "automation_mode": self.autom_mode,
            "max_instances": self.max_instances,
            "script": self.script,
            "project": self.project,
        }

class Entity:
    """
    Class to represent an entity.
    """

    integration: str = None
    entity_name: str | list = None
    parameter_role: int = None
    parent: int = None
    position: int = None
    expected_value: dict = None

    def __init__(
        self,
        param_role,
        position,
        integration,
        entity_name,
        parent=None,
        expected_value=None,
    ):
        """
        Create an entity from the automation part.

        Args:
            integration (str): The integration of the entity
            entity_name (str): The name of the entity
            expected_value (int | str | dict): The possible value of the entity

        Returns:
            dict: The entity as a dictionary
        """

        self.parent = parent
        self.position = position
        self.parameter_role = param_role
        self.integration = integration
        self.entity_name = integration + "." + entity_name
        if expected_value == {} or expected_value is None:
            self.expected_value = None
        else:
            self.expected_value = expected_value.copy()

    def serialize(self)->dict:
        """
        Serialize the entity into a dictionary

        Returns:
            dict: The entity as a dictionary
        """
        return {
            "integration": self.integration,
            "entity_name": self.entity_name,
            "parameter_role": self.parameter_role,
            "parent_position": self.parent,
            "position": self.position,
            "expected_value": self.expected_value,
        }
