# Automation Test Environment for Home Assistant

## Introduction

This repository contains the application and its individual components of the test environment for Home Assistant automations.

## Structure

The structure of the repository consists of the actuall source code in [`./src`](https://github.com/JeroPluy/Automation_test_env/tree/main/src), additional documentation to the application concept in [`./docs`](https://github.com/JeroPluy/Automation_test_env/tree/main/docs) and the test or example data in [`./test_data`](https://github.com/JeroPluy/Automation_test_env/tree/main/test_data). The source code is separated in different packages for the [frontend](https://github.com/JeroPluy/Automation_test_env/tree/main/src/backend), [backend](https://github.com/JeroPluy/Automation_test_env/tree/main/src/backend) and [tests](https://github.com/JeroPluy/Automation_test_env/tree/main/src/test) and the main application is run in the [`main.py`](https://github.com/JeroPluy/Automation_test_env/blob/main/src/main.py)

To get to know more about each and every part of this repository, corresponding documentations can be used. Every file in this repository is documented right at the beginning (if possible) to make its purpose clear. Every folder is documented with either a `README.md` or an `__init__.py` (for python source code) or both, describing the content of the file/folder.

## Installation

### Requirements

This project uses publicly available third party libraries for Python, called "modules". These modules must be installed in order to provide all needed funccionality, for example from [PyPI](https://pypi.org/) using pip. In addition, the listed packages of the project must be installed so that the main script can access them. How that can be done specifically for this project is described in this part.

Firstly, setup a virtual environment and activate it:

```shell
python -m venv .venv
source .venv/bin/activate
```

The next step contains the installation of the `setup.py`. This file downloads and installs all necessary packages and modules in the virtual environment.

```shell
pip install -e .
```

---

To uninstall all modules, simply uninstall the modules from the requirements.txt file

```shell
pip uninstall -y -r requirements.txt
```

## Usage

The [`main.py`](https://github.com/JeroPluy/Automation_test_env/blob/main/src/main.py) and thus the entire application can be started with the following command.

```shell
python ./src/main.py
```

## Author

This project was implemented by Jerome Albert. The use of code from other sources is documented at the beginning of the relevant program scripts by means of links and call details.

The coding process was supported by following AI-Tools:

- [GitHub-Copilot](https://github.com/features/copilot) 
- and [Phind](https://www.phind.com)
