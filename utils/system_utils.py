"""
system_utils
Common system wrappers
"""
import platform
import subprocess
import os

class SystemUtilsError(Exception):
    """
    Custom exception for SystemUtilsError errors.
    Used to handle specific issues related to system utils execution.
    """

class SystemUtils:
    """
    A wrapper class to execute system commands across different platforms (Windows, Mac, Linux).
    Also provides utilities for ADB commands.
    """

    @staticmethod
    def get_os():
        """
        Detects the operative system type.

        returns:
        ---------
        str:
            'Windows', 'Linux' or 'Mac'.
        """
        return platform.system()

    @staticmethod
    def send_cmd(command, shell=False):
        """
        Executes a system command and returns the output.

        Parameters
        ----------
        command : str or list
            The command to execute. Can be a string (for shell execution) or a list (for subprocess.run).
        shell : bool, optional
            Whether to run the command in a shell environment (default is False).

        Returns
        -------
        str
            The command output as a string.
        """
        try:
            output = subprocess.run(command, shell=shell, capture_output=True, text=True)
            return output.stdout.strip()
        except Exception as e:
            raise SystemUtilsError(f"Failed to execute command: {command}") from e

    @staticmethod
    def list_adb_devices():
        """
        List of Android devices connected using adb.
        Returns
        -------
        list:
            A list of connected device IDs.
        """
        output = SystemUtils.send_cmd(["adb", "devices"])
        devices = [line.split()[0] for line in output.splitlines() if "device" in line and "List" not in line]
        return devices if devices else []

    @staticmethod
    def is_adb_available():
        """
        Checks if ADB is installed and accessible.

        Returns
        -------
        bool
            True if ADB is available, False otherwise.
        """
        try:
            output = SystemUtils.send_cmd(["adb", "version"])
            return "Android Debug Bridge" in output
        except RuntimeError:
            return False