from aiogram.utils import executor
from sqlalchemy.orm import declarative_base

from air_humidity_bot.bot import dp
from air_humidity_bot.main_for_database import main_for_database


def main():
    declarative_base()
    main_for_database()
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
