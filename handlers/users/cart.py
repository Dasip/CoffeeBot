from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from handlers.users.start import send_starter
from keyboards.inline import add_to_cart, from_cart_keyboard, show_cart, from_cart_content_keyboard
from loader import dp, db
from states.cart import CartStates
from states.coffees import CoffeeState
from states.teas import TeaState


@dp.callback_query_handler(add_to_cart.filter(do_go="true"), state=CoffeeState.Choice)
@dp.callback_query_handler(add_to_cart.filter(do_go="true"), state=TeaState.Choice)
async def set_cart_amount(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await CartStates.GetAmount.set()
    #print(await state.set_data())
    await call.answer()
    await call.message.answer(text="Введите количество пачек, которое вы хотите заказать (на складе сейчас 1342346536 "
                                   "пачек)")


@dp.message_handler(state=CartStates.GetAmount)
async def get_cart_amount(message: types.Message, state: FSMContext):
    amount = message.text
    if amount.isdigit():
        if int(amount) > 0:
            await state.update_data(item_amount=int(amount))
            data = await state.get_data()
            await db.add_item_to_cart(message.chat.id, data.get("item_name"), data.get("item_amount"))
            await message.answer(text=f"В вашу корзину добавлен {data.get('item_name')} "
                                      f"в количестве {data.get('item_amount')} пачек.",
                                 reply_markup=from_cart_keyboard)
            await state.finish()

        else:
            await send_amount(message)
    else:
        await send_amount(message)


@dp.message_handler(Command("cart"))
async def open_cart(message: types.Message, state: FSMContext):
    await state.finish()
    await show_the_cart(message)


@dp.callback_query_handler(show_cart.filter(do_go="true"))
async def show_cart(call: types.CallbackQuery):
    await show_the_cart(call.message)


async def show_the_cart(message: types.Message):
    info = await db.select_cart_by_id(message.chat.id)
    the_cont = ""
    final_result = 0
    for item, amount in zip(info["items"], info["amounts"]):
        value = await db.get_item_price(item)
        the_cont += f"{item}\t------> {value * amount} руб. ({value} * {amount} шт.)\n"
        final_result += value * amount

    res_line = f"Итого: {final_result} руб."
    await message.answer(text=f"Ваша корзина:\n{the_cont}{res_line}",
                              reply_markup=from_cart_content_keyboard)


async def send_amount(message: types.Message):
    await message.answer(text="Возможно, произошла какая-то ошибка при вводе. Пожалуйста, введите количество пачек,"
                              " которое вы хотите заказать (на складе сейчас 1342346536 пачек)")
