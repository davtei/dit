#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A module that defines the git tree leaf class."""

class GitTreeLeaf:
    """Represents a leaf node in a git tree structure,
    specifically in the work directory.
    Attributes:
        mode: The mode of the leaf node.
            Files: beginning with 100
            Directories: beginning with 040
        path: The path of the leaf node (file or directory).
        ssh: The sha of the leaf node.
    """

    def __init__(self, mode, path, sha):
        """Initialize a git tree leaf.
        Args:
            mode (str): The mode of the leaf node.
            path (str): The path of the leaf node (file or directory).
            sha (str): The sha of the leaf node.
        """
        # defines the mode of the tree leaf:
        # (files: beginning with 100, directories: beginning with 040)
        self.mode = mode
        self.path = path
        self.sha = sha
