import logging
import logging.config
"""
Файл с конфигурацией логгера
"""

class FilterError(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.ERROR


dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "%(levelname)s | %(name)s | %(asctime)s | %(filename)s | %(funcName)s | %(lineno)s | %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "base",
        },
        "info": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "when": "H",
            "interval": 24,
            "formatter": "base",
            "filename": "info.log",
        },
        "error": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "ERROR",
            "when": "H",
            "interval": 24,
            "formatter": "base",
            "filename": "error.log",
            "filters": ["error"]
        },
    },
    "loggers": {
        "bot_logger": {
            "level": "INFO",
            "handlers": ["console", "info", "error"]
        },
    },
    "filters": {
        "error": {
            "()": FilterError
        }
    }
}


def cust_logger(logger_name: str) -> logging.Logger:
    """
    Функция - для применения стандартной конфигурации Логгера
    :param logger_name: str
    :return: Logger
    """
    logging.config.dictConfig(dict_config)
    logger = logging.getLogger(logger_name)
    return logger