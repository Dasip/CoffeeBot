import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline import tea_choice, tea_item_keyboard
from loader import dp, db
from states import StartChoiceState
from states.teas import TeaState


@dp.callback_query_handler(tea_choice.filter(), state=StartChoiceState.Tea)
async def show_this_tea(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    info = db.format_info(await db.get_tea_info(callback_data.get("tea_name")))
    logging.info(info)
    await state.update_data(item_type="tea")
    await call.answer()
    await call.message.answer(text=info, reply_markup=tea_item_keyboard)
    await TeaState.Choice.set()
    await state.update_data(item_name=callback_data.get("tea_name"))
    logging.info(f"state data in tea_item: {await state.get_data()}")
