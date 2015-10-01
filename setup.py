#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="pytest-session_to_file",
    version='0.1.1',
    author='Richard Vézina',
    author_email='ml.richard.vezina@gmail.com',
    license='LGPLv3 (http://www.gnu.org/licenses/lgpl.html)',
    packages=[],
    description='pytest-session_to_file is a py.test plugin for capturing and saving to file the stdout of py.test.',
    long_description=read('README.md'),
    url="https://pypi.python.org/pypi/pytest-session_to_file",
    # the following makes a plugin available to py.test
    entry_points={'pytest11': ['pytest-session_to_file = pytest_session_to_file']},
    keywords='py.test pytest plugin plugins',
    install_requires=['pytest'],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
    ],
)
