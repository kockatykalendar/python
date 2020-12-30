import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return fd.read()


setup(
    name="kockatykalendar",
    version="0.1.0",
    url="https://github.com/kockatykalendar/python",
    license='MIT',

    author="Adam Zahradník",
    author_email="adam@zahradnik.xyz",

    description="API, tools and utilities for working with KockatyKalendar.sk",
    long_description=read("README.md"),

    packages=find_packages(exclude=('tests',)),

    install_requires=[],
    extras_requires={
        "django": ["django>=1.7"],
        "api": ["requests>=2.0.0"]
    },

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
