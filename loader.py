import logging
from typing import Union

import gspread_asyncio
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from gino import Gino
from peewee import SqliteDatabase

from data.config import load_config, PostgresConfig, SqliteConfig, Config
from utils.db_api.postgresql_api import db as postgres_db


config = load_config(".env")

storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

bot['google_client_manager'] = gspread_asyncio.AsyncioGspreadClientManager(
    config.misc.google_config.google_scoped_credentials
) if config.misc.google_config is not None else None

bot['config']: Config = config
bot['database']: Union[Gino, SqliteDatabase, None] = None
if config.db is not None:
    if isinstance(config.db, PostgresConfig):
        bot['database'] = postgres_db
    elif isinstance(config.db, SqliteConfig):
        bot['database'] = SqliteDatabase(database=config.db.filename, pragmas={'foreign_keys': 1})

dp = Dispatcher(bot=bot, storage=storage)
