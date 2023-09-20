#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A module that defines the git blob object class."""

from src.objects.gitobject_class import GitObject


class BlobObject(GitObject):
    """A class that defines a git blob object, a subclass of the GitObject class.
    Attributes:
        object_format: The format of the git object.
            A git blob object has the format "blob".
        blob_data: The data of the git blob object.
    """
    # blob: binary large object
    object_format = "blob"

    def __init__(self, repo, data=None):
        """Initialize a git blob object with the provided repo and
        data (optional)."""
        GitObject.__init__(self, repo, data)

    # Convert the blob object to a string representation
    def serialize(self):
        """Serialize the git blob object."""
        return self.blob_data

    # Convert the string representation of a blob object to a blob object,
    #  an instance of the BlobObject class
    def deserialize(self, data):
        """Deserialize the git blob object."""
        self.blob_data = data
