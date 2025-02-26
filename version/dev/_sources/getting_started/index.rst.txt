.. _ref_getting_started:

Getting started
===============

PyMechanical is part of the broader `PyAnsys <pyansys_>`_ initiative,
enabling the use of Ansys technologies directly from Python.
It allows users to integrate the Mechanical multiphysics solver
into custom applications via ``ansys-mechanical-core``, which provides a Python-friendly
interface to drive the software that facilitates the use of
:ref:`ref_user_guide_scripting` commands.


.. grid:: 1 2 2 2

    .. grid-item-card:: Installation guide
        :padding: 2 2 2 2
        :link: installation
        :link-type: doc
        :text-align: left

        Instructions to install and verify PyMechanical.

    .. grid-item-card:: Launching PyMechanical
        :padding: 2 2 2 2
        :link: running_mechanical
        :link-type: doc
        :text-align: left

        Steps to run PyMechanical.

    .. grid-item-card:: Docker setup
        :padding: 2 2 2 2
        :link: docker
        :link-type: doc
        :text-align: left

        How to run Mechanical Docker containers.

    .. grid-item-card:: Windows Subsystem for Linux (WSL)
        :padding: 2 2 2 2
        :link: wsl
        :link-type: doc
        :text-align: left

        Installing PyMechanical on Linux via WSL.


Background
----------

PyMechanical contains two interfaces: a remote session and an embedded instance.
For information on the application architecture of Mechanical and why there are
two Python interfaces, see :ref:`ref_architecture`.

.. toctree::
   :hidden:
   :maxdepth: 2

   installation
   running_mechanical
   docker
   wsl
   ../architecture
