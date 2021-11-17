from aiogram.dispatcher.filters.state import StatesGroup, State


class CartStates(StatesGroup):

    GetAmount = State()