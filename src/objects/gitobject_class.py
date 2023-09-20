#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A module that defines the git object class."""


class GitObject:
    """A class that defines a git object.
    A git object is a file that is stored in the .git/objects directory.
    It is a compressed file that contains the data of the object.
    The data is serialized and deserialized by the git object class.
    """
    repo = None

    def __init__(self, repo, data=None):
        """Initialize a git object."""
        self.repo = repo

        if data is not None:
            self.deserialize(data)

    def init(self):
        """Initialize a git object."""
        # pass

    # Convert the git object to a string representation
    def serialize(self):
        """Serialize the git object."""
        raise NotImplementedError()

    # Convert the string representation of a git object to a git object,
    #  an instance of the GitObject class
    def deserialize(self, data):
        """Deserialize the git object."""
        raise NotImplementedError()
