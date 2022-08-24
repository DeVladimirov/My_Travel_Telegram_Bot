from database.models import DataBaseModel
from loader import bot, logger
from handlers.default_handlers import *

if __name__ == '__main__':
    DataBaseModel._init_user_tables()
    bot.infinity_polling()
    logger.info('Get Started!')
