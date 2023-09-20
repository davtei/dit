#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""A module that defines the dit commands."""

from src.dit_commands.cat_file import dit_cat_file
from src.dit_commands.checkout import dit_checkout
from src.dit_commands.hash_object import dit_hash_object
from src.dit_commands.init import dit_init
from src.dit_commands.ls_tree import dit_ls_tree
from src.dit_commands.show_ref import dit_show_ref
from src.dit_commands.symbolic_ref import dit_symbolic_ref
from src.dit_commands.tag import dit_tag
from src.dit_commands.update_ref import dit_update_ref
from src.parsers import parser


def main(arg=None):
    """Main function."""
    if arg is None:
        args = parser.parse_args()
    else:
        args = arg


    # Call the function that matches the command name
    command = args.dit_command

    if command == "cat-file":
        dit_cat_file(args)
    elif command == "checkout":
        dit_checkout(args)
    elif command == "hash-object":
        dit_hash_object(args)
    elif command == "init":
        dit_init(args)
    elif command == "ls-tree":
        dit_ls_tree(args)
    elif command == "show-ref":
        dit_show_ref(args)
    elif command == "symbolic-ref":
        dit_symbolic_ref(args)
    elif command == "tag":
        dit_tag(args)
    elif command == "update-ref":
        dit_update_ref(args)
    else:
        print(f"#{command} is not a dit command. See dit --help.")


if __name__ == "__main__":
    main()
