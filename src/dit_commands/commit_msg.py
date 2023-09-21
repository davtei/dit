#!/usr/bin/env python3
"""A module that defines a git commit message."""

import collections


def commit_msg_parse(raw, begin=0, dictn=None):
    """Parse a commit message as a key-value list message with support for
    multiline values.
    """
    # Making sure the commit message is not empty:
    if not dictn:
        dictn = collections.OrderedDict()

    # Find the next space and newline characters:
    next_space = raw.find(b' ', begin)
    next_newline = raw.find(b'\n', begin)

    # If the next space or newline characters are not found, set them to the
    # length of the raw string:
    if next_space == -1:
        next_space = len(raw)
    if next_newline == -1:
        next_newline = len(raw)

    # If the next space character is found before the next newline character,
    # then the key-value pair is on the same line:
    if next_space < next_newline:
        key = raw[begin:next_space]
        value_start = next_space + 1
        value_end = next_newline

        # Check if the value continues on the next line
        #  (starts with space or tab):
        while value_end < len(raw) and (
            raw[value_end] == b' ' or
            raw[value_end] == b'\t'
            ):
            next_newline = raw.find(b'\n', value_end + 1)
            if next_newline == -1:
                next_newline = len(raw)
            value_end = next_newline

    # If the next newline character is found before the next space character,
    #  then the key-value pair is on different lines:
        value = raw[value_start:value_end]
        dictn[key] = value

        # Recursively call the function with the next newline as the beginning
        return commit_msg_parse(raw, next_newline + 1, dictn)
    else:
        # If the next space character is not found before the next newline
        #  character, then the key-value pair is on different lines:
        return dictn    # Return the key-value list


# TODO: Fix this function to include the commit message:
def commit_msg_serialize(dictn):
    """Serialize a commit message as a key-value list message with support for
    multiline values.
    """
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
        raise ValueError(
            f"expected {len(dictn[None]) + 2} bytes, got {len(msg)}")
    return msg
