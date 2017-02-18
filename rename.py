#!/usr/bin/env python3
import argparse
import logging
import os
import os.path
import re


def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="the path to start renaming files recursively")
    parser.add_argument("old_pattern", help="the old pattern to be replaced by")
    parser.add_argument("new_pattern", help="the new pattern to be replaced with")
    args = parser.parse_args()

    # rename_files(args.path, new_name=new_name7)
    f = multi_replace_curry([(args.old_pattern, args.new_pattern)])
    rename_files(args.path, new_name_func=f)


def multi_replace_curry(replacements):
    def multi_replace(name):
        new_name = name
        for old, new in replacements:
            new_name = new_name.replace(old, new)
        return new_name

    return multi_replace


def new_name1(name):
    return multi_replace_curry([(' Volume', ''), (' Suite', '')])(name)


def new_name2(name):
    return multi_replace_curry([(' Volume', '')])(name)


def new_name3(name):
    return multi_replace_curry([('Volume ', 'iMusic ')])(name)


def new_name4(name):
    return multi_replace_curry([('5', 'iMusic 5')])(name)


def new_name5(name):
    pattern = r"Track (\d)\.flac"
    single_digits = re.findall("%s" % pattern, name)
    if single_digits:
        double_digit = '0' + single_digits[0]
        return re.sub(r"%s" % pattern, "Track %s.flac" % double_digit, name)
    return name


def new_name6(name):
    return multi_replace_curry([('\.', '.')])(name)


def new_name7(name):
    return re.sub(r"Track \d+ -", "Track", name)


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
