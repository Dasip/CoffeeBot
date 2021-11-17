import logging
from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config
from utils.db_api import tea_db, coffee_db


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):

        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self,
                      command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_tables(self):
        cart = """
        CREATE TABLE IF NOT EXISTS Cart(
        id SERIAL PRIMARY KEY,
        telegram_id INTEGER NOT NULL,
        items TEXT[],
        amounts INTEGER[]
        );
        """
        teas = """
        CREATE TABLE IF NOT EXISTS Tea(
        id VARCHAR(255) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description VARCHAR NOT NULL,
        price INTEGER NOT NULL
        );
        """
        coffees = """
        CREATE TABLE IF NOT EXISTS Coffee(
        id VARCHAR(255) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description VARCHAR NOT NULL,
        price INTEGER NOT NULL
        );
        """
        for elem in [teas, coffees, cart]:
            await self.execute(elem, execute=True)

        #await self.add_tea_from_db()
        #await self.add_coffee_from_db()

    async def select_all_carts(self):
        sql = "SELECT * FROM cart"
        return await self.execute(sql, fetch=True)

    @staticmethod
    def format_args(sql, params: dict):
        sql += " AND ".join([f"{item}=${num}" for num, item in enumerate(params.keys(), start=1)])
        return sql, tuple(params.values())

    @staticmethod
    def format_info(record_arr):
        the_line = record_arr
        the_result = f"{the_line['name']}\n{the_line['description']}\nЦена за упаковку: {the_line['price']} руб."
        return the_result

    async def select_cart_by_id(self, telegid):
        sql = "SELECT * FROM cart WHERE telegram_id = $1"
        return await self.execute(sql, telegid, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        return await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_tables(self):
        for i in ["Tea", "Coffee", "Cart"]:
            sql = f"DROP TABLE {i}"
            await self.execute(sql, execute=True)

    async def add_coffee_from_db(self):
        info = coffee_db.get_info()
        for i in info:
            await self.add_coffee(i["id"], i["name"], i["description"], i["price"])

    async def add_coffee(self, tid, tname, tdesc, tprice):
        sql = "INSERT INTO Coffee(id, name, description, price) VALUES($1, $2, $3, $4)"
        return await self.execute(sql, tid, tname, tdesc, tprice, execute=True)

    async def add_tea_from_db(self):
        info = tea_db.get_info()
        for i in info:
            await self.add_tea(i["id"], i["name"], i["description"], i["price"])

    async def add_tea(self, tid, tname, tdesc, tprice):
        sql = "INSERT INTO Tea(id, name, description, price) VALUES($1, $2, $3, $4)"
        return await self.execute(sql, tid, tname, tdesc, tprice, execute=True)

    async def get_tea_price(self, tid):
        sql = "SELECT price FROM tea WHERE id = $1"
        result = await self.execute(sql, tid, fetchval=True)
        return result

    async def get_coffee_price(self, tid):
        sql = "SELECT price FROM coffee WHERE id = $1"
        result = await self.execute(sql, tid, fetchval=True)
        return result

    async def get_item_price(self, tid):
        result1 = await self.get_tea_price(tid)
        result2 = await self.get_coffee_price(tid)
        return result1 if result1 else result2

    async def get_tea_info(self, tid):
        sql = "SELECT * FROM tea WHERE id = $1"
        return await self.execute(sql, tid, fetchrow=True)

    async def get_coffee_info(self, tid):
        sql = "SELECT * FROM coffee WHERE id = $1"
        return await self.execute(sql, tid, fetchrow=True)

    async def get_item_info(self, tid):
        sql1 = await self.get_coffee_info(tid)
        sql2 = await self.get_tea_info(tid)
        return sql1 if sql1 else sql2

    async def get_four_teas(self):
        sql = "SELECT * FROM tea LIMIT 4"
        return await self.execute(sql, fetch=True)

    async def get_four_coffees(self):
        sql = "SELECT * FROM coffee LIMIT 4"
        return await self.execute(sql, fetch=True)

    async def add_cart(self, telegid):
        sql = "INSERT INTO cart(telegram_id, items, amounts) VALUES($1, $2, $3) returning *"
        result = await self.execute(sql, telegid, [], [], fetchrow=True)
        logging.info(f"СОЗДАНА КОРЗИНА {result}")
        return result

    async def add_item_to_cart(self, telegid, item_id, amount):
       # sql = "SELECT * FROM cart WHERE telegram_id"
        uzver = await self.select_cart_by_id(telegid)
        if not uzver:
            uzver = await self.add_cart(telegid)

        item_list = uzver["items"]
        logging.info(item_list)
        if item_id in item_list:
            all_amount = uzver["amounts"]
            all_amount[item_list.index(item_id)] += amount
            new_sql = "UPDATE cart SET amounts = $1 WHERE telegram_id = $2"
            await self.execute(new_sql, all_amount, telegid, execute=True)

        else:
            item_list.append(item_id)
            all_amount = uzver["amounts"]
            all_amount.append(amount)
            logging.info(item_list)
            logging.info(all_amount)
            new_sql = "UPDATE cart SET items = $1, amounts = $2 WHERE telegram_id = $3"
            await self.execute(new_sql, item_list, all_amount, telegid, execute=True)
        logging.info(await self.select_cart_by_id(telegid))

    async def get_invoice_data(self, telegid: int):
        the_cart = await self.select_cart_by_id(telegid)
        the_info = {"user_id": the_cart["telegram_id"], "data": []}
        for item, amount in zip(the_cart["items"], the_cart["amounts"]):
            item_info = await self.get_item_info(item)
            item_data = {"name": item_info["name"], "price": item_info["price"], "amount": amount}
            the_info["data"].append(item_data)
        logging.info(f"ЗАКАЗ К ОПЛАТЕ: {the_info}")
        return the_info

