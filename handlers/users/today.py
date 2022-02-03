from aiogram.types import Message

from loader import dp
from utils.menu_worker.site_worker import SiteWorker


@dp.message_handler(state="*", commands=['today'], is_admin=True)
async def tomorrow_command(message: Message):
    msg = await message.answer(text='Дождитесь окончания обработки файлов')
    sw = SiteWorker(site_auth=dp.bot.get('config').misc.school_auth,
                    folder_paths=dp.bot.get('config').misc.files_paths)
    sw.copy_tomorrow_today()
    await dp.bot.edit_message_text(text='Файлы обновлены', chat_id=message.chat.id, message_id=msg.message_id)