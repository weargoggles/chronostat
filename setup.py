#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import sys

from setuptools import setup


name = 'chronostat'
package = 'chronostat'
description = 'Context manager and decorator for timing to Stathat'
url = 'http://github.com/weargoggles/chronostat'
author = 'Pete Wildsmith'
author_email = 'pete@dabapps.com'
license = 'BSD'
install_requires = ['chrono', 'stathat']
tests_require = ['tox', 'responses']


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(package + '.py').read()
    return re.search("^__version__ = ['\"]([^'\"]+)['\"]", init_py,
                     re.MULTILINE).group(1)


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    args = {'version': get_version(package)}
    print "You probably want to also tag the version now:"
    print "  git tag -a %(version)s -m 'version %(version)s'" % args
    print "  git push --tags"
    sys.exit()

setup(
    name=name,
    version=get_version(package),
    url=url,
    license=license,
    description=description,
    author=author,
    author_email=author_email,
    py_modules=['chronostat'],
    package_data=get_package_data(package),
    install_requires=install_requires,
    tests_require=tests_require,
)
