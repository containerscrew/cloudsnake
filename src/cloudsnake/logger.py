# https://docs.python.org/3/howto/logging.html
import logging
from typing import Any


class CustomFormatter(logging.Formatter):
    BLUE1 = "\033[95m"
    BLUE2 = "\033[96m"
    SUCCESS = "\033[92m"
    WARNING = "\033[93m"
    ERROR = "\033[91m"
    NOCOLOR = "\033[0m"
    format = "[%(asctime)s] %(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: BLUE1 + format + NOCOLOR,
        logging.INFO: BLUE2 + format + NOCOLOR,
        logging.WARNING: WARNING + format + NOCOLOR,
        logging.ERROR: ERROR + format + NOCOLOR,
        logging.CRITICAL: ERROR + format + NOCOLOR,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def configure_boto3_logger(handler, log_level):
    boto3_logger = logging.getLogger("boto3")
    boto3_logger.setLevel(log_level)
    boto3_logger.addHandler(handler)

    # Also configure botocore logger to use the same handler and level
    botocore_logger = logging.getLogger("botocore")
    botocore_logger.setLevel(log_level)
    botocore_logger.addHandler(handler)


def init_logger(log_level: Any) -> logging.Logger:
    logger = logging.getLogger("cloudsnake")
    logger.setLevel(log_level)

    # Create console handler
    ch = logging.StreamHandler()
    ch.setLevel(log_level)

    # Create formatter and add it to the handler
    ch.setFormatter(CustomFormatter())

    # Add the handler to the logger
    logger.addHandler(ch)

    # Configure boto3 to use the same logger
    configure_boto3_logger(ch, log_level)

    return logger
