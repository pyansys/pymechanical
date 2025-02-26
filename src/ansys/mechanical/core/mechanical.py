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

"""Connect to Mechanical gRPC server and issues commands."""
import atexit
from contextlib import closing
import datetime
import fnmatch
from functools import wraps
import glob
import os
import pathlib
import socket
import subprocess  # nosec: B404
import sys
import threading
import time
from typing import Optional
import warnings
import weakref

import ansys.api.mechanical.v0.mechanical_pb2 as mechanical_pb2
import ansys.api.mechanical.v0.mechanical_pb2_grpc as mechanical_pb2_grpc
import ansys.tools.path as atp
import grpc

import ansys.mechanical.core as pymechanical
from ansys.mechanical.core import LOG
from ansys.mechanical.core.errors import (
    MechanicalExitedError,
    MechanicalRuntimeError,
    VersionError,
    protect_grpc,
)
from ansys.mechanical.core.launcher import MechanicalLauncher
from ansys.mechanical.core.misc import (
    check_valid_ip,
    check_valid_port,
    check_valid_start_instance,
    threaded,
)

# Check if PyPIM is installed
try:
    import ansys.platform.instancemanagement as pypim  # pragma: nocover noqa: F401

    _HAS_ANSYS_PIM = True
    """Whether or not PyPIM exists."""
except ImportError:
    _HAS_ANSYS_PIM = False


# Checking if tqdm is installed.
# If it is, the default value for progress_bar is true.
try:
    from tqdm import tqdm

    _HAS_TQDM = True
    """Whether or not tqdm is installed."""
except ModuleNotFoundError:  # pragma: no cover
    _HAS_TQDM = False

# Default 256 MB message length
MAX_MESSAGE_LENGTH = int(os.environ.get("PYMECHANICAL_MAX_MESSAGE_LENGTH", 256 * 1024**2))
"""Default message length."""

# Chunk sizes for streaming and file streaming
DEFAULT_CHUNK_SIZE = 256 * 1024  # 256 kB
"""Default chunk size."""
DEFAULT_FILE_CHUNK_SIZE = 1024 * 1024  # 1MB
"""Default file chunk size."""


def setup_logger(loglevel="INFO", log_file=True, mechanical_instance=None):
    """Initialize the logger for the given mechanical instance."""
    # Return existing log if this function has already been called
    if hasattr(setup_logger, "log"):
        return setup_logger.log
    else:
        setup_logger.log = LOG.add_instance_logger("Mechanical", mechanical_instance)

    setup_logger.log.setLevel(loglevel)

    if log_file:
        if isinstance(log_file, str):
            setup_logger.log.log_to_file(filename=log_file, level=loglevel)

    return setup_logger.log


