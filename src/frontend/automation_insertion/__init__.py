"""
This package contains the modules for the automation insertion windows for the frontend.
"""

# main modules of the package
from .automation_insertion import AutomationCreationFrame
from .automation_entities import AutomationEntityFrame
from .antomation_script import AutomationScriptFrame
from .automation_infos import AutomationInfosFrame

# util modules of the package
from . import automation_insertion_utils as ai_utils




__all__ = [
    "AutomationCreationFrame",
    "AutomationEntityFrame",
    "AutomationScriptFrame",
    "AutomationInfosFrame",
    "ai_utils",
]
