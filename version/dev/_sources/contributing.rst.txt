.. _ref_contributing:

Contribute
==========

Overall guidance on contributing to a PyAnsys library appears in
`Contributing <https://dev.docs.pyansys.com/how-to/contributing.html>`_
in the *PyAnsys Developer's Guide*. Ensure that you are thoroughly familiar
with this guide before attempting to contribute to PyMechanical.

The following contribution information is specific to PyMechanical.

Clone the repository and install project dependencies
-----------------------------------------------------

To clone and install the latest PyMechanical release in development mode, run
these commands:

Clone the repository and create a virtual environment:

.. code::

  # Clone the repository
  git clone https://github.com/ansys/pymechanical
  cd pymechanical

  # Create a virtual environment
  python -m venv .venv

Activate the virtual environment:

.. tab-set::

    .. tab-item:: Windows

       .. code::

          .venv\Scripts\activate.bat

    .. tab-item:: PowerShell

       .. code::

          .venv\Scripts\Activate.ps1

    .. tab-item:: Linux/UNIX

       .. code::

          source .venv/bin/activate

Install tools and dependencies:

.. code::

  # Install build system tools
  python -m pip install --upgrade pip tox flit twine

  # Install the project, documentation, and test dependencies in editable mode
  python -m pip install -e .[doc,tests]


Test PyMechanical
-----------------

PyMechanical uses `PyTest`_ and `tox`_ for unit testing. Prior to running the tests,
ensure Mechanical is installed on your system with a valid license and the test
dependencies are installed. Run this command to install the test dependencies::

  pip install -e .[tests]

Using ``pytest``
^^^^^^^^^^^^^^^^

To run the tests, navigate to the root directory of the repository and run this command::

    pytest

The ``pytest`` command runs all of the tests in the ``tests`` folder. After ``pytest`` is
done running, it shows the test coverage of each of the files in the repository. To run
specific tests, run these commands::

    # Run tests for embedded instances
    pytest -m embedding

    # Run tests for embedded instances that use subprocess
    pytest -m embedding_scripts

    # Run tests that launch Mechanical and work with the gRPC server inside of it
    pytest -m remote_session_launch

    # Run tests that connect to Mechanical and work with the gRPC server inside of it
    pytest -m remote_session_connect

See the ``pyproject.toml`` file for a full list of markers (-m) and their descriptions.

To run specific tests based on a keyword, use the ``-k`` argument::

    # Run all tests containing the word ``appdata``
    # This would run ``test_private_appdata`` and ``test_normal_appdata`` only
    pytest -k appdata

Using ``tox``
^^^^^^^^^^^^^

This project takes advantage of `tox`_. This tool automates common development
tasks (similar to ``Makefile``), but it is oriented towards Python development.

While ``Makefile`` has rules, ``tox`` has environments. In fact, ``tox``
creates its own virtual environment so that anything being tested is isolated
from the project to guarantee the project's integrity.

The following environment commands are provided:

- ``tox -e style``: Checks for coding style quality.
- ``tox -e py``: Checks for unit tests.
- ``tox -e py-coverage``: Checks for unit testing and code coverage.
- ``tox -e doc``: Checks for documentation-building process.

Remote testing
^^^^^^^^^^^^^^
If you do not have a licensed copy of Mechanical installed locally but want to
run PyMechanical unit tests on a remote instance, you must set up environment
variables.

**On Linux**

.. code::

    export PYMECHANICAL_START_INSTANCE=False
    export PYMECHANICAL_PORT=<MECHANICAL Port> (default 10000)
    export PYMECHANICAL_IP=<MECHANICAL IP> (default 127.0.0.1)

**On Windows**

.. code::

    SET PYMECHANICAL_START_INSTANCE=False
    SET PYMECHANICAL_PORT=<MECHANICAL Port> (default 10000)
    SET PYMECHANICAL_IP=<MECHANICAL IP> (default 127.0.0.1)

The environment variables for your operating system tell PyMechanical
to attempt to connect to the existing Mechanical service by default
when you use the :func:`launch_mechanical() <ansys.mechanical.core.launch_mechanical>`
method.

Adhere to coding style
----------------------

As indicated in `Coding style <https://dev.docs.pyansys.com/coding-style/index.html>`_
in the *PyAnsys Developer's Guide*, PyMechanical follows PEP8 guidelines. PyMechanical
implements `pre-commit <https://pre-commit.com/>`_ for style checking.

To ensure your code meets minimum code styling standards, run these commands::

  pip install pre-commit
  pre-commit run --all-files

You can also install this as a pre-commit hook by running this command::

  pre-commit install

This way, it's not possible for you to push code that fails the style checks::

  $ pre-commit install
  $ git commit -am "added my cool feature"
  check pre-commit.ci config...............................................Passed
  black....................................................................Passed
  blacken-docs.............................................................Passed
  isort....................................................................Passed
  flake8...................................................................Passed
  codespell................................................................Passed
  Add License Headers......................................................Passed
  Ansys Technical Review...................................................Passed
  pydocstyle...............................................................Passed
  check for merge conflicts................................................Passed
  debug statements (python)................................................Passed
  check yaml...............................................................Passed
  trim trailing whitespace.................................................Passed
  check for added large files..............................................Passed
  Validate GitHub Workflows................................................Passed

Documentation
-------------

For building documentation, you can run the usual rules provided in the
`Sphinx`_ ``make`` file:

.. code:: bash

    #  build and view the doc from the POSIX system
    make -C doc html && your_browser_name doc/html/index.html

    # build and view the doc from a Windows environment
    make -C doc clean
    make -C doc html
    start .\doc\_build\html\index.html

However, the recommended way of checking documentation integrity is to use
``tox``:

.. code:: bash

    tox -e doc && your_browser_name .tox/doc_out/index.html

View documentation
------------------

Documentation for the latest stable release of PyMechanical is hosted at
`PyMechanical Documentation <https://mechanical.docs.pyansys.com>`_.

In the upper right corner of the documentation's title bar, there is an option
for switching from viewing the documentation for the latest stable release
to viewing the documentation for the development version or previously
released versions.

Post issues
-----------

Use the `PyMechanical Issues <https://github.com/ansys/pymechanical/issues>`_
page to submit questions, report bugs, and request new features. When possible,
use these templates:

* `File a bug report <https://github.com/ansys/pymechanical/issues/new?assignees=&labels=bug&projects=&template=bug.yml&title=Bug+located+in+...>`_
* `File a documentation issue <https://github.com/ansys/pymechanical/issues/new?assignees=&labels=documentation&projects=&template=documentation.yml&title=Modify+...>`_
* `Request a feature <https://github.com/ansys/pymechanical/issues/new?assignees=&labels=enhancement&projects=&template=feature.yml&title=Add+...>`_
* `Add an example <https://github.com/ansys/pymechanical/issues/new?assignees=&labels=example&projects=&template=examples.yml&title=Example+proposal%3A+...>`_
* `Post all other issues <https://github.com/ansys/pymechanical/issues/new>`_

If your issue does not fit into one of these template categories, create your own issue.

.. LINKS AND REFERENCES
.. _PyAnsys Developer's Guide: https://dev.docs.pyansys.com/
.. _PyTest: https://docs.pytest.org/en/stable/
.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _black: https://github.com/psf/black
.. _flake8: https://flake8.pycqa.org/en/latest/
.. _isort: https://github.com/PyCQA/isort
.. _tox: https://tox.wiki/
