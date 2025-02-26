.. _ref_contributing:

==========
Contribute
==========
Overall guidance on contributing to a PyAnsys library appears in
`Contributing <https://dev.docs.pyansys.com/how-to/contributing.html>`_
in the *PyAnsys Developer's Guide*. Ensure that you are thoroughly familiar
with this guide before attempting to contribute to PyMechanical.
 
The following contribution information is specific to PyMechanical.


Install in developer mode
-------------------------

Installing PyMechanical in developer mode allows
you to modify the source and enhance it.

.. note::

    Before contributing to the project, ensure that you are thoroughly familiar
    with the `PyAnsys Developer's Guide`_.

To install PyMechanical in developer mode, perform these steps:

#. Clone the ``pymechanical`` repository:

   .. code:: bash

      git clone https://github.com/pyansys/pymechanical

#. Access the ``pymechanical`` directory where the repository has been cloned:

   .. code:: bash

      cd pymechanical

#. Create a clean Python virtual environment and activate it:

.. tab-set::

    .. tab-item:: Windows

        .. tab-set::

            .. tab-item:: CMD

                .. code-block:: text

                    python -m venv .venv
                    .venv\Scripts\activate.bat

            .. tab-item:: PowerShell

                .. code-block:: text

                    python -m venv .venv
                    .venv\Scripts\Activate.ps1

    .. tab-item:: Linux/UNIX

        .. code-block:: text

            python -m venv .venv
            source .venv/bin/activate
  

#. Ensure that you have the latest required build system tools:

   .. code:: bash

      python -m pip install -U pip tox flit twine

#. Install the project in editable mode:

   .. code:: bash

      # Install the minimum requirements
      python -m pip install -e .

      # Install the minimum + tests requirements
      python -m pip install -e .[tests]

      # Install the minimum + doc requirements
      python -m pip install -e .[doc]

      # Install all requirements
      python -m pip install -e .[tests,doc]

#. Verify your development installation:

    .. code:: bash

        tox


Test PyMechanical
-----------------
PyMechanical uses `PyTest`_ and `tox`_ for unit testing.

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


Without ``tox``
^^^^^^^^^^^^^^^

If required, from the command line, you can call style commands like
`black`_, `isort`_, and `flake8`_. You can also call unit testing commands like `PyTest`_.
However, running these commands do not guarantee that your project is being tested
in an isolated environment, which is the reason why tools like ``tox`` exist.


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


Documentation
-------------

For building documentation, you can run the usual rules provided in the
`Sphinx`_ ``make`` file. Here is an example:

.. code:: bash

    #  build and view the doc from the POSIX system
    make -C doc/ html && your_browser_name doc/html/index.html

    # build and view the doc from a Windows environment
    .\doc\make.bat clean
    .\doc\make.bat html
    start .\doc\_build\html\index.html


However, the recommended way of checking documentation integrity is to use
``tox``:

.. code:: bash

    tox -e doc && your_browser_name .tox/doc_out/index.html


Distributing
------------

If you would like to create either source or wheel files, start by installing
the building requirements and then executing the build module:

.. code:: bash

    python -m pip install -U pip
    python -m flit build
    python -m twine check dist/*


Post issues
-----------
Use the `PyMechanical Issues <https://github.com/pyansys/pymechanical/issues>`_
page to submit questions, report bugs, and request new features. When possible,
use these templates:

* Bug report
* Feature request

If your issue does not fit into one of these template categories, create your own issue.

To reach the PyAnsys core team, email `pyansys.core@ansys.com <pyansys.core@ansys.com>`_.


View documentation
------------------
Documentation for the latest stable release of PyMechanical is hosted at
`PyMechanical Documentation <https://mechanical.docs.pyansys.com>`_.

Documentation for the latest development version, which tracks the
``main`` branch, is hosted at `Development PyMechanical Documentation <https://mechanical.docs.pyansys.com/version/dev/index.html>`_.
This version is automatically kept up to date via GitHub actions.


Code style
----------
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
  black....................................................................Passed
  isort....................................................................Passed
  flake8...................................................................Passed
  codespell................................................................Passed


.. LINKS AND REFERENCES
.. _PyAnsys Developer's Guide: https://dev.docs.pyansys.com/
.. _PyTest: https://docs.pytest.org/en/stable/
.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _black: https://github.com/psf/black
.. _flake8: https://flake8.pycqa.org/en/latest/
.. _isort: https://github.com/PyCQA/isort
.. _tox: https://tox.wiki/
