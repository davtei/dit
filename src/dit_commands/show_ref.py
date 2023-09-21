#!/usr/bin/env python3
"""A module that defines the show-ref command."""

import collections

from src.dit_commands.resolve_list_refs import list_refs
from src.parsers import subparsers
from src.repos.find_root import find_repo_root

# dit show-ref: allows showing the references in the repository
# dit show-ref will be implemented as dit show-ref <ref>
# It will instantiate the tree object and write the files to the path provided
show_ref_arg = subparsers.add_parser(
    "show-ref",
    help="List references in a local repository",
    usage="dit show-ref",
    epilog="See 'dit show-ref --help' for more information on a specific "
    "command.")


def show_ref(repo, refs, with_hash=True, prefix=""):
    """List references in a local repository."""
    # iterating through the references:
    for name, ref in refs.items():
        # making sure the reference is not a directory:
        if isinstance(ref, collections.OrderedDict):
            show_ref(repo, ref, with_hash, prefix + name + "/")
        else:
            # printing the reference:
            print(ref, prefix + name)


def dit_show_ref(args):
    """List references in a local repository.
    Usage:
        dit show-ref
        dit show-ref (-h | --help)
    Options:
        -h, --help  Show this screen and exit.
    """
    repo = find_repo_root()
    refs = list_refs(repo)
    show_ref(repo, refs, prefix="refs/")
