import logging

from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)
    logging.info("СОЗДАЕМ ПОДКЛЮЧЕНИЕ")
    await db.create()
    logging.info("СОЗДАЕМ ТАБЛИЦУ ПОЛЬЗОВАТЕЛЕЙ")
    await db.create_tables()
    logging.info("ТАБЛИЦЫ СОЗДАНЫ/ПОДКЛЮЧЕНЫ")
    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

