.. _ref_embedding_user_guide_libraries:

Libraries
=========

.. note::

    This is an experimental feature. Some of these libraries may not work.

Most of Mechanical's scripting APIs are implemented in C#. However, there are a small number
of Python modules that are distributed with the installation of Mechanical that can be used
from within the Mechanical Scripting Pane. These modules are not available for use from an
embedded instance of Mechanical in Python because Python does not know where to find them.

But, in order to use these modules, you need to use the experimental function
``add_mechanical_python_libraries`` to help Python locate them and make it possible to import
them. In addition, it is necessary to first initialize the embedded instance of Mechanical
because these libraries may expect the .NET Common Language Runtime to be initialized as well
as for the appropriate C# libraries to be loaded.

To use the above function, run the following:

.. code:: python


   from ansys.mechanical.core import App, global_variables
   from ansys.mechanical.core.embedding import add_mechanical_python_libraries

   app = App(version=241)

   add_mechanical_python_libraries(app)
   import materials  # This is materials.py that's shipped with Mechanical v241

.. warning::

    Using version as argument to ``add_mechanical_python_libraries()`` is deprecated.