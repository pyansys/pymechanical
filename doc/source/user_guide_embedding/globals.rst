.. _ref_embedding_user_guide_globals:

Globals
=======

When using Mechanical scripting APIs (in either Mechanical's graphical user interface or when
sending scripts to a remote session of Mechanical), there are many global variables that are
by default usable from Python. Some of these are API entry points, like those discussed in
:ref:`ref_user_guide_scripting`, while others are types and namespaces that are used by the
scripting APIs. Examples of those are the ``Quantity``, ``Transaction`` class or the ``DataModel``
entry point.

To add these global variables to the Python scope, create an instance of the ``App`` class
with the ``globals`` argument set to the Python global variables:

.. code:: python

   from ansys.mechanical.core import App

   # The following line creates an instance of the app, extracts the global API entry points,
   # and merges them into your Python global variables.
   app = App(globals=globals())

Alternatively, you can use the ``update_globals`` method of the ``App`` class to update the global
variables:

.. code:: python

   from ansys.mechanical.core import App

   app = App()
   app.update_globals(globals())

Some enum types are available when scripting inside of Mechanical, such as ``SelectionTypeEnum``
or ``LoadDefineBy``. Because these number in the thousands, by default, these enums are
included in these global variables. To avoid including them, set the second argument of
``update_globals`` to False. This option is only available for the ``update_globals`` method,
not for the ``globals`` argument of the ``App`` class:

.. code:: python

   from ansys.mechanical.core import App

   app = App()
   app.update_globals(globals(), False)
