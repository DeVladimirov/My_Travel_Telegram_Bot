import sqlite3

from dataclasses import dataclass
from typing import Union, List
from telebot.types import Message, CallbackQuery

@dataclass()
class User:
    """
    Dataclass для хранения пользовательской информации
    """
    date: str = ''
    user_id: int = 0
    command: str = ''
    currency: str = ''
    locale: str = ''
    city: str = ''
    city_id: str = ''
    count_hotel: int = 0
    date_in: str = ''
    date_out: str = ''
    day_period: int = 0
    photo: str = ''
    count_photo: int = 0
    min_distance: float = 0
    max_distance: float = 0
    price_min: int = 0
    price_max: int = 0
    bot_message: Union[Message, CallbackQuery] = ''

class UserHandle:
    """
    Класс, созданный для получения, заполнения и редактирования
    пользовательской информации
    """

    def __init__(self) -> None:
        self.user: User = User()

    def get_tuple(self) -> tuple:
        """
        Метод класса UserHandle (геттер), возвращающий кортеж значений, необходимых для записи в БД
        :return: tuple
        """
        return (
            self.user.date,
            self.user.user_id,
            self.user.command,
            self.user.city,
            self.user.currency,
            self.user.date_in,
            self.user.date_out,
            self.user.min_distance,
            self.user.max_distance,
            self.user.price_min,
            self.user.price_max
        )

    def set_default(self) -> None:
        """
        Метод класса UserHandle (сеттер), для присваивания атрибутам дефолтного значения
        :return: None
        """
        self.user.date = ''
        self.user.user_id = 0
        self.user.command = ''
        self.user.currency = ''
        self.user.locale = ''
        self.user.city = ''
        self.user.city_id = ''
        self.user.count_hotel = 0
        self.user.date_in = ''
        self.user.date_out = ''
        self.user.day_period = 0
        self.user.photo = ''
        self.user.count_photo = 0
        self.user.min_distance = 0
        self.user.max_distance = 0
        self.user.price_min = 0
        self.user.price_max = 0

    def edit(self, key: str, value: Union[str, int, float]) -> None:
        """
        Метод класса UserHandle (сеттер) для изменения данных по ключу
        :param key: str
        :param value: Union[str, int, float]
        :return: None
        """
        self.user.__dict__[key] = value



user = UserHandle()

class Hotel:
    """
    Класс для хранения информации об выведенных пользователю отелях
    """

    def __init__(self, user_id: int, hotel_info: str) -> None:
        self.user_id = user_id
        self.hotel_info = hotel_info
        self.photo = ''
        self.command_id = 0

    def get_tuple(self) -> tuple:
        """
        Метод класса Hotel (геттер), возвращающий кортеж значений, необходимых для записи в БД
        :return: tuple
        """
        return (
            self.user_id,
            self.hotel_info,
            self.photo,
            self.command_id,
        )

class DataBaseModel:
    pass
