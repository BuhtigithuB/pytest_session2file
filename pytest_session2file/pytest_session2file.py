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

Version : 0.1.5
Date : 2015-10-13 23:20:24 
Copyright (C) 2015 Richard Vézina <ml.richard.vezinar @ gmail.com>
License: LGPLv3 (http://www.gnu.org/licenses/lgpl.html)
"""

import pytest
import sys
import tempfile


def pytest_addoption(parser):
    group = parser.getgroup("terminal reporting")
    group._addoption('--session2file', action='store', metavar='path', default='pytest_session.txt',
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
            config._pytestsessionfile.write(str(s))
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
    :contents: paste contents
    :returns: url to the pasted contents
    """
    path = config.option.session2file
    with open(path, 'w') as f:
        f.writelines(contents)


def pytest_terminal_summary(terminalreporter):
    import _pytest.config
    tr = terminalreporter
    if 'failed' in tr.stats:
        for rep in terminalreporter.stats.get('failed'):
            try:
                msg = rep.longrepr.reprtraceback.reprentries[-1].reprfileloc
            except AttributeError:
                msg = tr._getfailureheadline(rep)
            tw = _pytest.config.create_terminal_writer(terminalreporter.config, stringio=True)
            rep.toterminal(tw)
            s = tw.stringio.getvalue()
            assert len(s)
            create_new_file(config=_pytest.config, contents=s)
