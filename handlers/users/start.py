from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery

from keyboards.inline import starter_keyboard, get_back_to_starter
from loader import dp, bot
from states import StartChoiceState


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await send_starter(message)


@dp.callback_query_handler(get_back_to_starter.filter(do_go="true"), state=StartChoiceState.Coffee)
@dp.callback_query_handler(get_back_to_starter.filter(do_go="true"), state=StartChoiceState.Tea)
@dp.callback_query_handler(get_back_to_starter.filter(do_go="true"), state=None)
async def bot_get_to_start(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer()
    await send_starter(call.message, call.from_user)


async def send_starter(message: types.Message, orig_user: types.User = None):
    name = message.from_user.full_name if not orig_user else orig_user.full_name
    await message.answer(text=f"Добро пожаловать в наш магазин кофе и чая, {name}!"
                              f"Что именно вы хотите купить?",
                         reply_markup=starter_keyboard)
