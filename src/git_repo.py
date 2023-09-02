#!/usr/bin/env python3

import configparser
import os


class GitRepo(object):
    # location of the version control files:
    workdir = None
    # where to save the .git dir:
    dotgit = None
    config = None

    def __init__(self, path, create=False):
        self.workdir = path
        self.dotgit = path + "/.git"

        if not (create or os.path.isdir(self.dotgit)):
            raise FileNotFoundError(f"fatal: {self.dotgit} is not a git repository")

        # reading the config file in the .git directory:
