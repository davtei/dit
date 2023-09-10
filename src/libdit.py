#!/usr/bin/env python3

import argparse
import configparser
import os
import sys
import zlib


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
        # case "add":         dit_add(args)
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
    try:
        create_repo(args.path)
        print(f"Initialized empty dit repository in {args.path}/.git/")
    except ValueError as err:
        print(err)


class GitObject:
    """A class that defines a git object."""
    repo = None

    def __init__(self, repo, data=None):
        """Initialize a git object."""
        self.repo = repo

        if data is not None:
            self.deserialize(data)

    def init(self):
        """Initialize a git object."""
        # pass

    def serialize(self):
        """Serialize the git object."""
        raise NotImplementedError()

    def deserialize(self, data):
        """Deserialize the git object."""
        raise NotImplementedError()


def read_object(repo, sha):
    """Read an object from the git repository."""
    # creating the path to the object:
    path = git_file_path(repo, "objects", sha[:2], sha[2:])

    # making sure the object exists:
    if not os.path.exists(path):
        raise ValueError(f"{sha} not found")

    # reading the object's content as a zlib compressed binary string:
    with open(path, "rb") as f:
        raw_data = zlib.decompress(f.read())

        # extracting the format of the object from the binary string:
        extract1 = raw_data.find(b"\x00", 1)[1:].decode()
        object_format = raw_data[:extract1]

        # extracting the size of the object from the binary string:
        extract2 = raw_data.find(b"\x00", extract1 + 1)[1:].decode()
        object_size = int(raw_data[extract1:extract2].decode("ascii"))
        # checking that the size of the object is correct:
        if object_size != str(len(raw_data[extract2:])):
            raise ValueError(
                f"expected {object_size} bytes, got {len(raw_data[extract2:])}")

        # Depending on the format of the object, the appropriate class is
        # selected to create an instance of the corresponding Git object
        # as GitBlob, GitCommit, GitTag, or GitTree:
        match object_format:
            case "blob": return GitBlob(repo, raw_data[extract2:])
            case "commit": return GitCommit(repo, raw_data[extract2:])
            case "tag": return GitTag(repo, raw_data[extract2:])
            case "tree": return GitTree(repo, raw_data[extract2:])
            case _: raise ValueError(f"Unknown object type {object_format}")


def find_object(repo, name, format=None, follow=True):
    """Find the object with the given name."""
    # making sure the name is not empty:
    if not name.strip():
        raise ValueError("invalid empty name")

    # making sure the name is not a sha:
    if len(name) == 40:
        return name

    # making sure the name is not a sha prefix:
    if len(name) >= 4 and all(c in "0123456789abcdef" for c in name):
        return name

    # making sure the name is not a tag:
    if git_file_path(repo, "refs", "tags", name):
        with open(git_file_path(repo, "refs", "tags", name)) as f:
            return f.read().strip()

    # making sure the name is not a branch:
    if git_file_path(repo, "refs", "heads", name):
        with open(git_file_path(repo, "refs", "heads", name)) as f:
            return f.read().strip()

    # making sure the name is not a remote branch:
    if git_file_path(repo, "refs", "remotes", name):
        with open(git_file_path(repo, "refs", "remotes", name)) as f:
            return f.read().strip()

    # making sure the name is not a note:
    if git_file_path(repo, "refs", "notes", name):
        with open(git_file_path(repo, "refs", "notes", name)) as f:
            return f.read().strip()

    # making sure the name is not a relative ref:
    if "/" in name:
        ref, name = name.split("/", 1)
        with open(git_file_path(repo, "refs", ref, name)) as f:
            return f.read().strip()

    # making sure the name is not a short sha:
    if len(name) >= 4:
        for sha in os.listdir(git_file_path(repo, "objects", name[:2])):
            if sha.startswith(name):
                return sha

    # making sure the name is not a loose object:
    if len(name) == 38:
        return name

    # making sure the name is not a loose object:
    if len(name) == 2:
        for sha in os.listdir(git_file_path(repo, "objects", name)):
            if sha.startswith(name):
                return sha

    # making sure the name is not a loose object:
    if len(name) == 0:
        for sha1 in os.listdir(git_file_path(repo, "objects")):
            for sha2 in os.listdir(git_file_path(repo, "objects", sha1)):
                if sha2.startswith(name):
                    return sha1 + sha2


def write_object(obj, actually_write=True):
    """Write an object to the git repository."""
    # serializing the object:
    data = obj.serialize()

    # creating the path to the object:
    path = git_file_path(obj.repo, "objects", obj.sha[:2], obj.sha[2:],
                         create_dir=actually_write)

    # writing the object to the git repository:
    if actually_write:
        with open(path, "wb") as f:
            f.write(zlib.compress(data))
    return path


class BlobObject(GitObject):
    """A class that defines a git blob object."""
    object_format = "blob"

    def __init__(self, repo, data=None):
        """Initialize a git blob object."""
        GitObject.__init__(self, repo, data)

    def serialize(self):
        """Serialize the git blob object."""
        return self.blob_data

    def deserialize(self, data):
        """Deserialize the git blob object."""
        self.blob_data = data
