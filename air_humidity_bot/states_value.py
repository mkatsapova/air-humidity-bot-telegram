from aiogram.dispatcher.filters.state import StatesGroup, State



class Value(StatesGroup):
    temp_dry = State()
    temp_wet = State()
