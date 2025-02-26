.. _using_standard_install:

***********************************************
Using PyMechanical from a standard installation
***********************************************

The ``ansys-mechanical-core`` package requires either a local or
remote instance of Mechanical to communicate with. This page describes
how Mechanical is installed from the Ansys standard installer and
describes how you launch and interface with Mechanical from Python.

Install Mechanical
------------------

Mechanical is installed by default from the Ansys standard installer.
When you run the standard installer, look under the **Structural Mechanics**
heading to verify that the **Mechanical Products** checkbox is selected.
Although options in the standard installer might change, this image provides
a reference:

.. figure:: ../images/unified_install_2023R1.jpg
    :width: 400pt

Launch a remote Mechanical session
----------------------------------
You can use PyMechanical to launch a Mechanical session on the local machine
Python is running on. Alternatively, you can run Mechanical's command line
directly on any machine to start Mechanical in server mode and then use its
IP address to manually connect to it from Python.

Launch Mechanical on the local machine using Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When Mechanical is installed locally on your machine, you can use the
:func:`launch_mechanical() <ansys.mechanical.core.launch_mechanical>` method to launch and automatically connect to
Mechanical. While this method provides the easiest and fastest way to launch Mechanical, it only works with a local
Mechanical installation.

Launch Mechanical locally with this code:

.. code:: pycon

    >>> from ansys.mechanical.core import launch_mechanical
    >>> mechanical = launch_mechanical()
    >>> mechanical

    Ansys Mechanical [Ansys Mechanical Enterprise]
    Product Version:231
    Software build date:Wednesday, August 10, 2022 4:28:15 PM


Launch a Mechanical server from the command line
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can launch Mechanical from the command line in server mode and then
manually connect to it.

**On Windows**

Assume that Mechanical is installed at ``C:/Program Files/ANSYS Inc/vXXX``
, where ``XXX`` is the three-digit format for the version. For example,
the path for 2023 R1 is typically ``C:/Program Files/ANSYS Inc/v231``.

Launch Mechanical in server mode with this code:

.. code::

    C:/Program Files/ANSYS Inc/v231/aisol/bin/winx64/.AnsysWBU.exe -DSApplet -AppModeMech -nosplash -notabctrl -grpc 10000

**On Linux**

Assume that Mechanical 2023 R1 is installed at ``/usr/ansys_inc``.

Launch Mechanical in server mode with this code:

.. code::

    /usr/ansys_inc/v231/aisol/.workbench -dsapplet -AppModeMech -nosplash -notabctrl -grpc 10000


View server information
~~~~~~~~~~~~~~~~~~~~~~~~
As Mechanical starts in server mode, you can see the server information:

.. code::

    Starting the grpc server at port 10000
    Started the grpc server at port 10000

If you want to configure the port that the Mechanical server listens on, when you launch
Mechanical, use the ``-grpc`` argument. For example, on Linux, launch Mechanical 2023 R1
on port ``10001`` with:

.. code::

    C:/Program Files/ANSYS Inc/v231/aisol/bin/winx64/.AnsysWBU.exe -grpc 10001


Connect to a Mechanical session
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can connect to a Mechanical session from the same host or from an external host.

Assuming that Mechanical is running locally at the default IP address (``127.0.0.1``) on the
default port (``10000``), you would use this code to connect to it with this code:

.. code:: python

    from ansys.mechanical.core import Mechanical

    mechanical = Mechanical()


Now assume that a remote instance of Mechanical has been started in server mode. To connect to
the computer on your local area network that is running Mechanical, you can use either
an IP address and port or a hostname and port.

**IP address and port**

Assume that Mechanical is running remotely at IP address ``192.168.0.1`` on port ``10000``.

You would connect to it with this code:

.. code:: python

    mechanical = Mechanical("192.168.0.1", port=10000)

**Hostname and port**

Assume that Mechanical is running remotely at hostname ``myremotemachine`` on port ``10000``.

You would connect to it with this code:

.. code:: python

    mechanical = Mechanical("myremotemachine", port=10000)


Launching issues
----------------

