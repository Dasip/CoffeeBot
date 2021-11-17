from aiogram import types

PICKUP_SHIPPING = types.ShippingOption(
    id="pickup",
    title="Самовывоз",
    prices=[
        types.LabeledPrice(
            "Самовывоз из магазина", 0)
    ]
)
