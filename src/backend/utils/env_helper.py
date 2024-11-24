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


def is_float_or_int(value: str) -> int | float | str:
    """
    Check if a string value is a float or an integer and return the value as a float or an integer.

    Args:
        value (str): The value to check.

    Returns:
        int | float | str: The value as an integer or a float or str if the value is not a number. 
    """
    try:
        value = float(value)
        if value.is_integer():
            value = int(value)
        return value
    except ValueError:
        return value