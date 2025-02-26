.. _ref_docker:

********************************
Using Mechanical through Docker
********************************
You can run Mechanical within a container on any operating system
using `Docker <https://www.docker.com/>`_ and connect to it with
PyMechanical.

Running Mechanical in a containerized environment like Docker or `Apptainer <http://apptainer.org/>`_
(formerly Singularity) is advantageous for several reasons, including:

- Ability to run in a consistent environment regardless of the host operating system
- Portability and ease of installation
- Large-scale cluster deployment using Kubernetes
- Genuine application isolation through containerization.


Install the Mechanical image
-----------------------------
There is a Docker image hosted in the `PyMechanical GitHub
<https://github.com/pyansys/pymechanical/pkgs/container/pymechanical%2Fmechanical>`_ repository that you
can download using your GitHub credentials.

Assuming that you have Docker installed, you can authorize Docker to access
this repository using a GitHub personal access token with ``packages read``
permissions. For more information, see `Creating a personal access token
<https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token>`_.

Save this token to a file with:

.. code::

   echo XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX > GH_TOKEN.txt


This lets you send the token to Docker without leaving the token value
in your history.

Next, authorize Docker to access this repository with:

.. code::

    GH_USERNAME=<my-github-username>
    cat GH_TOKEN.txt | docker login ghcr.io -u $GH_USERNAME --password-stdin


You can now launch Mechanical directly from Docker with a short script or
directly from the command line. Because this image does not contain a license
server, you must enter in the IP address of your license server in the
``LICENSE_SERVER`` environment variable.

Launch Mechanical with:

.. code::

    LICENSE_SERVER=1055@XXX.XXX.XXX.XXX
    VERSION=v23.1.0

    IMAGE=ghcr.io/pyansys/pymechanical/mechanical:$VERSION
    docker run -e ANSYSLMD_LICENSE_FILE=$LICENSE_SERVER -p ip:10000:10000 $IMAGE


Note that port ``10000``, which is local to the container, is mapped to
port ``10000`` on the host. This makes it possible to use different
port mappings to launch multiple instances of Mechanical.

As Mechanical starts, you can see status information:

.. code::

    Starting the grpc server at port 10000
    Started the grpc server at port 10000


Connect to the Mechanical container
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You can now connect to the Mechanical container with:

.. code:: python

    >>> from ansys.mechanical.core import Mechanical
    >>> mechanical = Mechanical()

If you mapped to any port other than ``10000``, you would specify this port when
connecting to Mechanical:

.. code:: python

    >>> mechanical = Mechanical(port=<my-port>)

Verify your connection with:

.. code:: python

    >>> print(mechanical)

    Ansys Mechanical [Ansys Mechanical Enterprise]
    Product Version:231
    Software build date:Wednesday, August 10, 2022 4:28:15 PM

Additional considerations
-------------------------
You can provide additional command line parameters to Mechanical by appending them
to the Docker command. For example, this code shows how you pass feature flags:

.. code::

    IMAGE=ghcr.io/pyansys/pymechanical/mechanical:$VERSION
    docker run -e ANSYSLMD_LICENSE_FILE=$LICENSE_SERVER -p 10000:10000 $IMAGE -featureflags mechanical.material.import;

For additional command line arguments, see the *Scripting in Mechanical Guide* in the
`ANSYS Help <https://ansyshelp.ansys.com>`_.
