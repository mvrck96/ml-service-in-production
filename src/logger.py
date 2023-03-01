import sys

from loguru import logger


def create_logger(serialized: bool = True) -> logger:
    """Creates logger according to user settings.

    @param  serialized[bool]: Structured logging flag
            └─> default: True
    @return [logger]: Logger
    """
    logger.remove()
    logger.add(sys.stdout, serialize=serialized)
    logger.info(f"Logger initialized, structured logs: {serialized}")
    return logger
