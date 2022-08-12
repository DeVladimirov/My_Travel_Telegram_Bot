import telebot

bot = telebot.TeleBot('5436119247:AAGQGWua92u-1tZAOeeoIqVJ-Y0FTLjQRWk')

@bot.message_handler(content_types=['text', 'document', 'audio'])
def get_text_messages(message):
    if message.text == "/hello_world":
        bot.send_message(message.from_user.id, "Hello there!")
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Наше общение - это сюрприз, безусловно, но приятный")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши Привет")
