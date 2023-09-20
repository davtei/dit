#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A module that defines the write_object function."""

import zlib

from src.repos.repo_paths import git_file_path


def write_object(obj, actually_write=True):
    """Writes an object to a git repository.
    It serializes the object, compresses it, and writes it to the repository.
    Args:
        obj: the object to be written.
        actually_write: if True, the object is written to the repository.
    Returns:
        The path to the object.
    """
    # serializing the object:
    data = obj.serialize()

    # creating the path to the object:
    path = git_file_path(obj.repo, "objects", obj.sha[:2], obj.sha[2:],
                         create_dir=actually_write)

    # writing the object to the git repository:
    if actually_write:
        with open(path, "wb") as f:
            f.write(zlib.compress(data))
    return path
