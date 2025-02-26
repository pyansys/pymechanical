Initial setup for launching a Mechanical session on the local machine
=====================================================================

To run, PyMechanical must know the location of your Mechanical installation.
Most of the time, PyMechanical can determine this location automatically. However,
if you have a non-standard installation, you must provide this location.

To test and set up your installation of PyMechanical, run the
:func:`launch_mechanical() <ansys.mechanical.core.launch_mechanical>`
method:

.. code:: python

    from ansys.mechanical.core import launch_mechanical

    mechanical = launch_mechanical()

The first time that you run this method, PyMechanical attempts to detect the location
of your Mechanical installation based on environment variables. If it cannot find
a Mechanical installation, PyMechanical asks you to supply the location of the
Mechanical executable file.

**On Linux**

.. code::

    Enter location of Mechanical executable: /usr/ansys_inc/v231/aisol/.workbench

**On Windows**

.. code::

    Enter location of Mechanical executable: C:/Program Files/ANSYS Inc/v231/aisol/bin/winx64/AnsysWBU.exe

The settings file for Mechanical is stored locally. You do not need to enter
the path again. If you must change the path, perhaps to change the default
version of Mechanical, run the following:

.. code:: python

    from ansys.mechanical import core as pymechanical

    new_path = "C:/Program Files/ANSYS Inc/v231/aisol/bin/winx64/AnsysWBU.exe"
    pymechanical.change_default_mechanical_path(new_path)

For more information, see the :func:`change_default_mechanical_path() <ansys.mechanical.core.change_default_mechanical_path>`
and :func:`find_mechanical() <ansys.tools.path.find_mechanical>` methods.

Additionally, you can use the ``exec_file`` keyword argument to specify the location of the
Mechanical executable file.

**On Linux**

.. code:: python

    from ansys.mechanical.core import launch_mechanical

    mechanical = launch_mechanical(exec_file="/usr/ansys_inc/v231/aisol/.workbench")

**On Windows**

.. code:: python

    from ansys.mechanical.core import launch_mechanical

    mechanical = launch_mechanical(
        exec_file="C:\\Program File\\ANSYS Inc\\v231\\aisol\\bin\\winx64\\AnsysWBU.exe"
    )

You can use the ``additional_switches`` keyword argument to specify additional arguments.

.. code:: python

    from ansys.mechanical.core import launch_mechanical

    custom_exec = "/usr/ansys_inc/v231/aisol/.workbench"
    add_switch = f"-featureflags mechanical.material.import;"
    mechanical = launch_mechanical(additional_switches=add_switch)

API reference
~~~~~~~~~~~~~
For more information on controlling how Mechanical launches locally, see the
:func:`launch_mechanical() <ansys.mechanical.core.launch_mechanical>` method.
