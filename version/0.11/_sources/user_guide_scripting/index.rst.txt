.. _ref_user_guide_scripting:

Mechanical scripting
====================

This section provides an overview of Mechanical scripting.

..
   This toctreemust be a top-level index to get it to show up in
   pydata_sphinx_theme.

.. toctree::
   :maxdepth: 1
   :hidden:

   self
   threading

Overview
--------

You could already perform scripting of Mechanical with Python from inside
Mechanical. PyMechanical leverages the same APIs but allows you to run your
automation from outside Mechanical.

For comprehensive information on these APIs, refer to the following documentation:

PyMechanical documentation:

* `Mechanical API Documentation`_ - Lists Mechanical APIs that can be used with PyMechanical.

Developer portal:

* `Mechanical scripting interface APIs`_ - Contains the same information as the `Mechanical API Documentation`_ but is located on the developer portal.

ACT API Reference Guide:

* `ACT API Reference Guide`_ - Provides descriptions of the objects, methods, and properties for all namespaces.

Recording
---------

Mechanical supports some level of recording. When you initiate an action from the user
interface (UI), the UI determines what API to run, executes this API, and prints it in the **Mechanical Scripting
View**. Examples of these actions are assigning selections to scoping, changing values in
the details view, and renaming an object in the **Outline**. In the following animated example,
a **Fixed Support** and a **Pressure** are added to the **Outline**.

.. figure:: ../images/gmech_scripting_recording.gif

Mechanical entities
-------------------

Mechanical has an extensive set of entities that represent all the functionality provided
by Mechanical. Here are descriptions of the entities at Mechanical's core:

* CAD: CAD entities, which are usually imported from a CAD application
* Mesh: The discretized geometry that is appropriate for Mechanical's solvers
* Materials: Engineering material models that come from **Engineering Data**, which is a subsystem of Ansys Workbench
* Objects: The entities in the **Outline** that represent the model, analyses, solutions, and results
* Graphics: The 3D graphics engine that renders data from Mechanical visually and can export images and animations
* Solvers: The solver integrations that allow a Mechanical model to be used to run a specific solver
* Post: The engine that computes useful engineering results from solver runs
* Extensions: Plugins or extensions defined externally from Mechanical that extend Mechanical

There is some overlap between these entities. For instance, the CAD data is represented visually in the 3D graphics
engine but also has representation in the **Outline**. The raw CAD data, which includes the tessellations used to render the
graphics and all the data needed to define vertices, edges, faces, volumes, and parts is collectively considered ``GeoData``.
You may interact with these bodies and parts in the **Outline**, assigning materials, thickness, and other data that does
not come from CAD entities. This is considered ``Geometry``. As a result, the API entry points for ``GeoData`` and ``Geometry``
are different.

The same is true for ``Mesh``. There is a representation in the **Outline** that contains the settings
used to generate the mesh and statistics about the mesh. Then, there is ``MeshData``, which is the actual nodes and
elements in the mesh. These have distinct API entry points.

Executing a sequence of APIs can sometimes be slow because Mechanical may perform background tasks each time any of its
entities are created, updated, or deleted. Mechanical scripting has a ``Transaction`` class for deferring many of these
tasks until after a block of commands are run. Here is an example:

.. code:: python

   with Transaction():
       for obj in Tree:
           obj.Name = obj.Name + " suffix"

API entry points
----------------

When running scripts inside of Mechanical, you can access the APIs via these entry points:

* ``ExtAPI``: Entry point for all APIs
* ``DataModel``: Entry point to access CAD and mesh entities and objects from the **Outline**
* ``Model``: The Model object from the **Outline**
* ``Tree``: The **Outline**
* ``Graphics``: The 3D graphics engine

You also have access to several types and namespaces that are included in the scripting scope but are not available
from those entry points.
