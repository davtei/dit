#!/usr/bin/env python3

from src.objects.tree_leaf_class import GitTreeLeaf

def tree_parse_one(raw, start=0):
    """Parse a git tree object."""
    # Find the next space and newline characters:
    end = raw.find(b"\x00", start)
    # If the next space or newline characters are not found,
    # set them to the length of the raw string:
    if end == -1:
        end = len(raw)

    # Extract the mode, path, and sha from the binary string:
    mode, path = raw[start:end].decode().split(" ", 1)
    sha = raw[end + 1:end + 21]

    # Return the tree leaf:
    return GitTreeLeaf(mode, path, sha), end + 21


# def tree_parse(repo, data):
def tree_parse(data):
    """Parse a git tree object."""
    # Create a list to store the tree leaves:
    leaves = []

    # Iterate through the tree leaves:
    for line in data.decode().split("\n"):
        if not line:
            continue
        # Extract the mode, path, and sha from the binary string:
        mode, path, sha = line.split(" ", 2)
        leaves.append(GitTreeLeaf(mode, path, sha))

    # Return the tree leaves:
    return leaves


def sort_tree_leaf(leaf):
    """Sort a git tree leaf."""
    # Sort the tree leaves by path (directories first, then files):
    if leaf.mode.startswith(b"10"):
        # leaves that start with 100 are files:
        return leaf.path
    else:
        # leaves that start with other modes are directories and
        # end with a slash:
        return leaf.path + "/"


def tree_serialize(obj):
    """Serialize a git tree object."""
    # Create a list to store the tree leaves:
    leaves = []

    # Iterate through the tree leaves:
    for entry in obj.leaves:
        leaves.append(f"{entry.mode} {entry.path}\x00{entry.sha}")

    # Join the tree leaves with a newline character:
    return b"\n".join(leaves)
