import os
import json
from appium import webdriver
from appium.options.android import UiAutomator2Options
from utils.system_utils import SystemUtils
from utils.logger import Logger


class AppiumDriverManagerError(Exception):
    """
    Custom exception for AppiumDriverManager errors.
    Used to handle specific issues related to driver initialization.
    """


class AppiumDriverManager:
    """
    Manages the initialization and configuration of the Appium WebDriver.

    This class reads configurations from YAML and JSON files, dynamically sets
    the desired capabilities, and initializes an Appium WebDriver session.
    """
    def __init__(self, device_index=None, application="calculator"):
        """
        Initializes the Appium driver manager.

        Parameters
        ----------
        device_index : int, optional
            Index of the device in the configuration file (default is 0).
        application : str, optional
            Name of the application to test, as defined in `appium_config.yaml` (default is "calculator").
        """
        self.config = SystemUtils.load_yaml("config/appium_config.yaml")
        self.devices = SystemUtils.load_json("config/device_config.json")["devices"]
        self.logger = Logger.get_logger()
        # Get device automatically if device index isn't provided
        if device_index is None:
            self.device = SystemUtils.get_device_from_adb()
        else:
            self.device = self.devices[device_index]
        self.device_name = self.device["deviceName"]

        self.logger.info(f"Initializing AppiumDriver Manager for {application}")
        self.application = self.config["applications"][application]
        if not self.application:
            raise AppiumDriverManagerError(f"Application '{application}' not found in appium_config.yaml")
        self.capabilities =  self.set_capabilities()
        self.save_capabilities(self.capabilities)
        self.driver = None
        self._options = UiAutomator2Options().load_capabilities(self.capabilities)



    def save_capabilities(self, capabilities):
        """
       Saves the device capabilities to a JSON file in the execution folder.

       Parameters
       ----------
       capabilities : dict
           The capabilities of the WebDriver session.
       """
        execution_folder = Logger.EXECUTION_DIR
        os.makedirs(execution_folder, exist_ok=True)

        capabilities_path = os.path.join(execution_folder, "device_capabilities.json")
        with open(capabilities_path, "w") as f:
            json.dump(capabilities, f, indent=4)

        self.logger.info(f"Device capabilities saved to {capabilities_path}")

    def set_capabilities(self):
        """
        Merges default Appium capabilities, device-specific configurations, and application settings.

        Returns
        -------
        dict
            Merged dictionary of capabilities.
        """
        self.logger.info("Setting up capabilities")
        capabilities = self.config["capabilities"].copy()
        capabilities.update(self.device)
        capabilities.update(self.application)
        self.logger.debug(f"Capabilities: {capabilities}")
        return capabilities

    @property
    def options(self):
        """
        Returns the configured Appium options.

        Returns
        -------
        UiAutomator2Options
            The options object for Appium WebDriver.
        """
        return self._options

    def start_driver(self):
        """
        Starts the Appium WebDriver session.

        Returns
        -------
        WebDriver
            The initialized Appium WebDriver instance.
        """
        try:
            self.logger.info(f"Starting WebDriver: {self.config["server"]["full_server_path"]}")
            self.driver = webdriver.Remote(command_executor=self.config["server"]["full_server_path"],
                                           options=self.options
            )
            return self.driver
        except Exception as e:
            raise AppiumDriverManagerError("Unable to start driver") from e

    def stop_driver(self):
        """
        Stops the WebDriver session.

        Raises
        ------
        AppiumDriverManagerError
            If the driver fails to stop properly.
        """
        try:
            self.logger.info(f"Stopping WebDriver: {self.config["server"]["full_server_path"]}")
            self.driver.quit()
        except Exception as e:
            raise AppiumDriverManagerError("Unable to stop driver") from e