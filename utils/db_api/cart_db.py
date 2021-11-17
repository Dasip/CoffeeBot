USER_CART = {}


def add_user_to_cart(u):
    USER_CART[u] = {}


def get_user_cart(u):
    return USER_CART[u]


def add_item_to_user_cart(u, item, amount):
    if not u in USER_CART.keys():
        add_user_to_cart(u)
    if item in USER_CART[u].keys():
        USER_CART[u][item] += amount
    else:
        USER_CART[u][item] = amount
