#!/usr/bin/env python3

import configparser
import os


class GitRepo:
    """A class that defines a git repository."""
    # location of the version control files:
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

    # making sure the directory is empty:
    if not os.path.exists(repo.workdir):
        os.makedirs(repo.workdir)
    elif not os.path.isdir(repo.workdir):
        raise ValueError(f"{repo.workdir} is not a directory")
    elif os.listdir(repo.workdir):
        raise ValueError(f"{repo.workdir} is not empty")

    # making sure the directory is empty:
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
        f.write("Unnamed repository; edit this file 'description' to name the repository.\n")

    # creating the HEAD file:
    with open(git_file_path(repo, "HEAD"), "w", encoding="utf-8") as f:
        f.write("ref: refs/heads/master\n")

    # creating the config file:
    repo.config.add_section("core")
    repo.config.set("core", "repositoryformatversion", "0")
    repo.config.set("core", "filemode", "false")
    repo.config.set("core", "bare", "false")
    repo.config.set("core", "logallrefupdates", "true")
    repo.config.set("core", "ignorecase", "true")
    repo.config.set("core", "precomposeunicode", "true")
    with open(git_file_path(repo, "config"), "w", encoding="utf-8") as f:
        repo.config.write(f)

    return repo

def find_repo(path=".", required=True):
    """Find the git repository in the path provided."""
    path = os.path.realpath(path)

    # making sure the path exists:
    if os.path.isdir(os.path.join(path, ".git")):
        return GitRepo(path)
    elif path == "/":
        if required:
            raise FileNotFoundError("fatal: not a git repository (or any of the parent directories)")
        else:
            return None
    else:
        return find_repo(os.path.dirname(path), required)

