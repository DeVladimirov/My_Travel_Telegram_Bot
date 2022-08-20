from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from typing import Callable
from requests import ReadTimeout
from log_config import cust_logger
from database.models import user
from states import default_answer
from config_data import api_settings

storage = StateMemoryStorage()
bot = TeleBot(token=api_settings.BOT_TOKEN, state_storage=storage)
logger = cust_logger('bot_logger')

def exception_handler(func: Callable) -> Callable:
    """
    Декоратор, оборачивающий функцию в try-except блок.
    :param func: Callable
    :return: Callable
    """
    def wrapped_func(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as error:
            logger.error('Исключение в работе бота!', exc_info=error)
            bot.send_message(user.user.user_id, default_answer.REQUEST_ERROR)
    return wrapped_func

def exception_request_handler(func: Callable) -> Callable:
    """
    Декоратор, оборачивающий функцию request в try-except блок.
    :param func: Callable
    :return: Callable
    """
    def wrapped_func(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except (ConnectionError, TimeoutError, ReadTimeout) as error:
            logger.error('В работе бота возникло исключение', exc_info=error)
            bot.send_message(user.user.user_id, default_answer.REQUEST_ERROR)
    return wrapped_func