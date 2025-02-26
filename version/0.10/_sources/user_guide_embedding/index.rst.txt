.. _ref_user_guide_embedding:

Embedded instances
==================

This section provides an overview of how you use PyMechanical to embed
an instance of Mechanical in Python.

..
   This toctree must be a top-level index to get it to show up in
   pydata_sphinx_theme.

.. toctree::
   :maxdepth: 1
   :hidden:

   configuration
   globals
   logging
   libraries

Overview
--------

The :class:`Application <ansys.mechanical.core.embedding.Application>` class provides
a Mechanical instance:

.. code:: python

   from ansys.mechanical.core import App

   app = App()
   ns = app.DataModel.Project.Model.AddNamedSelection()

The :class:`Application <ansys.mechanical.core.embedding.Application>` class has access
to the global scripting entry points that are available from built-in Mechanical scripting:

* ExtAPI: ``Application.ExtAPI``
* DataModel: ``Application.DataModel``
* Model: ``Application.DataModel.Project.Model``
* Tree: ``Application.DataModel.Tree``
* Graphics: ``Application.ExtAPI.Graphics``

Besides scripting entry points, many other types and objects are available from
built-in Mechanical scripting. To learn how to import scripting entry points,
namespaces, and types, see :ref:`ref_embedding_user_guide_globals`.

Additional configuration
------------------------

By default, an instance of the :class:`Application <ansys.mechanical.core.embedding.Application>` class
uses the same Addin configuration as standalone Mechanical. To customize Addins, see
:ref:`ref_embedding_user_guide_addin_configuration`.

Diagnosing problems with embedding
----------------------------------

In some cases, debugging the embedded Mechanical instance may require additional logging.
For information on how to configure logging, see :ref:`ref_embedding_user_guide_logging`.

Running PyMechanical embedding scripts inside Mechanical with IronPython
------------------------------------------------------------------------

If your PyMechanical embedding script does not use any other third-party Python package, such as `NumPy`,
it is possible to adapt it so that it can run inside of Mechanical with IronPython.
The scripting occurs inside Mechanical's command line interface. For instance, consider the following PyMechanical code:

.. code:: python

  from ansys.mechanical.core import App, global_variables

  app = App()
  globals().update(global_variables(app))
  ns = DataModel.Project.Model.AddNamedSelection()
  ns.Name = "Jarvis"

The above code can be written as a Python file, such as ``file.py`` with only the following content:

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

   Alternately user can use the following commands in the command prompt of Windows and the terminal
   for Linux systems.

   **On Windows**

   .. code::

      "C:/Program Files/ANSYS Inc/v241/aisol/bin/winx64/AnsysWBU.exe -DSApplet -AppModeMech -script file.py"

   PowerShell users can run the preceding command without including the opening and
   closing quotation marks.

   **On Linux**

   .. code::

      /usr/ansys_inc/v231/aisol/.workbench -DSApplet -AppModeMech -nosplash -notabctrl -script file.py


   ``-nosplash`` and ``-notabctrl`` not needed for versions 23.2 or above

   On either Windows or Linux, add the command line argument ``-b`` to run the script in batch mode.
