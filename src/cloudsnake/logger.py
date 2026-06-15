import logging
from typing import Any

from rich.logging import RichHandler


def configure_boto3_logger(handler: logging.Handler, log_level: Any) -> None:
    for name in ("boto3", "botocore"):
        logger = logging.getLogger(name)
        logger.setLevel(log_level)
        logger.addHandler(handler)


def init_logger(log_level: Any) -> logging.Logger:
    handler = RichHandler(rich_tracebacks=True, show_path=False)
    handler.setLevel(log_level)

    logger = logging.getLogger("cloudsnake")
    logger.setLevel(log_level)
    logger.addHandler(handler)

    configure_boto3_logger(handler, log_level)

    return logger
