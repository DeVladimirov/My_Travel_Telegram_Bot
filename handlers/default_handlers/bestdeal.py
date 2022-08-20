import re
import json
from typing import List, Dict, Union
from telebot.types import Message, CallbackQuery
from database.models import user
from loader import bot, logger, exception_handler
from states import default_answer
from req_api.api_req import request_bestdeal
from .lowprice_highprice import count_hotel
from .start_help import start_bot_com
from config_data import api_settings
@exception_handler
def price_min(message: Message) -> None:
    """
    Функция, проверяющая на корректность введённой информации пользователем о минимальной цене.
    Если ответ корректный, запрашивает данные о максимальной цене, если нет, повторяет предыдущий запрос.
    :param message: Message
    :return: None
    """
    logger.info(str(message.from_user.id))
    if message.text in default_answer.COMMAND_LIST:
        start_bot_com(message)
    else:
        if message.text.isdigit():
            user.edit('price_min', int(message.text))
            bot.edit_message_text(
                chat_id=user.user.bot_message.chat.id, message_id=user.user.bot_message.message_id,
                text=default_answer.RESULT_MIN_PRICE.format(message.text)
            )
            bot_message = bot.send_message(message.from_user.id, default_answer.MAX_PRICE)
            user.edit('bot_message', bot_message)
            bot.register_next_step_handler(message, price_max)
        else:
            bot.send_message(message.from_user.id, default_answer.INCORRECT_PRICE)
            bot.send_message(message.from_user.id, default_answer.MIN_PRICE)
            bot.register_next_step_handler(message, price_min)

@exception_handler
def price_max(message: Message) -> None:
    """
    Функция, проверяющая на корректность введённой информации пользователем о максимальной цене.
    Если ответ корректный, запрашивает данные о минимальном расстоянии поиска, если нет, повторяет предыдущий запрос.
    :param message: Message
    :return: None
    """
    logger.info(str(message.from_user.id))
    if message.text in default_answer.COMMAND_LIST:
        start_bot_com(message)
    else:
        if message.text.isdigit():
            user.edit('price_max', int(message.text))
            if user.user.price_min >= user.user.price_max:
                bot.send_message(message.from_user.id, default_answer.INCORRECT_VALUE_PRICE)
                bot.send_message(message.from_user.id, default_answer.MAX_PRICE)
                bot.register_next_step_handler(message, price_max)
            else:
                bot.edit_message_text(
                    chat_id=user.user.bot_message.chat.id, message_id=user.user.bot_message.message_id,
                    text=default_answer.RESULT_MAX_PRICE.format(message.text)
                )
                bot.send_message(message.from_user.id, default_answer.DISTANCE_RANGE)
                bot_message = bot.send_message(message.from_user.id, default_answer.MIN_DISTANCE)
                user.edit('bot_message', bot_message)
                bot.register_next_step_handler(message, distance_min)
        else:
            bot.send_message(message.from_user.id, default_answer.INCORRECT_PRICE)
            bot.send_message(message.from_user.id, default_answer.MAX_PRICE)
            bot.register_next_step_handler(message, price_max)

@exception_handler
def distance_min(message: Message) -> None:
    """
    Функция, отправляющая запрос на корректность введенных данных в функцию check_num.
    Если ответ корректный, запрашивает данные о максимальном расстоянии поиска, если нет,
    повторяет предыдущий запрос.
    :param message: Message
    :return: None
    """
    logger.info(str(message.from_user.id))
    if message.text in default_answer.COMMAND_LIST:
        start_bot_com(message)
    else:
        min_dist = check_num(message.text)
        if min_dist:
            user.edit('min_distance', float(min_dist))
            bot.edit_message_text(
                chat_id=user.user.bot_message.chat.id, message_id=user.user.bot_message.message_id,
                text=default_answer.RESULT_MIN_DISTANCE.format(message.text)
            )
            bot_message = bot.send_message(message.from_user.id, default_answer.MAX_DISTANCE)
            user.edit('bot_message', bot_message)
            bot.register_next_step_handler(message, distance_max)
        else:
            bot.send_message(message.from_user.id, default_answer.INCORRECT_DISTANCE)
            bot.send_message(message.from_user.id, default_answer.MIN_DISTANCE)
            bot.register_next_step_handler(message, distance_min)

