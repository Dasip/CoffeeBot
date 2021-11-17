from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import coffee_choice, get_back_to_starter, get_back_to_coffee, add_to_cart
from loader import db


async def get_coffee_keyboard():
    info = await db.get_four_coffees()
    coffee_keyboard = InlineKeyboardMarkup(row_width=2,
                                           inline_keyboard=[
                                               [
                                                   InlineKeyboardButton(text=info[0]["name"],
                                                                        callback_data=coffee_choice.new(info[0]["id"])),
                                                   InlineKeyboardButton(text=info[1]["name"],
                                                                        callback_data=coffee_choice.new(info[1]["id"]))
                                               ],
                                               [
                                                   InlineKeyboardButton(text=info[2]["name"],
                                                                        callback_data=coffee_choice.new(info[2]["id"])),
                                                   InlineKeyboardButton(text=info[3]["name"],
                                                                        callback_data=coffee_choice.new(info[3]["id"]))
                                               ],
                                               [
                                                   InlineKeyboardButton(text="Обратно",
                                                                        callback_data=get_back_to_starter.new("true"))
                                               ]
                                           ])
    return coffee_keyboard

coffee_item_keyboard = InlineKeyboardMarkup(row_width=2,
                                            inline_keyboard=[
                                                [
                                                    InlineKeyboardButton(text="В корзину",
                                                                         callback_data=add_to_cart.new("true")),
                                                    InlineKeyboardButton(text="К ассортименту",
                                                                         callback_data=get_back_to_coffee.new("true"))
                                                ]
                                            ])
