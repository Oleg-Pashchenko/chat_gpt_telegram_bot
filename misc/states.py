from aiogram.dispatcher.filters.state import StatesGroup, State


class NormalMode(StatesGroup):
    question = State()


class Predict(StatesGroup):
    commands_names = State()
    date = State()
