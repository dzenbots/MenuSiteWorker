from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.inline.menu_notification import site_admin_callbacks
from loader import dp
from utils.menu_worker.menu_updater import update_tomorrow


class CommandTomorrow(Command):

    def __init__(self):
        super().__init__(['tomorrow'])


@dp.message_handler(CommandTomorrow(),
                    is_admin=True,
                    chat_type='private')
async def tomorrow_command(message: Message):
    await message.answer(text='Дождитесь окончания обработки файлов')
    await update_tomorrow(dp=dp, message=message)


@dp.callback_query_handler(site_admin_callbacks.filter(function='update_tomorrow'),
                           chat_type='private')
async def update_tomorrow_menu_notification(call: CallbackQuery):
    await call.answer(cache_time=1)
    await dp.bot.edit_message_text(chat_id=call.message.chat.id,
                                   message_id=call.message.message_id,
                                   text='Обновление завтрашнего меню в процессе. Ожидайте')
    await update_tomorrow(dp=dp, message=call.message)
    await dp.bot.edit_message_text(text='Файлы обновлены', chat_id=call.message.chat.id,
                                   message_id=call.message.message_id)
