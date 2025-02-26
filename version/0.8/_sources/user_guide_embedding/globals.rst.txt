.. _ref_embedding_user_guide_globals:

*******
Globals
*******

When using Mechanical scripting APIs (in either Mechanical's graphical user interface or when
sending scripts to a remote session of Mechanical), there are many global variables that are
by default usable from Python. Some of these are API entry points, like those discussed in
:ref:`ref_user_guide_scripting`, while others are types and namespaces that are used by the
scripting APIs. Examples of those are the ``Quantity`` class or the ``DataModelObjectCategory``
enum.

Embedding Mechanical into Python is as simple as constructing an application object. This can
not automatically change the global variables available to the Python scope that constructed
it. As a utility, a function that adds the API entry points is available. To use it, run the
following code:

.. code:: python

   from ansys.mechanical.core import App, global_variables

   app = App()
   # The following line extracts the global API entry points and merges them into your global
   # Python global variables.
   globals().update(global_variables(app))
