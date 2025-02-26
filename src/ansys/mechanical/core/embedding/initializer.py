# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
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

"""Initializer for Mechanical embedding. Sets up paths and resolvers."""
from importlib.metadata import distribution
import os
from pathlib import Path
import platform
import sys
import warnings

from ansys.mechanical.core.embedding.loader import load_clr
from ansys.mechanical.core.embedding.resolver import resolve
from ansys.mechanical.core.mechanical import LOG

INITIALIZED_VERSION = None
"""Constant for the initialized version."""

SUPPORTED_MECHANICAL_EMBEDDING_VERSIONS = {
    251: "2025R1",
    242: "2024R2",
    241: "2024R1",
    232: "2023R2",
}
"""Supported Mechanical embedding versions on Windows."""


def __add_sys_path(version: int) -> str:
    install_path = Path(os.environ[f"AWP_ROOT{version}"])
    platform_string = "winx64" if os.name == "nt" else "linx64"
    bin_path = install_path / "aisol" / "bin" / platform_string
    sys.path.append(str(bin_path.resolve()))


def __workaround_material_server(version: int) -> None:
    """Workaround material server bug in 2024 R1.

    A REST server is used as a backend for the material model GUI.
    In 2024 R1, this GUI is used even in batch mode. The server
    starts by default on a background thread, which may lead to
    a race condition on shutdown.
    """
    if version in [241]:
        os.environ["ENGRDATA_SERVER_SERIAL"] = "1"


def __check_for_supported_version(version) -> None:
    """Check if Mechanical version is supported with current version of PyMechanical.

    If specific environment variable is enabled, then users can overwrite the supported versions.
    However, using unsupported versions may cause issues.
    """
    allow_old_version = os.getenv("ANSYS_MECHANICAL_EMBEDDING_SUPPORT_OLD_VERSIONS") == "1"

    # Check if the version is supported
    if not allow_old_version and version < min(SUPPORTED_MECHANICAL_EMBEDDING_VERSIONS):
        raise ValueError(f"Mechanical version {version} is not supported.")

    return version


def _get_latest_default_version() -> int:
    """Try to get the latest Mechanical version from the environment.

    Checks if multiple versions of Mechanical found in system.
    For Linux it will be only one since ``mechanical-env`` takes care of that.
    If multiple versions are detected, select the latest one, as no specific version is provided.
    """
    awp_roots = [value for key, value in os.environ.items() if key.startswith("AWP_ROOT")]
    if not awp_roots:
        raise Exception("No Mechanical installations found.")

    versions_found = []
    for path in awp_roots:
        folder = os.path.basename(os.path.normpath(path))
        version = folder.split("v")[-1]
        versions_found.append(int(version))

    LOG.info(f"Available versions of Mechanical: {versions_found}")

    latest_version = max(versions_found)

    if len(awp_roots) > 1:
        LOG.warning(
            f"Multiple versions of Mechanical found! Using latest version {latest_version} ..."
        )
    return latest_version


def __check_python_interpreter_architecture() -> None:
    """Embedding support only 64 bit architecture."""
    if platform.architecture()[0] != "64bit":
        raise Exception("Mechanical Embedding requires a 64-bit Python environment.")


def __set_environment(version: int) -> None:
    """Set environment variables to configure embedding."""
    if os.name == "nt":  # pragma: no cover
        if version < 251:
            os.environ["MECHANICAL_STARTUP_UNOPTIMIZED"] = "1"

    # Set an environment variable to use the custom CLR host
    # for embedding.
    # In the future (>251), it would always be used.
    if version == 251:
        if "PYMECHANICAL_NO_CLR_HOST_LITE" not in os.environ:
            os.environ["ANSYS_MECHANICAL_EMBEDDING_CLR_HOST"] = "1"


def __check_for_mechanical_env():
    """Embedding in linux platform must use mechanical-env."""
    if platform.system() == "Linux" and os.environ.get("PYMECHANICAL_EMBEDDING") != "TRUE":
        raise Exception(
            "On linux, embedding an instance of the Mechanical process using"
            "the App class requires running python inside of a Mechanical environment."
            "Use the `mechanical-env` script to do this. For more information, refer to:"
            "https://mechanical.docs.pyansys.com/version/stable/"
            "getting_started/running_mechanical.html#embed-a-mechanical-instance"
        )


def __is_lib_loaded(libname: str):  # pragma: no cover
    """Return whether a library is loaded."""
    import ctypes

    RTLD_NOLOAD = 4
    try:
        ctypes.CDLL(libname, RTLD_NOLOAD)
    except OSError:
        return False
    return True


def __check_loaded_libs(version: int = None):  # pragma: no cover
    """Ensure that incompatible libraries aren't loaded prior to PyMechanical load."""
    if platform.system() != "Linux":
        return

    if version < 251:
        return

    # For 2025 R1, PyMechanical will crash on shutdown if libX11.so is already loaded
    # before starting Mechanical
    if __is_lib_loaded("libX11.so"):
        LOG.warning(
            "libX11.so is loaded prior to initializing the Embedded Instance of Mechanical.\
                      Python will crash on shutdown..."
        )


def initialize(version: int = None):
    """Initialize Mechanical embedding."""
    global INITIALIZED_VERSION
    if version is None:
        version = _get_latest_default_version()

    version = __check_for_supported_version(version=version)

    if INITIALIZED_VERSION is not None:
        if INITIALIZED_VERSION != version:
            raise ValueError(
                f"Initialized version {INITIALIZED_VERSION} "
                f"does not match the expected version {version}."
            )
        return INITIALIZED_VERSION

    __check_python_interpreter_architecture()  # blocks 32 bit python
    __check_for_mechanical_env()  # checks for mechanical-env in linux embedding

    __set_environment(version)

    __check_loaded_libs(version)

    __workaround_material_server(version)

    # need to add system path in order to import the assembly with the resolver
    __add_sys_path(version)

    # Check if 'pythonnet' is installed... and if so, throw warning
    try:
        distribution("pythonnet")
        warnings.warn(
            "The pythonnet package was found in your environment "
            "which interferes with the ansys-pythonnet package. "
            "Some APIs may not work due to pythonnet being installed.\n\n"
            "For using PyMechanical, we recommend you do the following:\n"
            "1. Uninstall your existing pythonnet package: pip uninstall pythonnet\n"
            "2. Install the ansys-pythonnet package: pip install --upgrade "
            "--force-reinstall ansys-pythonnet\n",
            stacklevel=2,
        )
    except ModuleNotFoundError:
        pass

    # load the CLR with mono that is shipped with the unified ansys installer
    load_clr(os.environ[f"AWP_ROOT{version}"])

    # attach the resolver
    resolve(version)

    INITIALIZED_VERSION = version
    return version
