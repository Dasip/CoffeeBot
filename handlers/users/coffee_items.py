import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline import tea_choice, tea_item_keyboard, coffee_choice, coffee_item_keyboard
from loader import dp, db
from states import StartChoiceState
from states.coffees import CoffeeState


@dp.callback_query_handler(coffee_choice.filter(), state=StartChoiceState.Coffee)
async def show_this_coffee(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    info = db.format_info(await db.get_coffee_info(callback_data.get("coffee_name")))
    logging.info(info)
    await state.update_data(item_type="coffee")
    await call.answer()
    await call.message.answer(text=info, reply_markup=coffee_item_keyboard)
    await CoffeeState.Choice.set()
    await state.update_data(item_name=callback_data.get("coffee_name"))
    logging.info(f"state data in coffee_item: {await state.get_data()}")
