"""
This module is the main module for the test environment application. It is the main module that is run to start the application.
"""

# import the automation insertion windows
from frontend import automation_insertion as aI


if __name__ == "__main__":
    app = aI.AutomationAddition(project="project1")
    app.mainloop()