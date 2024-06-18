from cloudsnake.logger import init_logger
from testfixtures import log_capture


@log_capture()
def test_logger(capture):
    logger = init_logger("INFO")
    logger.info("a message")
    logger.error("an error")

    capture.check(
        ("cloudsnake", "INFO", "a message"),
        ("cloudsnake", "ERROR", "an error"),
    )


# def test_logger_levels():
#     logger = init_logger(log_level="DEBUG")
#     assert logger.level == logging.DEBUG
#     for handler in logger.handlers:
#         assert handler.level == logging.DEBUG


# def test_boto3_logging():
#     logger = init_logger("INFO")
#     boto3_logger = logging.getLogger("boto3")
#     assert boto3_logger.level == logging.INFO
#     botocore_logger = logging.getLogger("botocore")
#     assert botocore_logger.level == logging.INFO

#     # Ensure they share the same handlers
#     assert boto3_logger.handlers[0] in logger.handlers
#     assert botocore_logger.handlers[0] in logger.handlers


# def test_logger_cleanup():
#     logger = init_logger("INFO")
#     logger.info('a message')
#     assert len(logger.handlers) > 0

#     # Clean up handlers
#     for handler in logger.handlers:
#         logger.removeHandler(handler)
#     assert len(logger.handlers) == 0
