#!/usr/bin/env python3
"""A module that defines the ls-tree command."""


from src.objects.read_object import read_object
from src.parsers import subparsers
from src.repos.find_root import find_repo_root

# ls-tree: allows listing the contents of a tree object
ls_tree_arg = subparsers.add_parser(
    "ls-tree",
    help="List the contents of a tree object",
    usage="dit ls-tree <tree-sha>",
    epilog="See 'dit ls-tree --help' for more information on a specific "
    "command.")

ls_tree_arg.add_argument(
    "-r",
    action="store_true",
    dest="recursive",
    help="Recurse into sub-trees")

ls_tree_arg.add_argument(
    "tree",
    metavar="tree",
    help="The tree to list")


def dit_ls_tree(args):
    """List the contents of a tree object.
    Usage:
        dit ls-tree <tree-sha>
        dit ls-tree (-h | --help)"""
    repo = find_repo_root()

# TODO: Error handling if the tree is not found or is not a tree:
    tree = read_object(repo, args.tree)
    # error handling if the tree is not found or is not a tree:
    try:
        if not tree:
            raise ValueError(f"{args.tree} not found")
    except ValueError as err:
        # print(err)
        raise ValueError(f"{args.tree} not found") from err

    if tree.object_format != "tree":
        raise ValueError(f"{args.tree} is not a tree object")
    ls_tree(repo, tree, args.recursive)


def ls_tree(repo, tree, recursive=False, path=""):
    """List the contents of a tree object."""
    stack = [(tree, "")] # (tree, path) tuples in a stack
    # while the stack is not empty
    while stack:
        node, path = stack.pop()    # pop the last element from the stack
        for leaf in node.leaves:    # for each leaf in the tree
            # print the leaf
            print(leaf.mode, leaf.sha, path + leaf.path, sep="\t")
            if leaf.mode.startswith(b"10") and recursive:
                subtree = read_object(repo, leaf.sha)
                if subtree.object_format == "tree":
                    # if the leaf is a tree, add it to the stack
                    stack.append((repo, subtree, path + leaf.path + "/"))
