import logging

COFFEE_TEXT = {
    "deluxe": "Изысканный кофе с великолепным вкусом станет прекрасным угощением для любого события",
    "extra_energy": "Этот микс заполненный кофе сорта робуста пробудит даже медведя из глубокой спячки!",
    "desire": "Утонченный кофе с мягким вкусом, этот микс станет идеальным дополнением для десерта",
    "death_wish": "ВНИМАНИЕ: НЕ ДЛЯ СЛАБЫХ СЕРДЦЕМ! Этот микс с высочайшей концентрацией кофеина поможет не"
                  " спать неделю подряд тем, у кого на кону стоит слишком многое."}

COFFEE_PRICE = {"deluxe": 999,
                "extra_energy": 799,
                "desire": 1299,
                "death_wish": 899}


COFFEE_NAME = {
"deluxe": "Deluxe",
"extra_energy": "XTra Energy",
"desire": "Desire",
"death_wish": "Death Wish"
}

def get_info():
    info = []
    for i in COFFEE_TEXT.keys():
        a = {}
        a["id"] = i
        a["name"] = COFFEE_NAME[i]
        a["price"] = COFFEE_PRICE[i]
        a["description"] = COFFEE_TEXT[i]
        info.append(a)
    return info


def get_coffee_price(key):
    if key in COFFEE_PRICE:
        return COFFEE_PRICE[key]
    return None


def get_coffee_info(key):
    return f"{COFFEE_TEXT[key]}\n Стоимость: {COFFEE_PRICE[key]} за пачку (500 гр)"
