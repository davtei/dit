#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A module that defines the find_object function."""


import os

from src.repos.repo_paths import git_file_path


def find_object(repo, name, format=None, follow=True):
    """Find the object with the given name.
    The name can be a sha, a tag, a relative ref, a short sha, or a sha prefix.
    Args:
        repo: the repository where the object is located.
        name: the name of the object.
        format: the format of the object.
        follow: if True, follow the object until a non-tag object is found.
    Returns:
        The object with the given name.
    Raises:
        ValueError: if the name is empty, a sha, a sha prefix, a tag, a relative
            ref, or a short sha.
    """
    # making sure the name is not empty:
    if not name.strip():
        raise ValueError("invalid empty name")

    # making sure the name is not a sha:
    if len(name) == 40:
        return name

    # making sure the name is not a sha prefix:
    if len(name) >= 4 and all(c in "0123456789abcdef" for c in name):
        return name

    # making sure the name is not a tag:
    if git_file_path(repo, "refs", "tags", name):
        with open(git_file_path(repo, "refs", "tags", name), encoding="utf-8") as f:
            return f.read().strip()

    # making sure the name is not a relative ref:
    if "/" in name:
        ref, name = name.split("/", 1)
        with open(git_file_path(repo, "refs", ref, name), encoding="utf-8") as f:
            return f.read().strip()

    # making sure the name is not a short sha:
    if len(name) >= 4:
        for sha in os.listdir(git_file_path(repo, "objects", name[:2])):
            if sha.startswith(name):
                return sha
