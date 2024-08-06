from setuptools import find_packages, setup

setup(
    name='test_environment_project',
    version='0.0.1',
    description='Contains all the code for the test environment application.',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    namespace_packages=['automation_test_environment'],
    install_requires=[
        'Jinja2==3.1.4',
        'MarkupSafe==2.1.5',
        'PyYAML==6.0.1',
        'slugify==0.0.1',
        'voluptuous==0.15.2',
        'voluptuous-serialize==2.6.0',
        'customtkinter==5.2.2',
        'darkdetect==0.8.0',
        'packaging==24.1',
        'pillow==10.3.0',
    ],
) 