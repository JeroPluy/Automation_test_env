from environment_package.utils.env_const import SINGLE


class Automation:
    """
    Class to represent an automation.
    """

    a_name: str = None
    autom_mode: int = None
    max_instances: int = None
    script: str = None
    project: str = None

    def __init__(
        self,
        automation_name,
        automation_script,
        project=None,
        automation_mode=SINGLE,
        max_instances=10,
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

    def serialize(self):
        return {
            "integration": self.integration,
            "entity_name": self.entity_name,
            "parameter_role": self.parameter_role,
            "parent_position": self.parent,
            "position": self.position,
            "expected_value": self.expected_value,
        }

def is_jinja_template(template_str: str) -> bool:
    return "{" in template_str and (
        "{%" in template_str or "{{" in template_str or "{#" in template_str
    )