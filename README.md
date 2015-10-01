pytest-session_to_file
======================

pytest-session_to_file is a py.test plugin that save failure or test session information to a file pass that can be
invoked as at command line when launching py.test run. It put in a file exactly what pytest return to stdout.

**Installation**


Install it with pip as follow :

    pip install pytest-pytest_session_to_file


**Usage**


Once the plugin is installed edit your `conftest.py` and insert in the top of the file :

    pytest_plugins = 'pytest_session_to_file'

Then you can launch your test with the new option `--session_to_file=` like this :

    py.test --session_to_file=FILENAME

If you don't want to edit your `conftest.py` you can invoque py.test like this :

    py.test -p pytest_session_to_file --session_to_file=FILENAME

At the end of the test execution you should obtain a text file with the content of stdout of py.test under the filename
provided that look like this :

============== test session starts ====================

...

============== 2 passed in 34.70 seconds ==============


**TODO:** Write test

**Inspire by:** _pytest.pastebin

**Ref:** https://github.com/pytest-dev/pytest/blob/master/_pytest/pastebin.py



**Platforms:** All

**Version:** 0.1.0

**Date:** 30 sept. 2015 11:25

**License:** LGPLv3 (http://www.gnu.org/licenses/lgpl.html)

Copyright (C) 2015 Richard Vézina <ml.richard.vezinar@gmail.com>

