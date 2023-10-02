# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.
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

import asyncio
from asyncio.subprocess import PIPE
import os
import sys
import typing
import warnings

import ansys.tools.path as atp
import click

from ansys.mechanical.core.embedding.appdata import UniqueUserProfile

# TODO - add logging options (reuse env var based logging initialization)
# TODO - add timeout


async def _read_and_display(cmd, env):
    """Read command's stdout and stderr and display them as they are processed."""
    # start process
    process = await asyncio.create_subprocess_exec(*cmd, stdout=PIPE, stderr=PIPE, env=env)

    # read child's stdout/stderr concurrently
    stdout, stderr = [], []  # stderr, stdout buffers
    tasks = {
        asyncio.Task(process.stdout.readline()): (stdout, process.stdout, sys.stdout.buffer),
        asyncio.Task(process.stderr.readline()): (stderr, process.stderr, sys.stderr.buffer),
    }
    while tasks:
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        assert done
        for future in done:
            buf, stream, display = tasks.pop(future)
            line = future.result()
            if line:  # not EOF
                buf.append(line)  # save for later
                display.write(line)  # display in terminal
                # schedule to read the next line
                tasks[asyncio.Task(stream.readline())] = buf, stream, display

    # wait for the process to exit
    rc = await process.wait()
    return rc, b"".join(stdout), b"".join(stderr)


def _run(args, env):
    if os.name == "nt":
        loop = asyncio.ProactorEventLoop()  # for subprocess' pipes on Windows
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()
    try:
        rc, *output = loop.run_until_complete(_read_and_display(args, env))
        if rc:
            sys.exit("child failed with '{}' exit code".format(rc))
    finally:
        loop.close()


@click.command()
@click.help_option("--help", "-h")
@click.option(
    "-p",
    "--project-file",
    default=None,
    help="Opens Mechanical project file (.mechdb). Cannot be mixed with -i",
)
@click.option(
    "--private-appdata",
    default=None,
    is_flag=True,
    help="Make the appdata folder private.\
 This enables you to run parallel instances of Mechanical.",
)
@click.option(
    "--port",
    type=int,
    help="Start mechanical in server mode with the given port number",
)
@click.option(
    "-i",
    "--input-script",
    default=None,
    help="Name of the input Python script. Cannot be mixed with -p",
)
@click.option(
    "--exit",
    is_flag=True,
    default=None,
    help="Exit the application after running an input script. \
You can only use this command with --input-script argument (-i). \
The command defaults to true you are not running the application in graphical mode. \
The ``exit`` command is only supported in version 2024 R1 or later.",
)
@click.option(
    "-s",
    "--show-welcome-screen",
    is_flag=True,
    default=False,
    help="Show the welcome screen, where you can select the file to open.\
 Only affects graphical mode",
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Show a debug dialog right when the process starts.",
)
@click.option(
    "-r",
    "--revision",
    default=None,
    type=int,
    help='Ansys Revision number, e.g. "241" or "232". If none is specified\
, uses the default from ansys-tools-path',
)
@click.option(
    "-g",
    "--graphical",
    is_flag=True,
    default=False,
    help="Graphical mode",
)
def cli(
    project_file: str,
    port: int,
    debug: bool,
    input_script: str,
    revision: int,
    graphical: bool,
    show_welcome_screen: bool,
    private_appdata: bool,
    exit: bool,
):
    """CLI tool to run mechanical.

    USAGE:

    The following example demonstrates the main use of this tool:

        $ ansys-mechanical -r 232 -g

        Starting Ansys Mechanical version 2023R2 in graphical mode...
    """
    if project_file and input_script:
        raise Exception("Cannot open a project file *and* run a script.")

    if (not graphical) and project_file:
        raise Exception("Cannot open a project file in batch mode.")

    if port:
        if project_file:
            raise Exception("Cannot open in server mode with a project file.")
        if input_script:
            raise Exception("Cannot open in server mode with an input script.")

    if not revision:
        exe, version = atp.find_mechanical()
    else:
        exe, version = atp.find_mechanical(version=revision)

    version = int(version * 10)
    version_name = atp.SUPPORTED_ANSYS_VERSIONS[version]

    args = [exe, "-DSApplet"]
    if (not graphical) or (not show_welcome_screen):
        args.append("-AppModeMech")

    if version < 232:
        args.append("-nosplash")
        args.append("-notabctrl")

    if graphical:
        mode = "Graphical"
    else:
        mode = "Batch"
        args.append("-b")

    if debug:
        os.environ["WBDEBUG_STOP"] = "1"

    if port:
        args.append("-grpc")
        args.append(str(port))

    if project_file:
        args.append("-file")
        args.append(project_file)

    if input_script:
        args.append("-script")
        args.append(input_script)

    if (not graphical) and input_script:
        exit = True
        if version < 241:
            warnings.warn(
                "Please ensure ExtAPI.Application.Close() is at the end of your script. "
                "Without this command, Batch mode will not terminate.",
                stacklevel=2,
            )

    if exit and input_script and version >= 241:
        args.append("-x")

    profile: UniqueUserProfile = None
    env: typing.Dict[str, str] = None
    if private_appdata:
        env = os.environ.copy()
        new_profile_name = f"Mechanical-{os.getpid()}"
        profile = UniqueUserProfile(new_profile_name)
        profile.update_environment(env)

    print(f"Starting Ansys Mechanical version {version_name} in {mode} mode...")
    if port:
        # TODO - Mechanical doesn't write anything to the stdout in grpc mode
        #        when logging is off.. Ideally we let Mechanical write it, so
        #        the user only sees the message when the server is ready.
        print(f"Serving on port {port}")

    _run(args, env)

    if private_appdata:
        profile.cleanup()


