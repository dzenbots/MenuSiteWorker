import logging

from aiogram import Dispatcher

from utils.set_bot_commands import set_admins_commands


async def on_startup_notify(dp: Dispatcher):
    for admin in dp.bot.get('config').tg_bot.admin_ids:
        try:
            await set_admins_commands(dp=dp, admin_chat_id=admin)
            await dp.bot.send_message(admin, "Бот Запущен")

        except Exception as err:
            logging.exception(err)


async def on_shutdown_notify(dp: Dispatcher):
    for admin in dp.bot.get('config').tg_bot.admin_ids:
        try:
            await dp.bot.send_message(admin, "Бот остановлен")

        except Exception as err:
            logging.exception(err)