For any number of reasons, launching Mechanical can fail. Some approaches
follow for debugging launch failures.

Manually set the location of the executable file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have a non-standard installation of Mechanical, PyMechanical might
not be able to find your installation. In this case, you should manually
set the location of your Mechanical executable file as the first parameter
for the :func:`launch_mechanical() <ansys.mechanical.core.launch_mechanical>` method.

**On Windows**

.. code:: python

    from ansys.mechanical.core import launch_mechanical

    exec_loc = "C:/Program Files/ANSYS Inc/v231/aisol/bin/winx64/AnsysWBU.exe"
    mechanical = launch_mechanical(exec_loc)


**On Linux**

.. code:: python

    from ansys.mechanical.core import launch_mechanical

    exec_loc = "/usr/ansys_inc/v231/aisol/.workbench"
    mechanical = launch_mechanical(exec_loc)


If, when using the :func:`launch_mechanical() <ansys.mechanical.core.launch_mechanical>`
method, Mechanical still fails to launch or hangs while launching, pass the
``verbose_mechanical=True`` parameter. This prints the output of Mechanical in the Python console.
You can then use this output to debug why Mechanical isn't launching.

.. Note::

    On Windows, output is limited because of the way Mechanical launches.

Debug from the command line
~~~~~~~~~~~~~~~~~~~~~~~~~~~
In some cases, debugging why Mechanical isn't launching might require
running the launch command from the command line. The following
Windows and Linux code examples assume that you are launching Mechanical
2023 R1.

**On Windows**

Open a command prompt and run this command:

.. code::

    "C:/Program Files/ANSYS Inc/v231/aiso/bin/winx64/AnsysWBU.exe -DSApplet -AppModeMech -nosplash -notabctrl -grpc 10000"

.. note::
   PowerShell users can run the preceding command without including the opening and
   closing quotation marks.


**On Linux**

.. code::

    /usr/ansys_inc/v231/aisol/.workbench -DSApplet -AppModeMech -nosplash -notabctrl -grpc 10000


If the preceding command for your operating system doesn't launch Mechanical, you might have
a variety of issues, including:

  - License server setup
  - Running behind a VPN
  - Missing dependencies


Embed a Mechanical instance
---------------------------

The instructions for embedding a Mechanical instance are different on
Windows and Linux. While the Python code is the same in both cases,
Linux requires some additional environment variables.

Python code
~~~~~~~~~~~
.. code:: pycon

    >>> from ansys.mechanical.core import App
    >>> mechanical = App()
    >>> mechanical
    Ansys Mechanical [Ansys Mechanical Enterprise]
    Product Version:231
    Software build date:Wednesday, August 10, 2022 4:28:15 PM

Additional information for Linux
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Starting with 2023 R2, it is possible to embed an instance of Mechanical on Linux.
However, because of differences in how Mechanical works on Linux, you cannot simply
run Python as usual. On Linux, certain environment variables must be set for the Python
process before it starts. You can set up these environment variables using the ``.workbench_lite``
script that is shipped with the Mechanical installation.

Assume that Mechanical 2023 R2 is installed at ``/usr/ansys_inc``.
You would run Python with this command:

.. code::

    /usr/ansys_inc/v232/aisol/.workbench_lite python


Licensing issues
----------------

`PADT <https://www.padtinc.com/>`_ has an `Ansys <https://www.padtinc.com/simulation/ansys-simulation-products/>`_
product section. Posts about licensing are common.

If you are responsible for maintaining an Ansys license or have a personal installation
of Ansys, you likely can access the
`Licensing <https://ansyshelp.ansys.com/account/secured?returnurl=/Views/Secured/prod_page.html?pn=Licensing&pid=Licensing&lang=en>`_
section of the Ansys Help, where you can view or download the *Ansys, Inc. Licensing Guide* for
comprehensive licensing information.


VPN issues
----------
Sometimes, Mechanical has issues starting when VPN software is running. For more information,
access the `Mechanical Users Guide <https://ansyshelp.ansys.com/account/secured?returnurl=/Views/Secured/corp/v231/en/wb_sim/ds_Home.html>`_
in the Ansys Help.
