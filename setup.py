# pylint: disable=invalid-name,redefined-builtin
"""Setup configuration for the project."""

from setuptools import find_packages, setup

# Define project metadata
name = "dit"
version = "0.1"
description = "An implementation of Git in Python"
author = "David Tei"
author_email = "daveteidt@gmail.com"
url = "https://github.com/davtei/dit"
license = "MIT"

# Specify project dependencies
install_requires = [
    # List your project's dependencies here
    "setuptools==68.2.2",
    "wheel==0.34.2"
]

# Read the README file for the long description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# Create the setup configuration
setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=author,
    author_email=author_email,
    url=url,
    license=license,
    # Automatically discover and include all packages
    packages=find_packages(exclude="tests*"),
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            # command-line scripts
            "dit = src.mainlib:main",
        ],
    },
)
