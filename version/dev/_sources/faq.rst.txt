.. _faq:

Frequently asked questions
==========================

This section provides answers to frequently asked questions.

.. dropdown:: How do you report issues?
    :animate: fade-in-slide-down

    You can report issues with PyMechanical, such as bugs, feature requests,
    and documentation errors, on the PyMechanical repository's `Issues
    <https://github.com/ansys/PyMechanical/issues>`_ page.

    If you want to ask more open-ended questions or are seeking advice
    from experts in the community, you can post on this repository's
    `Discussions <https://github.com/ansys/pymechanical/discussions>`_ page.

.. dropdown:: How is PyMechanical positioned with respect to other related Ansys tools?
    :animate: fade-in-slide-down

    When you want to automate or extend Ansys Mechanical, you should
    consider these tools:

    * ACT in Mechanical
    * Scripting in Mechanical
    * PyMechanical

    Although all of these tools work best in interactive mode, there is increasing support
    for batch mode. You can use the first two tools from either Ansys Workbench or from
    standalone Mechanical.

    **ACT in Mechanical**

    In Mechanical, ACT is a customization framework. When specific features are missing,
    you can add them using ACT. Of course, some of those missing features might be
    automations or scripts of existing features. But, in many cases, they can be new
    capabilities, such as extensions to Mechanical's data model, the ability to connect
    to callbacks, and even integrations of external solvers.

    **Scripting in Mechanical**

    The Python scripting capability in Mechanical was born out of the same development
    that brought ACT to Mechanical. This tool provides the same APIs as those used for
    PyMechanical but can only be run by Mechanical. While they use IronPython 2.7 by
    default, recent Mechanical versions provide a feature flag for scripting in CPython 3.x.
    Mechanical's intuitive user interface for scripting, the **Mechanical Scripting View**,
    provides script recording, autocomplete, and a snippet library. However, it is possible
    to use this tool in batch mode without the Mechanical user interface.

    **PyMechanical**

    PyMechanical allows you to write Python scripts outside of Mechanical, with tight
    integration with other open source modules and Ansys products. With this tool, you
    bring your own Python environment, which may contain other modules and tools. There is
    no dependency on opening the Mechanical user interface.

.. dropdown:: What is the relationship with Ansys Workbench?
    :animate: fade-in-slide-down

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

.. dropdown:: How do you restart a script?
    :animate: fade-in-slide-down

    If you have trouble terminating a simulation, you do not have to close Python, reopen it, and
    clear all previous data, such as the mesh, using this code:

    .. code:: python

        import sys

        sys.modules[__name__].__dict__.clear()

    Simply exiting Python should clear the solution within Python. This is because
    stopping the original process means that nothing should be present in
    a new process.

    The way that you clear all data from Mechanical in PyMechanical depends on if
    Mechanical is a remote session or embedded.

    - If Mechanical is a remote session, use either the
      `Mechanical.clear() <../api/ansys/mechanical/core/mechanical/Mechanical.html#Mechanical.clear>`_
      method or exit and restart Mechanical.
    - If Mechanical is embedded, use the
      `app.new() <../api/ansys/mechanical/core/embedding/app/App.html#App.new>`_
      method.

.. dropdown:: How do you check if a license is active with PyMechanical?
    :animate: fade-in-slide-down

    Information about Mechanical can be printed with remote and embedding mode:

    .. tab-set::

        .. tab-item:: Remote

            .. code-block:: python

                import ansys.mechanical.core as pymechanical

                mechanical = pymechanical.launch_mechanical()
                print(mechanical)

        .. tab-item:: Embedding

            .. code-block:: python

                import ansys.mechanical.core as pymechanical

                app = pymechanical.App()
                print(app)

    The output from the above code will indicate the license being used inside the brackets, next to *Ansys Mechanical*.
    If PyMechanical is unable to retrieve any license, the field will be left blank.

    .. tab-set::

        .. tab-item:: With License

            .. code-block:: shell

                Ansys Mechanical [Ansys Mechanical Enterprise]
                Product Version:251
                Software build date: 11/27/2024 09:34:44

        .. tab-item:: Without License

            .. code-block:: shell

                Ansys Mechanical []
                Product Version:251
                Software build date: 11/27/2024 09:34:44

    Alternatively, once the ``app`` is created ``readonly`` method can be used to see if license is active.
    If license is not checked out then it is in read only mode.


.. dropdown:: Why do I get ``mechanical-env`` exception in Linux?
    :animate: fade-in-slide-down

    To use the embedded instance on Linux, ``mechanical-env`` should be invoked before
    starting the Python shell or running a Python script.

    .. code-block:: shell

        $ mechanical-env python
        >>> import ansys.mechanical.core as mech
        >>> app=mech.App(version=251)

    or

    .. code-block:: shell

        $ mechanical-env python test.py



