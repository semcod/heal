"""
Main module for the heal package.

This module contains core functionality for the heal package.
"""


def hello() -> str:
    """
    Return a greeting message.

    Returns:
        str: A friendly greeting message.
    """
    return "Hello from heal package - your LLM-powered shell assistant!"


def get_version() -> str:
    """
    Get the current version of the heal package.

    Returns:
        str: The version string.
    """
    from . import __version__

    return __version__


class ShellHealer:
    """
    A shell healer class for managing error fixing sessions.
    """

    def __init__(self, name="ShellHealer"):
        """
        Initialize the ShellHealer.

        Args:
            name (str): The name of the healer.
        """
        self.name = name

    def heal(self, command, error_output):
        """
        Analyze and provide healing suggestions for shell errors.

        Args:
            command (str): The command that failed.
            error_output (str): The error output.

        Returns:
            str: A message about the healing analysis.
        """
        return (
            f"{self.name} is analyzing: '{command}' with error: {error_output[:100]}..."
        )

    def __str__(self):
        return f"ShellHealer({self.name})"
