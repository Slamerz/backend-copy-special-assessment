#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Copyspecial Assignment"""

# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import argparse
import os
import re
import shutil
import sys
from zipfile import ZipFile

# This is to help coaches and graders identify student assignments
__author__ = "Jacob Walker"


def create_zip(zip_file_name, files_to_zip):
    """Attempts to create a zip file with the given name, containing the given list of files."""
    try:
        with ZipFile(zip_file_name, 'w') as z:
            for f in files_to_zip:
                z.write(f, os.path.basename(f))
    except IOError as e:
        print("An Error Occurred \n" + str(e))


def move_files(files, dest):
    """Takes a list of files and copies them to a given destination."""
    print("Starting to copy files")
    for f in files:
        shutil.copy(f, dest)
    print("Finished Copying {} files to {}".format(len(files), os.path.abspath(dest)))


def get_special_files(search_directory):
    """returns a list of all files inside of a given directory who's filenames contain double underscores,
    then characters, followed by double underscores.
    example: xyz__hello__.txt """
    files_list = os.listdir(search_directory)
    results = []
    for f in files_list:
        path = os.path.abspath(os.path.join(search_directory, f))
        if os.path.isdir(path):
            results += get_special_files(path)
        if re.search(r"__\w+.*__.*", f):
            results.append(path)
    return results


def create_parser():
    """Create a parser to pull all needed arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--todir', help='dest dir for special files')
    parser.add_argument('--tozip', help='dest zipfile for special files')
    parser.add_argument('from_dir', help='dir to search for special files')
    return parser


def main(args):
    parser = create_parser()
    args = parser.parse_args(args)

    if not args:
        parser.print_usage()
        sys.exit(1)
    special_files_list = get_special_files(args.from_dir)

    if not special_files_list:
        print('No special files found')
        return

    if args.todir:
        move_files(special_files_list, args.todir)
    elif args.tozip:
        create_zip(args.tozip, special_files_list)
    else:
        print(special_files_list)


if __name__ == "__main__":
    main(sys.argv[1:])
