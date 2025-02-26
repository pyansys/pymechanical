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
The ``ansys.mechanical.core`` package supports Python 3.7 through
Python 3.10 on Windows, Mac, and Linux.

You should consider installing PyMechanical in a virtual environment.
For more information, see Python's
`venv -- Creation of virtual environments <https://docs.python.org/3/library/venv.html>`_.

Install the latest package from `PyPi
<https://pypi.org/project/ansys-mechanical-core/>`_ with:

.. code::

   pip install ansys-mechanical-core


Alternatively, install the latest package from `GitHub
<https://github.com/pyansys/pymechanical/>`_ with:

.. code::

   pip install git+https://github.com/pyansys/pymechanical.git


Installing a *development* version of PyMechanical allows you to make modifications
locally and have these changes reflected in your setup once you restart the
Python kernel.

Install a local development version with:

.. code::

   git clone https://github.com/pyansys/pymechanical.git
   cd pymechanical
   pip install -e .


Install offline
---------------
If you want to install PyMechanical on a computer without access to the internet,
you can download a wheelhouse archive that corresponds to your
machine architecture from the `Releases page <https://github.com/pyansys/pymechanical/releases>`_.

Each wheelhouse archive contains all the Python wheels necessary to install
PyMechanical from scratch on Windows and Linux for Python 3.7 through Python 3.10. You can install
a wheelhouse archive on an isolated system with a fresh Python installation or on a
virtual environment.

For example, on Linux with Python 3.7, unzip the wheelhouse archive and install it with:

.. code::

   unzip ansys-mechanical-core-v0.6.0-wheelhouse-Linux-3.7 wheelhouse
   pip install ansys-mechanical-core -f wheelhouse --no-index --upgrade --ignore-installed

If you are on Windows with Python 3.9, unzip the ``ansys-mechanical-core-v0.6.0-wheelhouse-Windows-3.9`` wheelhouse archive
to a ``wheelhouse`` directory and then install using the preceding code.

Verify your installation
------------------------
Verify your installation by starting Mechanical from Python:

.. code:: python

    >>> from ansys.mechanical.core import launch_mechanical
    >>> mechanical = launch_mechanical()
    >>> print(mechanical)

    Ansys Mechanical [Ansys Mechanical Enterprise]
    Product Version:231
    Software build date:Wednesday, August 10, 2022 4:28:15 PM

If you see a response from the server, you can begin using Mechanical
as a service. For information on the PyMechanical interface, see
:ref:`ref_mechanical_user_guide`.
