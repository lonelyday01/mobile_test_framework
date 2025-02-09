import os
import datetime
import pytest
import inspect

class FileManagerError(Exception):
    """
    Custom exception for FileManager errors.
    Used to handle specific issues related to framework structure
    """

class FileManager:
    BASE_REPORT_DIR = "reports/"
    SUITE_DIR = None
    LOG_DIR = None
    EXECUTION_DIR = None
    STACK_IGNORE_LIST = ["pytest", "conftest",  "fixture", "__init__", "runner"]

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
        print(f"Johanny's flag1: {test_name=}")

        if test_name:
            print(f"Johanny's flag2: {test_name=}")
            return test_name

    @classmethod
    def setup_execution_folder(cls):
        """
        Creates necessary directories for the test execution.
        """


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