.. _ref_user_guide_embedding:

==================
Embedded instances
==================
This section provides an overview of how you use PyMechanical to embed
an instance of Mechanical in Python.


..
   This toctreemust be a top-level index to get it to show up in
   pydata_sphinx_theme.

.. toctree::
   :maxdepth: 1
   :hidden:

   configuration
   globals
   logging


Overview
========
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
is configured in the same way as Mechanical. To customize an instance, see
:ref:`ref_embedding_user_guide_configuration`.

Diagnosing problems with embedding
----------------------------------
In some cases, debugging why the embedded Mechanical instance is not working requires additional logging.
 For information on how to configure logging, see :ref:`ref_embedding_user_guide_logging` .

Running PyMechanical embedding scripts inside Mechanical with IronPython
------------------------------------------------------------------------
If your PyMechanical embedding script does not use any other third-party Python package, such as `NumPy`,
it is possible to adapt it so that it can run inside of Mechanical with IronPython with scripting inside
Mechanical's command line interface. For instance, the consider the following PyMechanical code:

.. code:: python

  from ansys.mechanical.core import App, global_variables

  app = App()
  globals().update(global_variables(app))
  ns = DataModel.Project.Model.AddNamedSelection()
  ns.Name = "Jarvis"

The above code can be written as a Python file, such as "file.py" with only the following content:

.. code:: python

  ns = DataModel.Project.Model.AddNamedSelection()
  ns.Name = "Jarvis"

That python file does not contain the PyMechanical import statements, and can inside Mechanical using the command line

**On Windows**

Open a command prompt and run this command:

.. code::

    "C:/Program Files/ANSYS Inc/v231/aisol/bin/winx64/AnsysWBU.exe -DSApplet -AppModeMech -script file.py"

.. note::
   PowerShell users can run the preceding command without including the opening and
   closing quotation marks.


**On Linux**

From a terminal, run this command:

.. code::

    /usr/ansys_inc/v231/aisol/.workbench -DSApplet -AppModeMech -nosplash -notabctrl -script file.py


On either Windows or Linux, add the command line argument `-b` to run the script in batch mode.
