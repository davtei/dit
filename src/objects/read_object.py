#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A module that defines the read_object function."""

import os
import zlib

from src.objects.blob_object_class import BlobObject
from src.objects.commit_object_class import CommitObject
from src.objects.tree_object_class import TreeObject
from src.repos.repo_paths import git_file_path


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
    if not os.path.exists(path):
        raise ValueError(f"{sha} not found")

    # reading the object's content as a zlib compressed binary string:
    with open(path, "rb") as f:
        raw_data = zlib.decompress(f.read())
        # extracting the format of the object from the binary string:
        extract1 = raw_data.index(b"\x00", 1)
        object_format = raw_data[:extract1].decode()
        # extracting the size of the object from the binary string:
        extract2 = raw_data.index(b"\x00", extract1 + 1)
        object_size = int(raw_data[extract1+1:extract2].decode("ascii"))
        # checking that the size of the object is correct:
        if object_size != len(raw_data[extract2+1:]):
            raise ValueError(
                f"expected {object_size} bytes, got {len(raw_data[extract2+1:])}")

        # Depending on the format of the object, the appropriate class is
        # selected to create an instance of the corresponding Git object
        # as BlobObject, CommitObject, TagObject or TreeObject:
        if object_format == "blob":
            return BlobObject(repo, raw_data[extract2+1:])
        elif object_format == "commit":
            return CommitObject(repo, raw_data[extract2+1:])
        # elif object_format == "tag":
        #     return TagObject(repo, raw_data[extract2+1:])
        elif object_format == "tree":
            return TreeObject(repo, raw_data[extract2+1:])
        else:
            raise ValueError(f"Unknown object type {object_format}")
