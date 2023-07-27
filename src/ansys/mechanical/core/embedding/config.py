"""Configuration system for embedded mechanical."""
import os


class Configuration:
    """Configuration class for Mechanical."""

    def __init__(self, addin_configuration: str = "Mechanical"):
        """Construct a new Configuration instance."""
        self._no_act_addins = False
        self._addin_configuration = addin_configuration

    @property
    def no_act_addins(self) -> bool:
        """Property to disable all ACT Addins."""
        return self._no_act_addins

    @no_act_addins.setter
    def no_act_addins(self, value: bool):
        self._no_act_addins = value

    @property
    def addin_configuration(self) -> str:
        """WB1 Addin configuration name."""
        return self._addin_configuration

    @addin_configuration.setter
    def addin_configuration(self, value: str):
        self._addin_configuration = value


def configure(configuration: Configuration):
    """Apply the given configuration."""
    if configuration.no_act_addins:
        os.environ["ANSYS_MECHANICAL_STANDALONE_NO_ACT_EXTENSIONS"] = "1"
