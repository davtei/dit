#!/usr/bin/env python3

import argparse
import configparser
import os
import sys


# Create a dictionary to store the command-line arguments
parser = argparse.ArgumentParser(
    description="dit - a git implementation in Python",
    prog="dit",
    usage="dit <dit_command> [<args>]",
    epilog="See 'dit <command> --help' for more information on a specific command.")
subparsers = parser.add_subparsers(
    title="dit Commands",
    dest="dit_command",
    required=True)

# Create a subparser for the init command
argsubparser = subparsers.add_parser(
    "init",
    help="Initialize a new, empty repository.")

# Add an argument to the init subparser
argsubparser.add_argument(
    "path",
    metavar="directory",
    nargs="?",
    default=".",
    help="Where to create the repository.")


class GitRepo:
    """A class that defines a git repository."""
    # local work directory of the version control files:
    workdir = None
    # where to save the .git dir:
    dotgit = None
    # the config file:
    config = None

    def __init__(self, path, create=False):
        """Initialize a git repository."""
        self.workdir = path
        self.dotgit = os.path.join(path, ".git")
        # making sure the path exists:
        if not (create or os.path.isdir(self.dotgit)):
            raise FileNotFoundError(
                f"fatal: {self.dotgit} is not a git repository")

        # reading the config file in the .git directory:
        self.config = configparser.ConfigParser()
        configfile = git_file_path(self, "config")

        if configfile and os.path.exists(configfile):
            self.config.read([configfile])
        elif not create:
            raise FileNotFoundError("fatal: config file missing")

        # making sure the version of the repository is supported by the
        # current version Git:
        # repositoryformatversion = 0 ==> original/compatible format
        if not create:
            version = int(self.config.get("core", "repositoryformatversion"))
            if version != 0:
                raise ValueError(
                    f"fatal: unsupported repositoryformatversion {version}")


def git_path_finder(repo, *path):
    """Return the path to a file or directory in the git directory."""
    # Ensure that the path components are all strings:
    path = [str(p) for p in path]
    return os.path.join(repo.dotgit, *path)


def git_file_path(repo, *path, create_dir=False):
    """Return the path to a file or directory in the git directory."""
    if git_path_finder(repo, *path[:1], create_dir):
        return git_path_finder(repo, *path)


def git_file_dir(repo, *path, create_dir=False):
    """Optionally creates the path to a file or directory in the git directory."""
    path = repo.git_file_path(*path)
    # making sure the path exists:
    if os.path.exists(path):
        if os.path.isdir(path):
            return path
    else:
        raise NotADirectoryError(f"fatal: {path} is not a directory")
    if create_dir:
        os.makedirs(path)
        return path
    else:
        return None


def create_repo(path):
    """Create a new git repository at the path provided."""
    repo = GitRepo(path, create=True)

    # making sure the local repo directory is empty:
    if not os.path.exists(repo.workdir):
        os.makedirs(repo.workdir)
    elif not os.path.isdir(repo.workdir):
        raise ValueError(f"{repo.workdir} is not a directory")
    elif os.listdir(repo.workdir):
        raise ValueError(f"{repo.workdir} is not empty")

    # making sure the .git directory is empty:
    if not os.path.exists(repo.dotgit):
        os.makedirs(repo.dotgit)
    elif not os.path.isdir(repo.dotgit):
        raise ValueError(f"{repo.dotgit} is not a directory")
    elif os.listdir(repo.dotgit):
        raise ValueError(f"{repo.dotgit} is not empty")

    # creating the subdirectories:
    for name in ["objects", "refs", "refs/heads", "refs/tags"]:
        os.makedirs(git_file_path(repo, name))

    # creating the description file:
    with open(git_file_path(repo, "description"), "w", encoding="utf-8") as f:
        f.write(
            "Unnamed repository; edit this file 'description' to name the repository.\n")

    # creating the HEAD file:
    with open(git_file_path(repo, "HEAD"), "w", encoding="utf-8") as f:
        f.write("ref: refs/heads/master\n")

    # creating the config file:
    repo.config.add_section("core")
    repo.config.set("core", "\trepositoryformatversion", "0")
    repo.config.set("core", "\tfilemode", "false")
    repo.config.set("core", "\tbare", "false")
    repo.config.set("core", "\tlogallrefupdates", "true")
    repo.config.set("core", "\tignorecase", "true")
    repo.config.set("core", "\tprecomposeunicode", "true")
    with open(git_file_path(repo, "config"), "w", encoding="utf-8") as f:
        repo.config.write(f)

    return repo


def find_repo_root(path=".", required=True):
    """Find the root directory of the git repository from the path provided."""
    path = os.path.realpath(path)

    # making sure the path exists:
    if os.path.isdir(os.path.join(path, ".git")):
        return GitRepo(path)
    elif path == "/":
        if required:
            raise FileNotFoundError(
                "fatal: not a git repository (or any of the parent directories)")
        else:
            return None
    else:
        return find_repo_root(os.path.dirname(path), required)


def main(argv=sys.argv[1:]):
    """Main function."""
    args = parser.parse_args(argv)

    # Call the function that matches the command name
    # TODO: Add more commands
    match args.dit_command:
        case "add": dit_add(args)
        # case "commit":    dit_commit(args)
        case "init":        dit_init(args)
        # case "log":       dit_log(args)
        # case "ls":        dit_ls(args)
        # case "status":    dit_status(args)
        # case "tag":       dit_tag(args)
        # case _:           print(f"#{parser} is not a dit command. See dit --help.")
        case _: print(f"#{subparsers} is not a dit command. See dit --help.")
        # TODO: find a way to print the subcmd in the error message


def dit_init(args):
    """Initialize a new, empty repository."""
    # TODO: Add a check to see if the directory is already a git repo
    create_repo(args.path)


def dit_add(args):
    """Testing dit add."""
    print("TESTING dit add")
    print(args)
