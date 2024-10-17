"""
This package contains the modules for the automation insertion windows for the frontend.
"""

from .automation_insertion import AutomationCreationFrame
from .automation_entities import AutomationEntityFrame
from .antomation_script import AutomationScriptFrame
from .automation_infos import AutomationInfosFrame
# from .entity_integration import EntityIntegrationFrame

__all__ = [
    "AutomationCreationFrame",
    "AutomationEntityFrame",
    "AutomationScriptFrame",
    "AutomationInfosFrame",
]
