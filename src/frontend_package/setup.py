from setuptools import find_packages, setup

setup(
    name='frontend_package',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'customtkinter==5.2.2',
        'darkdetect==0.8.0',
        'packaging==24.1',
        'pillow==10.3.0',
    ],
) 