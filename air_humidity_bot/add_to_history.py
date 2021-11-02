import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from air_humidity_bot.main_for_database import UserHumidityDataBase


def add_history(from_user_id, first_name, username, temp_dry, temp_wet, humidity):
    try:
        Base = declarative_base()
        engine = create_engine('sqlite:///users_history.db')

        Base.metadata.create_all(engine)
        # noinspection PyPep8Naming
        SessionAsClass = sessionmaker(bind=engine)
        session = SessionAsClass()

        new_data_from_user = UserHumidityDataBase(id_user=from_user_id,
                                                  first_name=first_name,
                                                  username=username,
                                                  temp_dry=temp_dry,
                                                  temp_wet=temp_wet,
                                                  humidity=humidity)
        session.add(new_data_from_user)
        session.commit()

        result = '📡'
    except sqlalchemy.exc.OperationalError:
        result = '☄️ something was wrong with the database.\n' \
                 'I can`t add you request to history...'
    except sqlalchemy.exc.StatementError:
        result = '☄️ something was wrong with the data.\n' \
                 'I can`t add you request to history...'
    #print(result)
    return result


if __name__ == '__main__':
    add_history('0', 'test', 'test', 'test', '11', '12')
    add_history('0', 'test', 'test', '10', '11', '12')
