from dataclasses import dataclass
from typing import List, Union

from aiogram.types import LabeledPrice

from data import config


@dataclass
class ResultItem:
    title: str
    description: str
    start_parameter: str
    currency: str
    prices: List[LabeledPrice]
    provider_data: dict = None
    photo_url: str = None
    photo_size: int = None
    photo_width: int = None
    photo_height: int = None
    need_name: bool = None
    need_phone_number: bool = None
    need_email: bool = None
    need_shipping_address: bool = None
    send_phone_number_to_provider: bool = None
    send_email_to_provider: bool = None
    is_flexible: bool = None
    provider_token: str = config.PAY_TOKEN

    def generate_into_dict(self):
        return self.__dict__


def generate_invoice(data: list):
    the_prices = []
    for elem in data:
        the_prices.append(LabeledPrice(
            label=elem["name"],
            amount=elem["price"]*elem["amount"]*100))

    new_item = ResultItem(
        title="Ваш заказ:",
        description="=========",
        currency="RUB",
        prices=the_prices,
        start_parameter="order",
        need_shipping_address=True,
        is_flexible=True
    )

    return new_item.generate_into_dict()
