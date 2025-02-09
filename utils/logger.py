import logging
import os
from utils.file_manager import FileManager


class Logger:
    """
    Logger utility for the automation framework
    Creates a separate directoryu for each test execution.
    """
    _loggers = {}

    @classmethod
    def setup_logger(cls, test_name):
        """
        Sets up the logger configuration

        Parameters
        ----------
        test_name : str
            The name of the test being executed.

        Returns
        ----------
        logging.logger
            Configurated logger instance.
        """
        if test_name in cls._loggers:
            return cls._loggers[test_name]

        log_file = os.path.join(FileManager.LOG_DIR, f"{test_name}.log")
        logger = logging.getLogger(test_name)

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
