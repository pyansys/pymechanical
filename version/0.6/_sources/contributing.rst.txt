.. _ref_contributing:

==========
Contribute
==========
Overall guidance on contributing to a PyAnsys library appears in
`Contribute <https://dev.docs.pyansys.com/how-to/contributing.html>`_
in the *PyAnsys Developer's Guide*. Ensure that you are thoroughly familiar
with this guide, paying particular attention to `Guidelines and Best Practices
<https://dev.docs.pyansys.com/how-to/index.html>`_, before attempting to
contribute to PyMechanical.
 
The following contribution information is specific to PyMechanical.

Clone the repository
--------------------
To clone and install the latest version of PyMechanical in
development mode, run:

.. code::

    git clone https://github.com/pyansys/pymechanical
    cd pymechanical
    pip install pip -U
    pip install -e .


Post issues
-----------
Use the `PyMechanical Issues <https://github.com/pyansys/pymechanical/issues>`_
page to submit questions, report bugs, and request new features. When possible,
use these templates:

* Bug report
* Feature request

If your issue does not fit into one of these template categories, create your own issue.

To reach the PyAnsys support team, email `pyansys.support@ansys.com <pyansys.support@ansys.com>`_.

View documentation
------------------
Documentation for the latest stable release of PyMechanical is hosted at
`PyMechanical Documentation <https://mechanical.docs.pyansys.com>`_.

Documentation for the latest development version, which tracks the
``main`` branch, is hosted at `Development PyMechanical Documentation <https://dev.mechanical.docs.pyansys.com/>`_.
This version is automatically kept up to date via GitHub actions.

Test PyMechanical
-----------------
If you do not have a licensed copy of Mechanical installed locally but
want to run PyMechanical unit tests, you must set up environment
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
when you use the ``launch_mechanical`` method.


Code style
----------
As indicated in `Coding style <https://dev.docs.pyansys.com/coding-style/index.html>`_
in the *PyAnsys Developer's Guide*, PyMechanical follows PEP8 guidelines. PyMechanical
implements `pre-commit <https://pre-commit.com/>`_ for style checking.

To ensure your code meets minimum code styling standards, run::

  pip install pre-commit
  pre-commit run --all-files

You can also install this as a pre-commit hook by running::

  pre-commit install

This way, it's not possible for you to push code that fails the style checks. For example::

  $ pre-commit install
  $ git commit -am "added my cool feature"
  black....................................................................Passed
  isort....................................................................Passed
  flake8...................................................................Passed
  codespell................................................................Passed

