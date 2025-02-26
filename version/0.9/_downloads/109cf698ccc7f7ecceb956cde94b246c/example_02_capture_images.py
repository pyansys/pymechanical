""".. _ref_example_02_capture_images:

Capture images after a solve
----------------------------

Using supplied files, this example shows how to resume a MECHDAT file
and capture the images of all results in a folder on the disk.

"""

###############################################################################
# Download required files
# ~~~~~~~~~~~~~~~~~~~~~~~
# Download the required files. Print the file paths for the MECHDAT file and
# script files.

import os

from matplotlib import image as mpimg
from matplotlib import pyplot as plt

from ansys.mechanical.core import launch_mechanical
from ansys.mechanical.core.examples import download_file

mechdat_path = download_file("example_03_simple_bolt_new.mechdat", "pymechanical", "00_basic")
print(f"Downloaded the MECHDAT file to: {mechdat_path}")

script_file_path = download_file("example_02_capture_images_helper.py", "pymechanical", "00_basic")
print(f"Downloaded the script files to: {script_file_path}")

###############################################################################
# Launch Mechanical
# ~~~~~~~~~~~~~~~~~
# Launch a new Mechanical session in batch, setting ``cleanup_on_exit`` to
# ``False``. To close this Mechanical session when finished, this example
# must call  the ``mechanical.exit()`` method.

mechanical = launch_mechanical(batch=True, cleanup_on_exit=False)
print(mechanical)

###############################################################################
# Initialize the variable needed for opening the MECHDAT file
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set the ``mechdat_path`` variable for later use.
# Make the variable compatible for Windows, Linux, and Docker containers.

project_directory = mechanical.project_directory
print(f"project directory = {project_directory}")

# Upload the file to the project directory.
mechanical.upload(file_name=mechdat_path, file_location_destination=project_directory)

# Build the path relative to the project directory.
base_name = os.path.basename(mechdat_path)
combined_path = os.path.join(project_directory, base_name)
mechdat_path_modified = combined_path.replace("\\", "\\\\")
mechanical.run_python_script(f"mechdat_path='{mechdat_path_modified}'")

# Verify the path for the MECHDAT file.
result = mechanical.run_python_script(f"mechdat_path")
print(f"MECHDATA file is stored on the server at: {result}")

###################################################################################
# Open the MECHDAT file
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run the script to open the MECHDAT file.

mechanical.run_python_script("ExtAPI.DataModel.Project.Open(mechdat_path)")

###################################################################################
# Initialize the variable needed for the image directory
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set the ``image_dir`` for later use.
# Make the variable compatible for Windows, Linux, and Docker containers.

# Open the MECHDAT file changes the project directory.
project_directory = mechanical.project_directory
print(f"project directory = {project_directory}")

image_directory_modified = project_directory.replace("\\", "\\\\")
mechanical.run_python_script(f"image_dir='{image_directory_modified}'")

# Verify the path for image directory.
result_image_dir_server = mechanical.run_python_script(f"image_dir")
print(f"Images are stored on the server at: {result_image_dir_server}")

###################################################################################
# Execute the Mechanical script
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run the Mechanical script file for creating the images.

mechanical.run_python_script_from_file(script_file_path)

###############################################################################
# Download the image and plot
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Download one image file from the server to the current working directory and plot
# using matplotlib.


def get_image_path(image_name):
    return result_image_dir_server + image_name


def display_image(path):
    print(f"Printing {path} using matplotlib")
    image1 = mpimg.imread(path)
    plt.figure(figsize=(15, 15))
    plt.axis("off")
    plt.imshow(image1)
    plt.show()


image_name = "Total Deformation @ 1 sec_Right.png"
image_path_server = get_image_path(image_name)

if image_path_server != "":
    current_working_directory = os.getcwd()

    local_file_path_list = mechanical.download(
        image_path_server, target_dir=current_working_directory
    )
    image_local_path = local_file_path_list[0]
    print(f"Local image path : {image_local_path}")

    display_image(image_local_path)

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
