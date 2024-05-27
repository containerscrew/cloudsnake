# https://docs.python.org/3/howto/logging.html
import logging


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


def init_logger(log_level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger("awstools")
    logger.setLevel(log_level)

    handler = logging.StreamHandler()
    handler.setFormatter(CustomFormatter())

    logger.addHandler(handler)

    return logger
