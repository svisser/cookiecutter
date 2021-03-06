#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.prompt
---------------------

Functions for prompting the user for project info.
"""

from __future__ import unicode_literals
import sys

PY3 = sys.version > '3'
if PY3:
    iteritems = lambda d: iter(d.items())
    def read_response(prompt=''):
        """
        Prompt the user for a response.

        Prints the given prompt (which should be a Unicode string),
        and returns the text entered by the user as a Unicode string.

        :param prompt: A Unicode string that is presented to the user.
        """
        # The Python 3 input function does exactly what we want
        return input(prompt)
else:
    def read_response(prompt=''):
        """
        Prompt the user for a response.

        Prints the given prompt (which should be a Unicode string),
        and returns the text entered by the user as a Unicode string.

        :param prompt: A Unicode string that is presented to the user.
        """
        # For Python 2, raw_input takes a byte string argument for the prompt.
        # This must be encoded using the encoding used by sys.stdout.
        # The result is a byte string encoding using sys.stdin.encoding.
        # However, if the program is not being run interactively, sys.stdout
        # and sys.stdin may not have encoding attributes.
        # In that case we don't print a prompt (stdin/out isn't interactive,
        # so prompting is pointless), and we assume the returned data is
        # encoded using sys.getdefaultencoding(). This may not be right,
        # but it's likely the best we can do.
        # Isn't Python 2 encoding support wonderful? :-)
        if sys.stdout.encoding:
            prompt = prompt.encode(sys.stdout.encoding)
        else:
            prompt = ''
        enc = sys.stdin.encoding or sys.getdefaultencoding()
        return raw_input(prompt).decode(enc)
    iteritems = lambda d: d.iteritems()


def prompt_for_config(context):
    """
    Prompts the user to enter new config, using context as a source for the
    field names and sample values.
    """
    cookiecutter_dict = {}

    for key, val in iteritems(context['cookiecutter']):
        prompt = "{0} (default is \"{1}\")? ".format(key, val)

        new_val = read_response(prompt).strip()

        if new_val == '':
            new_val = val

        cookiecutter_dict[key] = new_val
    return cookiecutter_dict


def query_yes_no(question, default="yes"):
    """
    Ask a yes/no question via `read_response()` and return their answer.

    :param question: A string that is presented to the user.
    :param default: The presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".

    Adapted from
    http://stackoverflow.com/questions/3041986/python-command-line-yes-no-input
    http://code.activestate.com/recipes/577058/

    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = read_response().lower()

        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")
