import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from air_humidity_bot.main_for_database import UserHumidityDataBase


def get_history(user_id):
    try:
        Base = declarative_base()
        engine = create_engine(
            'sqlite:///users_history.db',
        )
        Base.metadata.create_all(engine)
        # noinspection PyPep8Naming
        SessionAsClass = sessionmaker(bind=engine)
        session = SessionAsClass()

        list_results = []
        history_query = session.query(
            UserHumidityDataBase.temp_dry,
            UserHumidityDataBase.temp_wet,
            UserHumidityDataBase.humidity,
            UserHumidityDataBase.date_time).where(UserHumidityDataBase.id_user.in_([user_id]))
        for history in history_query:
            history = f'DRY: {history[0]}°C, WET: {history[1]}°C => Hum.: {history[2]} |{history[3]}'
            list_results.append(history)
        result = ''
        for data in list_results:
            result += '\n' + str(data) + '\n'
    except sqlalchemy.exc.OperationalError:
        result = '...is not available or empty. \n for sure try again later 🪐'
    # print(result)
    return result


if __name__ == '__main__':
    get_history(546332530)
