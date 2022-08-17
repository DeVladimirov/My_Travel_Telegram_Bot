from telebot.types import CallbackQuery
from database.models import user
from loader import bot, logger, exception_handler
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from keyboards.keyboards_text import LSTEP
import commands
from datetime import date, timedelta, datetime
from handlers.default_handlers import lowprice_highprice

class CustCalendar(DetailedTelegramCalendar):
    """
    Дочерний Класс (Родитель - DetailedTelegramCalendar). Необходим для изменения
    дефолтного значения у параметров empty month_button и empty_year_button.
    """
    empty_month_button: str = ''
    empty_year_button: str = ''

@exception_handler
def date_in(call: CallbackQuery) -> None:
    """
    Функция, запрашивающая у пользователя минимальную дату для проживания в отеле.
    После запроса, для взаимодействия с пользователем, создаёт inline-календарь.
    :param call: CallbackQuery
    :return: None
    """
    logger.info(str(call.from_user.id))
    calendar, step = CustCalendar(
        calendar_id=0,
        locale='ru',
        min_date=date.today() + timedelta(days=1),
        max_date=date.today() + timedelta(days=180)
    ).build()
    bot.send_message(call.from_user.id, commands.DATE_IN)
    bot_message = bot.send_message(call.from_user.id, f"Выберите {LSTEP[step]}:", reply_markup=calendar)
    user.edit('bot_message', bot_message)

@exception_handler
@bot.callback_query_handler(func=CustCalendar.func(calendar_id=0))
def callback_first_calendar(call: CallbackQuery) -> None:
    """
    Функция обработчик inline-календаря. Реагирует только на календарь с id = 0.
    После обработки пользовательской информации, перенаправляет в функцию date_out.
    :param call: CallbackQuery
    :return: None
    """
    logger.info(str(call.from_user.id))
    result, key, step = CustCalendar(
        calendar_id=0,
        locale='ru',
        min_date=date.today(),
        max_date=date.today() + timedelta(days=180)
    ).process(call.data)
    if not result and key:
        bot_message = bot.edit_message_text(
            f"Выберите {LSTEP[step]}:", call.message.chat.id, call.message.message_id, reply_markup=key
        )
        user.edit('bot_message', bot_message)
    elif result:
        bot.edit_message_text(f"Дата заезда {result}", call.message.chat.id, call.message.message_id)
        user.edit('date_in', result)
        date_out(call, result)

@exception_handler
def date_out(call: CallbackQuery, result: datetime) -> None:
    """
    Функция, запрашивающая у пользователя максимальную дату для проживания в отеле.
    После запроса,для взаимодействия с пользователем, создаёт inline-календарь.
    :param call: CallbackQuery
    :param result: datetime
    :return: None
    """
    logger.info(str(call.from_user.id))
    min_date = result + timedelta(days=1)
    second_calendar, second_step = CustCalendar(
        calendar_id=15,
        locale='ru',
        min_date=min_date,
        max_date=min_date + timedelta(days=180)
    ).build()
    bot.send_message(call.from_user.id, commands.DATE_OUT)
    bot_message = bot.send_message(
        call.from_user.id, f"Выберите {LSTEP[second_step]}:", reply_markup=second_calendar
    )
    user.edit('bot_message', bot_message)
