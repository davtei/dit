#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A module that defines the find_repo_root function."""

import os
from .gitrepo_class import GitRepo


def find_repo_root(path=".", required=True):
    """Find the root directory of the git repository from the path provided.
    Args:
        path: the path to the git repository.
        required: if True, raise an exception if the path is not a
            git repository.
    Returns:
        The root directory of the git repository.
    Raises:
        FileNotFoundError: if the path is not a git repository.
    """
    path = os.path.realpath(path)

    # making sure the path exists:
    if os.path.isdir(os.path.join(path, ".git")): # if the path exists
        return GitRepo(path)                       # return the path
    elif path == "/":
        if required: # if the path is required
            raise FileNotFoundError(
                "fatal: not a git repository (or any of the parent "
                "directories)")
        else:
            return None
    else:
        # recursively call find_repo_root on the parent directory
        return find_repo_root(os.path.dirname(path), required)
