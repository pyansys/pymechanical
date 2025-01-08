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

"""Convenience CLI to run mechanical."""

import json
import os
from pathlib import Path
import sys
import sysconfig

import ansys.tools.path as atp
import click


def _cli_impl(
    ide: str = "vscode",
    settings_type: str = "user",
    revision: int = None,
):
    """Provide the user with the path to the settings.json file and autocomplete settings.

    Parameters
    ----------
    ide: str
        The IDE to set up autocomplete settings. By default, it's ``vscode``.
    settings_type: str
        The type of settings to update. Either "user" or "workspace" in VS Code.
        By default, it's ``user``.
    revision: int
        The Mechanical revision number. For example, "242".
        If unspecified, it finds the default Mechanical version from ansys-tools-path.
    """
    # Check the IDE and raise an exception if it's not VS Code
    if ide != "vscode":
        raise Exception(f"{ide} is not supported at the moment.")

    # Update the user or workspace settings
    if settings_type == "user":
        # Get the path to the user's settings.json file depending on the platform
        if "win" in sys.platform:
            settings_json = Path(os.environ.get("APPDATA")) / "Code" / "User" / "settings.json"
        elif "lin" in sys.platform:
            settings_json = (
                Path(os.environ.get("HOME")) / ".config" / "Code" / "User" / "settings.json"
            )
    elif settings_type == "workspace":
        # Get the current working directory
        current_dir = Path.cwd()
        # Get the path to the settings.json file based on the git root & .vscode folder
        settings_json = current_dir / ".vscode" / "settings.json"

    # Location where the stubs are installed -> .venv/Lib/site-packages, for example
    stubs_location = (
        Path(sysconfig.get_paths()["purelib"]) / "ansys" / "mechanical" / "stubs" / f"v{revision}"
    )

    # The settings to add to settings.json for autocomplete to work
    settings_json_data = {
        "python.autoComplete.extraPaths": [str(stubs_location)],
        "python.analysis.extraPaths": [str(stubs_location)],
    }
    # Pretty print dictionary
    pretty_dict = json.dumps(settings_json_data, indent=4)

    print(f"Update {settings_json} with the following information:\n")

    if settings_type == "workspace":
        print(
            "Note: Please ensure the .vscode folder is in the root of your project or repository.\n"
        )

    print(pretty_dict)


@click.command()
@click.help_option("--help", "-h")
@click.option(
    "--ide",
    default="vscode",
    type=str,
    help="The IDE being used.",
)
@click.option(
    "--settings_type",
    default="user",
    type=str,
    help="The type of settings to update - either user or workspace settings.",
)
@click.option(
    "--revision",
    default=None,
    type=int,
    help='The Mechanical revision number, e.g. "242" or "241". If unspecified,\
it finds and uses the default version from ansys-tools-path.',
)
def cli(ide: str, settings_type: str, revision: int) -> None:
    """CLI tool to update settings.json files for autocomplete with ansys-mechanical-stubs.

    Parameters
    ----------
    ide: str
        The IDE to set up autocomplete settings. By default, it's ``vscode``.
    settings_type: str
        The type of settings to update. Either "user" or "workspace" in VS Code.
        By default, it's ``user``.
    revision: int
        The Mechanical revision number. For example, "242".
        If unspecified, it finds the default Mechanical version from ansys-tools-path.

    Usage
    -----
    The following example demonstrates the main use of this tool:

        $ ansys-mechanical-autocomplete --ide vscode --location user --revision 242

    """
    exe = atp.get_mechanical_path(allow_input=False, version=revision)
    version = atp.version_from_path("mechanical", exe)

    return _cli_impl(
        ide,
        settings_type,
        version,
    )
