from typing import Any, Mapping


class ScriptVariables:
    """Class to hold and render script variables."""

    def __init__(self, variables: dict[str, Any]) -> None:
        """Initialize script variables."""
        self.variables = variables
        self._has_template: bool | None = None

    def as_dict(self) -> dict[str, Any]:
        """Return dict version of this class."""
        return self.variables
    