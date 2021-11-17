import logging

TEA_TEXT = {"royal_black": "Классический черный чай в лучших королевских традициях чаепития. Подойдет как для семейного"
                           "чаепития, так и для приема послов других стран.",
            "chinese_ceremonial": "Изысканный и роскошный зеленый чай, подходящий для любой чайной церемонии!",
            "dessert_fruit": "Утонченный и сладкий этот дессертный чай подойдет для любого праздника.",
            "imperial_yellow": "Этот великолепный чай с нотками чабреца станет истинным украшением любого чаепития"
                               "и безусловно впечатлит каждого ценителя чая."}

TEA_PRICE = {"royal_black": 599,
             "chinese_ceremonial": 899,
             "dessert_fruit": 599,
             "imperial_yellow": 1199}


TEA_NAME = {"royal_black": "Королевский черный чай",
             "chinese_ceremonial": "Китайский церемониальный чай",
             "dessert_fruit": "Десертный фруктовый чай",
             "imperial_yellow": "Императорский желтый чай"
}



def get_info():
    info = []
    for i in TEA_TEXT.keys():
        a = {}
        a["id"] = i
        a["description"] = TEA_TEXT[i]
        a["price"] = TEA_PRICE[i]
        a["name"] = TEA_NAME[i]
        info.append(a)
    return info


def get_tea_price(key):
    if key in TEA_PRICE:
        return TEA_PRICE[key]
    return None


def get_tea_info(key):
    return f"{TEA_TEXT[key]}\n Стоимость: {TEA_PRICE[key]} за пачку (500 гр)"