@click.command()
@click.help_option("--help", "-h")
@click.option(
    "-r",
    "--revision",
    default=None,
    type=int,
    help='Ansys Revision number, e.g. "241" or "232".\
         If a revision number is not specified, it uses the default from \
            ansys-tools-path.',
)
@click.argument("args", nargs=-1)
def cli_env(revision: int, args):
    """CLI tool to load the environment required to run in Linux.

    Parameters
    ----------
    revision : int
        The Ansys Revision number.

    Examples
    --------
    $ mechanical-env -r 232 -- python test.py
    Loads the environment to run a test.py file in Linux.

    $ mechanical-env -- make -C doc html
    Loads the environment to generate Sphinx documents in Linux.
    """
    #  Should not update env variables in Windows
    if os.name == "nt":
        print("This feature is not available in Windows!")
        return True

    # Gets the revision number
    if not revision:
        exe, version = atp.find_mechanical()
    else:
        exe, version = atp.find_mechanical(version=revision)
    version = int(version * 10)

    env = os.environ.copy()
    # workbench (mechanical) installation directory
    env["DS_INSTALL_DIR"] = os.path.dirname(exe)
    DS_INSTALL_DIR = env.get("DS_INSTALL_DIR")
    env[f"AWP_ROOT{version}"] = f"{DS_INSTALL_DIR}/.."
    AWP_ROOT = env.get(f"AWP_ROOT{version}")  # AWP_ROOT with revision number

    # Env vars used by workbench (mechanical) code
    env[f"AWP_LOCALE{version}"] = "en-us"
    env[
        f"CADOE_LIBDIR{version}"
    ] = f'{AWP_ROOT}/commonfiles/language/{env.get(f"AWP_LOCALE{version}")}'
    env["ANSYSLIC_DIR"] = f"{AWP_ROOT}/../shared_files/licensing"
    env["ANSYSCOMMON_DIR"] = f"{AWP_ROOT}/commonfiles"
    env[f"ANSYSCL{version}_DIR"] = f"{AWP_ROOT}/licensingclient"

    # MainWin vars
    env["ANSISMAINWINLITEMODE"] = "1"
    env["MWCONFIG_NAME"] = "amd64_linux"
    env["MWDEBUG_LEVEL"] = "0"
    env["MWHOME"] = f"{AWP_ROOT}/commonfiles/MainWin/linx64/mw"
    env["MWOS"] = "linux"
    env["MWREGISTRY"] = f'{DS_INSTALL_DIR}/WBMWRegistry/hklm_{env.get("MWCONFIG_NAME")}.bin'
    env["MWRT_MODE"] = "classic"
    env["MWRUNTIME"] = "1"
    env["MWUSER_DIRECTORY"] = env.get("HOME") + "/.mw"
    env["MWDONT_XCLOSEDISPLAY"] = "1"

    # dynamic library preload
    env["LD_PRELOAD"] = "libstdc++.so.6.0.28"

    # dynamic library load path
    env["LD_LIBRARY_PATH"] = (
        f"{AWP_ROOT}/tp/stdc++:"
        + f"{AWP_ROOT}/tp/openssl/1.1.1/linx64/lib:"
        + f'{env.get("MWHOME")}/lib-amd64_linux:'
        + f'{env.get("MWHOME")}/lib-amd64_linux_optimized:'
        + f'{env.get("LD_LIBRARY_PATH")}:'
        + f"{AWP_ROOT}/Tools/mono/Linux64/lib:"
        + f"{DS_INSTALL_DIR}/lib/linx64:"
        + f"{DS_INSTALL_DIR}/dll/linx64:"
        + f"{DS_INSTALL_DIR}/libshared/linx64:"
        + f"{AWP_ROOT}/tp/IntelCompiler/2019.3.199/linx64/lib/intel64:"
        + f"{AWP_ROOT}/tp/qt_fw/5.9.6/Linux64/lib:"
        + f"{AWP_ROOT}/commonfiles/CAD/Acis/linx64:"
        + f"{AWP_ROOT}/commonfiles/fluids/lib/linx64:"
        + f"{AWP_ROOT}/Framework/bin/Linux64"
    )

    # system path
    env["PATH"] = (
        f'{env.get("MWHOME")}/bin-amd64_linux_optimized:'
        + f"{DS_INSTALL_DIR}/CommonFiles/linx64:"
        + f"{DS_INSTALL_DIR}/CADIntegration/linx64:"
        + f"{AWP_ROOT}/Tools/mono/Linux64/bin:"
        + env.get("PATH")
    )

    _run(args, env)
