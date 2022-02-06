from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from utils.set_bot_commands import set_user_commands, set_admins_commands


@dp.message_handler(CommandStart(),
                    is_admin=True,
                    chat_type='private')
async def bot_start(message: types.Message):
    await set_admins_commands(dp=dp, admin_chat_id=message.from_user.full_name)
    await message.answer(f"Привет, {message.from_user.full_name}!")


@dp.message_handler(CommandStart(),
                    chat_type='private')
async def bot_start(message: types.Message):
    await set_user_commands(dp=dp, chat_id=message.from_user.full_name)
    await message.answer(f"Привет, {message.from_user.full_name}!")
