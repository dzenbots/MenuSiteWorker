import asyncio

from aiogram import executor
from gino import Gino
from loguru import logger
from peewee import SqliteDatabase

from loader import dp
import middlewares
import filters
import handlers
from utils.db_api.postgresql_api import on_startup_postresql, on_shutdown_postresql
from utils.db_api.sqlite_api import on_startup_sqlite, on_shutdown_sqlite
from utils.notify_admins import on_startup_notify, on_shutdown_notify
from utils.scheduler.scheduler import scheduler


async def on_startup(dispatcher):
    logger.add("bot_log.log", filter=lambda record: record["level"].name == "INFO")
    if dispatcher.bot['database'] is not None:
        if isinstance(dispatcher.bot['database'], SqliteDatabase):
            on_startup_sqlite()
        if isinstance(dispatcher.bot['database'], Gino):
            await on_startup_postresql(dispatcher)

    # Уведомляет про запуск и устанавливаем команды
    await on_startup_notify(dispatcher)

    asyncio.create_task(scheduler(dp=dp))


async def on_shutdown(dispatcher):
    if dispatcher.bot['database'] is not None:
        if isinstance(dispatcher.bot['database'], SqliteDatabase):
            on_shutdown_sqlite()
        if isinstance(dispatcher.bot['database'], Gino):
            await on_shutdown_postresql(dispatcher)
    await on_shutdown_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           on_startup=on_startup,
                           on_shutdown=on_shutdown,
                           skip_updates=True)
