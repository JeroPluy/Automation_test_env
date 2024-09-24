"""
This script provides functions for loading and parsing YAML files from Home Assistant.

It is a partical copy of the original script from Home Assistant.   
    core/homeassistant/util/yaml/loader.py : https://github.com/home-assistant/core/blob/dev/homeassistant/util/yaml/loader.py (VERSION: XX.XX.XXXX)
        (VERSION: 17.05.2024 parent 4edee94 commit 87bb7ce)
"""

import logging
import os
from io import StringIO, TextIOWrapper
from typing import Any, TextIO

import yaml

from .home_assistant_exception import HomeAssistantError, YamlTypeError

try:
    from yaml import CSafeLoader as FastestAvailableSafeLoader

    HAS_C_LOADER = True
except ImportError:
    HAS_C_LOADER = False
    from yaml import SafeLoader as FastestAvailableSafeLoader

JSON_TYPE = list | dict | str

_LOGGER = logging.getLogger(__name__)



class FastSafeLoader(FastestAvailableSafeLoader):
    """The fastest available safe loader, either C or Python."""

    def __init__(self, stream: Any) -> None:
        """Initialize a safe line loader."""
        self.stream = stream

        # Set name in same way as the Python loader does in yaml.reader.__init__
        if isinstance(stream, str):
            self.name = "<unicode string>"
        elif isinstance(stream, bytes):
            self.name = "<byte string>"
        else:
            self.name = getattr(stream, "name", "<file>")

        super().__init__(stream)


class PythonSafeLoader(yaml.SafeLoader):
    """Python safe loader."""

    def __init__(self, stream: Any) -> None:
        """Initialize a safe line loader."""
        super().__init__(stream)


type LoaderType = FastSafeLoader | PythonSafeLoader


def save_automation(automation_txt: list) -> str:
    """
    Save the automation to a file to enable the validation and disssection of the automation
    
    Args:
        automation_txt (list): the automation text as a list of strings
        
    Returns:
        str: the path to the file
    """
    
    yaml_file_path = os.path.join("data", "automation.yaml")
    
    with open (yaml_file_path, "w") as file:
        for line in automation_txt:
            file.write(line)
            
    return yaml_file_path


def load_yaml_dict(fname: str | os.PathLike[str]) -> dict:
    """Load a YAML file and ensure the top level is a dict.

    Raise if the top level is not a dict.
    Return an empty dict if the file is empty.
    """
    loaded_yaml = load_yaml(fname)
    if loaded_yaml is None:
        loaded_yaml = {}
    if not isinstance(loaded_yaml, dict):
        raise YamlTypeError(f"YAML file {fname} does not contain a dict")
    return loaded_yaml


def load_yaml(fname: str | os.PathLike[str]) -> JSON_TYPE | None:
    """Load a YAML file."""
    try:
        with open(fname, encoding="utf-8") as conf_file:
            return parse_yaml(conf_file)
    except UnicodeDecodeError as exc:
        _LOGGER.error("Unable to read file %s: %s", fname, exc)
        raise HomeAssistantError(exc) from exc


def parse_yaml(content: str | TextIO | StringIO) -> JSON_TYPE:
    """Parse YAML with the fastest available loader."""
    if not HAS_C_LOADER:
        return _parse_yaml_python(content)
    try:
        return _parse_yaml(FastSafeLoader, content)
    except HomeAssistantError:
        # Loading failed, so we now load with the Python loader which has more
        # readable exceptions
        if isinstance(content, (StringIO, TextIO, TextIOWrapper)):
            # Rewind the stream so we can try again
            content.seek(0, 0)
        try:
            return _parse_yaml_python(content)
        except HomeAssistantError:
            return {}


def _parse_yaml_python(content: str | TextIO | StringIO) -> JSON_TYPE:
    """Parse YAML with the python loader (this is very slow)."""
    try:
        return _parse_yaml(PythonSafeLoader, content)
    except Exception as exc:
        _LOGGER.error(str(exc))
        raise HomeAssistantError(exc) from exc


def _parse_yaml(
    loader: type[FastSafeLoader | PythonSafeLoader],
    content: str | TextIO,
) -> JSON_TYPE:
    """Load a YAML file."""
    try:
        return yaml.load(content, Loader=loader)  # type: ignore[arg-type]
    except Exception as exc:
        raise HomeAssistantError(exc) from exc