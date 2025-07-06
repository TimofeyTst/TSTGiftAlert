"""Methods for working with logger."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from gift_alerter import settings

_log_format = (
    "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s "
)


def get_file_handler(file_name: str) -> RotatingFileHandler:
    Path(file_name).absolute().parent.mkdir(exist_ok=True, parents=True)
    file_handler = RotatingFileHandler(
        filename=file_name,
        maxBytes=5242880,
        backupCount=10,
    )
    file_handler.setFormatter(logging.Formatter(_log_format))
    return file_handler


def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(_log_format))
    return stream_handler


def get_logger(name):
    """Get logger.

    Examples:
        ::

            >>> from app.pkg.logger import get_logger
            >>> logger = get_logger(__name__)
            >>> logger.info("Hello, World!")
            2021-01-01 00:00:00,000 - [INFO] - app.pkg.logger - (logger.py).get_logger(43) - Hello, World!
    """
    logger = logging.getLogger(name)
    file_path = str(
        Path(
            settings.LOGGER_FOLDER_PATH,
            f"gift_alerter.log",
        ).absolute(),
    )
    logger.addHandler(get_file_handler(file_name=file_path))
    logger.addHandler(get_stream_handler())
    logger.setLevel("INFO")
    return logger

