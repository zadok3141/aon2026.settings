"""Compatibility shim for zc.buildout develop installs.

All real metadata lives in pyproject.toml (hatchling backend).
This file exists only because zc.buildout requires setup.py.
"""
import re

from pathlib import Path

from setuptools import find_namespace_packages
from setuptools import setup


def get_version():
    init = Path(__file__).parent / "src/aon2026/settings/__init__.py"
    return re.search(r'__version__\s*=\s*["\']([^"\']+)', init.read_text()).group(1)


setup(
    name="aon2026.settings",
    version=get_version(),
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    install_requires=[
        "Products.CMFPlone",
        "plone.api",
        "z3c.jbot",
    ],
)
