import os
from dotenv import load_dotenv, find_dotenv

"""
Файл содержащий базовые конфигурации бота и API (Токен, API-ключ, заголовок, параметры и url-адреса)
"""

if not find_dotenv():
    exit('Файл .env отсутствует')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')

URL_SEARCH = 'https://hotels4.p.rapidapi.com/locations/v2/search'
URL_PROPERTY_LIST = 'https://hotels4.p.rapidapi.com/properties/list'
URL_PHOTO = 'https://hotels4.p.rapidapi.com/properties/get-hotel-photos'
URL_HOTEL = 'https://www.hotels.com/ho{}'

DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Вывести справку")
)


HEADERS = {
    'X-RapidAPI-Host': 'hotels4.p.rapidapi.com',
    'X-RapidAPI-Key': RAPID_API_KEY
}


QUERY_SEARCH = {
    'query': 'new_york',
    'locale': 'en_US',
    'currency': 'USD'
}
QUERY_PROPERTY_LIST = {
    'destinationId': '1506246',
    'pageNumber': '1',
    'pageSize': '25',
    'checkIn': '2020-01-08',
    'checkOut': '2020-01-15',
    'adults1': '1',
    'sortOrder': 'PRICE',
    'locale': 'en_US',
    'currency': 'USD'
}
QUERY_BESTDEAL = {
    'destinationId': '1506246',
    'pageNumber': '1',
    'pageSize': '25',
    'checkIn': '2020-01-08',
    'checkOut': '2020-01-15',
    'adults1': '1',
    'priceMin': '50',
    'priceMax': '300',
    'sortOrder': 'DISTANCE_FROM_LANDMARK',
    'locale': 'en_US',
    'currency': 'EUR'
}
QUERY_PHOTO = {'id': '1178275040'}