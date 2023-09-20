#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A module that defines the git repository class."""

import configparser
import os

from .repo_paths import git_file_path


class GitRepo:
    """A class that defines a git repository.
    A git repository is a directory that contains a .git directory.
    """
    # local work directory of the version control files:
    workdir = None
    # where to save the .git dir:
    dotgit = None
    # the config file:
    config = None

    def __init__(self, path, create=False):
        """Initialize a git repository.
        Args:
            path: the path to the git repository.
            create: if True, create the git repository.
        Raises:
            FileNotFoundError: if the path is not a git repository.
            ValueError: if the repository format version is not supported.
        """
        self.workdir = path
        self.dotgit = os.path.join(path, ".git")
        # making sure the path exists:
        if not (create or os.path.isdir(self.dotgit)):
            raise FileNotFoundError(
                f"fatal: {self.dotgit} is not a git repository")

        # reading the config file in the .git directory:
        self.config = configparser.ConfigParser()
        configfile = git_file_path(self, "config")

        if configfile and os.path.exists(configfile):
            self.config.read([configfile])
        elif not create:
            raise FileNotFoundError("fatal: config file missing")

        # making sure the version of the repository is supported by the
        # current version Git:
        # repositoryformatversion = 0 ==> original/compatible format
        if not create:
            version = int(self.config.get("core", "repositoryformatversion"))
            if version != 0:
                raise ValueError(
                    f"fatal: unsupported repositoryformatversion {version}")