@exception_handler
def distance_max(message: Message) -> None:
    """
    Функция - Отправляющая запрос на корректность введенных данных в функцию check_num. Если
    ответ корректный, совершается переход в функцию check_distance для проверки разницы расстояния
    (Чтобы минимальное расстояние, не было больше максимального), если нет, повторяется запрос
    о максимальном расстоянии.
    :param message: Message
    :return: None
    """
    logger.info(str(message.from_user.id))
    if message.text in default_answer.COMMAND_LIST:
        start_bot_com(message)
    else:
        max_dist = check_num(message.text)
        if max_dist:
            user.edit('max_distance', float(max_dist))
            check_distance(message)
        else:
            bot.send_message(message.from_user.id, default_answer.INCORRECT_DISTANCE)
            bot.send_message(message.from_user.id, default_answer.MAX_DISTANCE)
            bot.register_next_step_handler(message, distance_max)


def check_num(message: str) -> str:
    """
    Функция, проверяющая на корректность введённой информации пользователем о максимальном расстоянии(число ли введено).
    В качестве корректного ответа от пользователя принимаются целые числа и числа с плавающей точкой
    (так же вместо точки обрабатывается запятая).
    :param message: str
    :return: str
    """
    float_pattern = r'\b[0-9]+[.,]?[0-9]+\b'
    int_pattern = r'\b[0-9]+\b'
    if [message] == re.findall(float_pattern, message) or [message] == re.findall(int_pattern, message):
        if ',' in message:
            dist = re.sub(r'[,]', '.', message)
        else:
            dist = message
        return dist

def check_distance(message) -> None:
    """
    Функция, проверяющая на корректность введённой информации пользователем о минимальном и максимальном расстоянии.
    (Чтобы минимальное расстояние, не было больше максимального) Если ответ корректный, возвращает в файл
    lowprice_highprice, функцию count_hotel  для дальнейшего прохождения сценария. Eсли ответ некорректный,
    повторяется запрос о максимальном расстоянии.
    :param message: Message
    :return: None
    """
    logger.info(str(message.from_user.id))
    if user.user.min_distance >= user.user.max_distance:
        bot.send_message(message.from_user.id, default_answer.INCORRECT_VALUE_DISTANCE)
        bot.send_message(message.from_user.id, default_answer.MAX_DISTANCE)
        bot.register_next_step_handler(message, distance_max)
    else:
        bot.edit_message_text(
            chat_id=user.user.bot_message.chat.id, message_id=user.user.bot_message.message_id,
            text=default_answer.RESULT_MAX_DISTANCE.format(message.text)
        )
        count_hotel(message)

@exception_handler
def bestdeal_logic(call: CallbackQuery, result_hotels: List[Dict], result: List) -> Union[List[Dict], bool]:
    """
    Функция, обрабатывающая десериализованный ответ с API. Проходит циклом по отелям и подбирает
    отель с подходящей удаленностью от центра. В случае, если не набралось необходимое количество отелей
    (Пользовательский выбор + 5 отелей запасных, в случае возникновения ошибок), то обращаемся к функции
    bestdeal_additional_request, для повторного запроса на следующей странице. Чтобы пользователь долго не ожидал
    инофрмацию, к API делается ещё два дополнительных запроса по отелям, если они не набирается необходимое
    количество отелей, то пользователь получает сообщение, что отели не найдены.
    :param call: CallbackQuery
    :param result_hotels: List[Dict]
    :param result: List
    :return: Union [List[Dict], bool]
    """
    logger.info(str(call.from_user.id))
    for hotel in result_hotels:
        distance = re.sub(r'[\D+]', '', hotel['landmarks'][0]['distance'])
        if user.user.min_distance <= int(distance) <= user.user.max_distance:
            result.append(hotel)
    if len(result) < user.user.count_hotel + 5:
        api_settings.QUERY_BESTDEAL['pageNumber'] = int(api_settings.QUERY_BESTDEAL['pageNumber']) + 1
        if api_settings.QUERY_BESTDEAL['pageNumber'] == 4:
            return False
        else:
            bestdeal_additional_request(call, result)
    elif len(result) >= user.user.count_hotel + 5:
        api_settings.QUERY_BESTDEAL['pageNumber'] = 1
        return result

@exception_handler
def bestdeal_additional_request(call: CallbackQuery, result) -> None:
    """
    Функция обращается к файлу request_api, функции request_bestdeal.
    Полученный ответ от API, отправляет в bestdeal_logic
    :param call: CallbackQuery
    :param result: List[Dict]
    :return: None
    """
    logger.info(str(call.from_user.id))
    response_hotels = request_bestdeal(call)
    result_hotels = json.loads(response_hotels.text)['data']['body']['searchResults']['results']
    bestdeal_logic(call, result_hotels, result)