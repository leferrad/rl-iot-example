#! /usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
from setuptools import find_packages

setup(
    name="tateti",
    version="0.1.0",
    author="Leandro Ferrado",
    author_email="ljferrado@gmail.com",
    url="https://github.com/leferrad/rl-iot-example",
    packages=find_packages(exclude=['scripts', 'docs', 'test']),
    license="LICENSE",
    description="Reinforcement Learning agent to solve Tic Tac Toe game, deployed on an IoT environment",
    long_description=open("README.md").read(),
    install_requires=open("requirements.txt").read().split()
)