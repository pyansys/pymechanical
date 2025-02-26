""".. _ref_example_02_run_python_script_scope:

Test variable and function scope
--------------------------------

This example calls the ``run_python_script`` method and checks the variable and
function scope between calls.

"""

###############################################################################
# Launch Mechanical
# ~~~~~~~~~~~~~~~~~
# Launch a new Mechanical session in batch, setting ``cleanup_on_exit`` to
# ``False``. To close this Mechanical session when finished, this example
# must call  the ``mechanical.exit()`` method.

from ansys.mechanical.core import launch_mechanical

mechanical = launch_mechanical(batch=True, cleanup_on_exit=False)
print(mechanical)

###################################################################################
# Set variable
# ~~~~~~~~~~~~
# Run the script to assign a value to a variable.

output = mechanical.run_python_script(
    """
x = 10
x
"""
)
print(f"x = {output}")

###################################################################################
# Access the variable in the next call
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run the script to change the variable value.

output = mechanical.run_python_script(
    """
x = x * 2
x
"""
)
print(f"x = {output}")

###################################################################################
# Define function
# ~~~~~~~~~~~~~~~
# Run the script to define a function and access the variable defined in the
# previous call.

output = mechanical.run_python_script(
    """
def multiply_by_10():
    return x*10

multiply_by_10()
"""
)
print(f"output = {output}")

###################################################################################
# Access the function
# ~~~~~~~~~~~~~~~~~~~
# Run the script to access the function defined in the previous call.

output = mechanical.run_python_script(
    """
multiply_by_10() * 2
"""
)
print(f"output = {output}")


###########################################################
# Close Mechanical
# ~~~~~~~~~~~~~~~~
# Close the Mechanical instance.

mechanical.exit()
