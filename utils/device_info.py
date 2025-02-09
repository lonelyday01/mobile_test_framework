import json
import os

from utils.logger import Logger


class DeviceInfo:
    """
    Utility to retrieve device capabilities from the saved JSON file.
    """

    @staticmethod
    def get_device_capabilities():
        """
        Reads the device capabilities from the latest execution folder.

        Returns
        -------
        dict
            The stored device capabilities.
        """
        # ✅ Ensure EXECUTION_DIR is set before using it
        if not hasattr(Logger, "EXECUTION_DIR") or not Logger.EXECUTION_DIR:
            raise RuntimeError(
                "Logger.EXECUTION_DIR is not set. Ensure Logger.setup_execution_folder() is called first.")

        execution_folder = Logger.EXECUTION_DIR
        capabilities_path = os.path.join(execution_folder, "device_capabilities.json")

        if not os.path.exists(capabilities_path):
            raise FileNotFoundError(f"Capabilities file not found: {capabilities_path}")

        with open(capabilities_path, "r") as f:
            return json.load(f)