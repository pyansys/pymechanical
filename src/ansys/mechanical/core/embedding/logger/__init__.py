"""Embedding logger.

Module to interact with the built-in logging system of Mechanical.

Usage
-----

Configuring logger
~~~~~~~~~~~~~~~~~~

Configuring the logger can be done using the Configuration class, for instance:

.. code:: python
  import ansys.mechanical.core as mech
  from ansys.mechanical.core.embedding.logger import Configuration, Logger

  Configuration.configure(level=logging.INFO, to_stdout=True, base_directory=None)
  app = mech.App(version=241)

Then, the Logger class can be used to write messages to the log, for instance:

.. code:: python

   Logger.error("message")


"""

import logging
import typing

from ansys.mechanical.core.embedding import initializer
from ansys.mechanical.core.embedding.logger import api, environ, sinks

LOGGING_SINKS: typing.Set[int] = set()
LOGGING_CONTEXT: str = "PYMECHANICAL"


def _get_backend() -> typing.Union[api.APIBackend, environ.EnvironBackend]:
    """Get the appropriate logger backend.

    Before embedding is initialized, logging is configured via environment variables
    After embedding is initialized, logging is configured by making API calls into the
    mechanical logging system.
    However, the API is mostly the same in both cases, though some methods only work
    in one of the two backends.
        Setting the base directory only works before initializing
        Actually logging a message or flushing the log only works after initializing
    """
    embedding_initialized = initializer.INITIALIZED_VERSION != None
    # TODO - use abc instead of a union type?
    return api.APIBackend() if embedding_initialized else environ.EnvironBackend()


class Configuration:
    """Logger configuration for Mechanical embedding."""

    @classmethod
    def configure(cls, level=logging.WARNING, directory=None, base_directory=None, to_stdout=True):
        """Configure the logger for PyMechanical embedding.

        Parameters
        ----------
        level : int, optional
            Level of logging that is defined in the ``logging`` package. The default is 'DEBUG'.
            Options are ``"DEBUG"``, ``"INFO"``, ``"WARNING"``, and ``"ERROR"``.
        directory : str, optional
            Directory to write log file to. The default is ``None``, but by default the logs
            will appear somewhere in the system temp folder.
        base_directory: str, optional
            Base directory to write log files to. This is only possible to set before the
            Mechanical application is initialized.
        to_stdout : bool, optional
            Whether to write log messages to the standard output, which is the
            command line. The default is ``True``.
        """
        # Setup the global log configuration.
        cls.set_log_directory(directory)
        cls.set_log_base_directory(base_directory)

        # Setup the sink-specific log configuration, store to global state.
        cls._store_stdout_sink_enabled(to_stdout)
        file_sink_enabled = directory != None or base_directory != None
        cls._store_file_sink_enabled(file_sink_enabled)

        # Commit the sink-specific log configuration global state to the backend.
        cls._commit_enabled_configuration()
        cls.set_log_level(level)

    @classmethod
    def set_log_to_stdout(cls, value: bool) -> None:
        """Configure logging to write to the stdout."""
        cls._store_stdout_sink_enabled(value)
        cls._commit_enabled_configuration()

    @classmethod
    def set_log_to_file(cls, value: bool) -> None:
        """Configure logging to write to a file."""
        cls._store_file_sink_enabled(value)
        cls._commit_enabled_configuration()

    @classmethod
    def set_log_level(cls, level: int) -> None:
        """Set the log level for all configured sinks."""
        if len(LOGGING_SINKS) == 0:
            raise Exception("No logging backend configured!")
        cls._commit_level_configuration(level)

    @classmethod
    def set_log_directory(cls, value: str) -> None:
        """Configure logging to write to a directory."""
        if value == None:
            return
        _get_backend().set_directory(value)

    @classmethod
    def set_log_base_directory(cls, value: str) -> None:
        """Configure logging to write in a time-stamped subfolder in the given directory."""
        if value == None:
            return
        _get_backend().set_base_directory(value)

    @classmethod
    def _commit_level_configuration(cls, level: int) -> None:
        for sink in LOGGING_SINKS:
            _get_backend().set_log_level(level, sink)

    @classmethod
    def _commit_enabled_configuration(cls) -> None:
        for sink in LOGGING_SINKS:
            _get_backend().enable(sink)

    @classmethod
    def _store_stdout_sink_enabled(cls, value: bool) -> None:
        if value:
            LOGGING_SINKS.add(sinks.StandardSinks.CONSOLE)
        else:
            LOGGING_SINKS.discard(sinks.StandardSinks.CONSOLE)

    @classmethod
    def _store_file_sink_enabled(cls, value: bool) -> None:
        if value:
            LOGGING_SINKS.add(sinks.StandardSinks.STANDARD_LOG_FILE)
        else:
            LOGGING_SINKS.discard(sinks.StandardSinks.STANDARD_LOG_FILE)


class Logger:
    """Logger class for embedding."""

    @classmethod
    def flush(cls):
        """Flush the log."""
        _get_backend().flush()

    @classmethod
    def can_log_message(cls, level: int) -> bool:
        """Get whether a message at the given level can be logged."""
        return _get_backend().can_log_message(level)

    @classmethod
    def debug(cls, msg: str):
        """Write a debug message to the log."""
        _get_backend().log_message(logging.DEBUG, LOGGING_CONTEXT, msg)

    @classmethod
    def error(cls, msg: str):
        """Write a error message to the log."""
        _get_backend().log_message(logging.ERROR, LOGGING_CONTEXT, msg)

    @classmethod
    def info(cls, msg: str):
        """Write a info message to the log."""
        _get_backend().log_message(logging.INFO, LOGGING_CONTEXT, msg)

    @classmethod
    def warning(cls, msg: str):
        """Write a warning message to the log."""
        _get_backend().log_message(logging.WARNING, LOGGING_CONTEXT, msg)

    @classmethod
    def fatal(cls, msg: str):
        """Write a fatal message to the log."""
        _get_backend().log_message(logging.FATAL, LOGGING_CONTEXT, msg)
