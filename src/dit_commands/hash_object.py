#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A module that defines the hash-object command.
Args:
    file: the file to compute the object ID from.
    type: the type of the object being written.
    write: actually write the object into the object database.
Returns:
    The object ID.
Raises:
    ValueError: if the repository already exists.
    Usage:
        dit hash-object <file>
        dit hash-object [-w] [-t TYPE] <file>
"""
# NOTE: The current implementation of hash-object does not support
# the -w and -t flags.
# NOTE: The current implementation of hash-object:
# dit hash-object <file>

# TODO: Implement the -w and -t flags.


import hashlib
import zlib

from src.parsers import subparsers
from src.repos.find_root import find_repo_root
from src.repos.repo_paths import git_file_path

hash_object_arg = subparsers.add_parser(
    "hash-object",
    help="Compute object ID and optionally creates a blob from a file",
    usage="dit hash-object [-w] [-t TYPE] <file>",
    epilog="See 'dit hash-object --help' for more information on a specific command.")

hash_object_arg.add_argument(
    "-w",
    action="store_true",
    dest="write",
    help="Actually write the object into the object database")

hash_object_arg.add_argument(
    "-t",
    metavar="type",
    dest="type",
    default="blob",
    choices=["blob", "commit", "tag", "tree"],
    help="Specify the type of the object being written")

hash_object_arg.add_argument(
    "file",
    metavar="file",
    help="The file to compute the object ID from")


def hash_object(repo, data, object_format, write=True):
    """Compute object ID and optionally creates a blob from a file."""
    # creating the header:
    header = f"{object_format} {len(data)}\x00".encode()

    # creating the object:
    store = header + data

    # creating the sha:
    sha = hashlib.sha1(store).hexdigest()

    # creating the path to the object:
    path = git_file_path(repo, "objects", sha[:2], sha[2:],
                         create_dir=write)

    # writing the object to the git repository:
    if write:
        with open(path, "wb") as f:
            f.write(zlib.compress(store))
    return sha


def dit_hash_object(args):
    """Compute object ID and optionally creates a blob from a file,
    that is, converts a file into a git object."""
    repo = find_repo_root()
    with open(args.file, "rb") as f:
        data = f.read()
    sha = hash_object(repo, data, args.type, args.write)
    print(sha)
