#!/usr/bin/env python3
import argparse
import logging
import os
import os.path
from shutil import move
from tempfile import mkstemp

from termcolor import colored

from strings import multi_replace_curry


def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(
        description='Replace old pattern with new pattern in all files in path recursively')
    parser.add_argument("path", help="the path to start recursively")
    parser.add_argument("old_pattern", help="the old pattern to be replaced by")
    parser.add_argument("new_pattern", help="the new pattern to be replaced with")
    args = parser.parse_args()

    f = multi_replace_curry([(args.old_pattern, args.new_pattern)])
    replace_files(args.path, new_string_func=f)


def replace_files(directory, new_string_func):
    try:
        for file_name in os.listdir(directory):
            file_path = os.path.join(directory, file_name)
            if os.path.isdir(file_path):
                replace_files(file_path, new_string_func)
            else:
                temp_path = make_temp_file(file_path, new_string_func)
                os.remove(file_path)
                move(temp_path, file_path)
    except FileNotFoundError:
        print("No such directory: %s" % directory)


def make_temp_file(file_path, new_string_func):
    fh, temp_path = mkstemp()

    with open(temp_path, 'w') as new_file:
        with open(file_path) as old_file:
            line_number = 1
            for line in old_file:
                new_line = new_string_func(line)
                new_file.write(new_line)

                if new_line != line:
                    print("%s:%d: %s => %s" % (
                        file_path, line_number, colored(line.lstrip().rstrip(), 'red'),
                        colored(new_line.lstrip().rstrip(), 'blue')))
                line_number += 1

    os.close(fh)
    return temp_path


if __name__ == '__main__':
    main()
