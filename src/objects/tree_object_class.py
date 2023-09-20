#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A module that defines the git tree object class."""

from src.objects.gitobject_class import GitObject
from src.dit_commands.tree_parsing import tree_serialize, tree_parse


class TreeObject(GitObject):
    """A class that defines a git tree object,
    a subclass of the GitObject class.
    Attributes:
        object_format: The format of the git object.
            A git tree object has the format "tree".
        leaves: The leaves of the git tree object.
            A leaf is a file or a directory.
            A leaf is an instance of the GitTreeLeaf class.
    """
    object_format = "tree"

    def __init__(self, repo, data=None):
        """Initialize a git tree object with the provided repo and
        data (optional).
        """
        GitObject.__init__(self, repo, data)

    # Convert the tree object to a string representation
    def serialize(self):
        """Serialize the git tree object."""
        return tree_serialize(self)

    # Convert the string representation of a tree object to a tree object,
    #  an instance of the TreeObject class
    def deserialize(self, data):
        """Deserialize the git tree object."""
        self.leaves = tree_parse(data)
