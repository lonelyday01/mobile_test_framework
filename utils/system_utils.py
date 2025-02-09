"""
system_utils
Common system wrappers
"""
import platform
import subprocess
import yaml
import json
import os

from utils.file_manager import FileManager


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

    @staticmethod
    def get_device_from_adb():
        """
        Detects connected devices via ADB and selects the first one available.

        Returns
        -------
        dict
            The device configuration dictionary.
        """
        configured_devices = SystemUtils.load_json("config/device_config.json")["devices"]
        connected_devices = SystemUtils.list_adb_devices()
        if not connected_devices:
            raise SystemUtilsError("No devices found via adb")

        print(f"Johanny flag: {connected_devices}")

        for device in configured_devices:
            print(f"{device=}")
            if device["deviceName"] in connected_devices:
                return device
        raise SystemUtilsError("No matchin device found in device_config.json")

    @staticmethod
    def load_yaml(path):
        """
        Loads a YAML configuration file.

        Parameters
        ----------
        path : str
            Path to the YAML file.

        Returns
        -------
        dict
            Parsed YAML file as a dictionary.
        """
        with open(path, "r") as f:
            return yaml.safe_load(f)

    @staticmethod
    def load_json(path):
        """
        Loads a JSON configuration file.

        Parameters
        ----------
        path : str
            Path to the JSON file.

        Returns
        -------
        dict
            Parsed JSON file as a dictionary.
        """
        with open(path, "r") as f:
            return json.load(f)

    @classmethod
    def capture_screenshot(cls, driver, test_name):
        """
        Captures a screenshot and saves it in the execution folder

        driver: WebDriver
            the active driver instance.

        test_name : str
            The name of each test case.
        """

        screenshot_path = os.path.join(FileManager.SCREENSHOT_DIR, f"{test_name}.png")
        driver.save_screenshot(screenshot_path)
