.. _ref_user_guide_embedding:

Embedded instance
=================

This section provides an overview of how you use PyMechanical to embed
an instance of Mechanical in Python.

..
   This toctree must be a top-level index to get it to show up in
   pydata_sphinx_theme.

.. toctree::
   :maxdepth: 1
   :hidden:

   self
   configuration
   globals
   libraries

.. small example of how to use embedded instance (update_globals, use APIs, etc.)

.. dropdown:: Mechanical Scripting APIs available in PyMechanical
    :animate: fade-in-slide-down

      When using Mechanical scripting APIs (in either Mechanical's graphical user interface or when
      sending scripts to a remote session of Mechanical), there are many global variables that are
      by default usable from Python: API entry points, types, and namespaces.

      The `App`_ class has access to the global scripting API entry points that are
      available from built-in Mechanical scripting:

      * ExtAPI: ``Application.ExtAPI``
      * DataModel: ``Application.DataModel``
      * Model: ``Application.DataModel.Project.Model``
      * Tree: ``Application.DataModel.Tree``
      * Graphics: ``Application.ExtAPI.Graphics``

      Some examples of types and namespaces usable by Python are the ``Quantity`` and
      ``Transaction`` classes or the ``DataModel`` entry point.

      .. code:: python

         from ansys.mechanical.core import App

         app = App()
         named_selection = app.DataModel.Project.Model.AddNamedSelection()

      Embedding Mechanical into Python is as simple as constructing an application object.
      This can not automatically change the global variables available to the Python scope
      that constructed it. As a utility, a function that adds the API entry points is
      available. To use it, run the following code:

      .. code:: python

         from ansys.mechanical.core import App

         app = App()
         # The following line extracts the global API entry points and merges them
         # into your global Python global variables.
         app.update_globals(globals())

      Some enum types are available when scripting inside of Mechanical, such as
      ``SelectionTypeEnum`` or ``LoadDefineBy``. Because these number in the thousands,
      by default, these enums are included in these global variables. To avoid including
      them, set the second argument of ``update_globals`` to False.

      .. code:: python

         app.update_globals(globals(), False)

.. dropdown:: Customize addin configuration
    :animate: fade-in-slide-down

      By default, an instance of the `App`_ class uses the same Addin configuration as
      standalone Mechanical. To customize Addins, see
      :ref:`ref_embedding_user_guide_addin_configuration`.

.. dropdown:: Debug problems with embedded instances using logging
    :animate: fade-in-slide-down

      Use the `Configuration <../api/ansys/mechanical/core/embedding/logger/Configuration.html>`_
      class to configure logging to the standard output for all warning, error, and fatal
      messages. It is possible to configure logging before or after creating the embedded
      application.

      For example:

      .. code:: python

         import logging
         import ansys.mechanical.core as mech
         from ansys.mechanical.core.embedding.logger import Configuration, Logger

         Configuration.configure(level=logging.WARNING, to_stdout=True)
         _ = mech.App()

      After the embedded application has been created, you can write messages to the same
      log using the `Logger <../api/ansys/mechanical/core/embedding/logger/Logger.html>`_
      class like this:

      .. code:: python

         from ansys.mechanical.core.embedding.logger import Logger

         Logger.error("message")

.. dropdown:: Run PyMechanical embedding scripts inside Mechanical with IronPython
    :animate: fade-in-slide-down

      If your PyMechanical embedding script does not use any other third-party Python package,
      such as `NumPy`, it is possible to adapt it so that it can run inside of Mechanical
      with IronPython. The scripting occurs inside Mechanical's command line interface.
      For instance, consider the following PyMechanical code:

      .. code:: python

         from ansys.mechanical.core import App

         app = App()
         app.update_globals(globals())
         ns = DataModel.Project.Model.AddNamedSelection()
         ns.Name = "Jarvis"

      The above code can be written as a Python file, such as ``file.py`` with only the
      following content:

      .. code:: python

         ns = DataModel.Project.Model.AddNamedSelection()
         ns.Name = "Jarvis"

      Because the file does not contain the PyMechanical import statements, you can run
      ``file.py`` using the command line inside Mechanical.

      **Using command line interface (CLI)**

      This can be achieved on both the Windows and Linux platforms using
      ``ansys-mechanical`` cli from the virtual environment where ``ansys-mechanical-core``
      has been installed. Activate the virtual environment and then use CLI to run the scripts.
      If multiple Mechanical versions are installed in the same system,
      versions can be specified using ``-r`` flag. Use ``-h`` for more information.

      .. code::

         ansys-mechanical -i file.py

      .. note::

         Alternately user can use the following commands in the command prompt of Windows and the
         terminal for Linux systems.

         **On Windows**

         .. code::

            "C:/Program Files/ANSYS Inc/v242/aisol/bin/winx64/AnsysWBU.exe -DSApplet -AppModeMech -script file.py"

            PowerShell users can run the preceding command without including the opening and
            closing quotation marks.

         **On Linux**

         .. code::

            /usr/ansys_inc/v242/aisol/.workbench -DSApplet -AppModeMech -script file.py

            On either Windows or Linux, add the command line argument ``-b`` to run the script in batch mode.
