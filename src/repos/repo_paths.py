#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A module that defines the paths to a git repository."""

import os


# The following function is a general function that returns the path
# to a file or directory in the git directory.
def git_path_finder(repo, *path):
    """Return the path to a file or directory in the git directory.
    Args:
        repo: the git repository.
        path: the path to the file or directory.
    Returns:
        The path to the file or directory in the git directory.
    """
    # Ensure that the path components are all strings:
    path = [str(p) for p in path]
    return os.path.join(repo.dotgit, *path)

# The following two functions are the same as the above function, but
# they are more specific to the file or directory being searched for.
# They also have an optional argument to create the directory if it
# doesn't exist.
def git_file_path(repo, *path, create_dir=False):
    """Return the path to a file or directory in the git directory.
    Args:
        repo: the git repository.
        path: the path to the file or directory.
        create_dir: if True, create the directory if it doesn't exist.
    Returns:
        The path to the file or directory in the git directory.
    """
    if git_path_finder(repo, *path[:1], create_dir): # if the path exists
        return git_path_finder(repo, *path)         # return the path
    return None


def git_file_dir(repo, *path, create_dir=False):
    """Optionally creates the path to a file or directory in the git directory.
    Args:
        repo: the git repository.
        path: the path to the file or directory.
        create_dir: if True, create the directory if it doesn't exist.
    Returns:
        The path to the file or directory in the git directory.
    Raises:
        NotADirectoryError: if the path is not a directory.
    """
    path = repo.git_file_path(*path)
    # making sure the path exists:
    if os.path.exists(path):
        if os.path.isdir(path):
            return path
    else:
        raise NotADirectoryError(f"fatal: {path} is not a directory")
    if create_dir:
        os.makedirs(path)
        return path
    return None
