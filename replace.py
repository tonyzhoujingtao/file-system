#!/usr/bin/env python3
import argparse
import logging
import os
import os.path
import re


def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description='Replace old pattern with new pattern in all files in path recursively')
    parser.add_argument("path", help="the path to start recursively")
    parser.add_argument("old_pattern", help="the old pattern to be replaced by")
    parser.add_argument("new_pattern", help="the new pattern to be replaced with")
    args = parser.parse_args()

    f = multi_replace_curry([(args.old_pattern, args.new_pattern)])
    rename_files(args.path, new_name_func=f)


def multi_replace_curry(replacements):
    def multi_replace(name):
        new_name = name
        for old, new in replacements:
            new_name = new_name.replace(old, new)
        return new_name

    return multi_replace


def rename_files(directory, new_name_func):
    for file_name in os.listdir(directory):
        old_file_path = os.path.join(directory, file_name)
        if os.path.isdir(old_file_path):
            rename_files(old_file_path, new_name_func)

        new_file_name = new_name_func(file_name)
        if new_file_name != file_name:
            new_file_path = os.path.join(directory, new_file_name)

            logging.info("Renaming '%s' to '%s'" % (old_file_path, new_file_path))
            os.rename(old_file_path, new_file_path)
        else:
            logging.debug("Ignoring '%s'" % old_file_path)


if __name__ == '__main__':
    main()
