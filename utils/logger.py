import logging
import os
from utils.file_manager import FileManager


class Logger:
    """
    Logger utility for the automation framework
    Creates a separate directoryu for each test execution.
    """
    _logger = None

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

        FileManager.setup_suite_folder(device_name=device_name)
        log_file = os.path.join(FileManager.LOG_DIR, "execution.log")
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
