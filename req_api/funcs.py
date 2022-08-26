import re
import json
import requests
from typing import Union, Any, Dict, Optional, List, Tuple
from requests.models import Response
from datetime import datetime
from keyboards.inline.keyboard import keyboard_commands
from loader import bot, logger, exception_handler
from database.models import user, DataBaseModel, Hotel
from handlers.default_handlers import bestdeal
from req_api.api_req import request_search, request_property_list, request_get_photo, request_bestdeal
from keyboards import keyboards_text
from keyboards.inline import keyboard, calendar
from telebot.types import CallbackQuery, InputMediaPhoto, Message
from handlers.default_handlers.start_help import start_bot_com, check_state_inline_keyboard
from config_data import api_settings, default_answer
from handlers.default_handlers import lowprice_highprice


@exception_handler
def found_city(message: Message) -> list:
    response = request_search(message)
    pattern_city_group = r'(?<="CITY_GROUP",).+?[\]]'
    find_cities = re.findall(pattern_city_group, response.text)
    for i in range(len(find_cities)):
        if len(find_cities[i]) > 20:
            pattern_dest = r'(?<="destinationId":")\d+'
            destination = re.findall(pattern_dest, find_cities[0])
            pattern_city = r'(?<="name":")\w+[\s, \w]\w+'
            city = re.findall(pattern_city, find_cities[0])
            city_list = list(zip(destination, city))
    return city_list