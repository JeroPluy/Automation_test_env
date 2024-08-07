"""
This module contains helper functions for the environment.
"""


def is_jinja_template(template_str: str) -> bool:
    """
    Check if a string is a Jinja template by looking for Jinja tags. 
    Jinja tags are "{%", "{{", and "{#".

    Args:
        template_str (str): The string to check.

    Returns:
        bool: True if the string is a Jinja template, False otherwise.
    """
    return "{" in template_str and (
        "{%" in template_str or "{{" in template_str or "{#" in template_str
    )
