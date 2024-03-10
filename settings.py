import logging.config
import os

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(blue)s%(asctime)s: %(log_color)s%(levelname)-8s%(reset)s "
                      "%(white)s%(module)-11s %(lineno)-4s %(light_white)s%(message)s%(reset)s",
            "log_colors": {
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
        },
        "file": {
            "format": "%(asctime)s %(levelname)-12s %(module)-12s %(lineno)-12s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
        "file_debug": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "formatter": "file",
            "filename": "debug.log",
        },
    },
    "loggers": {
        "logger": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
        "": {
            "handlers": ["file_debug"],
            "level": "DEBUG",
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)