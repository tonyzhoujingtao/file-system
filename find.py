#!/usr/bin/env python3

# find out all the files under a directory with the following criteria:
#
#   1. any of its parent directories must contain an OWNERS file
#   2. the OWNERS file must contain 'alexlevenson' and 'bpence'
#   3. the file must contain 'science/src' or 'science/test'
import argparse
import logging
import os


def has_file(path, file_name):
    return any(fn == file_name for fn in os.listdir(path))


def has_all_targets(file, targets):
    logging.debug("Searching %s for all of %s ...\n" % (file, targets))
    return has_targets(file, targets, all)


def has_any_targets(file, targets):
    logging.debug("Searching %s for any of %s ...\n" % (file, targets))
    return has_targets(file, targets, any)


def has_targets(file, targets, func):
    with open(file, 'r') as f:
        try:
            content = f.read()
            return func([t in content for t in targets])
        except (UnicodeDecodeError, OSError):
            logging.debug("Cannot read %s because it is not in 'utf-8'" % file)
            return False


def search_file(path, target_patterns):
    logging.info(
        "Searching %s for %s in every files ...\n" % (path, target_patterns))

    files = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    filtered_files = [f for f in files if has_any_targets(f, target_patterns)]

    return filtered_files


def search_sub_dirs(path, target_patterns, target_owners, owned_by_parent=False):
    sub_dirs = [os.path.join(path, f) for f in os.listdir(path) if
                os.path.isdir(os.path.join(path, f)) and not f.startswith('.')]
    nested_filtered_files = [search(sub_dir, target_patterns, target_owners, owned_by_parent) for sub_dir in sub_dirs]
    flatten_nested_filtered_files = [item for sublist in nested_filtered_files for item in sublist]
    return flatten_nested_filtered_files


def is_owner(path, target_owners):
    target_file_name = 'OWNERS'
    target_file = os.path.join(path, target_file_name)
    return has_file(path, target_file_name) and has_any_targets(target_file, target_owners)


def search(path, target_patterns, target_owners, owned_by_parent=False):
    logging.debug("Searching %s ...\n" % path)

    if owned_by_parent or is_owner(path, target_owners):
        return search_file(path, target_patterns) + search_sub_dirs(path, target_patterns, target_owners, True)
    else:
        logging.debug('recursively search for the child directories ...\n')
        return search_sub_dirs(path, target_patterns, target_owners, False)


def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="the path to start searching files")
    args = parser.parse_args()

    target_patterns = ['science/src', 'science/test']
    target_owners = ['bpence', 'pankajg', 'pnarang']
    ignore_file_extensions = ['BUILD', '.thrift', '.scala', '.rst', '.md', 'README', '.repl']
    affected_files = [f for f in search(args.path, target_patterns, target_owners) if
                      not any([f.endswith(e) for e in ignore_file_extensions])]

    print("\n".join(affected_files))
    print("%d file(s) owned by %s to check under %s" % (len(affected_files), target_owners, args.path))


if __name__ == '__main__':
    main()
