from aiogram.types import Message

from loader import dp


@dp.message_handler(state="*", commands=['tomorrow'], is_admin=True)
async def tomorrow_command(message: Message):
    pass
