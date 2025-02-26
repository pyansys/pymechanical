# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

""" .. _ref_embedding_remote:

Remote & Embedding Example
--------------------------
This code, which uses the same example, first demonstrates how to use
a remote session and then demonstrates how to use an embedding instance.

"""

###############################################################################
# --------------
# Remote Session
# --------------


###############################################################################
# Download required files
# ~~~~~~~~~~~~~~~~~~~~~~~
# Download the required files. Print the file paths for the geometry file and
# script file.

import os

from ansys.mechanical.core import launch_mechanical
from ansys.mechanical.core.examples import download_file

geometry_path = download_file("Valve.pmdb", "pymechanical", "embedding")
print(f"Downloaded the geometry file to: {geometry_path}")

script_file_path = download_file("remote_script.py", "pymechanical", "embedding")
print(f"Downloaded the script file to: {script_file_path}")


###############################################################################
#
# Launch Mechanical
# ~~~~~~~~~~~~~~~~~
# Launch a new Mechanical session in batch, setting ``cleanup_on_exit`` to
# ``False``. To close this Mechanical session when finished, this example
# must call  the ``mechanical.exit()`` method.

import os

from ansys.mechanical.core import launch_mechanical

# Launch mechanical
mechanical = launch_mechanical(batch=True, loglevel="DEBUG")
print(mechanical)


###############################################################################
# Initialize variable for workflow
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set the ``part_file_path`` variable on the server for later use.
# Make this variable compatible for Windows, Linux, and Docker containers.

project_directory = mechanical.project_directory
print(f"project directory = {project_directory}")

# Upload the file to the project directory.
mechanical.upload(file_name=geometry_path, file_location_destination=project_directory)

# Build the path relative to project directory.
base_name = os.path.basename(geometry_path)
combined_path = os.path.join(project_directory, base_name)
part_file_path = combined_path.replace("\\", "\\\\")
mechanical.run_python_script(f"part_file_path='{part_file_path}'")

# Verify the path
result = mechanical.run_python_script("part_file_path")
print(f"part_file_path on server: {result}")


###############################################################################
# Run mechanical automation script
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run remote_script.py in the mechanical remote session.

mechanical.run_python_script_from_file(script_file_path)


###############################################################################
# Get list of generated files
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~

list_files = mechanical.list_files()
for file in list_files:
    print(file)


###############################################################################
# Write the file contents to console
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def write_file_contents_to_console(path, number_lines=-1):
    count = 1
    with open(path, "rt") as file:
        for line in file:
            if number_lines == -1 or count <= number_lines:
                print(line, end="")
                count = count + 1
            else:
                break


###############################################################################
# Download files back to local working directory
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

dest_dir = "download"
dest_dir = os.path.join(os.getcwd(), dest_dir)
for file in list_files:
    downloaded = mechanical.download(file, target_dir=dest_dir)
    if file.endswith(".out"):
        print("contents of ", downloaded, " : ")
        write_file_contents_to_console(downloaded[0], number_lines=-1)


###############################################################################
# Exit remote session
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Close the Mechanical instance.

mechanical.exit()

###############################################################################
# -----------------
# Embedded Instance
# -----------------


###############################################################################
# Download the geometry file
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# Download Valve.pmdb.

import os

import ansys.mechanical.core as mech
from ansys.mechanical.core.examples import download_file

geometry_path = download_file("Valve.pmdb", "pymechanical", "embedding")
print(f"Downloaded the geometry file to: {geometry_path}")


###############################################################################
# Embed Mechanical and set global variables
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Find the mechanical installation path & version.
# Open an embedded instance of Mechanical and set global variables.

app = mech.App()
globals().update(mech.global_variables(app))
print(app)


###############################################################################
# Add Static Analysis
# ~~~~~~~~~~~~~~~~~~~
# Add static analysis to the Model.

analysis = Model.AddStaticStructuralAnalysis()


###############################################################################
# Import geometry
# ~~~~~~~~~~~~~~~

geometry_file = geometry_path
geometry_import = Model.GeometryImportGroup.AddGeometryImport()
geometry_import_format = Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.Format.Automatic
geometry_import_preferences = Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences()
geometry_import_preferences.ProcessNamedSelections = True
geometry_import.Import(geometry_file, geometry_import_format, geometry_import_preferences)


###############################################################################
# Assign material
# ~~~~~~~~~~~~~~~

matAssignment = Model.Materials.AddMaterialAssignment()
tempSel = ExtAPI.SelectionManager.CreateSelectionInfo(
    Ansys.ACT.Interfaces.Common.SelectionTypeEnum.GeometryEntities
)
bodies = [
    body
    for body in ExtAPI.DataModel.Project.Model.Geometry.GetChildren(
        Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory.Body, True
    )
]
geobodies = [body.GetGeoBody() for body in bodies]
ids = System.Collections.Generic.List[System.Int32]()
[ids.Add(item.Id) for item in geobodies]
tempSel.Ids = ids
matAssignment.Location = tempSel
matAssignment.Material = "Structural Steel"


###############################################################################
# Define mesh settings
# ~~~~~~~~~~~~~~~~~~~~

mesh = Model.Mesh
mesh.ElementSize = Quantity("25 [mm]")
mesh.GenerateMesh()


###############################################################################
# Define boundary conditions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~

fixedSupport = analysis.AddFixedSupport()
fixedSupport.Location = ExtAPI.DataModel.GetObjectsByName("NSFixedSupportFaces")[0]

frictionlessSupport = analysis.AddFrictionlessSupport()
frictionlessSupport.Location = ExtAPI.DataModel.GetObjectsByName("NSFrictionlessSupportFaces")[0]

pressure = analysis.AddPressure()
pressure.Location = ExtAPI.DataModel.GetObjectsByName("NSInsideFaces")[0]

inputs_quantities = [Quantity("0 [s]"), Quantity("1 [s]")]
output_quantities = [Quantity("0 [Pa]"), Quantity("15 [MPa]")]

inputs_quantities_2 = System.Collections.Generic.List[Ansys.Core.Units.Quantity]()
[inputs_quantities_2.Add(item) for item in inputs_quantities]

output_quantities_2 = System.Collections.Generic.List[Ansys.Core.Units.Quantity]()
[output_quantities_2.Add(item) for item in output_quantities]

pressure.Magnitude.Inputs[0].DiscreteValues = inputs_quantities_2
pressure.Magnitude.Output.DiscreteValues = output_quantities_2


###############################################################################
# Solve model
# ~~~~~~~~~~~

Model.Solve()


###############################################################################
# Add results
# ~~~~~~~~~~~

solution = analysis.Solution
solution.AddTotalDeformation()
solution.AddEquivalentStress()
solution.EvaluateAllResults()


###############################################################################
# Save model
# ~~~~~~~~~~

project_directory = ExtAPI.DataModel.Project.ProjectDirectory
print(f"project directory = {project_directory}")
ExtAPI.DataModel.Project.SaveAs(os.path.join(project_directory, "file.mechdb"))


###############################################################################
# Export result values to a text file
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

fileExtension = r".txt"
results = solution.GetChildren(
    Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory.Result, True
)

for result in results:
    fileName = str(result.Name)
    print(f"filename: {fileName}")
    path = os.path.join(project_directory, fileName + fileExtension)
    print(path)
    result.ExportToTextFile(f"{path}")
    print("Exported Text file Contents", path)
    try:
        write_file_contents_to_console(path, number_lines=20)
    except:
        print(os.listdir(project_directory))

app.close()
