import os

from aiogram import Dispatcher
from aiogram.types import Message
from loguru import logger

from utils.menu_worker.ilovepdf_compressor import PdfCompressor
from utils.menu_worker.mail_worker import MailWorker
from utils.menu_worker.site_worker import SiteWorker


async def update_tomorrow(dp: Dispatcher, message: Message):
    mw = MailWorker(server=dp.bot.get('config').misc.mail_auth.imap_server,
                    login=dp.bot.get('config').misc.mail_auth.login,
                    password=dp.bot.get('config').misc.mail_auth.password,
                    save_dir=dp.bot.get('config').misc.files_paths.local_dir_path,
                    menu_folder_name=dp.bot.get('config').misc.files_paths.mail_folder_name)
    if not mw.auth_status:
        logger.info('Mail Server authentication failed')
        await dp.bot.edit_message_text(text='Ошибка авторизации на почтовом сервере',
                                       chat_id=message.chat.id,
                                       message_id=message.message_id,
                                       reply_markup=None)
        return
    if not mw.get_folder_list():
        logger.info('Error while getting folders list on mail server')
        await dp.bot.edit_message_text(text='Ошибка получения списка папок на почтовом сервере',
                                       chat_id=message.chat.id,
                                       message_id=message.message_id,
                                       reply_markup=None)
        return
    if not mw.select_folder():
        logger.info('Menu folder was not found on mail server')
        await dp.bot.edit_message_text(text='Ошибка получения списка папок на почтовом сервере',
                                       chat_id=message.from_user.id,
                                       message_id=message.message_id,
                                       reply_markup=None)
        return
    result = mw.get_messages_from_folder()
    if not result:
        logger.info('No new menus on mail server')
        await dp.bot.edit_message_text(text='Нет новых писем с меню',
                                       chat_id=message.from_user.id,
                                       message_id=message.message_id,
                                       reply_markup=None)
        return
    for message in mw.messages:
        with open(os.path.join(mw.save_dir, str(message.subject.uk) + '.pdf'), "wb") as fp:
            fp.write(message.file.content)
            fp.close()
    for filename in os.listdir(mw.save_dir):
        if filename[0] == '.':
            continue
        compressor = PdfCompressor()
        compressor.compress_file(filepath=os.path.join(mw.save_dir, filename),
                                 output_directory_path=dp.bot.get('config').misc.files_paths.local_dir_compressed_path)
    sw = SiteWorker(site_auth=dp.bot.get('config').misc.school_auth,
                    folder_paths=dp.bot.get('config').misc.files_paths)
    if not sw.authorized:
        logger.info('Site authentification failed')
        await dp.bot.edit_message_text(text='Ошибка авторизации на школьном сайте',
                                       chat_id=message.from_user.id,
                                       message_id=message.message_id,
                                       reply_markup=None)
        return
    sw.delete_all_in_folder(folder_path=dp.bot.get('config').misc.files_paths.tomorrow_folder_path)
    sw.upload_files(folder_path=dp.bot.get('config').misc.files_paths.tomorrow_folder_path,
                    files=[os.path.join(dp.bot.get('config').misc.files_paths.local_dir_compressed_path, file) for file in
                           os.listdir(dp.bot.get('config').misc.files_paths.local_dir_compressed_path)],
                    )
    await dp.bot.edit_message_text(text='Файлы с меню на завтра размещены',
                                   chat_id=message.from_user.id,
                                   message_id=message.message_id,
                                   reply_markup=None)


def update_today(dp: Dispatcher):
    sw = SiteWorker(site_auth=dp.bot.get('config').misc.school_auth,
                    folder_paths=dp.bot.get('config').misc.files_paths)
    sw.copy_tomorrow_today()
