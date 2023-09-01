#!/usr/bin/env python3

import argparse
import sys

parser = argparse.ArgumentParser(
    description="dit - a git implementation in Python",
    prog="dit",
    usage="dit <dit_command> [<args>]",
    epilog="See 'dit <command> --help' for more information on a specific command.")
subparsers = parser.add_subparsers(
    title="dit Commands",
    dest="dit_command",
    required=True)


def main(argv=sys.argv[1:]):
    args = parser.parse_args(argv)

    # Call the function that matches the command name
    # TODO: Add more commands
    match args.dit_command:
        case "add":    dit_add(args)
        case "commit": dit_commit(args)
        case "init":   dit_init(args)
        case "log":    dit_log(args)
        case "ls":     dit_ls(args)
        case "status": dit_status(args)
        case "tag":    dit_tag(args)
        case _: print(f"#{parser} is not a dit command. See dit --help.")
        # TODO: find a way to print the subcmd in the error message


def dit_add(args):
        '''Testing subfxn.'''
        print("TESTING dit add")
