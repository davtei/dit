#!/usr/bin/env python3
"""A module that defines the init command."""

import sys

from src.parsers import subparsers
from src.repos.create_repo import create_repo

# Create a subparser for the init command
init_arg = subparsers.add_parser(
    "init",
    help="Initialize a new, empty repository.")

# Add an argument to the init subparser
init_arg.add_argument(
    "path",
    metavar="path",
    nargs="?",
    default=".",
    help="Where to create the repository.")


def dit_init(args):
    """Initialize a new, empty repository.
    The init command is used to initialize a new, empty repository.
    Args:
        path: the path to the directory where the repository will be created.
    Returns:
        A new, empty repository.
    Raises:
        ValueError: if the repository already exists.
    Usage:
        dit init <path>
        dit init (-h | --help)
    Options:
        -h, --help  Show this screen and exit.
    """
    try:
        create_repo(args.path)
        print(f"Initialized a git repository in {args.path}/.git/")
    except ValueError as err:
        print(err)
        sys.exit(1)
