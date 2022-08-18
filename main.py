from handlers.default_handlers import bestdeal, history, start_help, lowprice_highprice
from database.models import DataBaseModel
from loader import bot, logger


if __name__ == '__main__':
    DataBaseModel._init_user_tables()
    bot.infinity_polling()
    logger.info('Get Started!')
