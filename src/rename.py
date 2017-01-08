#!/usr/bin/env python3
import argparse
import logging
import os
import os.path
import re


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="the path to start renaming files recursively")
    args = parser.parse_args()

    rename_files(args.path, new_name=new_name7)


def new_name1(name):
    return name.replace(' Volume', '').replace(' Suite', '')


def new_name2(name):
    return name.replace(' Volume', '')


def new_name3(name):
    return name.replace('Volume ', 'iMusic ')


def new_name4(name):
    return name.replace('5', 'iMusic 5')


def new_name5(name):
    pattern = r"Track (\d)\.flac"
    single_digits = re.findall("%s" % pattern, name)
    if single_digits:
        double_digit = '0' + single_digits[0]
        return re.sub(r"%s" % pattern, "Track %s.flac" % double_digit, name)
    return name


def new_name6(name):
    return name.replace('\.', '.')


def new_name7(name):
    return re.sub(r"Track \d+ -", "Track", name)


def rename_files(path, new_name):
    for file_name in os.listdir(path):
        old_file_path = path.join(path, file_name)
        if path.isdir(old_file_path):
            rename_files(old_file_path, new_name)

        new_file_name = new_name(file_name)
        if new_file_name != file_name:
            new_file_path = path.join(path, new_file_name)

            logging.info("Renaming '%s' to '%s'" % (old_file_path, new_file_path))
            os.rename(old_file_path, new_file_path)
        else:
            logging.debug("Ignoring '%s'" % old_file_path)


if __name__ == '__main__':
    main()
