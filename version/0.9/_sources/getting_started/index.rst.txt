===============
Getting started
===============
To run PyMechanical, you must have a licensed copy of Ansys Mechanical
installed locally. The version installed dictates the interface and
features that are available to you.

PyMechanical is compatible with Mechanical 2023 R1 and later on Windows
and Linux. Later releases provide significantly better support and features.

For more information, see the `Ansys Mechanical <https://www.ansys.com/products/structures/ansys-mechanical>`_
page on the Ansys website.

.. toctree::
   :hidden:
   :maxdepth: 2

   running_mechanical
   versioning
   docker
   faq
   wsl

Install the package
-------------------
The ``ansys.mechanical.core`` package supports Python 3.8 through
Python 3.11 on Windows, Linux, and Mac.

You should consider installing PyMechanical in a virtual environment.
For more information, see Python's
`venv -- Creation of virtual environments <https://docs.python.org/3/library/venv.html>`_.

Install the latest package from `PyPi
<https://pypi.org/project/ansys-mechanical-core/>`_ with this command:

.. code::

   pip install ansys-mechanical-core


Install offline
---------------
If you want to install PyMechanical on a computer without access to the internet,
you can download a wheelhouse archive that corresponds to your
machine architecture from the `Releases page <https://github.com/ansys/pymechanical/releases>`_ 
of the PyMechanical repository.

Each wheelhouse archive contains all the Python wheels necessary to install
PyMechanical from scratch on Windows and Linux for Python 3.8 through Python 3.10. You can install
a wheelhouse archive on an isolated system with a fresh Python installation or on a
virtual environment.

For example, on Linux with Python 3.8, unzip the wheelhouse archive and install it with
this code:

.. code::

   unzip ansys-mechanical-core-v0.7.dev0-wheelhouse-Linux-3.8 wheelhouse
   pip install ansys-mechanical-core -f wheelhouse --no-index --upgrade --ignore-installed

If you are on Windows with Python 3.9, unzip the ``ansys-mechanical-core-v0.7.dev0-wheelhouse-Windows-3.9``
wheelhouse archive to a ``wheelhouse`` directory and then install it using ``pip`` like
in the preceding example.

Verify your installation
------------------------
The way that you verify your installation depends on whether you want to run
Mechanical using a remote session or an embedded instance.

Verify a remote session
^^^^^^^^^^^^^^^^^^^^^^^
Verify your installation by starting a remote session of Mechanical from Python:

.. code:: pycon

    >>> from ansys.mechanical.core import launch_mechanical
    >>> mechanical = launch_mechanical()
    >>> mechanical

    Ansys Mechanical [Ansys Mechanical Enterprise]
    Product Version:231
    Software build date:Wednesday, August 10, 2022 4:28:15 PM

If you see a response from the server, you can begin using Mechanical
as a service. For information on the PyMechanical interface, see
:ref:`ref_mechanical_user_guide`.

Verify an embedded instance
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Verify your installation by loading an embedded instance of Mechanical in Python.

.. note::
   If you are running on Linux, you must set some environment variables for
   embedding of Mechanical in Python to work. A script that sets these variables is
   distributed with Mechanical 2023 R2 and later. For 2023 R2, the script is located
   here:
   
   ``/path/to/ansys_inc/v232/aisol/.workbench_lite``

To use the script, prepend it to any invocation of Python:

.. code::

    /path/to/ansys_inc/v232/aisol/.workbench_lite python


Inside of Python, use the following commands to load an embedded instance:

.. code:: pycon

   >>> from ansys.mechanical.core import App
   >>> app = App()
   >>> print(app)
   Ansys Mechanical [Ansys Mechanical Enterprise]
   Product Version:231
   Software build date:Wednesday, August 10, 2022 4:28:15 PM
