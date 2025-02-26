""".. _ref_example_03_show_object_properties:

Display properties for an object
---------------------------------

Using supplied files, this example shows how to display the properties
that you would see in an object's details view.

"""

###############################################################################
# Download required files
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Download the required files. Print the file path for the MECHDATA file.

import os

from ansys.mechanical.core import launch_mechanical
from ansys.mechanical.core.examples import download_file

mechdat_path = download_file("example_03_simple_bolt_new.mechdat", "pymechanical", "00_basic")
print(f"Downloaded the MECHDAT file to: {mechdat_path}")

###############################################################################
# Launch Mechanical
# ~~~~~~~~~~~~~~~~~
# Launch a new Mechanical session in batch, setting ``cleanup_on_exit`` to
# ``False``. To close this Mechanical session when finished, this example
# must call  the ``mechanical.exit()`` method.

mechanical = launch_mechanical(batch=True, cleanup_on_exit=False)
print(mechanical)

###############################################################################
# Initialize the variable needed for this workflow
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set the path for the ``mechdat_path`` variable for later use.
# Make this variable compatible for Windows, Linux, and Docker containers.

project_directory = mechanical.project_directory
print(f"project directory = {project_directory}")

# Upload the file to the project directory.
mechanical.upload(file_name=mechdat_path, file_location_destination=project_directory)

# Build the path relative to project directory.
base_name = os.path.basename(mechdat_path)
combined_path = os.path.join(project_directory, base_name)
mechdat_path_modified = combined_path.replace("\\", "\\\\")
mechanical.run_python_script(f"mechdat_path='{mechdat_path_modified}'")

# Verify the path.
result = mechanical.run_python_script(f"mechdat_path")
print(f"MECHDATA file is stored on the server at: {result}")

###################################################################################
# Execute the script
# ~~~~~~~~~~~~~~~~~~
# Run the Mechanical script to display the properties and their current values
# for the analysis object.

result = mechanical.run_python_script(
    """
import json

ExtAPI.DataModel.Project.Open(mechdat_path)

analysisSettings = Model.Analyses[0].AnalysisSettings
props = {}
if hasattr(analysisSettings,'VisibleProperties') != False:
    for prop in analysisSettings.VisibleProperties:
        props[prop.Caption] = prop.StringValue

json.dumps(props, indent=1)
"""
)
print(f"AnalysisSettings properties:\n{result}")

###################################################################################
# Clear the data
# ~~~~~~~~~~~~~~
# Clear the data so it isn't saved to the project.

mechanical.clear()

###########################################################
# Close Mechanical
# ~~~~~~~~~~~~~~~~
# Close the Mechanical instance.

mechanical.exit()
