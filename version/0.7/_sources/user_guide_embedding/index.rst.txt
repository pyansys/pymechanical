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
