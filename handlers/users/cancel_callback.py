from aiogram.types import CallbackQuery

from keyboards.inline.menu_notification import site_admin_callbacks
from loader import dp


@dp.callback_query_handler(site_admin_callbacks.filter(function='cancel'),
                           chat_type='private')
async def cancel_notification(call: CallbackQuery):
    await call.answer(cache_time=1)
    await dp.bot.edit_message_text(chat_id=call.message.chat.id,
                                   message_id=call.message.message_id,
                                   text='Действие с меню на сайте отменено')
