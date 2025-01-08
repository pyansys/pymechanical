.. _ref_embedding_user_guide_new_features:

New features
============

This page showcases new features of the embedding instance of PyMechanical.

.. contents::
   :backlinks: none

The ``launch_gui`` function
---------------------------

The `launch_gui() <../api/ansys/mechanical/core/embedding/launch_gui/index.html>`_ function
graphically launches the current state of the embedded instance the
`App <../api/ansys/mechanical/core/embedding/app/App.html>`_ has been saved.

Process
~~~~~~~

#. Save the active mechdb file.
#. Save a new mechdb file with a temporary name.
#. Open the original mechdb file from step 1.
#. Launch the GUI for the mechdb file with a temporary name from step 2.
#. Determine what to do with the temporary mechdb file.

   * Delete the temporary file (default option).
      * Remove the temporary mechdb file and folder when the GUI is closed.

   * Keep the temporary file.
      * Let the user know that the GUI mechdb will not automatically get cleaned up.

This setup automatically deletes the temporary mechdb file when the GUI is closed:

.. code:: python

    import ansys.mechanical.core as pymechanical

    app = pymechanical.App()
    app.save()
    app.launch_gui()

This setup does not delete the temporary mechdb file when the GUI is closed:

.. code:: python

    import ansys.mechanical.core as pymechanical

    app = pymechanical.App()
    app.save()
    app.launch_gui(delete_tmp_on_close=False)


The ``ansys-mechanical-ideconfig`` command
------------------------------------------

The ``ansys-mechanical-ideconfig`` command prints the settings that are necessary for
autocomplete to work with ``ansys-mechanical-stubs``. This command takes in three arguments:

* ``--ide``: Currently only accepts ``vscode`` as a valid IDE.
* ``--target``: The settings for autocomplete can be updated for either the workspace or user in VS Code. Because of this, the valid inputs for this argument are ``user`` or ``workspace``.
* ``--revision``: The Mechanical revision number, for example "242". If the revision number is not supplied, ``ansys-tools-path`` will retrieve the Mechanical version from your system.

**Note**: This setting configuration assumes ``ansys-mechanical-stubs`` is installed on your system.

Process
~~~~~~~

#. If the IDE is not ``vscode``, an exception is thrown.
#. Locate the ``settings.json`` file for the ``user`` or ``workspace``

   * The user ``settings.json`` location:
      .. tab-set::

        .. tab-item:: Windows

            .. code-block::

                %APPDATA%/Code/User/settings.json

        .. tab-item:: Linux

            .. code-block::

                $HOME/.config/Code/User/settings.json


   * The workspace ``settings.json`` location is at the root of the repository or project:
       .. code-block::

           {project_directory}/pymechanical/.vscode/settings.json

#. Find the location of the ``ansys-mechanical-stubs`` package depending on virtual environment usage.
    .. tab-set::

        .. tab-item:: Windows

            .. tab-set::

                .. tab-item:: Virtual environment

                    .. code-block:: text

                        {project_directory}\\.venv\\Lib\\site-packages\\ansys\\mechanical\\stubs\\v{revision}

                .. tab-item:: No virtual environment

                    .. code-block:: text

                        C:\\Users\\{username}\\AppData\\Local\\Programs\\Python\\Python{version}\\Lib\\site-packages\\ansys\\mechanical\\stubs\\v{revision}

        .. tab-item:: Linux

            .. tab-set::

                .. tab-item:: Virtual environment

                    .. code-block:: text

                        {project_directory}/.venv/lib/python{version}/site-packages/ansys/mechanical/stubs/v{revision}

                .. tab-item:: No virtual environment

                    .. code-block:: text

                        $HOME/.local/lib/python{version}/site-packages/ansys/mechanical/stubs/v{version}

#. Print out the autocomplete settings depending on settings type and virtual environment usage.
    .. tab-set::

        .. tab-item:: Windows

            .. tab-set::

                .. tab-item:: User settings

                    .. code-block:: text

                        Update C:\Users\{username}\AppData\Roaming\Code\User\settings.json with the following information:

                        {
                            "python.autoComplete.extraPaths": [
                                "{project_directory}\\.venv\\Lib\\site-packages\\ansys\\mechanical\\stubs\\v{revision}"
                            ],
                            "python.analysis.extraPaths": [
                                "{project_directory}\\.venv\\Lib\\site-packages\\ansys\\mechanical\\stubs\\v{revision}"
                            ]
                        }

                .. tab-item:: Workspace settings

                    .. code-block:: text

                        Update {project_directory}\.vscode\settings.json with the following information:

                        Note: Please ensure the .vscode folder is in the root of your project or repository.

                        {
                            "python.autoComplete.extraPaths": [
                                "{project_directory}\\.venv\\Lib\\site-packages\\ansys\\mechanical\\stubs\\v{revision}"
                            ],
                            "python.analysis.extraPaths": [
                                "{project_directory}\\.venv\\Lib\\site-packages\\ansys\\mechanical\\stubs\\v{revision}"
                            ]
                        }

        .. tab-item:: Linux

            .. tab-set::

                .. tab-item:: User settings

                    .. code-block:: text

                        Update /home/{username}/.config/Code/User/settings.json with the following information:

                        {
                            "python.autoComplete.extraPaths": [
                                "{project_directory}/.venv/lib/python{version}/site-packages/ansys/mechanical/stubs/v{revision}"
                            ],
                            "python.analysis.extraPaths": [
                                "{project_directory}/.venv/lib/python{version}/site-packages/ansys/mechanical/stubs/v{revision}"
                            ]
                        }

                .. tab-item:: Workspace settings

                    .. code-block:: text

                        Update {project_directory}/.vscode/settings.json with the following information:

                        Note: Please ensure the .vscode folder is in the root of your project or repository.

                        {
                            "python.autoComplete.extraPaths": [
                                "{project_directory}/.venv/lib/python{version}/site-packages/ansys/mechanical/stubs/v{revision}"
                            ],
                            "python.analysis.extraPaths": [
                                "{project_directory}/.venv/lib/python{version}/site-packages/ansys/mechanical/stubs/v{revision}"
                            ]
                        }
