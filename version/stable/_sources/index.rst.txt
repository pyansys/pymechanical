
.. title:: PyMechanical


.. image:: /_static/logo/pymechanical-logo-light.png
   :class: only-light
   :alt: PyMechanical Logo Light
   :width: 580px
   :align: center

.. image:: /_static/logo/pymechanical-logo-dark.png
   :class: only-dark
   :alt: PyMechanical Logo Dark
   :width: 580px
   :align: center


Python API to interact with `Ansys Mechanical`_ (FEA software for structural engineering) from **2023R2** and later versions.

.. grid:: 3


    .. grid-item-card:: Getting started :fa:`person-running`
        :padding: 2 2 2 2
        :link: getting_started/index
        :link-type: doc

        Learn how to install and use PyMechanical. Explains architecture
        and background.

        :bdg-primary-line:`Install` :bdg-primary-line:`Architecture` :bdg-primary-line:`Docker`

    .. grid-item-card:: Examples :fa:`scroll`
        :padding: 2 2 2 2
        :link: examples/index
        :link-type: doc

        Dive into examples created using PyMechanical.

        :bdg-primary-line:`Basic` :bdg-primary-line:`Technology-showcase` :bdg-primary-line:`Tips`

    .. grid-item-card:: API reference :fa:`book-bookmark`
        :padding: 2 2 2 2
        :link: api/index
        :link-type: doc

        Understand PyMechanical API endpoints and their capabilities

        :bdg-primary-line:`Classes` :bdg-primary-line:`Methods` :bdg-primary-line:`Error handling`

    .. grid-item-card:: Embedding instance :fa:`window-maximize`
        :padding: 2 2 2 2
        :link: user_guide_embedding/index
        :link-type: doc

        A Mechanical object implemented in .NET is directly loaded into Python memory.

        :bdg-primary-line:`Python.NET` :bdg-primary-line:`no-GUI`

    .. grid-item-card:: Remote session :fa:`window-restore`
        :padding: 2 2 2 2
        :link: user_guide_session/index
        :link-type: doc

        Using gRPC, Mechanical operates as a server, ready to respond to client requests.

        :bdg-primary-line:`gRPC` :bdg-primary-line:`GUI`


    .. grid-item-card:: Mechanical scripting :fa:`code`
        :padding: 2 2 2 2
        :link: user_guide_scripting/index
        :link-type: doc

        Overview of Ansys Mechanical scripting.

        :bdg-primary-line:`ACT` :bdg-primary-line:`Threading`

    .. grid-item-card:: FAQs :fa:`fa-solid fa-circle-question`
        :padding: 2 2 2 2
        :link: faq
        :link-type: doc

        Frequently asked questions and their answers.

        :bdg-primary-line:`How` :bdg-primary-line:`Why` :bdg-primary-line:`What`

    .. grid-item-card:: Known issues and limitations :fa:`fa-solid fa-bug`
        :padding: 2 2 2 2
        :link: kil/index
        :link-type: doc

        Issues and limitations on both PyMechanical and Mechanical.

        :bdg-primary-line:`23R2` :bdg-primary-line:`24R1` :bdg-primary-line:`24R2` :bdg-primary-line:`25R1`

    .. grid-item-card:: Contribute :fa:`people-group`
        :padding: 2 2 2 2
        :link: contributing
        :link-type: doc

        Learn how to contribute to the PyMechanical codebase
        or documentation.

        :bdg-primary-line:`Test` :bdg-primary-line:`Documentation` :bdg-primary-line:`Issues`


.. toctree::
   :hidden:
   :maxdepth: 3

   getting_started/index
   examples/index
   user_guide_session/index
   user_guide_embedding/index
   user_guide_scripting/index
   api/index
   contributing
   kil/index
   faq
   changelog