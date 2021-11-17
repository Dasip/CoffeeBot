import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline import starter_choice, get_tea_keyboard, get_back_to_starter, get_back_to_tea, get_back_to_coffee
from keyboards.inline.coffee_choice import get_coffee_keyboard
from loader import dp
from states import StartChoiceState
from states.coffees import CoffeeState
from states.teas import TeaState


@dp.callback_query_handler(starter_choice.filter(item_name="tea"), state=None)
async def starter_handler(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=3)
    logging.info(f"callback query data = {call.data}")
    logging.info(f"callback data = {callback_data}")
    await send_tea(call.message)


@dp.callback_query_handler(starter_choice.filter(item_name="coffee"), state=None)
async def starter_handler_2(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=3)
    logging.info(f"callback query data = {call.data}")
    logging.info(f"callback data = {callback_data}")
    await send_coffee(call.message)


@dp.callback_query_handler(get_back_to_tea.filter(do_go="true"), state=TeaState.Choice)
async def bot_get_to_tea(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer()
    logging.info(f"state data in back_to_tea: {await state.get_data()}")
    await send_tea(call.message)


@dp.callback_query_handler(get_back_to_coffee.filter(do_go="true"), state=CoffeeState.Choice)
async def bot_get_to_coffee(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer()
    logging.info(f"state data in back_to_coffee: {await state.get_data()}")
    await send_coffee(call.message)


async def send_tea(message: types.Message):
    await message.answer(text="У нас огромный ассортимент чая высшего сорта на любой вкус!"
                              " Какой чай вы бы хотели заказать?",
                         reply_markup=await get_tea_keyboard())
    await StartChoiceState.Tea.set()


async def send_coffee(message: types.Message):
    await message.answer(text="У нас огромный ассортимент кофе высшего сорта на любой вкус!"
                              " Какой кофе вы бы хотели заказать?",
                         reply_markup=await get_coffee_keyboard())
    await StartChoiceState.Coffee.set()
