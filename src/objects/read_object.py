#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A module that defines the read_object function."""

import os
import zlib

from src.dit_commands.tree_parsing import tree_parse, tree_serialize
from src.objects.blob_object_class import BlobObject
from src.objects.commit_object_class import CommitObject
from src.objects.gitobject_class import GitObject
# from src.objects.tree_object_class import TreeObject
from src.repos.repo_paths import git_file_path


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
        Args:
            repo (str): The path to the git repository.
            data (str): The serialized git tree object.
        """
        # GitObject.__init__(self, repo, data)
        super().__init__(repo, data)

    # Convert the tree object to a string representation
    def serialize(self):
        """Serialize the git tree object."""
        return tree_serialize(self)

    # Convert the string representation of a tree object to a tree object,
    #  an instance of the TreeObject class
    def deserialize(self, data):
        """Deserialize the git tree object."""
        self.leaves = tree_parse(data)



def read_object(repo, sha):
    """Reads an object from a git repository.
    It reads the object's content from the repository, decompresses it, and
    extracts the format and size information.
    Based on the format, it creates an instance of the corresponding git object
    class, such as BlobObject or TreeObject.
    Args:
        repo: path to the git repository
        sha: SHA hash of the object to be read.
    Returns:
        An instance of the corresponding git object class.
    Raises:
        ValueError: if the object is not found or the size of the object is
            incorrect.
    """

    # creating the path to the object:
    path = git_file_path(repo, "objects", sha[:2], sha[2:])

    # making sure the object exists
    #  (a ValueError is raised to indicate mismatch):
    try:
        assert os.path.exists(path)
    except AssertionError as err:
        raise ValueError(f"{sha} not found") from err

    # if not os.path.exists(path):
    #     raise ValueError(f"{sha} not found")

    # reading the object's content as a zlib compressed binary string:
    with open(path, "rb") as f:
        decompressor = zlib.decompressobj()
        object_format = None
        object_size = None
        raw_data_chunks = []
        object_data = b""

        while True:
            # reading the object's content in chunks:
            chunk = f.read(1024)
            if not chunk:
                break
            raw_data_chunks.append(decompressor.decompress(chunk))

            if object_format is None or object_size is None:
                raw_data = b"".join(raw_data_chunks)

                if object_format is None:
                    # null_index = raw_data.find(b"\x00", 1)
                    null_index = raw_data.find(b" ")
                    # object_format = raw_data[:null_index].decode()
                    object_format = raw_data[:null_index]

                # if object_size is None:
                #     null_index = raw_data.find(b"\x00", null_index + 1)
                #     object_size = raw_data[null_index+1:null_index+21]
                #     expected_size = int(object_size.decode("ascii"))
                #     if expected_size != len(raw_data):
                #         raise ValueError(f"expected {expected_size} bytes, "
                #                          f"got {len(raw_data)}")

            if len(raw_data_chunks) > 1:
                object_data += chunk

        object_classes = {
            b"blob": BlobObject,
            b"commit": CommitObject,
            b"tree": TreeObject,
        }
        object_class = object_classes.get(object_format)
        if object_class is None:
            raise ValueError(f"Unknown object type {object_format}")

        if object_data:
            object_data += decompressor.flush()

        return object_class(repo, object_data)
