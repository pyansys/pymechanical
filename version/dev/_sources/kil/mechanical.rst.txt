.. _ref_kil_mechanical:

Mechanical standalone
=====================

In addition to Standalone Mechanical known issues and limitations given below,
please refer

- `Mechanical API known issues and limitations`_.
- `ACT known issues and limitations`_.

Known issues and limitations
----------------------------

24R2
^^^^

- In Read Only mode, the application does not display error messages when the geometry is imported in batch mode.
- Section planes can not be added through batch mode.
- Mechanical is not thread safe.
- Spaceclaim geometry (.scdocx) can not be imported on Linux platform.
- On Linux based platforms, Ansys Motion and LSDYNA analysis support are limited.
- A fatal error currently exists when you are shutting down Mechanical on the
  Linux platform using Embedding (`#85 <https://github.com/ansys/pymechanical/issues/85>`_).

24R1
^^^^

- `Python libraries <https://mechanical.docs.pyansys.com/version/stable/user_guide_embedding/libraries.html>`_
  that are distributed with the installation of Mechanical does not work when there are syntax differences
  between IronPython and CPython (`#515 <https://github.com/ansys/pymechanical/issues/515>`_).
- Trace Import fails with PyMechanical Embedding when using ``python 3.10`` only.


