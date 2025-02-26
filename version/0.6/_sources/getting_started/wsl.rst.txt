  .. _ref_guide_wsl:


PyAnsys libraries in the Windows Subsystem for Linux and Docker
###############################################################

This page shows how you use a PyAnsys library, more specifically PyMechanical,
in the Windows Subsystem for Linux (WSL). WSL is a compatibility layer for
running Linux binary executables natively on Windows 10, Windows 11, and
Windows Server 2019. For more information, see:

- Wikipedia's `Windows Subsystem for Linux`_
- Microsoft's `What is the Windows Subsystem for Linux?`_


.. _Windows Subsystem for Linux: https://en.wikipedia.org/wiki/Windows_Subsystem_for_Linux
.. _What is the Windows Subsystem for Linux?: https://docs.microsoft.com/en-us/windows/wsl/about

This page walks you through the installation of WSL on Windows and then
shows how to use it together with Mechanical, PyMechanical, and Docker.

.. warning::
   These instructions have not been fully tested with a VPN connection. If you
   experience any problems connecting WSL to the internet, try to disconnect from the VPN.


Running PyMechanical on WSL
***************************

Install WSL
============

Install WSL by following the instructions in Microsoft's `Install Linux on Windows with WSL`_.

.. _Install Linux on Windows with WSL: https://docs.microsoft.com/en-us/windows/wsl/install/

There are two versions of WSL, WSL1 and WSL2. Because WSL2 provides many improvements
over WSL1, you should upgrade to and use WSL2.


Install the CentOS7 WSL distribution
=====================================

When working with PyAnsys libraries, you should use the CentOS7 WSL distribution.

You can install this distribution using an unofficial WSL distribution from
`<https://github.com/wsldl-pg/CentWSL/>`_ or
`<https://github.com/mishamosher/CentOS-WSL/>`_ .

Optionally, you can try Ubuntu in the context of WSL.


Install Ansys products in WSL CentOS7
=====================================

Prerequisites
--------------
If you are using CentOS 7, before installing Mechanical, you must install some
required libraries:

Install Ansys products
-----------------------

To install ANSYS products in WSL:

1. Download the Ansys Structures image for the `Current  Release
   <https://download.ansys.com/Current%20Release>`_ from the Ansys Customer Portal.
   
   If you are  downloading the image on a Windows machine, you should later copy the image to
   WSL.

2. Extract the compressed source code file (tar.gz) with:

   .. code:: bash

       tar xvzf STRUCTURES_2022R2_LINX64.tgz


3. To install Mechanical, go into the folder where the files have been extracted
   and run this command:

   .. code:: bash

       sudo ./INSTALL -silent -install_dir /usr/ansys_inc/ -mechapdl

   where:

   - ``-silent`` : Initiates a silent installation, which means no GUI is shown.
   - ``-install_dir /path/`` : Specifies the directory to install the product or
     license manager to. If you want to install to the default location, you can
     omit the ``-install_dir`` argument. The default location is ``/ansys_inc``
     if the symbolic link is set. Otherwise, it defaults to ``/usr/ansys_inc``.
   - ``-<product_flag>`` : Specifies the one or more products to install.
     If you omit this argument, all products are installed. A list of valid
     values for the ``product_flags`` argument is available in Chapter 6 of The
     *ANSYS Inc. Installation Guide*. In the preceding example for Mechanical, you
     only need to specify the ``-mechapdl`` flag.

After installing Mechanical directly in ``/ansys_inc`` or in ``/usr/ansys_inc``,
create a symbolic link with:

.. code:: bash

    sudo ln -s /usr/ansys_inc /ansys_inc

