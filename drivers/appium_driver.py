import yaml
import json
from appium import webdriver
from appium.options.android import UiAutomator2Options






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
    def __init__(self, device_index=0, application="calculator"):
        """
        Initializes the Appium driver manager.

        Parameters
        ----------
        device_index : int, optional
            Index of the device in the configuration file (default is 0).
        application : str, optional
            Name of the application to test, as defined in `appium_config.yaml` (default is "calculator").
        """
        self.config = self.load_yaml("config/appium_config.yaml")
        self.devices = self.load_json("config/device_config.json")["devices"]
        self.device = self.devices[device_index]
        self.application = self.config["applications"][application]
        if not self.application:
            raise AppiumDriverManagerError(f"Application '{application}' not found in appium_config.yaml")
        self.capabilities =  self.set_capabilities()
        self.driver = None
        self._options = UiAutomator2Options().load_capabilities(self.capabilities)


    def load_yaml(self, path):
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

    def load_json(self, path):
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

    def set_capabilities(self):
        """
        Merges default Appium capabilities, device-specific configurations, and application settings.

        Returns
        -------
        dict
            Merged dictionary of capabilities.
        """
        capabilities = self.config["capabilities"].copy()
        capabilities.update(self.device)
        capabilities.update(self.application)
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
            self.driver.quit()
        except Exception as e:
            raise AppiumDriverManagerError("Unable to stop driver") from e