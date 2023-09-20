#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A module that defines the argument parser for dit."""

import argparse

# Create a dictionary to store the command-line arguments
parser = argparse.ArgumentParser(
    description="dit - a git implementation in Python",
    prog="dit",
    usage="dit <dit_command> [<args>]",
    epilog="See 'dit <command> --help' for more information on a specific "
    "command.")

# Create a subparser for the dit commands
subparsers = parser.add_subparsers(
    title="dit Commands",
    dest="dit_command",
    required=True)
