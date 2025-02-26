""".. _ref_example_01_simple_structural_solve:

Static structural analysis
--------------------------

Using supplied files, this example shows how to insert a static structural
analysis into a new Mechanical session and execute a sequence of Python scripting
commands that define and solve the analysis. Deformation results are then reported.

"""

###############################################################################
# Download required files
# ~~~~~~~~~~~~~~~~~~~~~~~
# Download the required files. Print the file path for the geometry file.
import os

from ansys.mechanical.core import launch_mechanical
from ansys.mechanical.core.examples import download_file

geometry_path = download_file("example_01_geometry.agdb", "pymechanical", "00_basic")
print(f"Downloaded the geometry file to: {geometry_path}")

###############################################################################
# Launch Mechanical
# ~~~~~~~~~~~~~~~~~
# Launch a new Mechanical session in batch, setting ``cleanup_on_exit`` to
# ``False``. To close this Mechanical session when finished, this example
# must call  the ``mechanical.exit()`` method.

mechanical = launch_mechanical(batch=True, cleanup_on_exit=False)
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

###################################################################################
# Execute the script
# ~~~~~~~~~~~~~~~~~~
# Run the Mechanical script to attach the geometry and set up and solve the
# analysis.

output = mechanical.run_python_script(
    """
import json

geometry_import_group_11 = Model.GeometryImportGroup
geometry_import_19 = geometry_import_group_11.AddGeometryImport()

geometry_import_19_format = Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.\
    Format.Automatic
geometry_import_19_preferences = Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences()
geometry_import_19_preferences.ProcessNamedSelections = True
geometry_import_19_preferences.ProcessCoordinateSystems = True

geometry_import_19.Import(part_file_path, geometry_import_19_format, geometry_import_19_preferences)

Model.AddStaticStructuralAnalysis()
STAT_STRUC = Model.Analyses[0]
CS_GRP = Model.CoordinateSystems
ANALYSIS_SETTINGS = STAT_STRUC.Children[0]
SOLN= STAT_STRUC.Solution

# Section 2 Set up the Unit System.

ExtAPI.Application.ActiveUnitSystem = MechanicalUnitSystem.StandardMKS
ExtAPI.Application.ActiveAngleUnit = AngleUnitType.Radian

# Section 3 Named Selection and Coordinate System.

NS1 = Model.NamedSelections.Children[0]
NS2 = Model.NamedSelections.Children[1]
NS3 = Model.NamedSelections.Children[2]
NS4 = Model.NamedSelections.Children[3]
GCS = CS_GRP.Children[0]
LCS1 = CS_GRP.Children[1]

# Section 4 Define remote point.

RMPT_GRP = Model.RemotePoints
RMPT_1 = RMPT_GRP.AddRemotePoint()
RMPT_1.Location = NS1
RMPT_1.XCoordinate=Quantity("7 [m]")
RMPT_1.YCoordinate=Quantity("0 [m]")
RMPT_1.ZCoordinate=Quantity("0 [m]")

#  Section 5 Define Mesh Settings.

MSH = Model.Mesh
MSH.ElementSize =Quantity("0.5 [m]")
MSH.GenerateMesh()

#  Section 6 Define boundary conditions.

# Insert FIXED Support
FIX_SUP = STAT_STRUC.AddFixedSupport()
FIX_SUP.Location = NS2

# Insert Frictionless Support
FRIC_SUP = STAT_STRUC.AddFrictionlessSupport()
FRIC_SUP.Location = NS3

#  Section 7 Define remote force.

REM_FRC1 = STAT_STRUC.AddRemoteForce()
REM_FRC1.Location = RMPT_1
REM_FRC1.DefineBy =LoadDefineBy.Components
REM_FRC1.XComponent.Output.DiscreteValues = [Quantity("1e10 [N]")]

#  Section 8 Define thermal condition.

THERM_COND = STAT_STRUC.AddThermalCondition()
THERM_COND.Location = NS4
THERM_COND.Magnitude.Output.DefinitionType=VariableDefinitionType.Formula
THERM_COND.Magnitude.Output.Formula="50*(20+z)"
THERM_COND.XYZFunctionCoordinateSystem=LCS1
THERM_COND.RangeMinimum=Quantity("-20 [m]")
THERM_COND.RangeMaximum=Quantity("1 [m]")

#  Section 9 Insert directional deformation.

DIR_DEF = STAT_STRUC.Solution.AddDirectionalDeformation()
DIR_DEF.Location = NS1
DIR_DEF.NormalOrientation =NormalOrientationType.XAxis

# Section 10 Add Total Deformation and force reaction probe

TOT_DEF = STAT_STRUC.Solution.AddTotalDeformation()

# Add Force Reaction
FRC_REAC_PROBE = STAT_STRUC.Solution.AddForceReaction()
FRC_REAC_PROBE.BoundaryConditionSelection = FIX_SUP
FRC_REAC_PROBE.ResultSelection =ProbeDisplayFilter.XAxis

# Section 11 Solve and get the results.

# Solve Static Analysis
STAT_STRUC.Solution.Solve(True)

dir_deformation_details = {
"Minimum": str(DIR_DEF.Minimum),
"Maximum": str(DIR_DEF.Maximum),
"Average": str(DIR_DEF.Average),
}

json.dumps(dir_deformation_details)
"""
)
print(output)


###############################################################################
# Download output file from solve and print contents
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Download the ``solve.out`` file from the server to the current working
# directory and print the contents. Remove the ``solve.out`` file.
def get_solve_out_path(mechanical):
    solve_out_path = ""
    for file_path in mechanical.list_files():
        if file_path.find("solve.out") != -1:
            solve_out_path = file_path
            break

    return solve_out_path


def write_file_contents_to_console(path):
    with open(path, "rt") as file:
        for line in file:
            print(line, end="")


solve_out_path = get_solve_out_path(mechanical)

if solve_out_path != "":
    current_working_directory = os.getcwd()

    mechanical.download(solve_out_path, target_dir=current_working_directory)
    solve_out_local_path = os.path.join(current_working_directory, "solve.out")

    write_file_contents_to_console(solve_out_local_path)

    os.remove(solve_out_local_path)

###########################################################
# Close Mechanical
# ~~~~~~~~~~~~~~~~
# Close the Mechanical instance.

mechanical.exit()
