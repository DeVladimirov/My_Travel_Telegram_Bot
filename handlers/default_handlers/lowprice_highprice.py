import json
import re
import requests

from typing import Union, Any, Dict, Optional, List, Tuple
from requests.models import Response
from datetime import datetime
from keyboards.inline.keyboard import keyboard_commands
from loader import bot, logger, exception_handler
from database.models import user, DataBaseModel, Hotel
import commands
import settings
import bestdeal
from api_requests.request_api import request_search, request_property_list, request_get_photo, request_bestdeal
from keyboards import keyboards_text
from keyboards.inline import keyboard, calendar
from telebot.types import CallbackQuery, InputMediaPhoto, Message
from .start_help import start_bot_com, check_state_inline_keyboard

@exception_handler
def record_command(message: Union[Message, CallbackQuery]) -> None:
    """
    Функция, запускающая  все команды: 'lowprice', 'highprice', 'bestdeal'. Проверяет входящий тип
    данных из предыдущей функции. С данной функции осуществляется начало сбора информации
    по команде для дальнейшего сохранения в базу данных. Так же функция оповещает пользователя,
    что поиск Российских городов временно приостановлен.
    :param message: Union[Message, CallbackQuery]
    :return: None
    """
    logger.info(str(message.from_user.id))
    check_state_inline_keyboard(message)
    if isinstance(message, CallbackQuery):
        user.edit('command', message.data[1:])
    else:
        user.edit('command', message.text[1:])
    bot.send_message(message.from_user.id, commands.DATA_ON_RUSSIAN_CITIES)
    choice_city(message)

@exception_handler
def choice_city(message: Union[Message, CallbackQuery]) -> None:
    """
    Функция проверяет входящий тип данных из предыдущей функции и запрашивает город
    для поиска отелей.
    :param message: Union[Message, CallbackQuery]
    :return: None
    """
    logger.info(str(message.from_user.id))
    bot.send_message(message.from_user.id, commands.CITY)
    if isinstance(message, CallbackQuery):
        bot.register_next_step_handler(message.message, search_city)
    else:
        bot.register_next_step_handler(message, search_city)


@exception_handler
def search_city(message: Message) -> None:
    """
    Функция - обрабатывает введённый пользователем город. Делает запрос на rapidapi.com.
    В случае ошибки запроса, сообщает о неполадках и возвращает пользователя на ввод города.
    В случае положительного ответа, обрабатывает его и в виде inline-кнопок отправляет
    пользователю все похожие варианты ответа.
    :param message: Message
    :return: None
    """
    logger.info(str(message.from_user.id))
    if message.text in commands.COMMAND_LIST:
        start_bot_com(message)
    else:
        response = request_search(message)
        if check_status_code(response):
            pattern_city_group = r'(?<="CITY_GROUP",).+?[\]]'
            find_cities = re.findall(pattern_city_group, response.text)
            if len(find_cities[0]) > 20:
                pattern_dest = r'(?<="destinationId":")\d+'
                destination = re.findall(pattern_dest, find_cities[0])
                pattern_city = r'(?<="name":")\w+[\s, \w]\w+'
                city = re.findall(pattern_city, find_cities[0])
                city_list = list(zip(destination, city))
                bot_message = bot.send_message(
                    message.from_user.id, commands.CORRECTION, reply_markup=keyboard.keyboards_city(city_list)
                )
                user.edit('bot_message', bot_message)
            else:
                bot.send_message(message.from_user.id, commands.INCORRECT_CITY)
                choice_city(message)
        else:
            bot.send_message(message.from_user.id, commands.REQUEST_ERROR)
            choice_city(message)

@bot.callback_query_handler(func=lambda call: call.data.isdigit())
@exception_handler
def callback_city(call: CallbackQuery) -> None:
    """
    Функция обработчик inline-кнопок. Реагирует только на информацию из кнопок
    выбора города. Далее, в формате inline-кнопок, предоставляет пользователю выбор валюты.
    :param call: CallbackQuery
    :return: None
    """
    logger.info(str(call.from_user.id))
    for city in call.message.json['reply_markup']['inline_keyboard']:
        if city[0]['callback_data'] == call.data:
            user.edit('city', city[0]['text'])
            user.edit('city_id', call.data)
            break
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    bot.edit_message_text(
        chat_id=call.message.chat.id, message_id=call.message.message_id,
        text=commands.CITY_RESULT.format(user.user.city)
    )
    bot_message = bot.send_message(
        call.from_user.id, commands.CURRENCY, reply_markup=keyboard.keyboards_currency()
    )
    user.edit('bot_message', bot_message)

@bot.callback_query_handler(func=lambda call: call.data in keyboards_text.CURRENCY_LIST)
@exception_handler
def callback_currency(call: CallbackQuery) -> None:
    """
    Функция обработчик inline-кнопок. Реагирует только на информацию входящую
    в список аббревиатур валют. Если начальная команда введенная пользователем равна 'bestdeal',
    то запрашиваем у пользователя информацию о диапазоне цен. Переходя в файл 'bestdeal.py', функцию 'price_min'
    Если команда равна 'lowprice', или 'highprice', переходим в следующую функцию 'count_hotel'.
    :param call: CallbackQuery
    :return: None
    """
    logger.info(str(call.from_user.id))
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    bot.edit_message_text(
        chat_id=call.message.chat.id, message_id=call.message.message_id,
        text=commands.RESULT_CURRENCY.format(call.data)
    )
    user.edit('currency', call.data)
    if user.user.command != commands.BESTDEAL[1:]:
        count_hotel(call)
    else:
        bot.send_message(call.from_user.id, commands.PRICE_RANGE.format(user.user.currency))
        bot_message = bot.send_message(call.from_user.id, commands.MIN_PRICE)
        user.edit('bot_message', bot_message)
        bot.register_next_step_handler(call.message, bestdeal.price_min)



def count_hotel(call: CallbackQuery) -> None:
    """
    Функция, предоставляющая пользователю выбрать количество отелей (от 1 до 10), в формате inline-кнопок.
    :param call: CallbackQuery
    :return: None
    """
    logger.info(str(call.from_user.id))
    bot_message = bot.send_message(
        call.from_user.id, commands.COUNT_HOTEL, reply_markup=keyboard.keyboards_count_photo()
    )
    user.edit('bot_message', bot_message)

