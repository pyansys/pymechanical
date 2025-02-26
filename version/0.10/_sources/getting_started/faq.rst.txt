.. _faq:

Frequently asked questions
==========================

This section provides answers to frequently asked questions.

How do you report issues?
-------------------------

You can report issues with PyMechanical, such as bugs, feature requests,
and documentation errors, on the PyMechanical repository's `Issues
<https://github.com/ansys/PyMechanical/issues>`_ page.

If you want to ask more open-ended questions or are seeking advice
from experts in the community, you can post on this repository's
`Discussions <https://github.com/ansys/pymechanical/discussions>`_ page.

How is PyMechanical positioned with respect to other related Ansys tools?
-------------------------------------------------------------------------

When you want to automate or extend Ansys Mechanical, you should
consider these tools:

* ACT in Mechanical
* Scripting in Mechanical
* PyMechanical

Although all of these tools work best in interactive mode, there is increasing support
for batch mode. You can use the first two tools from either Ansys Workbench or from
standalone Mechanical.

ACT in Mechanical
^^^^^^^^^^^^^^^^^

In Mechanical, ACT is a customization framework. When specific features are missing,
you can add them using ACT. Of course, some of those missing features might be
automations or scripts of existing features. But, in many cases, they can be new
capabilities, such as extensions to Mechanical's data model, the ability to connect
to callbacks, and even integrations of external solvers.

Scripting in Mechanical
^^^^^^^^^^^^^^^^^^^^^^^

The Python scripting capability in Mechanical was born out of the same development
that brought ACT to Mechanical. This tool provides the same APIs as those used for
PyMechanical but can only be run by Mechanical. While they use IronPython 2.7 by
default, recent Mechanical versions provide a feature flag for scripting in CPython 3.x.
Mechanical's intuitive user interface for scripting, the **Mechanical Scripting View**,
provides script recording, autocomplete, and a snippet library. However, it is possible
to use this tool in batch mode without the Mechanical user interface.

PyMechanical
^^^^^^^^^^^^

PyMechanical allows you to write Python scripts outside of Mechanical, with tight
integration with other open source modules and Ansys products. With this tool, you
bring your own Python environment, which may contain other modules and tools. There is
no dependency on opening the Mechanical user interface.

What is the relationship with Ansys Workbench?
----------------------------------------------

Ansys Workbench is a no-code environment to set up analysis systems that can be linked
together. It is part of the Ansys family of software tools for process automation and design
exploration. This family includes Ansys OptiSLang, which may be a more natural fit
for integration with PyMechanical. The most popular app within the Workbench environment is
Mechanical, and for many years, Workbench was the only environment you could run Mechanical from.

Because Workbench is a no-code environment, a lot of the complexity around managing data
transfer between Ansys apps and running parametric studies is hidden. PyMechanical and
PyAnsys libraries more broadly give you much more control over your process automation and design
exploration. However, eliminating Workbench means that you miss out on what it handled under
the hood.

How do you restart a script?
----------------------------

If you have trouble terminating a simulation, you do not have to close Python, reopen it, and
clear all previous data such as the mesh using this code:

.. code:: python

    import sys

    sys.modules[__name__].__dict__.clear()

Simply exiting Python should clear the solution within Python. This is because
stopping the original process means that nothing should be in present in
a new process.

The way that you clear all data from Mechanical in PyMechanical depends on if
Mechanical is a remote session or embedded.

- If Mechanical is a remote session, use either the
  :func:`Mechanical.clear() <ansys.mechanical.core.Mechanical.clear>`
  method or exit and restart Mechanical.
- If Mechanical is embedded, use the
  :func:`app.new() <ansys.mechanical.core.embedding.Application.new>`
  method.
