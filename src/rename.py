#!/usr/bin/env python3
import os
import os.path
import re
import sys


def main():
    path = '.' if len(sys.argv) <= 1 else sys.argv[1]
    rename_files(path, new_name=new_name7)


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

            print("Renaming '%s' to '%s'" % (old_file_path, new_file_path))
            os.rename(old_file_path, new_file_path)


if __name__ == '__main__':
    main()