def suppress_logging(func):
    """Decorate a function to suppress the logging for a Mechanical instance."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        mechanical = args[0]
        prior_log_level = mechanical.log.level
        if prior_log_level != "CRITICAL":
            mechanical.set_log_level("CRITICAL")

        out = func(*args, **kwargs)

        if prior_log_level != "CRITICAL":
            mechanical.set_log_level(prior_log_level)

        return out

    return wrapper


LOCALHOST = "127.0.0.1"
"""Localhost address."""

MECHANICAL_DEFAULT_PORT = 10000
"""Default Mechanical port."""

GALLERY_INSTANCE = [None]
"""List of gallery instances."""


def _cleanup_gallery_instance():  # pragma: no cover
    """Clean up any leftover instances of Mechanical from building the gallery."""
    if GALLERY_INSTANCE[0] is not None:
        mechanical = Mechanical(
            ip=GALLERY_INSTANCE[0]["ip"],
            port=GALLERY_INSTANCE[0]["port"],
        )
        mechanical.exit(force=True)


atexit.register(_cleanup_gallery_instance)


def port_in_use(port, host=LOCALHOST):
    """Check whether a port is in use at the given host.

    You must actually *bind* the address. Just checking if you can create
    a socket is insufficient because it is possible to run into permission
    errors like::

        An attempt was made to access a socket in a way forbidden by its
        access permissions.
    """
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((host, port)) == 0:
            return True
        else:
            return False


def check_ports(port_range, ip="localhost"):
    """Check the state of ports in a port range."""
    ports = {}
    for port in port_range:
        ports[port] = port_in_use(port, ip)
    return ports


def close_all_local_instances(port_range=None, use_thread=True):
    """Close all Mechanical instances within a port range.

    You can use this method when cleaning up from a failed pool or
    batch run.

    Parameters
    ----------
    port_range : list, optional
        List of a range of ports to use when cleaning up Mechanical. The
        default is ``None``, in which case the ports managed by
        PyMechanical are used.

    use_thread : bool, optional
        Whether to use threads to close the Mechanical instances.
        The default is ``True``. So this call will return immediately.

    Examples
    --------
    Close all Mechanical instances connected on local ports.

    >>> import ansys.mechanical.core as pymechanical
    >>> pymechanical.close_all_local_instances()

    """
    if port_range is None:
        port_range = pymechanical.LOCAL_PORTS

    @threaded
    def close_mechanical_threaded(port, name="Closing Mechanical instance in a thread"):
        close_mechanical(port, name)

    def close_mechanical(port, name="Closing Mechanical instance"):
        try:
            mechanical = Mechanical(port=port)
            LOG.debug(f"{name}: {mechanical.name}.")
            mechanical.exit(force=True)
        except OSError:  # pragma: no cover
            pass

    ports = check_ports(port_range)
    for port_temp, state in ports.items():
        if state:
            if use_thread:
                close_mechanical_threaded(port_temp)
            else:
                close_mechanical(port_temp)


def create_ip_file(ip, path):
    """Create the ``mylocal.ip`` file needed to change the IP address of the gRPC server."""
    file_name = os.path.join(path, "mylocal.ip")
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(ip)


def get_mechanical_path(allow_input=True):
    """Get path.

    Deprecated - use `ansys.tools.path.get_mechanical_path` instead
    """
    return atp.get_mechanical_path(allow_input)


def check_valid_mechanical():
    """Change to see if the default Mechanical path is valid.

    Example (windows)
    -----------------

    >>> from ansys.mechanical.core import mechanical
    >>> from ansys.tools.path import change_default_mechanical_path
    >>> mechanical_path = 'C:/Program Files/ANSYS Inc/v251/aisol/bin/win64/AnsysWBU.exe'
    >>> change_default_mechanical_path(mechanical_pth)
    >>> mechanical.check_valid_mechanical()
    True


    """
    mechanical_path = atp.get_mechanical_path(False)
    if mechanical_path is None:
        return False
    mechanical_version = atp.version_from_path("mechanical", mechanical_path)
    return not (mechanical_version < 232 and os.name != "posix")


def change_default_mechanical_path(exe_loc):
    """Change default path.

    Deprecated - use `ansys.tools.path.change_default_mechanical_path` instead.
    """
    return atp.change_default_mechanical_path(exe_loc)


def save_mechanical_path(exe_loc=None):  # pragma: no cover
    """Save path.

    Deprecated - use `ansys.tools.path.save_mechanical_path` instead.
    """
    return atp.save_mechanical_path(exe_loc)


client_to_server_loglevel = {
    "DEBUG": 1,
    "INFO": 2,
    "WARN": 3,
    "WARNING": 3,
    "ERROR": 4,
    "CRITICAL": 5,
}


class Mechanical(object):
    """Connects to a gRPC Mechanical server and allows commands to be passed."""

    # Required by `_name` method to be defined before __init__ be
    _ip = None
    _port = None

    def __init__(
        self,
        ip=None,
        port=None,
        timeout=60.0,
        loglevel="WARNING",
        log_file=False,
        log_mechanical=None,
        cleanup_on_exit=False,
        channel=None,
        remote_instance=None,
        keep_connection_alive=True,
        **kwargs,
    ):
        """Initialize the member variable based on the arguments.

        Parameters
        ----------
        ip : str, optional
            IP address to connect to the server.  The default is ``None``
            in which case ``localhost`` is used.
        port : int, optional
            Port to connect to the Mecahnical server. The default is ``None``,
            in which case ``10000`` is used.
        timeout : float, optional
            Maximum allowable time for connecting to the Mechanical server.
            The default is ``60.0``.
        loglevel : str, optional
            Level of messages to print to the console. The default is ``WARNING``.

            - ``ERROR`` prints only error messages.
            - ``WARNING`` prints warning and error messages.
            - ``INFO`` prints info, warning and error messages.
            - ``DEBUG`` prints debug, info, warning and error messages.

        log_file : bool, optional
            Whether to copy the messages to a file named ``logs.log``, which is
            located where the Python script is executed. The default is ``False``.
        log_mechanical : str, optional
            Path to the output file on the local disk for writing every script
            command to. The default is ``None``. However, you might set
            ``"log_mechanical='pymechanical_log.txt"`` to write all commands that are
            sent to Mechanical via PyMechanical in this file so that you can use them
            to run a script within Mechanical without PyMechanical.
        cleanup_on_exit : bool, optional
            Whether to exit Mechanical when Python exits. The default is ``False``,
            in which case Mechanical is not exited when the garbage for this Mechanical
            instance is collected.
        channel : grpc.Channel, optional
            gRPC channel to use for the connection. The default is ``None``.
            You can use this parameter as an alternative to the ``ip`` and ``port``
            parameters.
        remote_instance : ansys.platform.instancemanagement.Instance
            Corresponding remote instance when Mechanical is launched
            through PyPIM. The default is ``None``. If a remote instance
            is specified, this instance is deleted when the
            :func:`mecahnical.exit <ansys.mechanical.core.Mechanical.exit>`
            function is called.
        keep_connection_alive : bool, optional
            Whether to keep the gRPC connection alive by running a background thread
            and making dummy calls for remote connections. The default is ``True``.

        Examples
        --------
        Connect to a Mechanical instance already running on locally on the
        default port (``10000``).

        >>> from ansys.mechanical import core as pymechanical
        >>> mechanical = pymechanical.Mechanical()

        Connect to a Mechanical instance running on the LAN on a default port.

        >>> mechanical = pymechanical.Mechanical('192.168.1.101')

        Connect to a Mechanical instance running on the LAN on a non-default port.

        >>> mechanical = pymechanical.Mechanical('192.168.1.101', port=60001)

        If you want to customize the channel, you can connect directly to gRPC channels.
        For example, if you want to create an insecure channel with a maximum message
        length of 8 MB, you would run:

        >>> import grpc
        >>> channel_temp = grpc.insecure_channel(
        ...     '127.0.0.1:10000',
        ...     options=[
        ...         ("grpc.max_receive_message_length", 8*1024**2),
        ...     ],
        ... )
        >>> mechanical = pymechanical.Mechanical(channel=channel_temp)
        """
        self._remote_instance = remote_instance
        self._channel = channel
        self._keep_connection_alive = keep_connection_alive

        self._locked = False  # being used within MechanicalPool

        # ip could be a machine name. Convert it to an IP address.
        ip_temp = ip
        if channel is not None:
            if ip is not None or port is not None:
                raise ValueError(
                    "If `channel` is specified, neither `port` nor `ip` can be specified."
                )
        elif ip is None:
            ip_temp = "127.0.0.1"
        else:
            ip_temp = socket.gethostbyname(ip)  # Converting ip or host name to ip

        self._ip = ip_temp
        self._port = port

        self._start_parm = kwargs

        self._cleanup_on_exit = cleanup_on_exit
        self._busy = False  # used to check if running a command on the server

        self._local = ip_temp in ["127.0.0.1", "127.0.1.1", "localhost"]
        if "local" in kwargs:  # pragma: no cover  # allow this to be overridden
            self._local = kwargs["local"]

        self._health_response_queue = None
        self._exiting = False
        self._exited = None

        self._version = None

        if port is None:
            port = MECHANICAL_DEFAULT_PORT
            self._port = port

        self._stub = None
        self._timeout = timeout

        if channel is None:
            self._channel = self._create_channel(ip_temp, port)
        else:
            self._channel = channel

        self._logLevel = loglevel
        self._log_file = log_file
        self._log_mechanical = log_mechanical

        self._log = LOG.add_instance_logger(self.name, self, level=loglevel)  # instance logger
        # adding a file handler to the logger
        if log_file:
            if not isinstance(log_file, str):
                log_file = "instance.log"
            self._log.log_to_file(filename=log_file, level=loglevel)

        self._log_file_mechanical = log_mechanical
        if log_mechanical:
            if not isinstance(log_mechanical, str):
                self._log_file_mechanical = "pymechanical_log.txt"
            else:
                self._log_file_mechanical = log_mechanical

        # temporarily disable logging
        # useful when we run some dummy calls
        self._disable_logging = False

        if self._local:
            self.log_info("Mechanical connection is treated as local.")
        else:
            self.log_info("Mechanical connection is treated as remote.")

        # connect and validate to the channel
        self._multi_connect(timeout=timeout)
        self.log_info("Mechanical is ready to accept grpc calls.")
        self._rpc_type = "grpc"

    def __del__(self):  # pragma: no cover
        """Clean up on exit."""
        if self._cleanup_on_exit:
            try:
                self.exit(force=True)
            except grpc.RpcError as e:
                self.log_error(f"exit: {e}")

    # def _set_log_level(self, level):
    #     """Set an alias for the log level."""
    #     self.set_log_level(level)

    @property
    def log(self):
        """Log associated with the current Mechanical instance."""
        return self._log

    @property
    def version(self) -> str:
        """Get the Mechanical version based on the instance.

        Examples
        --------
        Get the version of the connected Mechanical instance.

        >>> mechanical.version
        '251'
        """
        if self._version is None:
            try:
                self._disable_logging = True
                script = (
                    'clr.AddReference("Ans.Utilities")\n'
                    "import Ansys\n"
                    "config = Ansys.Utilities.ApplicationConfiguration.DefaultConfiguration\n"
                    "config.VersionInfo.VersionString"
                )
                self._version = self.run_python_script(script)
            except grpc.RpcError:  # pragma: no cover
                raise
            finally:
                self._disable_logging = False
        return self._version

    @property
    def name(self):
        """Name (unique identifier) of the Mechanical instance."""
        try:
            if self._channel is not None:
                if self._remote_instance is not None:  # pragma: no cover
                    return f"GRPC_{self._channel._channel._channel.target().decode()}"
                else:
                    return f"GRPC_{self._channel._channel.target().decode()}"
        except Exception as e:  # pragma: no cover
            LOG.error(f"Error getting the Mechanical instance name: {str(e)}")

        return f"GRPC_instance_{id(self)}"  # pragma: no cover

    @property
    def busy(self):
        """Return True when the Mechanical gRPC server is executing a command."""
        return self._busy

    @property
    def locked(self):
        """Instance is in use within a pool."""
        return self._locked

    @locked.setter
    def locked(self, new_value):
        """Instance is in use within a pool."""
        self._locked = new_value

    def _multi_connect(self, n_attempts=5, timeout=60):
        """Try to connect over a series of attempts to the channel.

        Parameters
        ----------
        n_attempts : int, optional
            Number of connection attempts. The default is ``5``.
        timeout : float, optional
            Maximum allowable time in seconds for establishing a connection.
            The default is ``60``.
        """
        # This prevents a single failed connection from blocking other attempts
        connected = False
        attempt_timeout = timeout / n_attempts
        self.log_debug(
            f"timetout:{timeout} n_attempts:{n_attempts} attempt_timeout={attempt_timeout}"
        )

        max_time = time.time() + timeout
        i = 1
        while time.time() < max_time and i <= n_attempts:
            self.log_debug(f"Connection attempt {i} with attempt timeout {attempt_timeout}s")
            connected = self._connect(timeout=attempt_timeout)

            if connected:
                self.log_debug(f"Connection attempt {i} succeeded.")
                break

            i += 1
        else:  # pragma: no cover
            self.log_debug(
                f"Reached either maximum amount of connection attempts "
                f"({n_attempts}) or timeout ({timeout} s)."
            )

        if not connected:  # pragma: no cover
            raise IOError(f"Unable to connect to Mechanical instance at {self._channel_str}.")

    @property
    def _channel_str(self):
        """Target string, generally in the form of ``ip:port``, such as ``127.0.0.1:10000``."""
        if self._channel is not None:
            if self._remote_instance is not None:
                return self._channel._channel._channel.target().decode()  # pragma: no cover
            else:
                return self._channel._channel.target().decode()
        return ""  # pragma: no cover

    def _connect(self, timeout=12, enable_health_check=False):
        """Connect a gRPC channel to a remote or local Mechanical instance.

        Parameters
        ----------
        timeout : float
            Maximum allowable time in seconds for establishing a connection. The
            default is ``12``.
        enable_health_check : bool, optional
            Whether to enable a check to see if the connection is healthy.
            The default is ``False``.
        """
        self._state = grpc.channel_ready_future(self._channel)
        self._stub = mechanical_pb2_grpc.MechanicalServiceStub(self._channel)

        # verify connection
        time_start = time.time()
        while ((time.time() - time_start) < timeout) and not self._state._matured:
            time.sleep(0.01)

        if not self._state._matured:  # pragma: no cover
            return False

        self.log_debug("Established a connection to the Mechanical gRPC server.")

        self.wait_till_mechanical_is_ready(timeout)

        # keeps Mechanical session alive
        self._timer = None
        if not self._local and self._keep_connection_alive:  # pragma: no cover
            self._initialised = threading.Event()
            self._t_trigger = time.time()
            self._t_delay = 30
            self._timer = threading.Thread(
                target=Mechanical._threaded_heartbeat, args=(weakref.proxy(self),)
            )
            self._timer.daemon = True
            self._timer.start()

        # enable health check
        if enable_health_check:  # pragma: no cover
            self._enable_health_check()

        self.__server_version = None

        return True

    def _enable_health_check(self):  # pragma: no cover
        """Place the status of the health check in the health response queue."""
        # lazy imports here to speed up module load
        from grpc_health.v1 import health_pb2, health_pb2_grpc

        def _consume_responses(response_iterator, response_queue):
            try:
                for response in response_iterator:
                    response_queue.put(response)
                # NOTE: We're doing absolutely nothing with this as
                # this point since the server-side health check
                # doesn't change state.
            except Exception:
                if self._exiting:
                    return
                self._exited = True
                raise MechanicalExitedError(
                    "Lost connection with the Mechanical gRPC server."
                ) from None

        # enable health check
        from queue import Queue

        request = health_pb2.HealthCheckRequest()
        self._health_stub = health_pb2_grpc.HealthStub(self._channel)
        rendezvous = self._health_stub.Watch(request)

        # health check feature implemented after 2023 R1
        try:
            status = rendezvous.next()
        except Exception as err:
            if err.code().name != "UNIMPLEMENTED":
                raise err
            return

        if status.status != health_pb2.HealthCheckResponse.SERVING:
            raise MechanicalRuntimeError(
                "Cannot enable health check and/or connect to the Mechanical server."
            )

        self._health_response_queue = Queue()

        # allow main process to exit by setting daemon to true
        thread = threading.Thread(
            target=_consume_responses,
            args=(rendezvous, self._health_response_queue),
            daemon=True,
        )
        thread.start()

    def _threaded_heartbeat(self):  # pragma: no cover
        """To call from a thread to verify that a Mechanical instance is alive."""
        self._initialised.set()
        while True:
            if self._exited:
                break
            try:
                time.sleep(self._t_delay)
                if not self.is_alive:
                    break
            except ReferenceError:
                break
            # except Exception:
            #     continue

    def _create_channel(self, ip, port):
        """Create an unsecured gRPC channel."""
        check_valid_ip(ip)

        # open the channel
        channel_str = f"{ip}:{port}"
        LOG.debug(f"Opening insecure channel at {channel_str}.")
        return grpc.insecure_channel(
            channel_str,
            options=[
                ("grpc.max_receive_message_length", MAX_MESSAGE_LENGTH),
            ],
        )

    @property
    def is_alive(self) -> bool:
        """Whether there is an active connection to the Mechanical gRPC server."""
        if self._exited:
            return False

        if self._busy:  # pragma: no cover
            return True

        try:  # pragma: no cover
            self._make_dummy_call()
            return True
        except grpc.RpcError:
            return False

    @staticmethod
    def set_log_level(loglevel):
        """Set the log level.

        Parameters
        ----------
        loglevel : str, int
            Level of logging. Options are ``"DEBUG"``, ``"INFO"``, ``"WARNING"``
            and ``"ERROR"``.

        Examples
        --------
        Set the log level to the ``"DEBUG"`` level.

        # >>> mechanical.set_log_level('DEBUG')
        #
        # Set the log level to info
        #
        # >>> mechanical.set_log_level('INFO')
        #
        # Set the log level to warning
        #
        # >>> mechanical.set_log_level('WARNING')
        #
        # Set the log level to error
        #
        # >>> mechanical.set_log_level('ERROR')
        """
        if isinstance(loglevel, str):
            loglevel = loglevel.upper()
        setup_logger(loglevel=loglevel)

    def get_product_info(self):
        """Get product information by running a script on the Mechanical gRPC server."""

        def _get_jscript_product_info_command():
            return (
                'ExtAPI.Application.ScriptByName("jscript").ExecuteCommand'
                '("var productInfo = DS.Script.getProductInfo();returnFromScript(productInfo);")'
            )

        def _get_python_product_info_command():
            return (
                'clr.AddReference("Ansys.Mechanical.Application")\n'
                "Ansys.Mechanical.Application.ProductInfo.ProductInfoAsString"
            )

        try:
            self._disable_logging = True
            if int(self.version) >= 232:
                script = _get_python_product_info_command()
            else:
                script = _get_jscript_product_info_command()
            return self.run_python_script(script)
        except grpc.RpcError:
            raise
        finally:
            self._disable_logging = False

    @suppress_logging
    def __repr__(self):
        """Get the user-readable string form of the Mechanical instance."""
        try:
            if self._exited:
                return "Mechanical exited."
            return self.get_product_info()
        except grpc.RpcError:
            return "Error getting product info."

    def launch(self, cleanup_on_exit=True):
        """Launch Mechanical in batch or UI mode.

        Parameters
        ----------
        cleanup_on_exit : bool, optional
            Whether to exit Mechanical when Python exits. The default is ``True``.
            When ``False``, Mechanical is not exited when the garbage for this
            Mechanical instance is collected.
        """
        if not self._local:
            raise RuntimeError("Can only launch with a local instance of Mechanical.")

        # let us respect the current cleanup behavior
        if self._cleanup_on_exit:
            self.exit()

        exec_file = self._start_parm.get("exec_file", get_mechanical_path(allow_input=False))
        batch = self._start_parm.get("batch", True)
        additional_switches = self._start_parm.get("additional_switches", None)
        additional_envs = self._start_parm.get("additional_envs", None)
        port = launch_grpc(
            exec_file=exec_file,
            batch=batch,
            additional_switches=additional_switches,
            additional_envs=additional_envs,
            verbose=True,
        )
        # update the new cleanup behavior
        self._cleanup_on_exit = cleanup_on_exit
        self._port = port
        self._channel = self._create_channel(self._ip, port)
        self._connect(port)

        self.log_info("Mechanical is ready to accept gRPC calls.")

    def wait_till_mechanical_is_ready(self, wait_time=-1):
        """Wait until Mechanical is ready.

        Parameters
        ----------
        wait_time : float, optional
            Maximum allowable time in seconds for connecting to the Mechanical gRPC server.
        """
        time_1 = datetime.datetime.now()

        sleep_time = 0.5
        if wait_time == -1:  # pragma: no cover
            self.log_info("Waiting for Mechanical to be ready...")
        else:
            self.log_info(f"Waiting for Mechanical to be ready. Maximum wait time: {wait_time}s")

        while not self.__isMechanicalReady():
            time_2 = datetime.datetime.now()
            time_interval = time_2 - time_1
            time_interval_seconds = int(time_interval.total_seconds())

            self.log_debug(
                f"Mechanical is not ready. You've been waiting for {time_interval_seconds}."
            )
            if self._timeout != -1:
                if time_interval_seconds > wait_time:
                    self.log_debug(
                        f"Allowed wait time {wait_time}s. "
                        f"Waited so for {time_interval_seconds}s, "
                        f"before throwing the error."
                    )
                    raise RuntimeError(
                        f"Couldn't connect to Mechanical. " f"Waited for {time_interval_seconds}s."
                    )

            time.sleep(sleep_time)

        time_2 = datetime.datetime.now()
        time_interval = time_2 - time_1
        time_interval_seconds = int(time_interval.total_seconds())

        self.log_info(f"Mechanical is ready. It took {time_interval_seconds} seconds to verify.")

    def __isMechanicalReady(self):
        """Whether the Mechanical gRPC server is ready.

        Returns
        -------
        bool
            ``True`` if Mechanical is ready, ``False`` otherwise.
        """
        try:
            script = "ExtAPI.DataModel.Project.ProductVersion"
            self.run_python_script(script)
        except grpc.RpcError as error:
            self.log_debug(f"Mechanical is not ready. Error:{error}.")
            return False

        return True

    @staticmethod
    def convert_to_server_log_level(log_level):
        """Convert the log level to the server log level.

        Parameters
        ----------
        log_level : str
            Level of logging. Options are ``"DEBUG"``, ``"INFO"``, ``"WARNING"``,
            ``"ERROR"``, and ``"CRITICAL"``.

        Returns
        -------
            Converted log level for the server.
        """
        value = client_to_server_loglevel.get(log_level)

        if value is not None:
            return value

        raise ValueError(
            f"Log level {log_level} is invalid. Possible values are "
            f"'DEBUG','INFO', 'WARNING', 'ERROR', and 'CRITICAL'."
        )

    def run_python_script(
        self, script_block: str, enable_logging=False, log_level="WARNING", progress_interval=2000
    ):
        """Run a Python script block inside Mechanical.

        It returns the string value of the last executed statement. If the value cannot be
        returned as a string, it will return an empty string.

        Parameters
        ----------
        script_block : str
            Script block (one or more lines) to run.
        enable_logging: bool, optional
            Whether to enable logging. The default is ``False``.
        log_level: str
            Level of logging. The default is ``"WARNING"``. Options are ``"DEBUG"``,
            ``"INFO"``, ``"WARNING"``, and ``"ERROR"``.
        progress_interval: int, optional
            Frequency in milliseconds for getting log messages from the server.
            The default is ``2000``.

        Returns
        -------
        str
            Script result.

        Examples
        --------
        Return a value from a simple calculation.

        >>> mechanical.run_python_script('2+3')
        '5'

        Return a string value from Project object.

        >>> mechanical.run_python_script('ExtAPI.DataModel.Project.ProductVersion')
        '2025 R1'

        Return an empty string, when you try to return the Project object.

        >>> mechanical.run_python_script('ExtAPI.DataModel.Project')
        ''

        Return an empty string for assignments.

        >>> mechanical.run_python_script('version = ExtAPI.DataModel.Project.ProductVersion')
        ''

        Return value from the last executed statement from a variable.

        >>> script='''
            addition = 2 + 3
            multiplication = 3 * 4
            multiplication
            '''
        >>> mechanical.run_python_script(script)
        '12'

        Return value from last executed statement from a function call.

        >>> script='''
            import math
            math.pow(2,3)
            '''
        >>> mechanical.run_python_script(script)
        '8'

        Handle an error scenario.

        >>> script = 'hello_world()'
        >>> import grpc
        >>> try:
                mechanical.run_python_script(script)
            except grpc.RpcError as error:
                print(error.details())
        name 'hello_world' is not defined

        """
        self.verify_valid_connection()
        result_as_string = self.__call_run_python_script(
            script_block, enable_logging, log_level, progress_interval
        )
        return result_as_string

    def run_python_script_from_file(
        self, file_path, enable_logging=False, log_level="WARNING", progress_interval=2000
    ):
        """Run the contents a python file inside Mechanical.

        It returns the string value of the last executed statement. If the value cannot be
        returned as a string, it will return an empty string.

        Parameters
        ----------
        file_path :
            Path for the Python file.
        enable_logging: bool, optional
            Whether to enable logging. The default is ``False``.
        log_level: str
            Level of logging. The default is ``"WARNING"``. Options are ``"DEBUG"``,
            ``"INFO"``, ``"WARNING"``, and ``"ERROR"``.
        progress_interval: int, optional
            Frequency in milliseconds for getting log messages from the server.
            The default is ``2000``.

        Returns
        -------
        str
            Script result.

        Examples
        --------
        Return a value from a simple calculation.

        Contents of **simple.py** file

        2+3

        >>> mechanical.run_python_script_from_file('simple.py')
        '5'

        Return a value from a simple function call.

        Contents of  **test.py** file

        import math

        math.pow(2,3)

        >>> mechanical.run_python_script_from_file('test.py')
        '8'

        """
        self.verify_valid_connection()
        self.log_debug(f"run_python_script_from_file started")
        script_code = Mechanical.__readfile(file_path)
        self.log_debug(f"run_python_script_from_file started")
        return self.run_python_script(script_code, enable_logging, log_level, progress_interval)

    def exit(self, force=False):
        """Exit Mechanical.

        Parameters
        ----------
        force : bool, optional
            Whether to force Mechanical to exit. The default is ``False``, in which case
            only Mechanical in UI mode asks for confirmation. This parameter overrides
            any environment variables that may inhibit exiting Mechanical.

        Examples
        --------
        Exit Mechanical.

        >>> mechanical.Exit(force=True)

        """
        if not force:
            if not get_start_instance():
                self.log_info("Ignoring exit due to PYMECHANICAL_START_INSTANCE=False")
                return

            # or building the gallery
            if pymechanical.BUILDING_GALLERY:
                self._log.info("Ignoring exit due to BUILDING_GALLERY=True")
                return

        if self._exited:
            return

        self.verify_valid_connection()

        self._exiting = True

        self.log_debug("In shutdown.")
        request = mechanical_pb2.ShutdownRequest(force_exit=force)
        self.log_debug("Shutting down...")

        self._busy = True
        try:
            self._stub.Shutdown(request)
        except grpc._channel._InactiveRpcError as error:
            self.log_warning("Mechanical exit failed: {str(error}.")
        finally:
            self._busy = False

        self._exited = True
        self._stub = None

        if self._remote_instance is not None:  # pragma: no cover
            self.log_debug("PyPIM delete has started.")
            try:
                self._remote_instance.delete()
            except Exception as error:
                self.log_warning("Remote instance delete failed: {str(error}.")
            self.log_debug("PyPIM delete has finished.")

            self._remote_instance = None
            self._channel = None
        else:
            self.log_debug("No PyPIM cleanup is needed.")

        local_ports = pymechanical.LOCAL_PORTS
        if self._local and self._port in local_ports:
            local_ports.remove(self._port)

        self.log_info("Shutdown has finished.")

    @protect_grpc
    def upload(
        self,
        file_name,
        file_location_destination=None,
        chunk_size=DEFAULT_FILE_CHUNK_SIZE,
        progress_bar=True,
    ):
        """Upload a file to the Mechanical instance.

        Parameters
        ----------
        file_name : str
            Local file to upload. Only the file name is needed if the file
            is relative to the current working directory. Otherwise, the full path
            is needed.
        file_location_destination : str, optional
            File location on the Mechanical server to upload the file to. The default is
            ``None``, in which case the project directory is used.
        chunk_size : int, optional
            Chunk size in bytes. The default is ``1048576``.
        progress_bar : bool, optional
            Whether to show a progress bar using ``tqdm``. The default is ``True``.
            A progress bar is helpful for viewing upload progress.

        Returns
        -------
        str
            Base name of the uploaded file.

        Examples
        --------
        Upload the ``hsec.x_t`` file  with the progress bar not shown.

        >>> mechanical.upload('hsec.x_t', progress_bar=False)
        """
        self.verify_valid_connection()

        if not os.path.isfile(file_name):
            raise FileNotFoundError(f"Unable to locate filename {file_name}.")

        self._log.debug(f"Uploading file '{file_name}' to the Mechanical instance.")

        if file_location_destination is None:
            file_location_destination = self.project_directory

        self._busy = True
        try:
            chunks_generator = self.get_file_chunks(
                file_location_destination,
                file_name,
                chunk_size=chunk_size,
                progress_bar=progress_bar,
            )
            response = self._stub.UploadFile(chunks_generator)
            self.log_debug(f"upload_file response is {response.is_ok}.")
        finally:
            self._busy = False

        if not response.is_ok:  # pragma: no cover
            raise IOError("File failed to upload.")
        return os.path.basename(file_name)

    def get_file_chunks(self, file_location, file_name, chunk_size, progress_bar):
        """Construct the file upload request for the server.

        Parameters
        ----------
        file_location_destination : str, optional
            Directory where the file to upload to the server is located.
        file_name : str
            Name of the file to upload.
        chunk_size : int
            Chunk size in bytes.
        progress_bar : bool
            Whether to show a progress bar using ``tqdm``.
        """
        pbar = None
        if progress_bar:
            if not _HAS_TQDM:  # pragma: no cover
                raise ModuleNotFoundError(
                    f"To use the keyword argument 'progress_bar', you must have "
                    f"installed the 'tqdm' package. To avoid this message, you can "
                    f"set 'progress_bar=False'."
                )

            n_bytes = os.path.getsize(file_name)

            base_name = os.path.basename(file_name)
            pbar = tqdm(
                total=n_bytes,
                desc=f"Uploading {base_name} to {self._channel_str}:{file_location}.",
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
            )

        with open(file_name, "rb") as f:
            while True:
                piece = f.read(chunk_size)
                length = len(piece)
                if length == 0:
                    if pbar is not None:
                        pbar.close()
                    return

                if pbar is not None:
                    pbar.update(length)

                chunk = mechanical_pb2.Chunk(payload=piece, size=length)
                yield mechanical_pb2.FileUploadRequest(
                    file_name=os.path.basename(file_name), file_location=file_location, chunk=chunk
                )

    @property
    def project_directory(self):
        """Get the project directory for the currently connected Mechanical instance.

        Examples
        --------
        Get the project directory of the connected Mechanical instance.

        >>> mechanical.project_directory
        '/tmp/ANSYS.username.1/AnsysMech3F97/Project_Mech_Files/'

        """
        return self.run_python_script("ExtAPI.DataModel.Project.ProjectDirectory")

    def list_files(self):
        """List the files in the working directory of Mechanical.

        Returns
        -------
        list
            List of files in the working directory of Mechanical.

        Examples
        --------
        List the files in the working directory.

        >>> files = mechanical.list_files()
        >>> for file in files: print(file)
        """
        result = self.run_python_script(
            "import pymechanical_helpers\npymechanical_helpers.GetAllProjectFiles(ExtAPI)"
        )

        files_out = result.splitlines()
        if not files_out:  # pragma: no cover
            self.log_warning("No files listed")
        return files_out

    def _get_files(self, files, recursive=False):
        self_files = self.list_files()  # to avoid calling it too much

        if isinstance(files, str):
            if self._local:  # pragma: no cover
                # in local mode
                if os.path.exists(files):
                    if not os.path.isabs(files):
                        list_files = [os.path.join(os.getcwd(), files)]
                    else:
                        # file exist
                        list_files = [files]
                elif "*" in files:
                    # using filter
                    list_files = glob.glob(files, recursive=recursive)
                    if not list_files:
                        raise ValueError(
                            f"The `'files'` parameter ({files}) didn't match any file using "
                            f"glob expressions in the local client."
                        )
                else:
                    raise ValueError(
                        f"The files parameter ('{files}') does not match any file or pattern."
                    )
            else:  # Remote or looking into Mechanical working directory
                if files in self_files:
                    list_files = [files]
                elif "*" in files:
                    # try filter on the list_files
                    if recursive:
                        self.log_warning(
                            "Because the 'recursive' keyword argument does not work with "
                            "remote instances, it is ignored."
                        )
                    list_files = fnmatch.filter(self_files, files)
                    if not list_files:
                        raise ValueError(
                            f"The `'files'` parameter ({files}) didn't match any file using "
                            f"glob expressions in the remote server."
                        )
                else:
                    raise ValueError(
                        f"The `'files'` parameter ('{files}') does not match any file or pattern."
                    )

        elif isinstance(files, (list, tuple)):
            if not all([isinstance(each, str) for each in files]):
                raise ValueError(
                    "The parameter `'files'` can be a list or tuple, but it "
                    "should only contain strings."
                )
            list_files = files
        else:
            raise ValueError(
                f"The `file` parameter type ({type(files)}) is not supported."
                "Only strings, tuple of strings, or list of strings are allowed."
            )

        return list_files

    def download(
        self,
        files,
        target_dir=None,
        chunk_size=DEFAULT_CHUNK_SIZE,
        progress_bar=None,
        recursive=False,
    ):  # pragma: no cover
        """Download files from the working directory of the Mechanical instance.

         It downloads them from the working directory to the target directory. It returns the list
         of local file paths for the downloaded files.

        Parameters
        ----------
        files : str, list[str], tuple(str)
            One or more files on the Mechanical server to download. The files must be
            in the same directory as the Mechanical instance. You can use the
            :func:`Mechanical.list_files <ansys.mechanical.core.mechanical.list_files>`
            function to list current files. Alternatively, you can specify *glob expressions* to
            match file names. For example, you could use ``file*`` to match every file whose
            name starts with ``file``.
        target_dir: str
            Default directory to copy the downloaded files to. The default is ``None`` and
            current working directory will be used as target directory.
        chunk_size : int, optional
            Chunk size in bytes. The default is ``262144``. The value must be less than 4 MB.
        progress_bar : bool, optional
            Whether to show a progress bar using  ``tqdm``. The default is ``None``, in
            which case a progress bar is shown. A progress bar is helpful for viewing download
            progress.
        recursive : bool, optional
            Whether to use recursion when using a glob pattern search. The default is ``False``.

        Returns
        -------
        List[str]
            List of local file paths.

        Notes
        -----
        There are some considerations to keep in mind when using the ``download()`` method:

        * The glob pattern search does not search recursively in remote instances.
        * In a remote instance, it is not possible to list or download files in a
          location other than the Mechanical working directory.
        * If you are connected to a local instance and provide a file path, downloading files
          from a different folder is allowed but is not recommended.

        Examples
        --------
        Download a single file.

        >>> local_file_path_list = mechanical.download('file.out')

        Download all files starting with ``file``.

        >>> local_file_path_list = mechanical.download('file*')

        Download every file in the Mechanical working directory.

        >>> local_file_path_list = mechanical.download('*.*')

        Alternatively, the recommended method is to use the
        :func:`download_project() <ansys.mechanical.core.mechanical.Mechanical.download_project>`
        method to download all files.

        >>> local_file_path_list = mechanical.download_project()

        """
        self.verify_valid_connection()

        if chunk_size > 4 * 1024 * 1024:  # 4MB
            raise ValueError(
                "Chunk sizes bigger than 4 MB can generate unstable behaviour in PyMechanical. "
                "Decrease the ``chunk_size`` value."
            )

        list_files = self._get_files(files, recursive=recursive)

        if target_dir:
            path = pathlib.Path(target_dir)
            path.mkdir(parents=True, exist_ok=True)
        else:
            target_dir = os.getcwd()

        out_files = []

        for each_file in list_files:
            try:
                file_name = os.path.basename(each_file)  # Getting only the name of the file.
                #  We try to avoid that when the full path is supplied. It crashes when trying
                # to do `os.path.join(target_dir"os.getcwd()", file_name "full filename path"`
                # This produces the file structure to flat out, but it is fine,
                # because recursive does not work in remote.
                self._busy = True
                out_file_path = self._download(
                    each_file,
                    out_file_name=os.path.join(target_dir, file_name),
                    chunk_size=chunk_size,
                    progress_bar=progress_bar,
                )
                out_files.append(out_file_path)
            except FileNotFoundError:
                # So far the gRPC interface returns the size of the file equal
                # zero, if the file does not exist, or if its size is zero,
                # but they are two different things.
                # In theory, since we are obtaining the files name from
                # `mechanical.list_files()`, they do exist, so
                # if there is any error, it means their size is zero.
                pass  # This is not the best.
            finally:
                self._busy = False

        return out_files

    @protect_grpc
    def _download(
        self,
        target_name,
        out_file_name,
        chunk_size=DEFAULT_CHUNK_SIZE,
        progress_bar=None,
    ):
        """Download a file from the Mechanical instance.

        Parameters
        ----------
        target_name : str
            Name of the target file on the server. The file must be in the same
            directory as the Mechanical instance. You can use the
            ``mechanical.list_files()`` function to list current files.
        out_file_name : str
            Name of the output file if the name is to differ from that for the target
            file.
        chunk_size : int, optional
            Chunk size in bytes. The default is ``"DEFAULT_CHUNK_SIZE"``, in which case
            256 kB is used. The value must be less than 4 MB.
        progress_bar : bool, optional
            Whether to show a progress bar using  ``tqdm``. The default is ``None``, in
            which case a progress bar is shown. A progress bar is helpful for showing download
            progress.

        Examples
        --------
        Download the remote result file "file.rst" as "my_result.rst".

        >>> mechanical.download('file.rst', 'my_result.rst')
        """
        self.verify_valid_connection()

        if not progress_bar and _HAS_TQDM:
            progress_bar = True

        request = mechanical_pb2.FileDownloadRequest(file_path=target_name, chunk_size=chunk_size)

        responses = self._stub.DownloadFile(request)

        file_size = self.save_chunks_to_file(
            responses, out_file_name, progress_bar=progress_bar, target_name=target_name
        )

        if not file_size:  # pragma: no cover
            raise FileNotFoundError(f'File "{out_file_name}" is empty or does not exist')

        self.log_info(f"{out_file_name} with size {file_size} has been written.")

        return out_file_name

    def save_chunks_to_file(self, responses, filename, progress_bar=False, target_name=""):
        """Save chunks to a local file.

        Parameters
        ----------
        responses :
        filename : str
            Name of the local file to save chunks to.
        progress_bar : bool, optional
            Whether to show a progress bar using  ``tqdm``. The default is ``False``.
        target_name : str, optional
            Name of the target file on the server. The default is ``""``. The file
            must be in the same directory as the Mechanical instance. You can use the
            ``mechanical.list_files()`` function to list current files.

        Returns
        -------
        file_size : int
            File size saved in bytes.  If ``0`` is returned, no file was written.
        """
        pbar = None
        if progress_bar:
            if not _HAS_TQDM:  # pragma: no cover
                raise ModuleNotFoundError(
                    "To use the keyword argument 'progress_bar', you need to have installed "
                    "the 'tqdm' package.To avoid this message you can set 'progress_bar=False'."
                )

        file_size = 0
        with open(filename, "wb") as f:
            for response in responses:
                f.write(response.chunk.payload)
                payload_size = len(response.chunk.payload)
                file_size += payload_size
                if pbar is None:
                    pbar = tqdm(
                        total=response.file_size,
                        desc=f"Downloading {self._channel_str}:{target_name} to {filename}",
                        unit="B",
                        unit_scale=True,
                        unit_divisor=1024,
                    )
                    pbar.update(payload_size)
                else:
                    pbar.update(payload_size)

        if pbar is not None:
            pbar.close()

        return file_size

    def download_project(self, extensions=None, target_dir=None, progress_bar=False):
        """Download all project files in the working directory of the Mechanical instance.

        It downloads them from the working directory to the target directory. It returns the list
        of local file paths for the downloaded files.

        Parameters
        ----------
        extensions : list[str], tuple[str], optional
            List of extensions for filtering files before downloading them. The
            default is ``None``.
        target_dir : str, optional
            Path for downloading the files to. The default is ``None``.
        progress_bar : bool, optional
            Whether to show a progress bar using ``tqdm``. The default is ``False``.
            A progress bar is helpful for viewing download progress.

        Returns
        -------
        List[str]
            List of local file paths.

        Examples
        --------
        Download all the files in the project.

        >>> local_file_path_list = mechanical.download_project()
        """
        destination_directory = target_dir.rstrip("\\/")

        # let us create the directory, if it doesn't exist
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

        project_directory = self.project_directory
        # remove the trailing slash - server could be windows or linux
        project_directory = project_directory.rstrip("\\/")

        # this is where .mechddb resides
        parent_directory = os.path.dirname(project_directory)

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
                    file_temp = os.path.join(project_directory, "**", f"*.{each_extension}")

                if self._local:
                    list_files_expanded = self._get_files(file_temp, recursive=True)

                    if "mechdb" == each_extension.lower():
                        # if we have more than one .mechdb in the parent folder
                        # filter to have only the current mechdb
                        self_files = self.list_files()
                        filtered_files = []
                        for temp_file in list_files_expanded:
                            if temp_file in self_files:
                                filtered_files.append(temp_file)
                        list_files = filtered_files
                    else:
                        list_files = list_files_expanded
                else:
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

    def clear(self):
        """Clear the database.

        Examples
        --------
        Clear the database.

        >>> mechanical.clear()

        """
        self.run_python_script("ExtAPI.DataModel.Project.New()")

    def _make_dummy_call(self):
        try:
            self._disable_logging = True
            self.run_python_script("ExtAPI.DataModel.Project.ProjectDirectory")
        except grpc.RpcError:  # pragma: no cover
            raise
        finally:
            self._disable_logging = False

    @staticmethod
    def __readfile(file_path):
        """Get the contents of the file as a string."""
        # open text file in read mode
        text_file = open(file_path, "r", encoding="utf-8")
        # read whole file to a string
        data = text_file.read()
        # close file
        text_file.close()

        return data

    def __call_run_python_script(
        self, script_code: str, enable_logging, log_level, progress_interval
    ):
        """Run the Python script block on the server.

        Parameters
        ----------
        script_block : str
            Script block (one or more lines) to run.
        enable_logging: bool
            Whether to enable logging
        log_level: str
            Level of logging. Options are ``"DEBUG"``, ``"INFO"``, ``"WARNING"``,
            and ``"ERROR"``.
        timeout: int, optional
            Frequency in milliseconds for getting log messages from the server.

        Returns
        -------
        str
            Script result.

        """
        log_level_server = self.convert_to_server_log_level(log_level)
        request = mechanical_pb2.RunScriptRequest()
        request.script_code = script_code
        request.enable_logging = enable_logging
        request.logger_severity = log_level_server
        request.progress_interval = progress_interval

        result = ""
        self._busy = True

        try:
            for runscript_response in self._stub.RunPythonScript(request):
                if runscript_response.log_info == "__done__":
                    result = runscript_response.script_result
                    break
                else:
                    if enable_logging:
                        self.log_message(log_level, runscript_response.log_info)
        except grpc.RpcError as error:
            error_info = error.details()
            error_info_lower = error_info.lower()
            # For the given script, return value cannot be converted to string.
            if (
                "the expected result" in error_info_lower
                and "cannot be return via this API." in error_info
            ):
                if enable_logging:
                    self.log_debug(f"Ignoring the conversion error.{error_info}")
                result = ""
            else:
                raise
        finally:
            self._busy = False

        self._log_mechanical_script(script_code)

        return result

    def log_message(self, log_level, message):
        """Log the message using the given log level.

         Parameters
        ----------
        log_level: str
            Level of logging. Options are ``"DEBUG"``, ``"INFO"``, ``"WARNING"``,
            and ``"ERROR"``.
        message : str
            Message to log.

        Examples
        --------
        Log a debug message.

        >>> mechanical.log_message('DEBUG', 'debug message')

        Log an info message.

        >>> mechanical.log_message('INFO', 'info message')

        """
        if log_level == "DEBUG":
            self.log_debug(message)
        elif log_level == "INFO":
            self.log_info(message)
        elif log_level == "WARNING":
            self.log_warning(message)
        elif log_level == "ERROR":
            self.log_error(message)

    def log_debug(self, message):
        """Log the debug message."""
        if self._disable_logging:
            return
        self._log.debug(message)

    def log_info(self, message):
        """Log the info message."""
        if self._disable_logging:
            return
        self._log.info(message)

    def log_warning(self, message):
        """Log the warning message."""
        if self._disable_logging:
            return
        self._log.warning(message)

    def log_error(self, message):
        """Log the error message."""
        if self._disable_logging:
            return
        self._log.error(message)

    def verify_valid_connection(self):
        """Verify whether the connection to Mechanical is valid."""
        if self._exited:
            raise MechanicalExitedError("Mechanical has already exited.")

        if self._stub is None:  # pragma: no cover
            raise ValueError(
                "There is not a valid connection to Mechanical. Launch or connect to it first."
            )

    @property
    def exited(self):
        """Whether Mechanical already exited."""
        return self._exited

    def _log_mechanical_script(self, script_code):
        if self._disable_logging:
            return

        if self._log_file_mechanical:
            try:
                with open(self._log_file_mechanical, "a", encoding="utf-8") as file:
                    file.write(script_code)
                    file.write("\n")
            except IOError as e:  # pragma: no cover
                self.log_warning(f"I/O error({e.errno}): {e.strerror}")
            except Exception as e:  # pragma: no cover
                self.log_warning("Unexpected error:" + str(e))


def get_start_instance(start_instance_default=True):
    """Check if the ``PYMECHANICAL_START_INSTANCE`` environment variable exists and is valid.

    Parameters
    ----------
    start_instance_default : bool, optional
        Value to return when ``PYMECHANICAL_START_INSTANCE`` is unset.

    Returns
    -------
    bool
        ``True`` when the ``PYMECHANICAL_START_INSTANCE`` environment variable exists
        and is valid, ``False`` when this environment variable does not exist or is not valid.
        If it is unset, ``start_instance_default`` is returned.

    Raises
    ------
    OSError
        Raised when ``PYMECHANICAL_START_INSTANCE`` is not either ``True`` or ``False``
        (case independent).

    """
    if "PYMECHANICAL_START_INSTANCE" in os.environ:
        if os.environ["PYMECHANICAL_START_INSTANCE"].lower() not in [
            "true",
            "false",
        ]:  # pragma: no cover
            val = os.environ["PYMECHANICAL_START_INSTANCE"]
            raise OSError(
                f'Invalid value "{val}" for PYMECHANICAL_START_INSTANCE\n'
                'PYMECHANICAL_START_INSTANCE should be either "TRUE" or "FALSE"'
            )
        return os.environ["PYMECHANICAL_START_INSTANCE"].lower() == "true"
    return start_instance_default


def launch_grpc(
    exec_file="",
    batch=True,
    port=MECHANICAL_DEFAULT_PORT,
    additional_switches=None,
    additional_envs=None,
    verbose=False,
) -> int:
    """Start Mechanical locally in gRPC mode.

    Parameters
    ----------
    exec_file : str, optional
        Path for the Mechanical executable file.  The default is ``None``, in which
        case the cached location is used.
    batch : bool, optional
        Whether to launch Mechanical in batch mode. The default is ``True``.
        When ``False``, Mechanical is launched in UI mode.
    port : int, optional
        Port to launch the Mechanical instance on. The default is
        ``MECHANICAL_DEFAULT_PORT``. The final port is the first
        port available after (or including) this port.
    additional_switches : list, optional
        List of additional arguments to pass. The default is ``None``.
    additional_envs : dictionary, optional
        Dictionary of additional environment variables to pass. The default
        is ``None``.
    verbose : bool, optional
        Whether to print all output when launching and running Mechanical. The
        default is ``False``. Printing all output is not recommended unless
        you are debugging the startup of Mechanical.

    Returns
    -------
    int
        Port number that the Mechanical instance started on.

    Notes
    -----
    If ``PYMECHANICAL_START_INSTANCE`` is set to FALSE, the ``launch_mechanical``
    method looks for an existing instance of Mechanical at ``PYMECHANICAL_IP`` on port
    ``PYMECHANICAL_PORT``, with default to ``127.0.0.1`` and ``10000`` if unset.
    This is typically used for automated documentation and testing.

    Examples
    --------
    Launch Mechanical using the default configuration.

    >>> from ansys.mechanical.core import launch_mechanical
    >>> mechanical = launch_mechanical()

    Launch Mechanical using a specified executable file.

    >>> exec_file_path = 'C:/Program Files/ANSYS Inc/v251/aisol/bin/win64/AnsysWBU.exe'
    >>> mechanical = launch_mechanical(exec_file_path)

    """
    # verify version
    if atp.version_from_path("mechanical", exec_file) < 232:
        raise VersionError("The Mechanical gRPC interface requires Mechanical 2023 R2 or later.")

    # get the next available port
    local_ports = pymechanical.LOCAL_PORTS
    if port is None:
        if not local_ports:
            port = MECHANICAL_DEFAULT_PORT
        else:
            port = max(local_ports) + 1

    while port_in_use(port) or port in local_ports:
        port += 1
    local_ports.append(port)

    mechanical_launcher = MechanicalLauncher(
        batch, port, exec_file, additional_switches, additional_envs, verbose
    )
    mechanical_launcher.launch()

    return port


def launch_rpyc(
    exec_file="",
    batch=True,
    port=MECHANICAL_DEFAULT_PORT,
    additional_switches=None,
    additional_envs=None,
    verbose=False,
) -> int:
    """Start Mechanical locally in RPyC mode."""
    _version = atp.version_from_path("mechanical", exec_file)
    if _version < 232:
        raise VersionError("The Mechanical gRPC interface requires Mechanical 2023 R2 or later.")

    # get the next available port
    local_ports = pymechanical.LOCAL_PORTS
    if port is None:
        if not local_ports:
            port = MECHANICAL_DEFAULT_PORT
        else:
            port = max(local_ports) + 1

    while port_in_use(port) or port in local_ports:
        port += 1
    local_ports.append(port)

    server_script = """
