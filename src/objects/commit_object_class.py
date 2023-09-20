#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A module that defines the git commit object class."""

import collections

from src.objects.gitobject_class import GitObject
from src.dit_commands.commit_msg import commit_msg_parse, commit_msg_serialize

class CommitObject(GitObject):
    """Defines a git commit object, a subclass of the GitObject class.
    Attributes:
        object_format: The format of the git object.
            A git commit object has the format "commit".
    """
    object_format = "commit"

    def __init__(self, repo, data=None):
        """Initialize a git commit object."""
        GitObject.__init__(self, repo, data)

    def serialize(self):
        """Serialize the git commit object."""
        # creating the dictionary to store the commit message:
        dictn = collections.OrderedDict()

        # creating the commit message:
        dictn[b"tree"] = self.tree
        dictn[b"parent"] = self.parent
        dictn[b"author"] = self.author
        dictn[b"committer"] = self.committer
        dictn[None] = self.message

        # serializing the commit message:
        return commit_msg_serialize(dictn)

    def deserialize(self, data):
        """Deserialize the git commit object."""
        # deserializing the commit message:
        dictn = commit_msg_parse(data)

        # extracting the commit message:
        self.tree = dictn[b"tree"]
        self.parent = dictn[b"parent"]
        self.author = dictn[b"author"]
        self.committer = dictn[b"committer"]
        self.message = dictn[None]
