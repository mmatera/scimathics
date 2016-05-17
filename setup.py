#!/usr/bin/env python
"""Setuptools based setup script for Mathics.
For the easiest installation just type the following command (you'll probably
need root privileges):
    python setup.py install
This will install the library in the default location. For instructions on
how to customize the install procedure read the output of:
    python setup.py --help install
In addition, there are some other commands:
    python setup.py clean -> will clean all trash (*.pyc and stuff)
To get a full list of avaiable commands, read the output of:
    python setup.py --help-commands
Or, if all else fails, feel free to write to the sympy list at
mathics-users@googlegroups.com and ask for help.
"""

import sys
from setuptools import setup, Command, Extension






# Ensure user has the correct Python version
if sys.version_info[:2] != (2, 7):
    print("Mathics supports Python 2.7. \
Python %d.%d detected" % sys.version_info[:2])
    sys.exit(-1)

# stores __version__ in the current namespace
execfile('mathics/version.py')

if sys.subversion[0] == 'PyPy':
    is_PyPy = True
else:
    is_PyPy = False

try:
    if is_PyPy:
        raise ImportError
    from Cython.Distutils import build_ext
except ImportError:
    EXTENSIONS = []
    CMDCLASS = {}
    INSTALL_REQUIRES = []
else:
    EXTENSIONS = {
        'core': ['expression', 'numbers', 'rules', 'pattern'],
        'builtin': ['arithmetic', 'numeric', 'patterns', 'graphics']
    }
    EXTENSIONS = [
        Extension('mathics.%s.%s' % (parent, module),
                  ['mathics/%s/%s.py' % (parent, module)])
        for parent, modules in EXTENSIONS.iteritems() for module in modules]
    CMDCLASS = {'build_ext': build_ext}
    INSTALL_REQUIRES = ['cython>=0.15.1']

# General Requirements
INSTALL_REQUIRES += ['sympy==0.7.6', 'scipy>=0.14' 'ply>=3.8',
                     'mpmath>=0.19', 'python-dateutil', 'colorama',
                     'interruptingcow']

# if sys.platform == "darwin":
#    INSTALL_REQUIRES += ['readline']


def subdirs(root, file='*.*', depth=10):
    for k in range(depth):
        yield root + '*/' * k + file


class initialize(Command):
    """
    Manually creates the database used by Django
    """

    description = "manually create the database used by django"
    user_options = []  # distutils complains if this is not here.

    def __init__(self, *args):
        self.args = args[0]  # so we can pass it to other classes
        Command.__init__(self, *args)

    def initialize_options(self):  # distutils wants this
        pass

    def finalize_options(self):    # this too
        pass

    def run(self):
        print "run"
        


class test(Command):
    """
    Runs the unittests
    """

    description = "runs the unittests"
    user_options = []

    def __init__(self, *args):
        self.args = args[0]  # so we can pass it to other classes
        Command.__init__(self, *args)

    def initialize_options(self):  # distutils wants this
        pass

    def finalize_options(self):    # this too
        pass

    def run(self):
        print "test"

CMDCLASS['initialize'] = initialize
CMDCLASS['test'] = test
setup(
    name="Mathics",
    cmdclass=CMDCLASS,
    ext_modules=EXTENSIONS,
    version=__version__,

    packages=[
        'scimathics',
    ],

    install_requires=INSTALL_REQUIRES,

    package_data={},

    entry_points={
        'console_scripts': [
            'mathics = mathics.main:main',
            'mathicsserver = mathics.server:main',
        ],
    },

    # don't pack Mathics in egg because of sqlite database, media files, etc.
    zip_safe=False,

    # metadata for upload to PyPI
    author="Mauricio Matera",
    author_email="mauricio.matera@gmail.com",
    description="Support of numerical linear algebra routines for mathics.",
    license="GPL",
    keywords="computer algebra system mathics mathematica scipy linear algebra",
    url="http://www.mathics.org/",   # project home page, if any

    # TODO: could also include long_description, download_url, classifiers,
    # etc.
)
