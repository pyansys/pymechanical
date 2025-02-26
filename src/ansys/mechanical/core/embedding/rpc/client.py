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
"""Client for Mechanical services."""

import os
import pathlib
import time

import rpyc

from ansys.mechanical.core.embedding.rpc.server import PYMECHANICAL_DEFAULT_RPC_PORT
from ansys.mechanical.core.mechanical import DEFAULT_CHUNK_SIZE


class Client:
    """Client for connecting to Mechanical services."""

    def __init__(self, host: str, port: int, timeout: float = 120.0, cleanup_on_exit=True):
        """Initialize the client.

        Parameters
        ----------
        host : str, optional
            IP address to connect to the server.  The default is ``None``
            in which case ``localhost`` is used.
        port : int, optional
            Port to connect to the Mecahnical server. The default is ``None``,
            in which case ``20000`` is used.
        timeout : float, optional
            Maximum allowable time for connecting to the Mechanical server.
            The default is ``60.0``.

        """
        if host is None:
            host = "localhost"
        self.host = host
        if port is None:
            port = PYMECHANICAL_DEFAULT_RPC_PORT
        self.port = port
        self.timeout = timeout
        self.connection = None
        self.root = None
        self._connect()
        self._cleanup_on_exit = cleanup_on_exit

    def __getattr__(self, attr):
        """Get attribute from the root object."""
        if hasattr(self.root, attr):
            return getattr(self.root, attr)
        propget_name = f"propget_{attr}"
        if hasattr(self.root, propget_name):
            exposed_fget = getattr(self.root, propget_name)
            return exposed_fget()
        return self.__dict__.items[attr]

    # TODO - implement setattr
    # def __setattr__(self, attr, value):
    #     if hasattr(self.root, attr):
    #         inner_prop = getattr(self.root.__class__, attr)
    #         if isinstance(inner_prop, property):
    #             inner_prop.fset(self.root, value)
    #     else:
    #         super().__setattr__(attr, value)

    def _connect(self):
        self._wait_until_ready()
        self.root = self.connection.root
        print(f"Connected to {self.host}:{self.port}")

    def _exponential_backoff(self, max_time=60.0, base_time=0.1, factor=2):
        """Generate exponential backoff timing."""
        t_max = time.time() + max_time
        t = base_time
        while time.time() < t_max:
            yield t
            t = min(t * factor, max_time)

    def _wait_until_ready(self):
        """Wait until the server is ready."""
        t_max = time.time() + self.timeout
        for delay in self._exponential_backoff(max_time=self.timeout):
            if time.time() >= t_max:
                break  # Exit if the timeout is reached
            try:
                self.connection = rpyc.connect(self.host, self.port)
                self.connection.ping()
                print("Server is ready.")
                return
            except Exception:
                time.sleep(delay)

        raise TimeoutError(
            f"Server at {self.host}:{self.port} not ready within {self.timeout} seconds."
        )

    def close(self):
        """Close the connection."""
        self.connection.close()
        print(f"Connection to {self.host}:{self.port} closed")

    def upload(
        self,
        file_name,
        file_location_destination=None,
        chunk_size=DEFAULT_CHUNK_SIZE,
        progress_bar=False,
    ):
        """Upload a file to the server."""
        print(f"arg: {file_name}, {file_location_destination}")
        print()
        if not os.path.exists(file_name):
            print(f"File {file_name} does not exist.")
            return
        file_base_name = os.path.basename(file_name)
        remote_path = os.path.join(file_location_destination, file_base_name)

        with open(file_name, "rb") as f:
            file_data = f.read()
            self.service_upload(remote_path, file_data)

        print(f"File {file_name} uploaded to {file_location_destination}")

    def download(
        self,
        files,
        target_dir=None,
        chunk_size=DEFAULT_CHUNK_SIZE,
        progress_bar=None,
        recursive=False,
    ):
        """Download a file from the server."""
        out_files = []
        os.makedirs(target_dir, exist_ok=True)

        response = self.service_download(files)

        if isinstance(response, dict) and response["is_directory"]:
            for relative_file_path in response["files"]:
                full_remote_path = os.path.join(files, relative_file_path)
                local_file_path = os.path.join(target_dir, relative_file_path)
                local_file_dir = os.path.dirname(local_file_path)
                os.makedirs(local_file_dir, exist_ok=True)

                out_file_path = self._download_file(
                    full_remote_path, local_file_path, chunk_size, overwrite=True
                )
        else:
            out_file_path = self._download_file(
                files, os.path.join(target_dir, os.path.basename(files)), chunk_size, overwrite=True
            )
        out_files.append(out_file_path)

        return out_files

    def _download_file(self, remote_file_path, local_file_path, chunk_size=1024, overwrite=False):
        if os.path.exists(local_file_path) and not overwrite:
            print(f"File {local_file_path} already exists locally. Skipping download.")
            return
        response = self.service_download(remote_file_path)
        if isinstance(response, dict):
            raise ValueError("Expected a file download, but got a directory response.")
        file_data = response

        # Write the file data to the local path
        with open(local_file_path, "wb") as f:
            f.write(file_data)

        print(f"File {remote_file_path} downloaded to {local_file_path}")

        return local_file_path

    def download_project(self, extensions=None, target_dir=None, progress_bar=False):
        """Download all project files in the working directory of the Mechanical instance."""
        destination_directory = target_dir.rstrip("\\/")
        if destination_directory:
            path = pathlib.Path(destination_directory)
            path.mkdir(parents=True, exist_ok=True)
        else:
            destination_directory = os.getcwd()
        # relative directory?
        if os.path.isdir(destination_directory):
            if not os.path.isabs(destination_directory):
                # construct full path
                destination_directory = os.path.join(os.getcwd(), destination_directory)
        _project_directory = self.project_directory
        _project_directory = _project_directory.rstrip("\\/")

        # this is where .mechddb resides
        parent_directory = os.path.dirname(_project_directory)

        list_of_files = []

        if not extensions:
            files = self.list_files()
        else:
            files = []
            for each_extension in extensions:
                # mechdb resides one level above project directory
                if "mechdb" == each_extension.lower():
                    file_temp = os.path.join(parent_directory, f"*.{each_extension}")
                else:
                    file_temp = os.path.join(_project_directory, "**", f"*.{each_extension}")

                list_files = self._get_files(file_temp, recursive=False)

                files.extend(list_files)

        for file in files:
            # create similar hierarchy locally
            new_path = file.replace(parent_directory, destination_directory)
            new_path_dir = os.path.dirname(new_path)
            temp_files = self.download(
                files=file, target_dir=new_path_dir, progress_bar=progress_bar
            )
            list_of_files.extend(temp_files)
        return list_of_files

    @property
    def is_alive(self):
        """Check if the Mechanical instance is alive."""
        try:
            self.connection.ping()
            return True
        except:
            return False

    def exit(self):
        """Shuts down the Mechanical instance."""
        print("Requesting server shutdown ...")
        self.service_exit()
        self.connection.close()
        print("Disconnected from server")

    def __del__(self):  # pragma: no cover
        """Clean up on exit."""
        if self._cleanup_on_exit:
            try:
                self.exit()
            except Exception as e:
                print(f"Failed to exit cleanly: {e}")
