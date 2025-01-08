.. _ref_user_guide_embedding:

Embedded instance
-----------------

This section provides an overview of how you use PyMechanical to embed an instance of Mechanical in Python.

.. toctree::
    :maxdepth: 2
    :hidden:

    new_features
    globals
    libraries
    configuration
    logging

Overview
^^^^^^^^

Create an instance of Mechanical with the `App <../api/ansys/mechanical/core/embedding/app/App.html>`_ class:

.. code:: python

   from ansys.mechanical.core import App

   app = App()
   ns = app.DataModel.Project.Model.AddNamedSelection()

The `App`_ class has access to the global scripting entry points that are
available from built-in Mechanical scripting:

* ExtAPI: ``Application.ExtAPI``
* DataModel: ``Application.DataModel``
* Model: ``Application.DataModel.Project.Model``
* Tree: ``Application.DataModel.Tree``
* Graphics: ``Application.ExtAPI.Graphics``

Additional information
^^^^^^^^^^^^^^^^^^^^^^

* :ref:`ref_embedding_user_guide_new_features`: See new features of the embedding instance for PyMechanical.
* :ref:`ref_embedding_user_guide_globals`: See how to import scripting entry points, namespaces, and types with globals.
* :ref:`ref_embedding_user_guide_addin_configuration`: See additional addin configuration options. By default, an instance of the `App`_ class uses the same Addin configuration as standalone Mechanical.
* :ref:`ref_embedding_user_guide_logging`: See information on how to configure logging in Mechanical for help with debugging the Mechanical instance.
* :ref:`ref_embedding_user_guide_scripts_inside_mechanical`: See information about how to run embedding scripts inside Mechanical with IronPython with the ``ansys-mechanical`` command.