By default, PyMechanical expects the Mechanical executable to be in
``/usr/ansys_inc``. Whether you install it there or not, you should
use a symbolic link to link that directory to your Ansys installation
directory (``/*/ansys_inc``).


Post-installation setup
=======================

Open ports
----------

**Theory:** You should open the ports ``1055`` and ``2325`` for license server
communication in the **Windows Control Panel**. For the steps to set advanced
Windows firewall options, see `How to open port in Windows 10 Firewall?
<https://answers.microsoft.com/en-us/windows/forum/all/how-to-open-port-in-windows-10-firewall/f38f67c8-23e8-459d-9552-c1b94cca579a/>`_

**Reality:** This works if you want to run a Docker image using a WSL Linux image
to host that Docker image. The Docker image successfully communicates with the Windows
License Server using these ports if you use the ``'-p'`` flag when running the
Docker image with these ports open.  See `Running Mechanical on a local Docker
image`_.

If you want to run Mechanical in the CentOS7 image and use the Windows License
Server, opening the ports might not work properly because the Windows firewall
seems to block all traffic coming from WSL.  For security purposes, you should
still try to open ports ``1055`` and ``2325`` in the Windows firewall and check if your
Mechanical installation can communicate with the Windows hosts. If you are having
problems after setting the firewall rules, you might have to disable the Windows
firewall for the WSL ethernet's virtual interface. Because this might pose some
unknown side effects and security risks, do so with caution. For more information,
see `Disable the firewall on the WSL ethernet`_.


Create an environmental variable in WSL that points to the license server on the Windows host
---------------------------------------------------------------------------------------------

The IP address for the Windows host is given in the WSL ``/etc/hosts`` file before the name
``host.docker.internal``.

.. note::
   This ``host.docker.internal`` definition might not be available if Docker is
   not installed.

Here is an example of the WSL ``/etc/hosts`` file:

.. code-block:: bash
   :emphasize-lines: 11

   # This file is automatically generated by WSL.
   # To stop automatic generation of this file, add the following lines to the
   # ``/etc/wsl.conf`` file:
   #
   # [network]
   # generateHosts = false
   #
   127.0.0.1       localhost
   127.0.1.1       AAPDDqVK5WqNLve.win.ansys.com   AAPDDqVK5WqNLve

   192.168.0.12    host.docker.internal
   192.168.0.12    gateway.docker.internal
   127.0.0.1       kubernetes.docker.internal

   # The following lines are desirable for IPv6 capable hosts.
   ::1     ip6-localhost ip6-loopback
   fe00::0 ip6-localnet
   ff00::0 ip6-mcastprefix
   ff02::1 ip6-allnodes
   ff02::2 ip6-allrouters


You can add the next lines to your WSL ``~/.bashrc`` file to create an
environment variable with the IP address:

.. code:: bash

    winhostIP=$(grep -m 1 host.docker.internal /etc/hosts | awk '{print $1}')
    export ANSYSLMD_LICENSE_FILE=1055@$winhostIP


Running Mechanical on a local Docker image
******************************************

To run a Docker image, you must follow all steps in `Running PyMechanical on WSL`_.

Additionally, run a Docker image of PyMechanical with:

.. code:: pwsh

    docker run -e ANSYSLMD_LICENSE_FILE=1055@host.docker.internal --restart always --name mechanical -p 10000:10000 ghcr.io/pyansys/pymechanical/mechanical > log.txt

Successive runs should restart the container. Or, delete the container and rerun it with:

.. code:: pwsh

    docker stop mechanical
    docker container prune

    docker run -e ANSYSLMD_LICENSE_FILE=1055@host.docker.internal --restart always --name mechanical -p 10001:10000 ghcr.io/pyansys/pymechanical/mechanical > log.txt


This creates a ``log.txt``file in your current directory location.


.. note:: Ensure that your port ``10001`` is open in your firewall.

You should use a script (batch ``'.bat'`` or PowerShell ``'.ps'``) file
to run the preceding commands all at once.

Notice that the WSL internal gRPC port (``10000``) is being mapped to a
different Windows host port (``10001``) to avoid ports conflicts.

This image is ready to be connected to from WSL or the Windows host. However,
you should specify the IP address and port using one of the following methods.

**Method 1**

.. code:: python

    from ansys.mechanical.core import launch_mechanical

    mechanical = launch_mechanical(ip='127.0.0.1', port=10001, start_instance=False)

**Method 2**

.. code:: python

    from ansys.mechanical.core import Mechanical

    mechanical = Mechanical(ip='127.0.0.1', port=10001)

**Method 3**

You can use specify the IP address and port using environment variables that are read when
the Mechanical instance is launched.

.. code:: bash

    export PYMECHANICAL_START_INSTANCE=False
    export pymechanical_port=10001
    export pymechanical_ip=127.0.0.1


Notes
=====

IP addresses
============

The IP address ``127.0.0.1`` specified in `Running Mechanical on a local Docker image`_ is
the IP address of WSL CentOS from the WSL perspective, whereas the IP address for the Windows
host is typically ``127.0.1.1``.

Docker builds the PyMechanical images using the WSL distribution as the base. Hence, PyMechanical
is running on a Linux WSL distribution, which is running on a Windows host. Because the Docker image
shares resources with WSL, it also shares the internal IP address with the WSL distribution.


Ansys installation flags
========================

To obtain license server information, use one of the following methods to access the ``INSTALL`` file
and then inspect the last few lines.

**Method 1**

.. code:: bash

    ./INSTALL --help

**Method 2**

.. code:: bash

    cat ./INSTALL


``-licserverinfo``
------------------

The ``-licserverinfo`` argument specifies information that the client for the license server uses.
This argument is valid only in conjunction with a silent installation (INSTALL).

**Single license server**

The format for a single license server is:

.. code:: bash

   -licserverinfo LI_port_number:FLEXlm_port_number:hostname

Here is an example:

.. code:: bash

   ./INSTALL -silent -install_dir /ansys_inc/ -mechapdl -licserverinfo 2325:1055:winhostIP

**Three license servers**

The format for three license servers is:

.. code:: bash

   -licserverinfo LI_port_number:FLEXlm_port_number:hostname1,hostname2,hostname3

Here is an example:

.. code:: bash

   ./INSTALL -silent -install_dir /ansys_inc/ -mechapdl -licserverinfo 2325:1055:abc,def,xyz


``-lang``
---------

The ``-lang`` argument specifies the language to use for the installation of the product.


``-productfile``
----------------
You can specify an ```options``` file that lists the products that you want to
install. When you do so, you must use the ``-productfile`` argument to specify the
full path to this file.


IP addresses in WSL and the Windows host
========================================

**Theory:** You should be able to access the Windows host using the IP address
specified in the WSL ``/etc/hosts`` file. This IP address is typically ``127.0.1.1``.
This means that the local WSL IP address is ``127.0.0.1``.

**Reality:** It is almost impossible to use the IP address ``127.0.1.1`` to
connect to the Windows host. However, it is possible to use the ``host.docker.internal``
hostname in the same WSL ``/etc/hosts`` file. This is an IP address that is
randomly allocated, which is an issue when you define the license server. However,
updating the ``.bashrc`` file as mentioned earlier resolves this issue.



Disable the firewall on the WSL ethernet
========================================

There are two methods for disabling the firewall on the WSL ethernet.

**Method 1**

This method shows a notification:

.. code:: pwsh

    Set-NetFirewallProfile -DisabledInterfaceAliases "vEthernet (WSL)"

**Method 2**

This method does not show a notification:

.. code:: pwsh

    powershell.exe -Command "Set-NetFirewallProfile -DisabledInterfaceAliases \"vEthernet (WSL)\""


On Windows 10, you can use the `wsl-windows-toolbar-launcher <https://github.com/cascadium/wsl-windows-toolbar-launcher#firewall-rules/>`_
package to launching Linux native applications directly from Windows
with the standard Windows toolbar. Because the toolbar in Windows 11 differs, the README
file for this package explains how to run Microsoft's `PowerToys <https://github.com/microsoft/PowerToys>`_
package instead.

Port forwarding on Windows 10
=============================


Link ports between WSL and Windows
----------------------------------

.. code:: pwsh

    netsh interface portproxy add v4tov4 listenport=1055 listenaddress=0.0.0.0 connectport=1055 connectaddress=XXX.XX.XX.XX


View all forwards
-----------------
You can use this PowerShell command to view all forwards:

.. code:: pwsh

    netsh interface portproxy show v4tov4


Delete port forwarding
----------------------

.. code:: pwsh

    netsh interface portproxy delete v4tov4 listenport=1055 listenaddres=0.0.0.0 protocol=tcp


Reset Windows network adapters
==============================

.. code:: pwsh

    netsh int ip reset all
    netsh winhttp reset proxy
    ipconfig /flushdns
    netsh winsock reset


Restart the WSL service
=======================

.. code:: pwsh

    Get-Service LxssManager | Restart-Service

Stop all processes with a given name
====================================

.. code:: pwsh

   Get-Process "AnsysWBU" | Stop-Process


Install ``xvfb`` in CentOS7
===========================

If you want to replicate the CI/CD behavior, ``xvfb`` must be installed. For more
information, see the ``.ci`` folder.

.. code:: bash

   yum install xorg-x11-server-Xvfb