import sys
from ansys.mechanical.core.embedding.rpc import MechanicalDefaultServer
server = MechanicalDefaultServer(port=int(sys.argv[1]), version=int(sys.argv[2]))
server.start()
"""
    env_copy = os.environ.copy()
    try:
        embedded_server = subprocess.Popen(
            [sys.executable, "-c", server_script, str(port), str(_version)], env=env_copy
        )  # nosec: B603
    except:
        raise RuntimeError("Unable to start the embedded server.")

    return port


def launch_remote_mechanical(
    version=None,
) -> (grpc.Channel, Optional["Instance"]):  # pragma: no cover
    """Start Mechanical remotely using the Product Instance Management (PIM) API.

    When calling this method, you must ensure that you are in an environment
    where PyPIM is configured. You can use the
    :func:`pypim.is_configured <ansys.platform.instancemanagement.is_configured>`
    method to verify that PyPIM is configured.

    Parameters
    ----------
    version : str, optional
        Mechanical version to run in the three-digit format. For example, ``"251"`` to
        run 2025 R1. The default is ``None``, in which case the server runs the latest
        installed version.

    Returns
    -------
        Tuple containing channel, remote_instance.
    """
    # Display warning if PyPIM is not installed
    if not _HAS_ANSYS_PIM:
        warnings.warn(
            "Installation of pim option required! Use ``pip install ansys-mechanical-core[pim]``."
        )
        return

    pim = pypim.connect()
    instance = pim.create_instance(product_name="mechanical", product_version=version)

    LOG.info("PyPIM wait for ready has started.")
    instance.wait_for_ready()
    LOG.info("PyPIM wait for ready has finished.")

    channel = instance.build_grpc_channel(
        options=[
            ("grpc.max_receive_message_length", MAX_MESSAGE_LENGTH),
        ]
    )

    return channel, instance


def launch_mechanical(
    allow_input=True,
    exec_file=None,
    batch=True,
    loglevel="ERROR",
    log_file=False,
    log_mechanical=None,
    additional_switches=None,
    additional_envs=None,
    start_timeout=120,
    port=None,
    ip=None,
    start_instance=None,
    verbose_mechanical=False,
    clear_on_connect=False,
    cleanup_on_exit=True,
    version=None,
    keep_connection_alive=True,
    backend="mechanical",
) -> Mechanical:
    """Start Mechanical locally.

    Parameters
    ----------
    allow_input: bool, optional
        Whether to allow user input when discovering the path to the Mechanical
        executable file.
    exec_file : str, optional
        Path for the Mechanical executable file. The default is ``None``,
        in which case the cached location is used. If PyPIM is configured
        and this parameter is set to ``None``, PyPIM launches Mechanical
        using its ``version`` parameter.
    batch : bool, optional
        Whether to launch Mechanical in batch mode. The default is ``True``.
        When ``False``, Mechanical launches in UI mode.
    loglevel : str, optional
        Level of messages to print to the console.
        Options are:

        - ``"WARNING"``: Prints only Ansys warning messages.
        - ``"ERROR"``: Prints only Ansys error messages.
        - ``"INFO"``: Prints all Ansys messages.

        The default is ``WARNING``.
    log_file : bool, optional
        Whether to copy the messages to a file named ``logs.log``, which is
        located where the Python script is executed. The default is ``False``.
    log_mechanical : str, optional
        Path to the output file on the local disk to write every script
        command to. The default is ``None``. However, you might set
        ``"log_mechanical='pymechanical_log.txt'"`` to write all commands that are
        sent to Mechanical via PyMechanical to this file. You can then use these
        commands to run a script within Mechanical without PyMechanical.
    additional_switches : list, optional
        Additional switches for Mechanical. The default is ``None``.
    additional_envs : dictionary, optional
        Dictionary of additional environment variables to pass. The default
        is ``None``.
    start_timeout : float, optional
        Maximum allowable time in seconds to connect to the Mechanical server.
        The default is ``120``.
    port : int, optional
        Port to launch the Mechanical gRPC server on. The default is ``None``,
        in which case ``10000`` is used. The final port is the first
        port available after (or including) this port. You can override the
        default behavior of this parameter with the
        ``PYMECHANICAL_PORT=<VALID PORT>`` environment variable.
    ip : str, optional
        IP address to use only when ``start_instance`` is ``False``. The
        default is ``None``, in which case ``"127.0.0.1"`` is used. If you
        provide an IP address, ``start_instance`` is set to ``False``.
        A host name can be provided as an alternative to an IP address.
    start_instance : bool, optional
        Whether to launch and connect to a new Mechanical instance. The default
        is ``None``, in which case an attempt is made to connect to an existing
        Mechanical instance at the given ``ip`` and ``port`` parameters, which have
        defaults of ``"127.0.0.1"`` and ``10000`` respectively. When ``True``,
        a local instance of Mechanical is launched. You can override the default
        behavior of this parameter with the ``PYMECHANICAL_START_INSTANCE=FALSE``
        environment variable.
    verbose_mechanical : bool, optional
        Whether to enable printing of all output when launching and running
        a Mechanical instance. The default is ``False``. This parameter should be
        set to ``True`` for debugging only as output can be tracked within
        PyMechanical.
    clear_on_connect : bool, optional
        When ``start_instance`` is ``False``, whether to clear the environment
        when connecting to Mechanical. The default is ``False``. When ``True``,
        a fresh environment is provided when you connect to Mechanical.
    cleanup_on_exit : bool, optional
        Whether to exit Mechanical when Python exits. The default is ``True``.
        When ``False``, Mechanical is not exited when the garbage for this Mechanical
        instance is collected.
    version : str, optional
        Mechanical version to run in the three-digit format. For example, ``"251"``
        for 2025 R1. The default is ``None``, in which case the server runs the
        latest installed version. If PyPIM is configured and ``exec_file=None``,
        PyPIM launches Mechanical using its ``version`` parameter.
    keep_connection_alive : bool, optional
        Whether to keep the gRPC connection alive by running a background thread
        and making dummy calls for remote connections. The default is ``True``.
    backend : str, optional
        Type of RPC to use. The default is ``"mechanical"`` which uses grpc.
        The other option is ``"python"`` which uses RPyC.

    Returns
    -------
    ansys.mechanical.core.mechanical.Mechanical
        Instance of Mechanical.

    Notes
    -----
    If the environment is configured to use `PyPIM <https://pypim.docs.pyansys.com>`_
    and ``start_instance=True``, then starting the instance is delegated to PyPIM.
    In this case, most of the preceding parameters are ignored because the server-side
    configuration is used.

    Examples
    --------
    Launch Mechanical.

    >>> from ansys.mechanical.core import launch_mechanical
    >>> mech = launch_mechanical()

    Launch Mechanical using a specified executable file.

    >>> exec_file_path = 'C:/Program Files/ANSYS Inc/v251/aisol/bin/win64/AnsysWBU.exe'
    >>> mech = launch_mechanical(exec_file_path)

    Connect to an existing Mechanical instance at IP address ``192.168.1.30`` on port
    ``50001``.

    >>> mech = launch_mechanical(start_instance=False, ip='192.168.1.30', port=50001)
    """
    # Start Mechanical with PyPIM if the environment is configured for it
    # and a directive on how to launch Mechanical was not passed.
    if _HAS_ANSYS_PIM and pypim.is_configured() and exec_file is None:  # pragma: no cover
        LOG.info("Starting Mechanical remotely. The startup configuration will be ignored.")
        channel, remote_instance = launch_remote_mechanical(version=version)
        return Mechanical(
            channel=channel,
            remote_instance=remote_instance,
            loglevel=loglevel,
            log_file=log_file,
            log_mechanical=log_mechanical,
            timeout=start_timeout,
            cleanup_on_exit=cleanup_on_exit,
            keep_connection_alive=keep_connection_alive,
        )

    if ip is None:
        ip = os.environ.get("PYMECHANICAL_IP", LOCALHOST)
    else:  # pragma: no cover
        start_instance = False
        ip = socket.gethostbyname(ip)  # Converting ip or host name to ip

    check_valid_ip(ip)  # double check

    if port is None:
        port = int(os.environ.get("PYMECHANICAL_PORT", MECHANICAL_DEFAULT_PORT))
        check_valid_port(port)

    # connect to an existing instance if enabled
    if start_instance is None:
        start_instance = check_valid_start_instance(
            os.environ.get("PYMECHANICAL_START_INSTANCE", True)
        )

        # special handling when building the gallery outside of CI. This
        # creates an instance of Mechanical the first time if PYMECHANICAL_START_INSTANCE
        # is False.
        # when you launch, treat it as local.
        # when you connect, treat it as remote. We cannot differentiate between
        # local vs container scenarios. In the container scenarios, we could be connecting
        # to a container using local ip and port
        if pymechanical.BUILDING_GALLERY:  # pragma: no cover
            # launch an instance of PyMechanical if it does not already exist and
            # starting instances is allowed
            if start_instance and GALLERY_INSTANCE[0] is None:
                mechanical = launch_mechanical(
                    start_instance=True,
                    cleanup_on_exit=False,
                    loglevel=loglevel,
                )
                GALLERY_INSTANCE[0] = {"ip": mechanical._ip, "port": mechanical._port}
                return mechanical

                # otherwise, connect to the existing gallery instance if available
            elif GALLERY_INSTANCE[0] is not None:
                mechanical = Mechanical(
                    ip=GALLERY_INSTANCE[0]["ip"],
                    port=GALLERY_INSTANCE[0]["port"],
                    cleanup_on_exit=False,
                    loglevel=loglevel,
                    local=False,
                )
                # we are connecting to the existing gallery instance,
                # we need to clear Mechanical.
                mechanical.clear()

                return mechanical

                # finally, if running on CI/CD, connect to the default instance
            else:
                mechanical = Mechanical(
                    ip=ip, port=port, cleanup_on_exit=False, loglevel=loglevel, local=False
                )
                # we are connecting for gallery generation,
                # we need to clear Mechanical.
                mechanical.clear()
                return mechanical

    if not start_instance:
        mechanical = Mechanical(
            ip=ip,
            port=port,
            loglevel=loglevel,
            log_file=log_file,
            log_mechanical=log_mechanical,
            timeout=start_timeout,
            cleanup_on_exit=cleanup_on_exit,
            keep_connection_alive=keep_connection_alive,
            local=False,
        )
        if clear_on_connect:
            mechanical.clear()

        # setting ip for the grpc server
        if ip != LOCALHOST:  # Default local ip is 127.0.0.1
            create_ip_file(ip, os.getcwd())

        return mechanical

    # verify executable
    if exec_file is None:
        exec_file = get_mechanical_path(allow_input)
        if exec_file is None:  # pragma: no cover
            raise FileNotFoundError(
                "Path to the Mechanical executable file is invalid or cache cannot be loaded. "
                "Enter a path manually by specifying a value for the "
                "'exec_file' parameter."
            )
    else:  # verify ansys exists at this location
        if not os.path.isfile(exec_file):
            raise FileNotFoundError(
                f'This path for the Mechanical executable is invalid: "{exec_file}"\n'
                "Enter a path manually by specifying a value for the "
                "'exec_file' parameter."
            )

    start_parm = {
        "exec_file": exec_file,
        "batch": batch,
        "additional_switches": additional_switches,
        "additional_envs": additional_envs,
    }

    if backend == "mechanical":
        try:
            port = launch_grpc(port=port, verbose=verbose_mechanical, **start_parm)
            start_parm["local"] = True
            mechanical = Mechanical(
                ip=ip,
                port=port,
                loglevel=loglevel,
                log_file=log_file,
                log_mechanical=log_mechanical,
                timeout=start_timeout,
                cleanup_on_exit=cleanup_on_exit,
                keep_connection_alive=keep_connection_alive,
                **start_parm,
            )
        except Exception as exception:  # pragma: no cover
            # pass
            raise exception
    elif backend == "python":
        port = launch_rpyc(port=port, **start_parm)
        from ansys.mechanical.core.embedding.rpc.client import Client

        mechanical = Client(
            "localhost", port, timeout=start_timeout, cleanup_on_exit=cleanup_on_exit
        )

    return mechanical


def connect_to_mechanical(
    ip=None,
    port=None,
    loglevel="ERROR",
    log_file=False,
    log_mechanical=None,
    connect_timeout=120,
    clear_on_connect=False,
    cleanup_on_exit=False,
    keep_connection_alive=True,
) -> Mechanical:
    """Connect to an existing Mechanical server instance.

    Parameters
    ----------
    ip : str, optional
        IP address for connecting to an existing Mechanical instance. The
        IP address defaults to ``"127.0.0.1"``.
    port : int, optional
        Port to listen on for an existing Mechanical instance. The default is ``None``,
        in which case ``10000`` is used. You can override the
        default behavior of this parameter with the
        ``PYMECHANICAL_PORT=<VALID PORT>`` environment variable.
    loglevel : str, optional
        Level of messages to print to the console.
        Options are:

        - ``"WARNING"``: Prints only Ansys warning messages.
        - ``"ERROR"``: Prints only Ansys error messages.
        - ``"INFO"``: Prints all Ansys messages.

        The default is ``WARNING``.
    log_file : bool, optional
        Whether to copy the messages to a file named ``logs.log``, which is
        located where the Python script is executed. The default is ``False``.
    log_mechanical : str, optional
        Path to the output file on the local disk to write every script
        command to. The default is ``None``. However, you might set
        ``"log_mechanical='pymechanical_log.txt'"`` to write all commands that are
        sent to Mechanical via PyMechanical to this file. You can then use these
        commands to run a script within Mechanical without PyMechanical.
    connect_timeout : float, optional
        Maximum allowable time in seconds to connect to the Mechanical server.
        The default is ``120``.
    clear_on_connect : bool, optional
        Whether to clear the Mechanical instance when connecting. The default is ``False``.
        When ``True``, a fresh environment is provided when you connect to Mechanical.
    cleanup_on_exit : bool, optional
        Whether to exit Mechanical when Python exits. The default is ``False``.
        When ``False``, Mechanical is not exited when the garbage for this Mechanical
        instance is collected.
    keep_connection_alive : bool, optional
        Whether to keep the gRPC connection alive by running a background thread
        and making dummy calls for remote connections. The default is ``True``.

    Returns
    -------
    ansys.mechanical.core.mechanical.Mechanical
        Instance of Mechanical.

    Examples
    --------
    Connect to an existing Mechanical instance at IP address ``192.168.1.30`` on port
    ``50001``..


    >>> from ansys.mechanical.core import connect_to_mechanical
    >>> pymech = connect_to_mechanical(ip='192.168.1.30', port=50001)
    """
    return launch_mechanical(
        start_instance=False,
        loglevel=loglevel,
        log_file=log_file,
        log_mechanical=log_mechanical,
        start_timeout=connect_timeout,
        port=port,
        ip=ip,
        clear_on_connect=clear_on_connect,
        cleanup_on_exit=cleanup_on_exit,
        keep_connection_alive=keep_connection_alive,
    )
