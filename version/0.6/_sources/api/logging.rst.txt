Logging
=======
To make the logging of events consistent, PyMechanical has a specific
logging architecture with global and local logging instances.

For these two types of loggers, the default format for a log message is:

.. code:: python

    >>> from ansys.mechanical.core import launch_mechanical
    >>> mechanical = launch_mechanical()
    >>> mechanical._log.info('This is an useful message')
      LEVEL - INSTANCE NAME - MODULE - FUNCTION - MESSAGE
      INFO - GRPC_127.0.0.1:10000 -  test - <module> - This is an useful message

The ``instance_name`` field depends on the name of the Mechanical instance,
which might not be set yet when the log record is created (for
example, during the initialization of the library).  If a Mechanical
instance is not yet created, this field might be empty.

Because both types of loggers are based in the Python ``logging`` module,
you can use any of the tools provided in this module to extend or modify
these loggers.


``Logger`` class
----------------
.. currentmodule:: ansys.mechanical.core.logging

.. autosummary::
   :toctree: _autosummary

   Logger
