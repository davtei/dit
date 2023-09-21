#!/usr/bin/env python3
"""A module that defines the ref_resolver and list_refs functions."""

import collections
import os

from src.repos.repo_paths import git_file_path

# References/refs: are files that store access to commit objects
# Refs are aliases to commit objects
# Refs contain a 48 byte hex string that is the sha of the commit object
# Refs may refer to other references
# Refs are stored in the .git/refs directory

def ref_resolver(repo, ref):
    """Resolve the reference to a commit sha.
    Args:
        repo: path to the git repository
        ref: the reference to resolve
    Returns:
        The commit sha.
    Raises:
        ValueError: if the reference is not found.
"""

    path = git_file_path(repo, ref)

    # making sure the reference exist:
    if not os.path.exists(path):
        raise ValueError(f"{ref} not found")

    # reading the reference without the newline character:
    with open(path, encoding="utf-8") as f:
        data = f.read()[:-1]

    # removing the prefix "ref: " from the reference:
    if data.startswith("ref: "):
        return ref_resolver(repo, data[5:])
    else:
        return data


# list_refs: allows listing the references in the repository
#   as a dictionary of key-value pairs
def list_refs(repo, path=None):
    """List the references in the repository as a dictionary of
    key-value pairs.
    Args:
        repo: path to the git repository
        path: path to the references
    Returns:
        A dictionary of references.
    """
    # creating the dictionary to store the references:
    refs = collections.OrderedDict()

    # creating the path to the references:
    if not path:
        path = git_file_path(repo, "refs")

    # iterating through the references:
    for name in os.listdir(path):
        # creating the path to the reference:
        fullname = os.path.join(path, name)

        # making sure the reference is not a directory:
        if os.path.isdir(fullname):
            refs[name] = list_refs(repo, fullname)
        else:
            # reading the reference without the newline character:
            with open(fullname, encoding="utf-8") as f:
                refs[name] = f.read()[:-1]

    # returning the dictionary of references:
    return refs
