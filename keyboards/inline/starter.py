from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import starter_choice, get_back_to_starter, show_cart, get_to_payment

starter_keyboard = InlineKeyboardMarkup(row_width=2,
                                        inline_keyboard=[
                                            [
                                                InlineKeyboardButton(
                                                    text="Чай",
                                                    callback_data=starter_choice.new("tea")
                                                ),
                                                InlineKeyboardButton(
                                                    text="Кофе",
                                                    callback_data=starter_choice.new("coffee")
                                                )
                                            ],
                                            [
                                                InlineKeyboardButton(
                                                    text="Просмотреть корзину",
                                                    callback_data=show_cart.new("true")
                                                )
                                            ]
                                        ])

from_cart_keyboard = InlineKeyboardMarkup(row_width=2,
                                          inline_keyboard=[
                                              [
                                                  InlineKeyboardButton(
                                                      text="Просмотреть корзину",
                                                      callback_data=show_cart.new("true")
                                                  ),
                                                  InlineKeyboardButton(
                                                      text="В магазин",
                                                      callback_data=get_back_to_starter.new("true")
                                                  )
                                              ]
                                          ])

from_cart_content_keyboard = InlineKeyboardMarkup(row_width=1,
                                                  inline_keyboard=[
                                                      [
                                                          InlineKeyboardButton(
                                                              text="В магазин",
                                                              callback_data=get_back_to_starter.new("true")
                                                          )
                                                      ],
                                                      [
                                                          InlineKeyboardButton(
                                                              text="Оплатить заказ",
                                                              callback_data=get_to_payment.new("true")
                                                          )
                                                      ]
                                                  ])
