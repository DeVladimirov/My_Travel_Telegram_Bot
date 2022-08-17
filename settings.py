import os
from dotenv import load_dotenv, find_dotenv

"""
Файл содержащий базовые конфигурации бота и API (Токен, API-ключ, заголовок, параметры и url-адреса)
"""

if not find_dotenv():
    exit('Файл .env отсутствует')
else:
    load_dotenv()

TOKEN = os.environ.get('TOKEN')
API_KEY = os.environ.get('API_KEY')

HEADERS = {
    'X-RapidAPI-Host': 'hotels4.p.rapidapi.com',
    'X-RapidAPI-Key': API_KEY
}