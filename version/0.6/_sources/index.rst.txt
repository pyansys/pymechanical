PyMechanical documentation |version|
====================================

.. toctree::
   :hidden:
   :maxdepth: 3


   getting_started/index
   user_guide/index
   api/index
   examples/index
   contributing



Introduction
------------
PyMechanical is part of the larger `PyAnsys <https://docs.pyansys.com>`_
effort to facilitate the use of Ansys technologies directly from
Python. Its primary package, ``ansys-mechanical-core``, provides
scripting of Ansys Mechanical through Python.

With PyMechanical, you can integrate the simulation capabilities
of the Mechanical multi-physics solver directly into novel apps.
The package presents a Python-friendly interface to drive the software
that manages the submission of low-level Mechanical scripting commands,
while exchanging data through high-performance gRPC interfaces.

Accelerate the preparation of your simulations using PyMechanical. Combine the
expressiveness of general-purpose Python code to control the flow in your
input decks with methods that drive the solver. Explore proof of concept
studies or capture knowledge using interactive Jupyter notebooks. Tap
the solver as the physics engine in your next Artificial Intelligence
application. Contributions to this open source library are welcome.


Background
----------
PyMechanical is based on `gRPC <https://grpc.io/>`_, a modern, open
source, high-performance Remote Procedure Call (RPC) framework. PyMechanical
allows the Mechanical application to function as a server, ready to
respond to connecting clients.

gRPC establishes secure connections so that a client app can directly call
methods on a potentially remote Mechanical instance as if it were a local
object. The use of HTTP/2 makes it friendly to modern internet infrastructures.
This, along with the use of binary transmission formats, favors higher
performance. Using gRPC, PyMechanical can send Mechanical scripting API
commands to an Mechanical instance running anywhere, while producing
network footprints that are compact and efficient.


Brief code
----------
Here is a brief code example showing how PyMechanical works:

.. code:: python

    >>> from ansys.mechanical.core import launch_mechanical
    >>> mechanical = launch_mechanical()
    >>> print(mechanical)

    Ansys Mechanical [Ansys Mechanical Enterprise]
    Product Version:231
    Software build date:Wednesday, August 10, 2022 4:28:15 PM

Mechanical is now active and you can send commands to it as a genuine
Python class. For example, you can send some scripts:

.. code:: python

    result = mechanical.run_python_script('2+3')
    result = mechanical.run_python_script('10*5')

Mechanical interactively returns the result of each command, storing
in to the logging module. Or, you can immediately print the result with::   

    print(mechanical.run_python_script('2+3')


Errors are caught immediately and Pythonically.

For comprehensive information on PyMechanical features, see the
:ref:`ref_user_guide`.


Project index
*************

* :ref:`genindex`
