from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from utils.set_bot_commands import set_user_commands, set_admins_commands


@dp.message_handler(CommandStart(), is_admin=True)
async def bot_start(message: types.Message):
    await set_admins_commands(admin_chat_id=message.from_user.full_name)
    await message.answer(f"Привет, {message.from_user.full_name}!")


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await set_user_commands(chat_id=message.from_user.full_name)
    await message.answer(f"Привет, {message.from_user.full_name}!")