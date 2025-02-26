.. _ref_embedding_user_guide_addin_configuration:

Addin configuration
===================

There are some configuration options that are respected when loading an embedded instance
of Mechanical into python.
The class `Configuration <../api/ansys/mechanical/core/embedding/addins/AddinConfiguration.html#ansys.mechanical.core.embedding.addins.AddinConfiguration>`_ can be
used to set up Addin configuration. This configuration can be supplied to the constructor
of the class `App <../api/ansys/mechanical/core/embedding/app/App.html>`_.

For example, to load an instance of Mechanical using the "Mechanical" configuration name and
without loading any ACT Addins:

.. code:: python

    from ansys.mechanical.core import App
    from ansys.mechanical.core.embedding import AddinConfiguration

    config = AddinConfiguration("Mechanical")
    config.no_act_addins = True
    app = App(config=config)
