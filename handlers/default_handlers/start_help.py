from telebot.apihelper import ApiTelegramException
from telebot.types import Message, CallbackQuery
from loader import bot, logger
from database.models import user
from keyboards.inline.keyboard import keyboard_commands
from handlers.default_handlers import lowprice_highprice, history
from config_data import default_answer


@bot.message_handler(commands=default_answer.COMMAND)
@bot.message_handler(content_types=['text', 'document', 'audio'])
def start_bot_com(message: Message) -> None:
    """
    Данная функция  обрабатывает сообщения. Используются комманды из списка COMMAND.
    После обработки какой-либо команды, пользователь отправляется в ветку какого-либо
    сценария.
    :param message:
    :return:
    """
    logger.info(str(message.from_user.id))
    check_state_inline_keyboard(user.user.bot_message)
    user.set_default()
    user.edit('user_id', message.from_user.id)
    if message.text == default_answer.START:
        bot.send_message(message.from_user.id, default_answer.WELCOME.format(message.from_user.first_name))
        bot_message = bot.send_message(
            message.from_user.id, default_answer.INSTRUCTION, reply_markup=keyboard_commands(message.text)
        )
        user.edit('bot_message', bot_message)
    elif message.text == default_answer.HELP:
        bot_message = bot.send_message(
            message.from_user.id, default_answer.HELP_MESSAGE, reply_markup=keyboard_commands(message.text)
        )
        user.edit('bot_message', bot_message)
    elif message.text in [default_answer.LOWPRICE, default_answer.HIGHPRICE, default_answer.BESTDEAL]:
        lowprice_highprice.record_command(message)
    elif message.text == default_answer.HISTORY:
        history.history_menu(message)

def find_a_hotel(message: Message) -> None:
    """
    Функция для поиска отелей
    :param message: Message
    :return: None
    """
    bot.send_message(message.from_user.id, default_answer.SUGGEST_FINDING)
    bot_message = bot.send_message(
        message.from_user.id, default_answer.HELP_MESSAGE, reply_markup=keyboard_commands(message.text)
    )
    user.edit('bot_message', bot_message)


@bot.message_handler(state=None)
def echo_handler(message: Message) -> None:
    """
    Данная функция обрабатывает все входящие сообщения, которые не входят в перечень основных
    команд бота.
    :param message: Message
    :return: None
    """
    logger.info(str(message.from_user.id))
    message_text = message.text.lower()
    if message_text.startswith(default_answer.WELCOME_LIST[0]) or message_text.startswith(
            default_answer.WELCOME_LIST[1]):
        bot.send_message(message.from_user.id, default_answer.WELCOME.format(message.from_user.first_name))
        bot_message = bot.send_message(message.from_user.id, default_answer.INSTRUCTION)
        user.edit('bot_message', bot_message)
    elif message_text.startswith(default_answer.WELCOME_LIST[2]) or message_text.startswith(
            default_answer.WELCOME_LIST[3]):
        bot.send_message(message.from_user.id, default_answer.HOW_ARE_YOU_ANSWER)
        bot.register_next_step_handler(message, find_a_hotel)
    elif message_text.startswith(default_answer.WELCOME_LIST[4]) or message_text.startswith(
            default_answer.WELCOME_LIST[5]):
        bot.send_message(message.from_user.id, default_answer.GOODBYE_MESSAGE)
        bot_message = bot.send_message(message.from_user.id, default_answer.INSTRUCTION)
        user.edit('bot_message', bot_message)
    else:
        bot.send_message(message.from_user.id, default_answer.WARNING_MESSAGE)

@bot.callback_query_handler(func=lambda call: call.data.startswith('/'))
def callback_command(call: CallbackQuery) -> None:
    """
    Функция обрабатывает inline-кнопки, реагирует только на команды. Отправляет
    пользователя в соответствующий сценарий.
    Первым делом, очищает экземпляр класса UserHandle,
    так как с данного места берут начало новые команды.
    :param call: CallbackQuery
    :return: None
    """
    logger.info(str(call.from_user.id))
    user.set_default()
    user.edit('user_id', call.from_user.id)
    if call.data == default_answer.HELP:
        bot_message = bot.send_message(
            call.from_user.id, default_answer.HELP_MESSAGE, reply_markup=keyboard_commands(call.data)
        )
        user.edit('bot_message', bot_message)
    elif call.data in [default_answer.LOWPRICE, default_answer.HIGHPRICE, default_answer.BESTDEAL]:
        lowprice_highprice.record_command(call)
    elif call.data == default_answer.HISTORY:
        history.history_menu(call)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)


def check_state_inline_keyboard(message: Message) -> None:
    """
    Функция для удаления inline-кнопок, в случае не активного статуса
    (когда пользователь перешёл в другую команду). Чтобы исключить повторное нажатие на кнопку вне сценария,
    данная функция удаляет оставшиеся inline-кнопки, если кнопки нет, то возникает исключение
    ApiTelegramException, которое функция устраняет.
    :param message: Message
    :return: None
    """
    try:
        bot.edit_message_reply_markup(message.chat.id, message.message_id)
    except ApiTelegramException:
        pass
    except AttributeError:
        pass