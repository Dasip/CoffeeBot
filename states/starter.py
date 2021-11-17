from aiogram.dispatcher.filters.state import StatesGroup, State


class StartChoiceState(StatesGroup):

    Tea = State()
    Coffee = State()