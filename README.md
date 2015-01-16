# requirements
Output requirements.txt for your python project by parsing "import.." string in python source code. It shows the modules that must be installed.
Not a fool proof requirements.txt though...

### how to run?
```
  $ wget -q https://raw.githubusercontent.com/hihellobolke/requirements/master/requirements.py

  $ python requirements.py /path/to/my/project/src
  dateutils
  flask
  py2neo
  ...
```

### Help!
```
  $ python requirements.py -h
  usage: requirements.py [-h] [--all] [directory]

  Generates requirements.txt for your python project by parsing "import.."
  string in python source code. It shows the modules that must be installed.
  Note: local modules directories in codebase dirare not shown. By default
  modules in sys.path are not shown

  positional arguments:
    directory   path to directory containing your python project

  optional arguments:
    -h, --help  show this help message and exit
    --all       show all modules even ones that are available
```
