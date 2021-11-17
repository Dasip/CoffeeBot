from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from data.invoice_data import PICKUP_SHIPPING
from keyboards.inline import get_to_payment
from loader import dp, bot, db
from utils.misc.invoice_item import generate_invoice


@dp.callback_query_handler(get_to_payment.filter(do_go="true"))
async def start_payment(call: types.CallbackQuery):
    the_data = await db.get_invoice_data(call.from_user.id)
    the_item = generate_invoice(the_data["data"])
    #await call.message.answer(text="FFF")
    print(the_item["prices"])
    await bot.send_invoice(call.from_user.id, **the_item, payload="123456768")


@dp.shipping_query_handler()
async def choose_shipping(query: types.ShippingQuery):
    await bot.answer_shipping_query(shipping_query_id=query.id,
                                    shipping_options=[
                                        PICKUP_SHIPPING
                                    ])

@dp.pre_checkout_query_handler()
async def pre_checkout_query(query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=query.id,
                                        ok=True)
    await bot.send_message(chat_id=query.from_user.id, text="ПЛАТИТЬ ВСЕГДА, ПЛАТИТЬ ВЕЗДЕ, СПАСИБО, ВСЕ, ПОКА.")