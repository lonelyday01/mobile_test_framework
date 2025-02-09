import logging
import shutil
import time

import pytest
import sys
import os

from utils.logger import Logger
from utils.system_utils import SystemUtils

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from drivers.appium_driver import AppiumDriverManager

logger= logging.getLogger(__name__)
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

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """
    Hook that runs at the start of the pytest configuration.
    It is used to dynamically configure the output path of the reports,
    using the device name obtained from AppiumDriverManager.
    """
    device_name = SystemUtils.get_device_from_adb()["deviceName"]
    Logger.setup_logger(device_name=device_name)
    suite_dir = Logger.SUITE_DIR
    # define the destination paths
    json_report_path = os.path.join(suite_dir, "test_report.json")
    html_report_path = os.path.join(suite_dir, "test_report.html")

    # add destination path to plugins options
    config.option.json_report_file = json_report_path
    config.option.htmlpath = html_report_path
