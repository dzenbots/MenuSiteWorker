from aiogram.types import Message, CallbackQuery

from keyboards.inline.menu_notification import site_admin_callbacks
from loader import dp
from utils.menu_worker.menu_updater import update_today


@dp.message_handler(state="*",
                    commands=['today'],
                    is_admin=True,
                    chat_type='private')
async def today_command(message: Message):
    msg = await message.answer(text='Обновление сегодняшнего меню в процессе. Ожидайте')
    update_today(dp)
    await dp.bot.edit_message_text(text='Файлы обновлены', chat_id=message.chat.id, message_id=msg.message_id)


@dp.callback_query_handler(site_admin_callbacks.filter(function='update', target='today'),
                           chat_type_callback='private')
async def update_today_menu_notification(call: CallbackQuery):
    await call.answer(cache_time=1)
    await dp.bot.edit_message_text(chat_id=call.message.chat.id,
                                   message_id=call.message.message_id,
                                   text='Обновление сегодняшнего меню в процессе. Ожидайте')
    update_today(dp=dp)
    await dp.bot.edit_message_text(chat_id=call.message.chat.id,
                                   message_id=call.message.message_id,
                                   text='Файлы обновлены')

