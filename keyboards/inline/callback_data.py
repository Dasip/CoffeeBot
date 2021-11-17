from aiogram.utils.callback_data import CallbackData

starter_choice = CallbackData("starter", "item_name")
tea_choice = CallbackData("tea", "tea_name")
coffee_choice = CallbackData("coffee", "coffee_name")

add_to_cart = CallbackData("add_cart", "do_go")
show_cart = CallbackData("show_cart", "do_go")

get_back_to_starter = CallbackData("back", "do_go")
get_back_to_tea = CallbackData("back_tea", "do_go")
get_back_to_coffee = CallbackData("back_coffee", "do_go")
get_to_payment = CallbackData("to_pay", "do_go")