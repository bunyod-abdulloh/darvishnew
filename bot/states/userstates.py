from aiogram.filters.state import StatesGroup, State


class UserAnketa(StatesGroup):
    addfullname = State()
    addphone = State()
