from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStates(StatesGroup):
    choose_lang = State()
    choose_category = State()



