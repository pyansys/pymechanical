.. _faq:

**************************
Frequently asked questions
**************************

How do you report issues?
-------------------------

You can report issues with PyMechanical, such as bugs, feature requests,
and documentation errors, on the repository's `Issues
<https://github.com/pyansys/PyMechanical/issues>`_ page.

If you want to ask more open-ended questions or are seeking advice
from experts in the community, post on the `Discussions
<https://github.com/pyansys/PyMechanical/discussions>`_ page.


What are the pros and cons of PyMechanical versus Mechanical ACT?
-----------------------------------------------------------------

Your scripting method depends on your pipeline and software approach.
Mechanical ACT is dependent on Ansys Workbench. You build extensions from within
the ACT App Builder and then run them from within Ansys Mechanical. If you
intend to vary parameters, you must use Ansys optiSLang and then
batch your solutions.

PyMechanical's main advantages over ACT are:

* Tight integration with Python tools and open source modules
  alongside Ansys software.
* Scripts are written in Python. ACT uses .NET, and you can call
  IronPython and potentially other tools available within Mechanical.
* Being outside of Mechanical means that you can call your application
  workflow without opening up the GUI for user interaction.
* PyMechanical is compatible with modern Python (Python 3), whereas
  ACT is only compatible with IronPython (Python 2).

The best approach depends on your workflow needs and how you would
like to develop software.


Why use PyMechanical over other Ansys products like Ansys Workbench?
--------------------------------------------------------------------

There are always tasks where one product is better than another.
Workbench is great tool to rapidly prototype, mesh, set
boundary conditions, and solve. A huge amount of Workbench development
effort has yielded many features that make it easy to run analyses.
However, Workbench is limited by its IronPython scripting. Additionally,
you cannot call multiple products at either a granular or high-level or
use Python packages such as ``numpy``, ``scipy``, ``pytorch``, and
``tensorflow``. PyMechanical ties all of these features in with
Mechanical, allowing you to have a fully parametric workflow that
leverages these machine learning tools.


How do you restart a script?
----------------------------
If you have trouble terminating a simulation, you do not have use the
following code to close Python, reopen it, and clear all previous data
such as the mesh.

.. code:: python

    import sys
    sys.modules[__name__].__dict__.clear()


Exiting Python should clear the solution within Python. This is because 
stopping the original process means that nothing should be in
a new process.

To clear all data from Mechanical, either use the
:func:`Mechanical.clear() <ansys.mechanical.core.Mechanical.clear>` method or exit and restart Mechanical.
