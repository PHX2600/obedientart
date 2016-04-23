#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='obediantart',
    version='1.0.0',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'tornado',
        'bcrypt',
        'tornado-mysql',
        'torndb',
        'MySQL-python',
    ],
    classifiers=[
        'Private :: Do Not Upload'
    ],
)
