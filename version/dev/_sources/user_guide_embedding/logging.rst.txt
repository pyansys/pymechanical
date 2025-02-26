.. _ref_embedding_user_guide_logging:

Logging
=======

Mechanical has a logging system that is useful when debugging issues. Normally, it is
enabled by setting environment variables before starting Mechanical. With PyMechanical,
it is possible to configure logging at any time, whether it is before or after creating
the embedded application, using the same Python API.

Use the `Configuration <../api/ansys/mechanical/core/embedding/logger/Configuration.html>`_ class to
configure logging to the standard output for all warning messages and above (which are error and fatal messages).
For example:

.. code:: python

    import logging
    import ansys.mechanical.core as mech
    from ansys.mechanical.core.embedding.logger import Configuration, Logger

    Configuration.configure(level=logging.WARNING, to_stdout=True)
    _ = mech.App()

After the embedded application has been created, you can write messages to the same
log using the `Logger <../api/ansys/mechanical/core/embedding/logger/Logger.html>` class like this:

.. code:: python

    from ansys.mechanical.core.embedding.logger import Logger

    Logger.error("message")
