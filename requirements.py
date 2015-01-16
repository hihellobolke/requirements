#!/usr/bin/env python
#
# -- g@ut.am

import os
import re
import pkgutil
import argparse

# verb [filter] noun [filter]
def parse_import_string(l):
    i = re.match('\s*import\s*([a-zA-Z0-9].+)\s+as\s+.+$', l) or \
        re.match('\s*import\s*([a-zA-Z0-9].+)$', l) or \
        re.match('\s*from\s+([a-zA-Z0-9].+)\s+import .+', l)
    if i:
        return [_.split('.')[0] for _ in re.split("\s+", i.group(1).strip().replace(",", " "))]
    return []


def grep_import_string_from_file(f):
    lines_with_import = []
    with open(f, 'r') as r:
        for l in r.read().splitlines():
            if "import " in l:
                lines_with_import.append(l)
    # print('\t{} lines: {}'.format(f, lines_with_import))
    return lines_with_import


def list_imports_from_file(f, existing_modules=[]):
    imports_in_file = []
    for import_string in grep_import_string_from_file(f):
        imports_in_file += parse_import_string(import_string)
    return list(set(imports_in_file) - set(existing_modules))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Guess requirements.txt for your python project by parsing ' +
                                                 '"import.." string in python source code. Shows the modules that ' +
                                                 'must be installed for your code to run.\n' +
                                                 'Note: local module directories inside codebase dir' +
                                                 'are not shown. By default modules in sys.path are also not shown.' +)
    parser.add_argument('directory', type=str, nargs="?", default=".",
                        help='path to directory containing your python project')
    parser.add_argument('--all', action="store_true", help="show all modules even ones that are available")
    args = parser.parse_args()

    rootDir = args.directory
    if args.all:
        system_module_list = []
    else:
        system_module_list = [m[1] for m in pkgutil.iter_modules()]
    local_module_list = []
    imported_module_list = []

    for dirName, subdirList, fileList in os.walk(rootDir):

        # Ignore svn and test dir
        if re.search('(\.svn|test)', dirName):
            continue

        # print('Found directory: {}'.format(dirName))
        # add dir containing __init__.py
        if "__init__.py" in fileList:
            local_module_list.append(os.path.basename(dirName))

        importable_modules = system_module_list + subdirList + [f.replace(".py", "") for f in fileList if re.match('.+\.py', f)]

        for fname in fileList:
            if not re.match('.*\.py', fname):
                continue
            imported_module_list += list_imports_from_file(dirName + '/' + fname, existing_modules=importable_modules)
            # print('\t\t{} -> {}'.format(fname, imported_module_in_file_list))


    imported_modules = set(imported_module_list) - set(local_module_list)

    for i in imported_modules:
        if system_module_list:
            if not pkgutil.get_loader(i):
                print(i)
        else:
            print(i)
