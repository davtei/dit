#!/usr/bin/env python3
"""A module that defines the update-ref command."""

from src.parsers import subparsers
from src.repos.repo_paths import git_file_path
from src.repos.find_root import find_repo_root


# dit update-ref: allows updating the references in the repository
# dit update-ref will be implemented as dit update-ref <ref> <sha>
# It will instantiate the tree object and write the files to the path provided
update_ref_arg = subparsers.add_parser(
    "update-ref",
    help="Update the object name stored in a ref safely",
    usage="dit update-ref <ref> <sha>",
    epilog="See 'dit update-ref --help' for more information on a "
    "specific command.")

update_ref_arg.add_argument(
    "ref",
    metavar="ref",
    help="The ref to update")

update_ref_arg.add_argument(
    "sha",
    metavar="sha",
    help="The sha to update the ref to")


def update_ref(repo, ref, sha):
    """Update the object name stored in a ref safely.
    Args:
        repo: the repository to update the reference in.
        ref: the reference to update.
        sha: the sha to update the reference to.
    Returns:
        The reference.
    """
    # creating the path to the reference:
    path = git_file_path(repo, ref, create_dir=True)

    # writing the reference to the git repository:
    with open(path, "w", encoding="utf-8") as f:
        f.write(sha + "\n")

    # returning the reference:
    return ref


def dit_update_ref(args):
    """Update the object name stored in a ref safely.
    Usage:
        dit update-ref <ref> <sha>
        dit update-ref (-h | --help)
    Options:
        -h, --help  Show this screen and exit.
    """
    repo = find_repo_root()
    update_ref(repo, args.ref, args.sha)
