import datetime

from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class UserHumidityDataBase(Base):
    __tablename__ = 'users_data'

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer)
    first_name = Column(String)
    username = Column(String)
    temp_dry = Column(Float)
    temp_wet = Column(Float)
    humidity = Column(Integer)
    # date = Column(DateTime, default=datetime.datetime.utcnow)
    date_time = Column(String, default=str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M')))

    def __repr__(self):
        return f"id: '{self.id}', " \
               f"user id in Telegram: {self.user_id}" \
               f"first name: {self.first_name}" \
               f"username: '{self.username}', " \
               f"data of dry thermometer: '{self.temp_dry}', " \
               f"data of wet thermometer: '{self.temp_wet}', " \
               f"humidity is: '{self.humidity} %' " \
               f"date {self.date_time}"


def data_base_show_all():
    engine = create_engine('sqlite:///users_history.db')
    Base.metadata.create_all(engine)
    # noinspection PyPep8Naming
    SessionAsClass = sessionmaker(bind=engine)
    session = SessionAsClass()
    all_history = session.query(UserHumidityDataBase.id,
                                UserHumidityDataBase.id_user,
                                UserHumidityDataBase.first_name,
                                UserHumidityDataBase.username,
                                UserHumidityDataBase.temp_dry,
                                UserHumidityDataBase.temp_wet,
                                UserHumidityDataBase.humidity,
                                UserHumidityDataBase.date_time).all()
    print(*all_history, sep='\n')


def main_for_database():
    engine = create_engine('sqlite:///users_history.db')
    Base.metadata.create_all(engine)
    # noinspection PyPep8Naming
    SessionAsClass = sessionmaker(bind=engine)
    session = SessionAsClass()
    session.commit()


if __name__ == '__main__':
    main_for_database()
    data_base_show_all()
