from aiogram import types
from aiogram.types import BotCommandScopeChat


async def set_admins_commands(dp, admin_chat_id):
    await dp.bot.set_my_commands(commands=[
        types.BotCommand("tomorrow", "Обновить завтрашнее меню"),
        types.BotCommand("today", "Обновить сегодняшнее меню"),
    ], scope=BotCommandScopeChat(
        chat_id=admin_chat_id
    )
    )


async def set_user_commands(dp, chat_id):
    await dp.bot.set_my_commands(commands=[

    ], scope=BotCommandScopeChat(
        chat_id=admin_chat_id
    )
    )
