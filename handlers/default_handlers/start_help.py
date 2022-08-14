from telebot.apihelper import ApiTelegramException
from telebot.types import Message, CallbackQuery
from loader import bot, logger
from config_data import config
import commands
import telebot
from dotenv import load_dotenv, find_dotenv


@bot.message_handler(commands=commands.COMMAND)
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
    if message.text == commands.START:
        bot.send_message(message.from_user.id, commands.WELCOME.format(message.from_user.first_name))
        bot_message = bot.send_message(
            message.from_user.id, commands.INSTRUCTION, reply_markup=keyboard_commands(message.text)
        )
        user.edit('bot_message', bot_message)
    elif message.text == commands.HELP:
        bot_message = bot.send_message(
            message.from_user.id, commands.HELP_MESSAGE, reply_markup=keyboard_commands(message.text)
        )
        user.edit('bot_message', bot_message)
    elif message.text in [commands.LOWPRICE, commands.HIGHPRICE, commands.BESTDEAL]:
        lowprice_highprice.record_command(message)
    elif message.text == commands.HISTORY:
        history.history_menu(message)

def find_a_hotel(message: Message) -> None:
    """
    Функция для поиска отелей
    :param message: Message
    :return: None
    """
    bot.send_message(message.from_user.id, commands.SUGGEST_FINDING)
    bot_message = bot.send_message(
        message.from_user.id, commands.HELP_MESSAGE, reply_markup=keyboard_commands(message.text)
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
    if message_text.startswith(commands.WELCOME_LIST[0]) or message_text.startswith(commands.WELCOME_LIST[1]):
        bot.send_message(message.from_user.id, commands.WELCOME.format(message.from_user.first_name))
        bot_message = bot.send_message(message.from_user.id, commands.INSTRUCTION)
        user.edit('bot_message', bot_message)
    elif message_text.startswith(commands.WELCOME_LIST[2]) or message_text.startswith(constants.WELCOME_LIST[3]):
        bot.send_message(message.from_user.id, commands.HOW_ARE_YOU_ANSWER)
        bot.register_next_step_handler(message, find_a_hotel)
    elif message_text.startswith(commands.WELCOME_LIST[4]) or message_text.startswith(constants.WELCOME_LIST[5]):
        bot.send_message(message.from_user.id, commands.GOODBYE_MESSAGE)
        bot_message = bot.send_message(message.from_user.id, commands.INSTRUCTION)
        user.edit('bot_message', bot_message)
    else:
        bot.send_message(message.from_user.id, commands.WARNING_MESSAGE)
