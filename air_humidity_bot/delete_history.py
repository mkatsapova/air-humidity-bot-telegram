import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from air_humidity_bot.main_for_database import UserHumidityDataBase

from aiogram.dispatcher.filters.state import StatesGroup, State


class Delete(StatesGroup):
    confirm_deletion = State()




def delete_history(user_id):
    try:
        Base = declarative_base()
        engine = create_engine('sqlite:///users_history.db')

        Base.metadata.create_all(engine)
        # noinspection PyPep8Naming
        SessionAsClass = sessionmaker(bind=engine)
        session = SessionAsClass()

        record_object = session.query(UserHumidityDataBase).filter(UserHumidityDataBase.id_user == user_id)
        # print(record_object)
        for data in record_object:
            session.delete(data)
        session.commit()
        result = 'history was cleaned up 🗑'
    except sqlalchemy.exc.OperationalError:
        result = 'no data from your history'
    #print(result)
    return result


if __name__ == '__main__':
    delete_history(546332531)
