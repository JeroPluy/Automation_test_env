from setuptools import find_packages, setup

setup(
    name='backend',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'Jinja2==3.1.4',
        'MarkupSafe==2.1.5',
        'PyYAML==6.0.1',
        'slugify==0.0.1',
        'voluptuous==0.15.2',
        'voluptuous-serialize==2.6.0',
    ],
) 

setup(
    name='frontend',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'customtkinter==5.2.2',
        'darkdetect==0.8.0',
        'packaging==24.1',
        'pillow==10.3.0',
    ],
) 