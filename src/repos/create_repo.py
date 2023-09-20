#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A module that defines the create_repo function."""

import os

from .gitrepo_class import GitRepo
from .repo_paths import git_file_path


def create_repo(path):
    """Create a new git repository at the path provided.
    Creates the local repo directory, the .git directory, and the
    subdirectories and files in the .git directory, including the
    HEAD file (and set it to point to the master branch), the
    config file (and set the necessary configuration variables),
    the description file, the objects directory, the refs directory,
    the refs/heads directory, and the refs/tags directory.
    Args:
        path: the path to the git repository.
    Returns:
        The git repository.
    Raises:
        ValueError: if the local repo directory is not empty, or if the .git
            directory is not empty.
    """
    repo = GitRepo(path, create=True)

    # making sure the local repo directory is empty:
    if not os.path.exists(repo.workdir):
        os.makedirs(repo.workdir)
    elif not os.path.isdir(repo.workdir):
        raise ValueError(f"{repo.workdir} is not a directory")
    elif os.listdir(repo.workdir):
        raise ValueError(f"{repo.workdir} is not empty")

    # making sure the .git directory is empty:
    if not os.path.exists(repo.dotgit):
        os.makedirs(repo.dotgit)
    elif not os.path.isdir(repo.dotgit):
        raise ValueError(f"{repo.dotgit} is not a directory")
    elif os.listdir(repo.dotgit):
        raise ValueError(f"{repo.dotgit} is not empty")

    # creating the subdirectories:
    for name in ["objects", "refs", "refs/heads", "refs/tags"]:
        os.makedirs(git_file_path(repo, name))

    # creating the description file:
    with open(git_file_path(repo, "description"), "w", encoding="utf-8") as f:
        f.write(
            "Unnamed repository; edit this file 'description' to name the repository.\n")

    # creating the HEAD file:
    with open(git_file_path(repo, "HEAD"), "w", encoding="utf-8") as f:
        f.write("ref: refs/heads/master\n")

    # creating the config file:
    repo.config.add_section("core")
    repo.config.set("core", "\trepositoryformatversion", "0")
    repo.config.set("core", "\tfilemode", "false")
    repo.config.set("core", "\tbare", "false")
    repo.config.set("core", "\tlogallrefupdates", "true")
    repo.config.set("core", "\tignorecase", "true")
    repo.config.set("core", "\tprecomposeunicode", "true")
    with open(git_file_path(repo, "config"), "w", encoding="utf-8") as f:
        repo.config.write(f)

    return repo
