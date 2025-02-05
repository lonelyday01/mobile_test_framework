import pytest
import sys
import os

import slash

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from drivers.appium_driver import AppiumDriverManager


@pytest.fixture(scope="function")
def driver():
    """
    Fixture to initialize and return an Appium WebDriver instance.
    Ensures proper setup and teardown of the driver.

    Yields
    ------
    WebDriver
        The initialized Appium WebDriver instance.
    """
    driver_manager = AppiumDriverManager(application="calculator")
    driver_instance = driver_manager.start_driver()
    yield driver_instance
    driver_manager.stop_driver()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_protocol(item):
    """
    Hook to capture the current test name in execution
    """
    pytest.current_test = item.nodeid
    yield