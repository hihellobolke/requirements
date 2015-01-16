#!/usr/bin/env python
#
# -- g@ut.am

import os
import re
import pkgutil
import argparse


def parse_import_string(l, debug=False):
    l = l.strip().split('#')[0]
    i = re.match('import\s*([a-zA-Z0-9][a-z0-9A-Z.-]+)\s+as\s+.+$', l) or \
        re.match('import\s*([a-zA-Z0-9][a-z0-9A-Z. ,-]+)$', l) or \
        re.match('from\s+([a-zA-Z0-9][^\s]+)\s+import [a-z0-9A-Z].*', l)
    if i:
        if debug:
            print "\t{}\t => {}".format(l, [_.split('.')[0] for _ in re.split("\s+", i.group(1).strip().replace(",", " "))])
        return [_.split('.')[0] for _ in re.split("\s+", i.group(1).strip().replace(",", " "))]
    return []


def grep_import_string_from_file(f, debug=False):
    lines_with_import = []
    with open(f, 'r') as r:
        for l in r.read().splitlines():
            if "import " in l:
                lines_with_import.append(l)
    return lines_with_import


def list_imports_from_file(f, existing_modules=[], debug=False):
    imports_in_file = []
    for import_string in grep_import_string_from_file(f, debug=debug):
        imports_in_file += parse_import_string(import_string, debug=debug)
    if debug:
        print "{} ->\n\t{}\n\t-\n\t{}".format(f, set(imports_in_file), set(existing_modules))
    return list(set(imports_in_file) - set(existing_modules))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Guess requirements.txt for your python project by parsing ' +
                    '"import.." string in python source code. Shows the modules that ' +
                    'must be installed for your code to run.\n' +
                    'Note: local module directories inside codebase dir' +
                    'are not shown. By default modules in sys.path are also not shown.')
    parser.add_argument('directory', type=str, nargs="?", default=".",
                        help='path to directory containing your python project')
    parser.add_argument('--all', action="store_true", help="show all modules even ones that are available")
    parser.add_argument('--debug', action="store_true", help="debug messages")
    args = parser.parse_args()
    debug = False
    system_module_list = []
    local_module_list = []
    imported_module_list = []

    rootDir = os.path.abspath(args.directory)
    if args.debug:
        debug = args.debug
    if not args.all:
        system_module_list = [m[1] for m in pkgutil.iter_modules()]

    for dirName, subdirList, fileList in os.walk(rootDir, topdown=True):

        # Ignore svn and test dir
        subdirList[:] = [d for d in subdirList
                         if os.path.basename(d)[0] != '.' and
                         not re.search('(test|\.bak)', os.path.basename(d))]
        if os.path.basename(dirName)[0] == '.' or re.search('(test|\.bak)', os.path.basename(dirName)):
            continue

        # add dir containing __init__.py to ignore
        if "__init__.py" in fileList:
            local_module_list.append(os.path.basename(dirName))

        importable_modules = system_module_list + subdirList +\
            [f.replace(".py", "") for f in fileList if re.match('.+\.py', f)]

        for fname in fileList:
            if not re.match('.*\.py', fname):
                continue
            imported_module_list += list_imports_from_file(dirName + '/' + fname,
                                                           existing_modules=importable_modules,
                                                           debug=debug)

    imported_modules = set(imported_module_list) - set(local_module_list)

    for i in imported_modules:
        if system_module_list:
            if not pkgutil.get_loader(i):
                print(i)
        else:
            print(i)
        #
    # end
