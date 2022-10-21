import logging
from os.path import splitext, basename
import sys
import time


def __configure_default_logger(logger: logging.Logger) -> None:
    logger.setLevel(logging.DEBUG)

    log_formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s: %(filename)s:%(lineno)d %(message)s')
    log_formatter.converter = time.gmtime

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(log_formatter)

    logger.addHandler(console_handler)


def get_default_logger(log_as: str = None) -> logging.Logger:
    if log_as is None:
        logger = logging.getLogger(splitext(basename(sys.argv[0]))[0])
    else:
        logger = logging.getLogger(log_as)

    __configure_default_logger(logger)

    return logger
