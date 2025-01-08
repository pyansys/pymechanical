.. _ref_embedding_user_guide_scripts_inside_mechanical:

Run PyMechanical embedding scripts inside Mechanical
====================================================

If your PyMechanical embedding script does not use any other third-party Python package, such as `NumPy`,
it is possible to adapt it so that it can run inside of Mechanical with IronPython.
The scripting occurs inside Mechanical's command line interface. For instance, consider the following PyMechanical code:

.. code:: python

  from ansys.mechanical.core import App

  app = App()
  app.update_globals(globals())
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

      "C:/Program Files/ANSYS Inc/v242/aisol/bin/winx64/AnsysWBU.exe -DSApplet -AppModeMech -script file.py"

   PowerShell users can run the preceding command without including the opening and
   closing quotation marks.

   **On Linux**

   .. code::

      /usr/ansys_inc/v242/aisol/.workbench -DSApplet -AppModeMech -script file.py

   On either Windows or Linux, add the command line argument ``-b`` to run the script in batch mode.
