import json
import logging
import os
import datetime
import inspect
import pytest


class Logger:
    """
    Logger utility for the automation framework
    Creates a separate directoryu for each test execution.
    """
    BASE_REPORT_DIR = "reports/"
    STACK_IGNORE_LIST = ["pytest", "conftest",  "fixture", "__init__", "runner"]
    SUITE_DIR = None
    LOG_DIR = None
    EXECUTION_DIR = None
    _logger = None

    @classmethod
    def get_execution_name(cls):
        """
        Determines the name of the execution folder based on the type of the test run

        Returns
        -------
        str:
            The appropriate execution name based on test scope.
        """
        if hasattr(pytest, "current_test"):
            return pytest.current_test.split("::")[-1]

        stack = inspect.stack()
        test_name = None

        for frame in stack:
            if (frame.function.startswith("test_") and
                    not any(ignored in frame.function or ignored in frame.filename for ignored in cls.STACK_IGNORE_LIST)):
                test_name = frame.function
                break

        if test_name:
            return test_name

    @classmethod
    def setup_execution_folder(cls, device_name="unknown_device"):
        """
        Creates necessary directories for the test execution.
        """
        if cls.SUITE_DIR is None:
            cls.setup_suite_folder(device_name=device_name)

        test_name = cls.get_execution_name()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        cls.EXECUTION_DIR = os.path.join(cls.SUITE_DIR, f"{test_name}-{timestamp}")
        cls.LOG_DIR = os.path.join(cls.EXECUTION_DIR, "logs/")
        cls.SCREENSHOT_DIR = os.path.join(cls.EXECUTION_DIR, "screenshots/")

        os.makedirs(cls.LOG_DIR, exist_ok=True)
        os.makedirs(cls.SCREENSHOT_DIR, exist_ok=True)

    @classmethod
    def setup_suite_folder(cls, device_name="uknown_device"):
        """
        Create a test_suite folder for device selected

        Parameters
        ----------
        device_name : str
            Name of the current device to execute the test suite
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        suite_name = f"test-suite-{device_name}-{timestamp}"
        cls.SUITE_DIR = os.path.join(cls.BASE_REPORT_DIR, suite_name)
        os.makedirs(cls.SUITE_DIR, exist_ok=True)

    @classmethod
    def setup_logger(cls, name="framework_logger", device_name="unknown-device"):
        """
        Sets up the logger configuration

        Parameters
        ----------
        name : str
            The name of the logger (default is 'Framework_logger')
        device_name : str
            The name of the device to execute the test suite

        Returns
        ----------
        logging.logger
            Configurated logger instance.
        """
        if cls._logger:
            return cls._logger

        cls.setup_execution_folder(device_name=device_name)
        log_file = os.path.join(cls.LOG_DIR, "execution.log")
        logger = logging.getLogger(name)

        if logger.hasHandlers():
            logger.handlers.clear()

        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Handler for log file
        file_handler = logging.FileHandler(log_file, mode="w")
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)

        # Handler for console log
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        cls._logger = logger

        return logger

    @classmethod
    def get_logger(cls):
        """
        Returns the configurated logger, else returns an exception if the logger is not configurated before
        """
        if not cls._logger:
            raise ValueError("Logger isn't configurated")
        return cls._logger

    @classmethod
    def capture_screenshot(cls, driver, test_name):
        """
        Captures a screenshot and saves it in the execution folder

        driver: WebDriver
            the active driver instance.

        test_name : str
            The name of each test case.
        """

        screenshot_path = os.path.join(cls.SCREENSHOT_DIR, f"{test_name}.png")
        driver.save_screenshot(screenshot_path)

