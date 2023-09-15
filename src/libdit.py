#!/usr/bin/env python3

import argparse
import collections
import configparser
import hashlib
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
init_arg = subparsers.add_parser(
    "init",
    help="Initialize a new, empty repository.")

# Add an argument to the init subparser
init_arg.add_argument(
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
        case "cat-file":    dit_cat_file(args)
        # case "commit":    dit_commit(args)
        case "hash-object": dit_hash_object(args)
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
            case "blob": return BlobObject(repo, raw_data[extract2:])
            # case "commit": return CommitObject(repo, raw_data[extract2:])
            # case "tag": return TagObject(repo, raw_data[extract2:])
            # case "tree": return TreeObject(repo, raw_data[extract2:])
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
        with open(git_file_path(repo, "refs", "tags", name), encoding="utf-8") as f:
            return f.read().strip()

    # making sure the name is not a branch:
    if git_file_path(repo, "refs", "heads", name):
        with open(git_file_path(repo, "refs", "heads", name), encoding="utf-8") as f:
            return f.read().strip()

    # making sure the name is not a remote branch:
    if git_file_path(repo, "refs", "remotes", name):
        with open(git_file_path(repo, "refs", "remotes", name), encoding="utf-8") as f:
            return f.read().strip()

    # making sure the name is not a note:
    if git_file_path(repo, "refs", "notes", name):
        with open(git_file_path(repo, "refs", "notes", name), encoding="utf-8") as f:
            return f.read().strip()

    # making sure the name is not a relative ref:
    if "/" in name:
        ref, name = name.split("/", 1)
        with open(git_file_path(repo, "refs", ref, name), encoding="utf-8") as f:
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
    # blob: binary large object
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


# TODO: dit cat-file implementation is not complete:
#       must be dit cat-file -t <object>
# OR:
#       must be dit cat-file -s <object>
#       https://www.youtube.com/watch?v=ZR1mZyy_Gvk

cat_file_arg = subparsers.add_parser(
    "cat-file",
    help="Provide content or type and size information for repository objects",
    usage="dit cat-file <type> <object>",
    epilog="See 'dit cat-file --help' for more information on a specific command.")

cat_file_arg.add_argument(
    "type",
    choices=["blob", "commit", "tag", "tree"],
    metavar="type",
    help="Specify the type")

cat_file_arg.add_argument(
    "object",
    metavar="object",
    help="The object to display")


def cat_file(repo, obj, format=None):
    """Provide content or type and size information for repository objects."""
    obj = read_object(repo, object)
    sys.stdout.buffer.write(obj.serialize())


def dit_cat_file(args):
    """Provide content or type and size information for repository objects."""
    repo = find_repo_root()
    cat_file(repo, args.object, args.type)


hash_object_arg = subparsers.add_parser(
    "hash-object",
    help="Compute object ID and optionally creates a blob from a file",
    usage="dit hash-object [-w] [-t TYPE] <file>",
    epilog="See 'dit hash-object --help' for more information on a specific command.")

hash_object_arg.add_argument(
    "-w",
    action="store_true",
    dest="write",
    help="Actually write the object into the object database")

hash_object_arg.add_argument(
    "-t",
    metavar="type",
    dest="type",
    default="blob",
    choices=["blob", "commit", "tag", "tree"],
    help="Specify the type of the object being written")

hash_object_arg.add_argument(
    "file",
    metavar="file",
    help="The file to compute the object ID from")


def hash_object(repo, data, object_format, write=True):
    """Compute object ID and optionally creates a blob from a file."""
    # creating the header:
    header = f"{object_format} {len(data)}\x00".encode()

    # creating the object:
    store = header + data

    # creating the sha:
    sha = hashlib.sha1(store).hexdigest()

    # creating the path to the object:
    path = git_file_path(repo, "objects", sha[:2], sha[2:],
                         create_dir=write)

    # writing the object to the git repository:
    if write:
        with open(path, "wb") as f:
            f.write(zlib.compress(store))
    return sha


def dit_hash_object(args):
    """Compute object ID and optionally creates a blob from a file."""
    repo = find_repo_root()
    with open(args.file, "rb") as f:
        data = f.read()
    sha = hash_object(repo, data, args.type, args.write)
    print(sha)


def commit_msg_parse(raw, begin=0, dictn=None):
    """Parse a commit message as a key-value list message with support for multiline values."""
    # Making sure the commit message is not empty:
    if not dictn:
        dictn = collections.OrderedDict()

    # Find the next space and newline characters:
    next_space = raw.find(b' ', begin)
    next_newline = raw.find(b'\n', begin)

    # If the next space or newline characters are not found, set them to the length of the raw string:
    if next_space == -1:
        next_space = len(raw)
    if next_newline == -1:
        next_newline = len(raw)

    # If the next space character is found before the next newline character, then the key-value pair is on the same line:
    if next_space < next_newline:
        key = raw[begin:next_space]
        value_start = next_space + 1
        value_end = next_newline

        # Check if the value continues on the next line (starts with space or tab)
        while value_end < len(raw) and (raw[value_end] == b' ' or raw[value_end] == b'\t'):
            next_newline = raw.find(b'\n', value_end + 1)
            if next_newline == -1:
                next_newline = len(raw)
            value_end = next_newline

    # If the next newline character is found before the next space character, then the key-value pair is on different lines:
        value = raw[value_start:value_end]
        dictn[key] = value

        # Recursively call the function with the next newline as the beginning
        return commit_msg_parse(raw, next_newline + 1, dictn)
    else:
        # If the next space character is not found before the next newline character, then the key-value pair is on different lines:
        return dictn    # Return the key-value list


# TODO: Fix this function to include the commit message:
def commit_msg_serialize(dictn):
    """Serialize a commit message as a key-value list message with support for multiline values."""
    msg = b''
    for key, value in dictn.items():
        # Skip the key-value pair if the key is None:
        # (the key is None when the value is the commit message)
        if key is None:
            continue
        value = dictn[key]
        # Make the value a list if it is not already a list:
        if not isinstance(value, list):
            value = [value]
        # Join the list of values with a newline character:
        for val in value:
            msg += key + b' ' + (val.replace(b'\n', b'\n ')) + b'\n'

    # Append the message with a newline character:
    msg += b'\n' + dictn[None] + b'\n'
    # Check that the length of the message is correct:
    if len(msg) != len(dictn[None]) + 2:
        raise ValueError(f"expected {len(dictn[None]) + 2} bytes, got {len(msg)}")
    return msg


def GitCommit(GitObject):
    """A class that defines a git commit object."""
    object_format = "commit"

    def __init__(self, repo, data=None):
        """Initialize a git commit object."""
        GitObject.__init__(self, repo, data)

    def serialize(self):
        """Serialize the git commit object."""
        # creating the dictionary to store the commit message:
        dictn = collections.OrderedDict()

        # creating the commit message:
        dictn[b"tree"] = self.tree
        dictn[b"parent"] = self.parent
        dictn[b"author"] = self.author
        dictn[b"committer"] = self.committer
        dictn[None] = self.message

        # serializing the commit message:
        return commit_msg_serialize(dictn)

    def deserialize(self, data):
        """Deserialize the git commit object."""
        # deserializing the commit message:
        dictn = commit_msg_parse(data)

        # extracting the commit message:
        self.tree = dictn[b"tree"]
        self.parent = dictn[b"parent"]
        self.author = dictn[b"author"]
        self.committer = dictn[b"committer"]
        self.message = dictn[None]


