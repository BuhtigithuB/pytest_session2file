#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pytest Plugin that save failure or test session information to a file pass as a command line argument to pytest.

It put in a file exactly what pytest return to the stdout.

To use it :
Put this file in the root of tests/ edit your conftest and insert in the top of the file :

    pytest_plugins = 'pytest_session2file'

Then you can launch your test with the new option --session2file= like this :

    py.test --session2file=FILENAME
Or :
    py.test -p pytest_session2file --session2file=FILENAME


Inspire by _pytest.pastebin
Ref: https://github.com/pytest-dev/pytest/blob/master/_pytest/pastebin.py

Version : 0.1.9
Date : 2016-03-16 12:35:41
Copyright (C) 2015 Richard Vézina <ml.richard.vezinar @ gmail.com>
License: LGPLv3 (http://www.gnu.org/licenses/lgpl.html)
"""

import pytest
import sys
import tempfile


def pytest_addoption(parser):
    group = parser.getgroup("terminal reporting")
    group._addoption('--session2file', action='store', metavar='path', default=None,
                     help="Save to file the pytest session information")


@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    tr = config.pluginmanager.getplugin('terminalreporter')
    # if no terminal reporter plugin is present, nothing we can do here;
    # this can happen when this function executes in a slave node
    # when using pytest-xdist, for example
    if tr is not None:
        config._pytestsessionfile = tempfile.TemporaryFile('w+')
        oldwrite = tr._tw.write

        def tee_write(s, **kwargs):
            oldwrite(s, **kwargs)
            if (sys.version_info > (3, 0)):
                config._pytestsessionfile.write(s)
            else:
                config._pytestsessionfile.write(s.encode('utf8'))
        tr._tw.write = tee_write


def pytest_unconfigure(config):
    if hasattr(config, '_pytestsessionfile'):
        # get terminal contents and delete file
        config._pytestsessionfile.seek(0)
        sessionlog = config._pytestsessionfile.read()
        config._pytestsessionfile.close()
        del config._pytestsessionfile
        # undo our patching in the terminal reporter
        tr = config.pluginmanager.getplugin('terminalreporter')
        del tr._tw.__dict__['write']
        # write summary
        create_new_file(config=config, contents=sessionlog)


def create_new_file(config, contents):
    """
    Creates a new file with pytest session contents.
    :contents: pytest stdout contents
    """
    path = config.option.session2file
    with open(path, 'w') as f:
        f.writelines(contents)

