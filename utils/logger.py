import logging
import sys


class CustomLogger:

    __instance = False

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
            # create custom logger
            cls.__instance.current_logger = logging.getLogger('custom_logger')
            # create console and file handlers
            cls.__instance.console_handler = logging.StreamHandler(sys.stdout)
            cls.__instance.file_handler = logging.FileHandler('debug_logs.log')
            # create and set formatter
            cls.__instance.formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
            cls.__instance.console_handler.setFormatter(cls.__instance.formatter)
            cls.__instance.file_handler.setFormatter(cls.__instance.formatter)
            # set logging level
            cls.__instance.console_handler.setLevel(logging.INFO)
            cls.__instance.file_handler.setLevel(logging.DEBUG)
            cls.__instance.current_logger.setLevel(logging.DEBUG)
            # add console and file handlers
            cls.__instance.current_logger.addHandler(cls.__instance.console_handler)
            cls.__instance.current_logger.addHandler(cls.__instance.file_handler)

        return cls.__instance

    def log(self, level, msg, *args, **kwargs):
        """Logs an event."""
        self.current_logger.log(level, msg, *args, **kwargs)


def log(msg, level='debug'):
    """Logs the message with the level."""

    level_mapping = {
        'info': logging.INFO,
        'error': logging.ERROR,
        'critical': logging.CRITICAL,
        'warning': logging.WARNING,
        'debug': logging.DEBUG
    }

    assert level in level_mapping.keys(), f'Incorrect level "{level}" for logger.\n' \
        f'Valid levels: {list(level_mapping.keys())}'

    logger = CustomLogger()
    logger.log(msg=msg, level=level_mapping[level])
